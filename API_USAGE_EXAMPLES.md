# 🌐 How to Hit the API from Any Service

Once deployed on Railway, you get a public URL like:
```
https://your-app-name.up.railway.app
```

**Anyone** can make HTTP POST requests to this URL. Here are examples from different platforms:

---

## 🔥 JavaScript/TypeScript (Frontend)

### React Example

```typescript
// In your React component
const scrapeWebsite = async (url: string) => {
  try {
    const response = await fetch('https://your-app.up.railway.app/scrape', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        url: url,
        save_assets: false,  // Set to false for faster response
        convert_to_webp: true,
        timeout: 60000
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Scraping failed:', error);
    throw error;
  }
};

// Usage in component
function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleScrape = async () => {
    setLoading(true);
    try {
      const data = await scrapeWebsite('https://example.com');
      setResult(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <button onClick={handleScrape} disabled={loading}>
        {loading ? 'Scraping...' : 'Scrape Website'}
      </button>
      {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
    </div>
  );
}
```

### Next.js API Route

```typescript
// pages/api/scrape.ts
import type { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { url } = req.body;

  try {
    const response = await fetch('https://your-app.up.railway.app/scrape', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        url,
        save_assets: false,
        timeout: 60000
      })
    });

    const data = await response.json();
    res.status(200).json(data);
  } catch (error) {
    res.status(500).json({ error: 'Scraping failed' });
  }
}
```

### Node.js

```javascript
const axios = require('axios');

async function scrapeWebsite(url) {
  try {
    const response = await axios.post(
      'https://your-app.up.railway.app/scrape',
      {
        url: url,
        save_assets: false,
        timeout: 60000
      }
    );
    
    return response.data;
  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
    throw error;
  }
}

// Usage
scrapeWebsite('https://example.com')
  .then(data => console.log(data))
  .catch(err => console.error(err));
```

---

## 🐍 Python

### Using requests

```python
import requests

def scrape_website(url: str):
    api_url = "https://your-app.up.railway.app/scrape"
    
    payload = {
        "url": url,
        "save_assets": False,
        "convert_to_webp": True,
        "timeout": 60000
    }
    
    try:
        response = requests.post(api_url, json=payload, timeout=120)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        raise

# Usage
result = scrape_website("https://example.com")
print(result['data']['meta']['title'])
```

### Using httpx (async)

```python
import httpx
import asyncio

async def scrape_website(url: str):
    api_url = "https://your-app.up.railway.app/scrape"
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            api_url,
            json={
                "url": url,
                "save_assets": False,
                "timeout": 60000
            }
        )
        response.raise_for_status()
        return response.json()

# Usage
result = asyncio.run(scrape_website("https://example.com"))
```

---

## 🦀 Rust

```rust
use reqwest;
use serde_json::json;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = reqwest::Client::new();
    
    let response = client
        .post("https://your-app.up.railway.app/scrape")
        .json(&json!({
            "url": "https://example.com",
            "save_assets": false,
            "timeout": 60000
        }))
        .send()
        .await?;
    
    let data: serde_json::Value = response.json().await?;
    println!("{:#?}", data);
    
    Ok(())
}
```

---

## 🏃 Go

```go
package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "io"
    "net/http"
)

type ScrapeRequest struct {
    URL           string `json:"url"`
    SaveAssets    bool   `json:"save_assets"`
    ConvertToWebp bool   `json:"convert_to_webp"`
    Timeout       int    `json:"timeout"`
}

func scrapeWebsite(url string) (map[string]interface{}, error) {
    apiURL := "https://your-app.up.railway.app/scrape"
    
    payload := ScrapeRequest{
        URL:           url,
        SaveAssets:    false,
        ConvertToWebp: true,
        Timeout:       60000,
    }
    
    jsonData, err := json.Marshal(payload)
    if err != nil {
        return nil, err
    }
    
    resp, err := http.Post(apiURL, "application/json", bytes.NewBuffer(jsonData))
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    
    body, err := io.ReadAll(resp.Body)
    if err != nil {
        return nil, err
    }
    
    var result map[string]interface{}
    err = json.Unmarshal(body, &result)
    if err != nil {
        return nil, err
    }
    
    return result, nil
}

func main() {
    result, err := scrapeWebsite("https://example.com")
    if err != nil {
        fmt.Println("Error:", err)
        return
    }
    
    fmt.Printf("%+v\n", result)
}
```

---

## 💎 Ruby

```ruby
require 'net/http'
require 'json'
require 'uri'

def scrape_website(url)
  api_url = URI('https://your-app.up.railway.app/scrape')
  
  payload = {
    url: url,
    save_assets: false,
    timeout: 60000
  }
  
  http = Net::HTTP.new(api_url.host, api_url.port)
  http.use_ssl = true
  http.read_timeout = 120
  
  request = Net::HTTP::Post.new(api_url)
  request['Content-Type'] = 'application/json'
  request.body = payload.to_json
  
  response = http.request(request)
  JSON.parse(response.body)
end

# Usage
result = scrape_website('https://example.com')
puts result['data']['meta']['title']
```

