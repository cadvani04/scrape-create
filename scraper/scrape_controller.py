"""
Main scraper controller that orchestrates all extraction tasks
"""

from playwright.async_api import async_playwright
import json
from pathlib import Path
from datetime import datetime

from .extract_content import extract_content
from .extract_assets import extract_assets, download_assets
from .extract_tokens import extract_tokens
from .extract_meta import extract_meta


async def scrape_website(url: str, save_assets: bool = True, convert_to_webp: bool = True, timeout: int = 60000) -> dict:
    """
    Main scraping function that coordinates all extraction tasks.
    
    Args:
        url: Website URL to scrape
        save_assets: Whether to download assets locally
        convert_to_webp: Convert images to WebP format
        timeout: Page load timeout in milliseconds
    
    Returns:
        Dictionary containing all extracted data
    """
    
    async with async_playwright() as p:
        # Launch browser with increased timeout settings
        # Railway/production-ready configuration
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-gpu',
                '--disable-software-rasterizer',
                '--disable-extensions',
                '--single-process',  # Important for Railway
            ]
        )
        
        try:
            # Create a new context with realistic settings
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            
            page = await context.new_page()
            
            # Set longer timeout for navigation
            page.set_default_timeout(timeout)
            
            print(f"[Scraper] Navigating to {url}...")
            
            # Navigate and wait for network to be idle
            await page.goto(url, wait_until='networkidle', timeout=timeout)
            
            # Additional wait for lazy-loaded content
            await page.wait_for_timeout(2000)
            
            # Scroll to bottom to trigger lazy-loaded images
            await page.evaluate("""
                async () => {
                    await new Promise((resolve) => {
                        let totalHeight = 0;
                        const distance = 100;
                        const timer = setInterval(() => {
                            window.scrollBy(0, distance);
                            totalHeight += distance;
                            
                            if(totalHeight >= document.body.scrollHeight){
                                clearInterval(timer);
                                resolve();
                            }
                        }, 100);
                    });
                }
            """)
            
            # Scroll back to top
            await page.evaluate("window.scrollTo(0, 0)")
            await page.wait_for_timeout(1000)
            
            print("[Scraper] Page loaded, extracting data...")
            
            # Extract all data in parallel where possible
            content_data = await extract_content(page)
            assets_data = await extract_assets(page, url)
            tokens_data = await extract_tokens(page)
            meta_data = await extract_meta(page, url)
            
            # Download assets if requested
            if save_assets and assets_data:
                print("[Scraper] Downloading assets...")
                assets_data = await download_assets(assets_data, convert_to_webp)
            
            # Save output files
            output_dir = Path("output")
            output_dir.mkdir(exist_ok=True)
            
            # Save individual JSON files
            with open(output_dir / "content.json", "w", encoding="utf-8") as f:
                json.dump(content_data, f, indent=2, ensure_ascii=False)
            
            with open(output_dir / "assets.json", "w", encoding="utf-8") as f:
                json.dump(assets_data, f, indent=2, ensure_ascii=False)
            
            with open(output_dir / "tokens.json", "w", encoding="utf-8") as f:
                json.dump(tokens_data, f, indent=2, ensure_ascii=False)
            
            with open(output_dir / "meta.json", "w", encoding="utf-8") as f:
                json.dump(meta_data, f, indent=2, ensure_ascii=False)
            
            print("[Scraper] Scraping complete!")
            
            # Return combined result
            return {
                "content": content_data,
                "assets": assets_data,
                "tokens": tokens_data,
                "meta": meta_data,
                "scraped_at": datetime.now().isoformat()
            }
            
        finally:
            await browser.close()
