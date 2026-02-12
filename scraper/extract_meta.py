"""
Extract metadata: title, description, OpenGraph tags
"""

async def extract_meta(page, url):
    """
    Extract SEO and social media metadata from the page.
    
    Includes title, description, OpenGraph tags, Twitter cards, etc.
    """
    
    meta = await page.evaluate("""
        (url) => {
            const result = {
                url: url,
                title: '',
                description: '',
                keywords: [],
                opengraph: {},
                twitter: {},
                favicon: null,
                canonical: null,
                language: null,
                author: null
            };
            
            // Page title
            result.title = document.title || '';
            
            // Meta tags
            document.querySelectorAll('meta').forEach(meta => {
                const name = meta.getAttribute('name') || meta.getAttribute('property');
                const content = meta.getAttribute('content');
                
                if (!name || !content) return;
                
                const lowerName = name.toLowerCase();
                
                // Standard meta tags
                if (lowerName === 'description') {
                    result.description = content;
                } else if (lowerName === 'keywords') {
                    result.keywords = content.split(',').map(k => k.trim());
                } else if (lowerName === 'author') {
                    result.author = content;
                } else if (lowerName === 'language' || lowerName === 'lang') {
                    result.language = content;
                }
                
                // OpenGraph tags
                if (name.startsWith('og:')) {
                    const key = name.substring(3);
                    result.opengraph[key] = content;
                }
                
                // Twitter card tags
                if (name.startsWith('twitter:')) {
                    const key = name.substring(8);
                    result.twitter[key] = content;
                }
            });
            
            // Canonical URL
            const canonical = document.querySelector('link[rel="canonical"]');
            if (canonical) {
                result.canonical = canonical.getAttribute('href');
            }
            
            // Favicon
            const favicon = document.querySelector('link[rel="icon"]') || 
                          document.querySelector('link[rel="shortcut icon"]');
            if (favicon) {
                result.favicon = favicon.getAttribute('href');
            }
            
            // Language from html tag
            if (!result.language) {
                result.language = document.documentElement.lang || null;
            }
            
            return result;
        }
    """, url)
    
    return meta