---

## 📱 cURL (Command Line)

### Basic Request
```bash
curl -X POST https://your-app.up.railway.app/scrape \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "save_assets": false,
    "timeout": 60000
  }'
```

### With Auth Header (if you add authentication)
```bash
curl -X POST https://your-app.up.railway.app/scrape \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-key" \
  -d '{
    "url": "https://example.com",
    "save_assets": false
  }'
```

### Save to File
```bash
curl -X POST https://your-app.up.railway.app/scrape \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}' \
  -o output.json
```

---

## 🔧 No-Code Tools

### Zapier
1. Choose "Webhooks by Zapier"
2. Action: POST
3. URL: `https://your-app.up.railway.app/scrape`
4. Data: 
   ```json
   {
     "url": "https://example.com",
     "save_assets": false
   }
   ```

### Make (Integromat)
1. Add HTTP module
2. Method: POST
3. URL: `https://your-app.up.railway.app/scrape`
4. Body type: Raw
5. Content type: JSON
6. Request content: Your JSON payload

### n8n
1. Add HTTP Request node
2. Method: POST
3. URL: `https://your-app.up.railway.app/scrape`
4. Body: JSON
5. Add your parameters

---

## 🎯 Real-World Use Cases

### 1. v0.dev Integration
```typescript
// Scrape site, then send to v0.dev
async function cloneWebsite(url: string) {
  // 1. Scrape website
  const scrapeResult = await fetch('https://your-app.up.railway.app/scrape', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url, save_assets: false })
  }).then(r => r.json());
  
  // 2. Build prompt from scraped data
  const prompt = buildV0Prompt(scrapeResult.data);
  
  // 3. Send to v0.dev
  const v0Result = await fetch('https://api.v0.dev/v1/chats', {
    method: 'POST',
    headers: {
      'Authorization': 'Bearer YOUR_V0_KEY',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      message: prompt,
      modelConfiguration: { responseMode: 'sync' }
    })
  }).then(r => r.json());
  
  return v0Result;
}
```

### 2. Scheduled Scraping (Cron)
```javascript
// In your backend, run this on a schedule
const cron = require('node-cron');

// Run every day at 9 AM
cron.schedule('0 9 * * *', async () => {
  const sites = ['https://example1.com', 'https://example2.com'];
  
  for (const site of sites) {
    const result = await fetch('https://your-app.up.railway.app/scrape', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: site })
    }).then(r => r.json());
    
    // Save to database, send notification, etc.
    await saveToDatabase(result);
  }
});
```

### 3. Webhook Endpoint
```typescript
// Receive webhook, scrape site, return data
app.post('/webhook/scrape', async (req, res) => {
  const { url } = req.body;
  
  const result = await fetch('https://your-app.up.railway.app/scrape', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url })
  }).then(r => r.json());
  
  res.json(result);
});
```

---

## 🔐 Adding Authentication (Optional)

If you want to restrict access, add this to `main.py`:

```python
from fastapi import Header, HTTPException
import os

async def verify_api_key(x_api_key: str = Header(None)):
    correct_key = os.environ.get("API_KEY", "your-secret-key")
    if x_api_key != correct_key:
        raise HTTPException(status_code=401, detail="Invalid API Key")

# Then add to endpoint
@app.post("/scrape", dependencies=[Depends(verify_api_key)])
async def scrape_endpoint(request: ScrapeRequest):
    # ... existing code
```

Set `API_KEY` environment variable in Railway, then call with:

```bash
curl -X POST https://your-app.up.railway.app/scrape \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-key" \
  -d '{"url": "https://example.com"}'
```

---

## 📊 Response Format

All requests return this structure:

```json
{
  "status": "success",
  "url": "https://example.com",
  "timestamp": "2026-02-12T10:30:00",
  "data": {
    "content": {
      "headings": [...],
      "paragraphs": [...],
      "lists": [...],
      "navigation": [...]
    },
    "assets": {
      "images": [...],
      "svgs": [...]
    },
    "tokens": {
      "colors": {...},
      "fonts": {...},
      "css_variables": {...}
    },
    "meta": {
      "title": "...",
      "description": "...",
      "opengraph": {...}
    }
  }
}
```

---

## 🚀 Interactive API Docs

Once deployed, visit:
```
https://your-app.up.railway.app/docs
```

You can **test the API directly in your browser** with Swagger UI!

---

## ⚡ Quick Reference

| Platform | HTTP Client |
|----------|-------------|
| JavaScript | `fetch()` |
| Node.js | `axios`, `node-fetch` |
| Python | `requests`, `httpx` |
| Go | `net/http` |
| Rust | `reqwest` |
| Ruby | `net/http` |
| PHP | `guzzle`, `curl` |
| Command Line | `curl`, `httpie` |

**Bottom Line:** Any service that can make HTTP POST requests can use your API! 🎉
