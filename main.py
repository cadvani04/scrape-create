"""
FastAPI Backend for Website Scraping
Handles single-URL scraping with full asset extraction
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
import asyncio
from datetime import datetime
import os
from pathlib import Path
import httpx

from scraper.scrape_controller import scrape_website
from scraper.v0_integration import build_v0_prompt, send_to_v0

app = FastAPI(
    title="Website Scraper API",
    description="Scrape websites for content, assets, design tokens, and metadata",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class ScrapeRequest(BaseModel):
    url: HttpUrl
    save_assets: bool = True
    convert_to_webp: bool = True
    timeout: int = 60000  # milliseconds

class ScrapeResponse(BaseModel):
    status: str
    url: str
    timestamp: str
    data: dict

@app.get("/")
async def root():
    return {
        "service": "Website Scraper API",
        "version": "1.0.0",
        "endpoints": {
            "/scrape": "POST - Scrape a website",
            "/health": "GET - Health check"
        }
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/scrape", response_model=ScrapeResponse)
async def scrape_endpoint(request: ScrapeRequest):
    """
    Scrape a website and extract all content, assets, and design tokens.
    
    - **url**: Website URL to scrape
    - **save_assets**: Whether to download and save assets locally
    - **convert_to_webp**: Convert images to WebP format
    - **timeout**: Page load timeout in milliseconds (default: 60000)
    """
    try:
        url = str(request.url)
        
        # Run the scraper
        result = await scrape_website(
            url=url,
            save_assets=request.save_assets,
            convert_to_webp=request.convert_to_webp,
            timeout=request.timeout
        )
        
        return ScrapeResponse(
            status="success",
            url=url,
            timestamp=datetime.now().isoformat(),
            data=result
        )
        
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=504,
            detail=f"Timeout while loading {request.url}. Try increasing the timeout parameter."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error scraping website: {str(e)}"
        )

@app.post("/scrape-and-create")
async def scrape_and_create(request: ScrapeRequest):
    """
    Scrape a website and automatically send to v0.dev to create an app.
    
    - **url**: Website URL to scrape
    - **save_assets**: Whether to download and save assets locally
    - **timeout**: Page load timeout in milliseconds
    """
    try:
        url = str(request.url)
        
        # Step 1: Scrape the website
        print(f"[API] Scraping {url}...")
        scrape_result = await scrape_website(
            url=url,
            save_assets=False,  # Faster without assets
            convert_to_webp=False,
            timeout=request.timeout
        )
        
        # Step 2: Build v0 prompt from scraped data
        print("[API] Building v0 prompt...")
        v0_prompt = build_v0_prompt(scrape_result, url)
        
        # Step 3: Send to v0.dev
        print("[API] Sending to v0.dev...")
        v0_api_key = os.environ.get("V0_API_KEY")
        
        if not v0_api_key:
            # Return scraped data with prompt, but don't send to v0
            return {
                "status": "success",
                "url": url,
                "timestamp": datetime.now().isoformat(),
                "scrape_data": scrape_result,
                "v0_prompt": v0_prompt,
                "v0_response": None,
                "message": "V0_API_KEY not set. Returning prompt only."
            }
        
        v0_response = await send_to_v0(v0_prompt, v0_api_key)
        
        return {
            "status": "success",
            "url": url,
            "timestamp": datetime.now().isoformat(),
            "scrape_data": scrape_result,
            "v0_prompt": v0_prompt,
            "v0_response": v0_response,
            "message": "Successfully scraped and sent to v0.dev!"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in scrape and create: {str(e)}"
        )

@app.delete("/clear-cache")
async def clear_cache():
    """Clear downloaded assets and cached data"""
    try:
        assets_dir = Path("assets")
        output_dir = Path("output")
        
        count = 0
        for directory in [assets_dir, output_dir]:
            if directory.exists():
                for file in directory.rglob("*"):
                    if file.is_file():
                        file.unlink()
                        count += 1
        
        return {
            "status": "success",
            "files_deleted": count,
            "message": "Cache cleared successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    import os
    
    # Use PORT from environment (Railway, Render, etc.) or default to 8000
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
