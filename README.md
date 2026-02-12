# Website Scraper API

A FastAPI-based web scraping service that extracts content, assets, design tokens, and metadata from any website using Playwright.

## Features

- 🚀 **Async/Await Architecture** - Fast, non-blocking scraping
- 🎨 **Complete Asset Extraction** - Images, SVGs, CSS backgrounds
- 🎭 **Design Token Extraction** - Colors, fonts, CSS variables
- 📝 **Content Structure** - Headings, paragraphs, lists, navigation
- 🔄 **WebP Conversion** - Automatic image optimization
- 🔍 **SEO Metadata** - OpenGraph, Twitter cards, meta tags
- ⚡ **Handles Dynamic Content** - Lazy-loaded images and JS-rendered content
- 🛡️ **Robust Error Handling** - Graceful timeout and error management

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Playwright Browsers

```bash
playwright install chromium
```

## Running the Server

### Development Mode

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at `http://localhost:8000`

## API Endpoints

### POST /scrape

Scrape a website and extract all data.

**Request Body:**
```json
{
  "url": "https://example.com",
  "save_assets": true,
  "convert_to_webp": true,
  "timeout": 60000
}
```

**Parameters:**
- `url` (required): Website URL to scrape
- `save_assets` (optional, default: true): Download assets locally
- `convert_to_webp` (optional, default: true): Convert images to WebP
- `timeout` (optional, default: 60000): Page load timeout in milliseconds

**Response:**
```json
{
  "status": "success",
  "url": "https://example.com",
  "timestamp": "2026-02-12T10:30:00",
  "data": {
    "content": { ... },
    "assets": { ... },
    "tokens": { ... },
    "meta": { ... }
  }
}
```

### GET /health

Health check endpoint.

### DELETE /clear-cache

Clear downloaded assets and cached data.

## Usage Examples

### Using curl

```bash
curl -X POST http://localhost:8000/scrape \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "save_assets": true,
    "convert_to_webp": true,
    "timeout": 60000
  }'
```

### Using Python

```python
import requests

response = requests.post(
    "http://localhost:8000/scrape",
    json={
        "url": "https://example.com",
        "save_assets": True,
        "convert_to_webp": True,
        "timeout": 60000
    }
)

data = response.json()
print(data)
```

### Using JavaScript/TypeScript

```javascript
const response = await fetch('http://localhost:8000/scrape', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    url: 'https://example.com',
    save_assets: true,
    convert_to_webp: true,
    timeout: 60000
  })
});

const data = await response.json();
console.log(data);
```

## Output Structure

The scraper generates 4 JSON files in the `output/` directory:

### content.json
- Headings (h1-h6) with hierarchy
- Paragraphs
- Lists (ul/ol)
- Navigation items
- Page structure (sections, articles)

### assets.json
- Images with URLs and local paths
- Inline SVGs
- Background images
- Deduplicated assets

### tokens.json
- CSS variables
- Color palette (primary, text, background, border)
- Font families, weights, and sizes
- Spacing values

### meta.json
- Page title and description
- Keywords and author
- OpenGraph tags
- Twitter card data
- Canonical URL and favicon

## Directory Structure

```
assetsscraper/
├── main.py                  # FastAPI application
├── requirements.txt         # Python dependencies
├── scraper/
│   ├── __init__.py
│   ├── scrape_controller.py # Main orchestrator
│   ├── extract_content.py   # Content extraction
│   ├── extract_assets.py    # Asset extraction & download
│   ├── extract_tokens.py    # Design token extraction
│   └── extract_meta.py      # Metadata extraction
├── assets/
│   ├── images/              # Downloaded images (WebP)
│   └── svg/                 # Inline SVGs
└── output/
    ├── content.json
    ├── assets.json
    ├── tokens.json
    └── meta.json
```

## Timeout Issues - FIXED! ✅

The previous timeout issues have been resolved by:

1. **Using Playwright instead of requests** - Handles JavaScript-rendered content
2. **Increased timeouts** - Default 60s, configurable per request
3. **Network idle detection** - Waits for all network requests to complete
4. **Lazy-load handling** - Scrolls page to trigger lazy-loaded images
5. **Async architecture** - Non-blocking operations
6. **Proper error handling** - Graceful degradation on failures

## Deployment

### Railway (Recommended) ⭐

**YES, this will work on Railway!** Full configuration included.

See [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) for detailed guide.

**Quick Deploy:**
```bash
# Push to GitHub, then on Railway:
1. New Project → Deploy from GitHub
2. Select your repo
3. Done! Railway auto-detects everything
```

Railway will automatically:
- Install Python dependencies
- Install Playwright + Chromium with system deps
- Set up health checks
- Provide a public URL

### Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install --with-deps chromium

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t scraper-api .
docker run -p 8000:8000 scraper-api
```

### Railway / Render / Fly.io

1. Connect your Git repository
2. Set build command: `pip install -r requirements.txt && playwright install chromium`
3. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Deploy!

## Performance Tips

- Use `save_assets: false` if you only need metadata
- Increase timeout for slow websites
- Run with multiple workers for high traffic
- Consider adding Redis caching for frequently scraped sites

## License

MIT License - Use for client-owned or permitted websites only.
# scrape-create
