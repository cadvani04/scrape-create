"""
Extract text content and page structure
"""

async def extract_content(page):
    """
    Extract all visible text content and page structure.
    
    Returns structured content including headings, paragraphs, lists, and navigation.
    """
    
    content = await page.evaluate("""
        () => {
            const result = {
                headings: [],
                paragraphs: [],
                lists: [],
                navigation: [],
                structure: []
            };
            
            // Helper to check if element is visible
            function isVisible(el) {
                const style = window.getComputedStyle(el);
                return style.display !== 'none' && 
                       style.visibility !== 'hidden' && 
                       style.opacity !== '0' &&
                       el.offsetParent !== null;
            }
            
            // Helper to get clean text
            function getCleanText(el) {
                return el.innerText?.trim() || '';
            }
            
            // Extract headings with hierarchy
            ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'].forEach(tag => {
                document.querySelectorAll(tag).forEach(el => {
                    if (isVisible(el)) {
                        const text = getCleanText(el);
                        if (text) {
                            result.headings.push({
                                level: parseInt(tag[1]),
                                text: text,
                                tag: tag
                            });
                        }
                    }
                });
            });
            
            // Extract paragraphs (exclude hidden ones)
            document.querySelectorAll('p').forEach(el => {
                if (isVisible(el)) {
                    const text = getCleanText(el);
                    if (text && text.length > 10) {  // Filter out very short paragraphs
                        result.paragraphs.push(text);
                    }
                }
            });
            
            // Extract lists
            document.querySelectorAll('ul, ol').forEach(el => {
                if (isVisible(el)) {
                    const items = Array.from(el.querySelectorAll('li'))
                        .filter(li => isVisible(li))
                        .map(li => getCleanText(li))
                        .filter(text => text);
                    
                    if (items.length > 0) {
                        result.lists.push({
                            type: el.tagName.toLowerCase(),
                            items: items
                        });
                    }
                }
            });
            
            // Extract navigation items
            document.querySelectorAll('nav a, header a, [role="navigation"] a').forEach(el => {
                if (isVisible(el)) {
                    const text = getCleanText(el);
                    const href = el.getAttribute('href');
                    if (text) {
                        result.navigation.push({
                            text: text,
                            href: href
                        });
                    }
                }
            });
            
            // Extract page structure (sections and their content)
            document.querySelectorAll('section, article, main, aside, header, footer').forEach(el => {
                if (isVisible(el)) {
                    const tagName = el.tagName.toLowerCase();
                    const className = el.className;
                    const id = el.id;
                    
                    // Get headings within this section
                    const sectionHeadings = Array.from(el.querySelectorAll('h1, h2, h3, h4, h5, h6'))
                        .filter(h => isVisible(h))
                        .map(h => getCleanText(h))
                        .filter(text => text);
                    
                    if (sectionHeadings.length > 0 || tagName === 'header' || tagName === 'footer') {
                        result.structure.push({
                            tag: tagName,
                            id: id || null,
                            class: className || null,
                            headings: sectionHeadings
                        });
                    }
                }
            });
            
            return result;
        }
    """)
    
    return content
