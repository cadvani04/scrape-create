"""
v0.dev integration for creating apps from scraped data
"""

import httpx
from typing import Dict, Any


def build_v0_prompt(scrape_data: Dict[str, Any], url: str) -> str:
    """
    Build a comprehensive v0 prompt from scraped website data.
    
    Args:
        scrape_data: The scraped data from scrape_website()
        url: Original website URL
    
    Returns:
        Formatted prompt string for v0.dev
    """
    
    content = scrape_data.get('content', {})
    assets = scrape_data.get('assets', {})
    tokens = scrape_data.get('tokens', {})
    meta = scrape_data.get('meta', {})
    
    # Build the prompt
    lines = []
    
    lines.append("Create a BEAUTIFUL, MODERN, PROFESSIONAL website using React + Tailwind CSS + shadcn/ui.")
    lines.append("")
    lines.append("🚨 CRITICAL REQUIREMENTS:")
    lines.append("1. Use EVERY piece of text content provided below EXACTLY as written")
    lines.append("2. Use ALL image URLs provided - do NOT use placeholders or dummy images")
    lines.append("3. Match the visual hierarchy and layout of the original")
    lines.append("4. Make it look modern, clean, and professional")
    lines.append("5. Fully responsive and mobile-friendly")
    lines.append("")
    lines.append("# Original Website")
    lines.append(f"URL: {url}")
    lines.append(f"Title: {meta.get('title', 'Untitled')}")
    if meta.get('description'):
        lines.append(f"Description: {meta.get('description')}")
    lines.append("")
    
    # Design tokens
    if tokens.get('colors'):
        lines.append("# Design System")
        lines.append("")
        
        colors = tokens['colors']
        if colors.get('primary'):
            lines.append("## Primary Colors")
            for color in colors['primary'][:3]:
                lines.append(f"- {color}")
            lines.append("")
        
        if colors.get('text'):
            lines.append("## Text Colors")
            for color in colors['text'][:2]:
                lines.append(f"- {color}")
            lines.append("")
    
    # Fonts
    if tokens.get('fonts', {}).get('families'):
        lines.append("## Typography")
        for font in tokens['fonts']['families'][:2]:
            lines.append(f"- Font: {font}")
        lines.append("")
    
    # Images - MOST IMPORTANT - Put this FIRST
    if assets.get('images'):
        lines.append("# 🖼️ IMAGES - USE THESE EXACT URLs!")
        lines.append("")
        lines.append("⚠️ IMPORTANT: Use these EXACT image URLs in your code. Do NOT use placeholders!")
        lines.append("")
        for i, img in enumerate(assets['images'], 1):
            url_full = img.get('url', '')
            alt = img.get('alt', f'Image {i}')
            lines.append(f"{i}. {alt}")
            lines.append(f"   URL: {url_full}")
            lines.append(f"   Alt text: {alt}")
            lines.append("")
        lines.append("")
    
    # All Headings with EXACT text
    if content.get('headings'):
        lines.append("# 📝 HEADINGS - Use EXACT Text")
        lines.append("")
        lines.append("Copy these headings EXACTLY as written, maintaining hierarchy:")
        lines.append("")
        for heading in content['headings']:
            level = heading.get('level', 1)
            text = heading.get('text', '')
            lines.append(f"{'#' * level} {text}")
        lines.append("")
    
    # All Paragraphs with EXACT text
    if content.get('paragraphs'):
        lines.append("# 📄 PARAGRAPHS - Use EXACT Text")
        lines.append("")
        lines.append("Include ALL of this text content in your website:")
        lines.append("")
        for i, para in enumerate(content['paragraphs'], 1):
            if len(para) > 10:
                lines.append(f"Paragraph {i}:")
                lines.append(f'"{para}"')
                lines.append("")
        lines.append("")
    
    # Navigation
    if content.get('navigation'):
        lines.append("# 🧭 NAVIGATION - Use EXACT Text")
        lines.append("")
        for nav in content['navigation']:
            text = nav.get('text', '')
            href = nav.get('href', '#')
            if text:
                lines.append(f"- {text} (link: {href})")
        lines.append("")
    
    # Lists
    if content.get('lists'):
        lines.append("# 📋 LISTS - Use EXACT Text")
        lines.append("")
        for list_item in content['lists']:
            list_type = list_item.get('type', 'ul')
            items = list_item.get('items', [])
            if items:
                for item in items:
                    lines.append(f"• {item}")
                lines.append("")
    
    # Layout guidance
    lines.append("# 🎨 DESIGN & LAYOUT REQUIREMENTS")
    lines.append("")
    lines.append("## Layout Structure")
    lines.append("1. **Header/Navigation**")
    lines.append("   - Sticky/fixed at top")
    lines.append("   - Use navigation items listed above")
    lines.append("")
    lines.append("2. **Hero Section**")
    lines.append("   - Use first image from images list above")
    lines.append("   - Use first heading as hero title")
    lines.append("   - Include primary CTA button")
    lines.append("")
    lines.append("3. **Content Sections**")
    lines.append("   - Use ALL headings in proper hierarchy")
    lines.append("   - Use ALL paragraph text provided")
    lines.append("   - Place images where they appear in the content flow")
    lines.append("")
    lines.append("4. **Footer**")
    lines.append("   - Contact information")
    lines.append("   - Navigation links")
    lines.append("")
    lines.append("## Visual Style")
    lines.append("- Modern, clean, professional aesthetic")
    lines.append("- Use color palette extracted above")
    lines.append("- Beautiful typography with proper hierarchy")
    lines.append("- Smooth animations and transitions")
    lines.append("- High contrast for readability")
    lines.append("- Mobile-first responsive design")
    lines.append("")
    lines.append("## 🚨 CRITICAL - DO NOT:")
    lines.append("- ❌ Do NOT use placeholder images - use the EXACT URLs provided")
    lines.append("- ❌ Do NOT use lorem ipsum - use the EXACT text provided")
    lines.append("- ❌ Do NOT skip any content - include EVERYTHING")
    lines.append("- ❌ Do NOT change the wording - copy it EXACTLY")
    lines.append("")
    lines.append("## ✅ MUST DO:")
    lines.append("- ✅ Use ALL images from the images list with their exact URLs")
    lines.append("- ✅ Use ALL text content exactly as provided")
    lines.append("- ✅ Make it look modern and beautiful")
    lines.append("- ✅ Make it fully functional and responsive")
    lines.append("- ✅ Use proper semantic HTML and accessibility")
    
    return "\n".join(lines)


async def send_to_v0(prompt: str, api_key: str) -> Dict[str, Any]:
    """
    Send prompt to v0.dev API to generate a website.
    
    Args:
        prompt: The formatted prompt
        api_key: v0.dev API key
    
    Returns:
        v0.dev API response
    """
    
    url = "https://api.v0.dev/v1/chats"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "system": "You are an expert frontend engineer. Create a complete, production-ready React + Tailwind CSS website. Use shadcn/ui components where appropriate. Return clean, well-structured code.",
        "message": prompt,
        "modelConfiguration": {
            "responseMode": "sync"
        }
    }
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(url, headers=headers, json=payload)
        
        if response.status_code != 200:
            raise Exception(f"v0 API error {response.status_code}: {response.text}")
        
        return response.json()
