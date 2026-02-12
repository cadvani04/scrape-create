"""
Extract and download images, SVGs, and other assets
"""

import aiohttp
import asyncio
from pathlib import Path
from urllib.parse import urljoin, urlparse
import hashlib
from PIL import Image
import io


async def extract_assets(page, base_url):
    """
    Extract all images (img tags, CSS backgrounds, inline SVGs).
    
    Returns list of assets with URLs and metadata.
    """
    
    assets = await page.evaluate("""
        (baseUrl) => {
            const result = {
                images: [],
                svgs: [],
                backgrounds: []
            };
            
            const seen = new Set();
            
            // Helper to resolve URLs
            function resolveUrl(url) {
                try {
                    return new URL(url, baseUrl).href;
                } catch {
                    return null;
                }
            }
            
            // Extract <img> tags
            document.querySelectorAll('img').forEach(img => {
                const src = img.getAttribute('src') || img.getAttribute('data-src');
                const srcset = img.getAttribute('srcset');
                const alt = img.getAttribute('alt') || '';
                
                if (src) {
                    const fullUrl = resolveUrl(src);
                    if (fullUrl && !seen.has(fullUrl)) {
                        seen.add(fullUrl);
                        result.images.push({
                            url: fullUrl,
                            alt: alt,
                            width: img.naturalWidth || img.width,
                            height: img.naturalHeight || img.height,
                            type: 'img'
                        });
                    }
                }
                
                // Parse srcset for additional images
                if (srcset) {
                    srcset.split(',').forEach(src => {
                        const url = src.trim().split(' ')[0];
                        const fullUrl = resolveUrl(url);
                        if (fullUrl && !seen.has(fullUrl)) {
                            seen.add(fullUrl);
                            result.images.push({
                                url: fullUrl,
                                alt: alt,
                                type: 'srcset'
                            });
                        }
                    });
                }
            });
            
            // Extract CSS background images
            document.querySelectorAll('*').forEach(el => {
                const style = window.getComputedStyle(el);
                const bgImage = style.backgroundImage;
                
                if (bgImage && bgImage !== 'none') {
                    const matches = bgImage.match(/url\\(["\']?([^"\'\\)]+)["\']?\\)/);
                    if (matches && matches[1]) {
                        const fullUrl = resolveUrl(matches[1]);
                        if (fullUrl && !seen.has(fullUrl)) {
                            seen.add(fullUrl);
                            result.backgrounds.push({
                                url: fullUrl,
                                element: el.tagName.toLowerCase(),
                                type: 'background'
                            });
                        }
                    }
                }
            });
            
            // Extract inline SVGs
            document.querySelectorAll('svg').forEach((svg, index) => {
                const svgContent = svg.outerHTML;
                result.svgs.push({
                    content: svgContent,
                    index: index,
                    width: svg.getAttribute('width'),
                    height: svg.getAttribute('height'),
                    type: 'inline-svg'
                });
            });
            
            return result;
        }
    """, base_url)
    
    return assets


async def download_assets(assets_data, convert_to_webp=True):
    """
    Download all assets and save them locally.
    Converts raster images to WebP and deduplicates.
    """
    
    images_dir = Path("assets/images")
    svg_dir = Path("assets/svg")
    images_dir.mkdir(parents=True, exist_ok=True)
    svg_dir.mkdir(parents=True, exist_ok=True)
    
    downloaded_images = []
    downloaded_svgs = []
    seen_hashes = {}
    
    # Download images
    all_images = assets_data.get('images', []) + assets_data.get('backgrounds', [])
    
    async with aiohttp.ClientSession() as session:
        for img_data in all_images:
            try:
                url = img_data['url']
                
                # Skip data URLs
                if url.startswith('data:'):
                    continue
                
                # Download image
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    if response.status == 200:
                        content = await response.read()
                        
                        # Calculate hash for deduplication
                        file_hash = hashlib.md5(content).hexdigest()
                        
                        if file_hash in seen_hashes:
                            # Skip duplicate
                            img_data['local_path'] = seen_hashes[file_hash]
                            downloaded_images.append(img_data)
                            continue
                        
                        # Determine file extension
                        parsed = urlparse(url)
                        original_ext = Path(parsed.path).suffix.lower()
                        
                        # Convert to WebP if requested and it's a raster image
                        if convert_to_webp and original_ext in ['.jpg', '.jpeg', '.png', '.gif']:
                            try:
                                image = Image.open(io.BytesIO(content))
                                
                                # Convert to RGB if needed
                                if image.mode in ('RGBA', 'LA', 'P'):
                                    background = Image.new('RGB', image.size, (255, 255, 255))
                                    if image.mode == 'P':
                                        image = image.convert('RGBA')
                                    background.paste(image, mask=image.split()[-1] if 'A' in image.mode else None)
                                    image = background
                                elif image.mode != 'RGB':
                                    image = image.convert('RGB')
                                
                                # Save as WebP
                                filename = f"{file_hash}.webp"
                                filepath = images_dir / filename
                                image.save(filepath, 'WEBP', quality=85)
                                
                                img_data['local_path'] = f"assets/images/{filename}"
                                img_data['converted'] = True
                                seen_hashes[file_hash] = img_data['local_path']
                                
                            except Exception as e:
                                print(f"[Warning] Could not convert {url} to WebP: {e}")
                                # Save original
                                ext = original_ext or '.jpg'
                                filename = f"{file_hash}{ext}"
                                filepath = images_dir / filename
                                filepath.write_bytes(content)
                                img_data['local_path'] = f"assets/images/{filename}"
                                seen_hashes[file_hash] = img_data['local_path']
                        else:
                            # Save original
                            ext = original_ext or '.jpg'
                            filename = f"{file_hash}{ext}"
                            filepath = images_dir / filename
                            filepath.write_bytes(content)
                            img_data['local_path'] = f"assets/images/{filename}"
                            seen_hashes[file_hash] = img_data['local_path']
                        
                        downloaded_images.append(img_data)
                        
            except Exception as e:
                print(f"[Warning] Failed to download {img_data.get('url')}: {e}")
                continue
    
    # Save inline SVGs
    for svg_data in assets_data.get('svgs', []):
        try:
            index = svg_data['index']
            content = svg_data['content']
            filename = f"inline-svg-{index}.svg"
            filepath = svg_dir / filename
            filepath.write_text(content, encoding='utf-8')
            svg_data['local_path'] = f"assets/svg/{filename}"
            downloaded_svgs.append(svg_data)
        except Exception as e:
            print(f"[Warning] Failed to save SVG {index}: {e}")
    
    return {
        'images': downloaded_images,
        'svgs': downloaded_svgs,
        'total_images': len(downloaded_images),
        'total_svgs': len(downloaded_svgs),
        'deduplicated': len(all_images) - len(downloaded_images)
    }
