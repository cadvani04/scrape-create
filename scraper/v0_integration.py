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
    
    lines.append("Recreate this website using React + Tailwind CSS + shadcn/ui.")
    lines.append("")
    lines.append("# Website Information")
    lines.append(f"- Original URL: {url}")
    lines.append(f"- Title: {meta.get('title', 'Untitled')}")
    if meta.get('description'):
        lines.append(f"- Description: {meta.get('description')}")
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
    
    # Content structure
    if content.get('headings'):
        lines.append("# Content Structure")
        lines.append("")
        lines.append("## Key Headings (maintain hierarchy)")
        for heading in content['headings'][:8]:
            level = heading.get('level', 1)
            text = heading.get('text', '')
            lines.append(f"{'#' * level} {text}")
        lines.append("")
    
    # Key content
    if content.get('paragraphs'):
        lines.append("## Key Copy/Content")
        for para in content['paragraphs'][:5]:
            if len(para) > 20:  # Skip very short paragraphs
                lines.append(f"- {para[:150]}..." if len(para) > 150 else f"- {para}")
        lines.append("")
    
    # Navigation
    if content.get('navigation'):
        lines.append("## Navigation Items")
        for nav in content['navigation'][:8]:
            lines.append(f"- {nav.get('text', '')}")
        lines.append("")
    
    # Images
    if assets.get('images'):
        lines.append("# Visual Assets")
        lines.append("")
        lines.append("## Images (use placeholder images with similar style)")
        for img in assets['images'][:5]:
            alt = img.get('alt', 'Image')
            lines.append(f"- {alt}: {img.get('url', '')[:80]}")
        lines.append("")
    
    # Layout guidance
    lines.append("# Layout & Design Guidelines")
    lines.append("")
    lines.append("## Structure")
    lines.append("- Sticky navigation bar at top")
    lines.append("- Hero section with primary CTA")
    lines.append("- Content sections with clear hierarchy")
    lines.append("- Footer with contact/info")
    lines.append("")
    lines.append("## Style")
    lines.append("- Modern, clean design")
    lines.append("- Mobile-first responsive")
    lines.append("- Smooth animations and transitions")
    lines.append("- High contrast for accessibility")
    lines.append("- Use the extracted color palette")
    lines.append("")
    lines.append("## Components Needed")
    if content.get('navigation'):
        lines.append("- Navigation/Header")
    lines.append("- Hero section")
    if content.get('headings'):
        lines.append(f"- {len([h for h in content['headings'] if h.get('level', 1) == 2])} main content sections")
    if assets.get('images'):
        lines.append("- Image gallery or showcase")
    lines.append("- Footer")
    lines.append("")
    lines.append("# Important")
    lines.append("- Match the visual style and brand feel of the original")
    lines.append("- Maintain the content hierarchy and flow")
    lines.append("- Make it fully responsive and accessible")
    lines.append("- Use real content from above, not lorem ipsum")
    
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
