"""
Extract design tokens: colors, fonts, CSS variables
"""

async def extract_tokens(page):
    """
    Extract design tokens from the page including CSS variables,
    colors, and font families.
    """
    
    tokens = await page.evaluate("""
        () => {
            const result = {
                css_variables: {},
                colors: {
                    primary: [],
                    text: [],
                    background: [],
                    border: []
                },
                fonts: {
                    families: [],
                    weights: [],
                    sizes: []
                },
                spacing: [],
                breakpoints: []
            };
            
            // Extract CSS variables from :root
            const rootStyles = window.getComputedStyle(document.documentElement);
            
            // Get all CSS variable names
            for (let i = 0; i < rootStyles.length; i++) {
                const prop = rootStyles[i];
                if (prop.startsWith('--')) {
                    const value = rootStyles.getPropertyValue(prop).trim();
                    result.css_variables[prop] = value;
                }
            }
            
            // Helper to normalize color
            function normalizeColor(color) {
                const div = document.createElement('div');
                div.style.color = color;
                document.body.appendChild(div);
                const computed = window.getComputedStyle(div).color;
                document.body.removeChild(div);
                return computed;
            }
            
            // Helper to check if color is unique
            function addUniqueColor(array, color) {
                const normalized = normalizeColor(color);
                if (normalized && normalized !== 'rgba(0, 0, 0, 0)' && !array.includes(normalized)) {
                    array.push(normalized);
                }
            }
            
            // Sample elements to extract colors and fonts
            const elementsToSample = [
                ...document.querySelectorAll('h1, h2, h3, h4, h5, h6'),
                ...document.querySelectorAll('p'),
                ...document.querySelectorAll('a'),
                ...document.querySelectorAll('button'),
                ...document.querySelectorAll('[class*="button"]'),
                ...document.querySelectorAll('[class*="btn"]'),
                document.body,
                document.querySelector('header'),
                document.querySelector('nav'),
                document.querySelector('footer')
            ].filter(Boolean);
            
            const seenFonts = new Set();
            const seenSizes = new Set();
            const seenWeights = new Set();
            
            elementsToSample.forEach(el => {
                const style = window.getComputedStyle(el);
                
                // Extract colors
                const color = style.color;
                const bgColor = style.backgroundColor;
                const borderColor = style.borderColor;
                
                // Categorize colors
                if (el.tagName === 'BODY' || el.tagName === 'HTML') {
                    addUniqueColor(result.colors.background, bgColor);
                } else if (el.tagName.startsWith('H') || el.tagName === 'P' || el.tagName === 'SPAN') {
                    addUniqueColor(result.colors.text, color);
                } else if (el.tagName === 'BUTTON' || el.className.includes('button') || el.className.includes('btn')) {
                    addUniqueColor(result.colors.primary, bgColor);
                    addUniqueColor(result.colors.primary, color);
                }
                
                if (bgColor && bgColor !== 'rgba(0, 0, 0, 0)') {
                    addUniqueColor(result.colors.background, bgColor);
                }
                
                if (borderColor && borderColor !== 'rgba(0, 0, 0, 0)') {
                    addUniqueColor(result.colors.border, borderColor);
                }
                
                // Extract fonts
                const fontFamily = style.fontFamily;
                if (fontFamily && !seenFonts.has(fontFamily)) {
                    seenFonts.add(fontFamily);
                    result.fonts.families.push(fontFamily);
                }
                
                const fontSize = style.fontSize;
                if (fontSize && !seenSizes.has(fontSize)) {
                    seenSizes.add(fontSize);
                    result.fonts.sizes.push(fontSize);
                }
                
                const fontWeight = style.fontWeight;
                if (fontWeight && !seenWeights.has(fontWeight)) {
                    seenWeights.add(fontWeight);
                    result.fonts.weights.push(fontWeight);
                }
            });
            
            // Try to extract spacing values from common elements
            const spacingElements = document.querySelectorAll('section, div[class*="container"], div[class*="wrapper"]');
            const seenSpacing = new Set();
            
            spacingElements.forEach(el => {
                const style = window.getComputedStyle(el);
                [style.padding, style.margin, style.gap].forEach(value => {
                    if (value && value !== '0px' && !seenSpacing.has(value)) {
                        seenSpacing.add(value);
                        result.spacing.push(value);
                    }
                });
            });
            
            // Sort font sizes numerically
            result.fonts.sizes.sort((a, b) => parseFloat(a) - parseFloat(b));
            
            // Limit results to most common values
            result.colors.primary = result.colors.primary.slice(0, 10);
            result.colors.text = result.colors.text.slice(0, 10);
            result.colors.background = result.colors.background.slice(0, 10);
            result.colors.border = result.colors.border.slice(0, 10);
            result.spacing = result.spacing.slice(0, 15);
            
            return result;
        }
    """)
    
    return tokens
