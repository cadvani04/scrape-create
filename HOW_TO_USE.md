# 🌐 How Any Service Hits This API

## TL;DR

Once deployed on Railway, you get a **public HTTPS URL**:
```
https://your-app-name.up.railway.app
```

**ANY service/app/frontend can make HTTP POST requests to this URL.** No authentication required (unless you add it).

---

## 🚀 After Deployment

### Step 1: Deploy to Railway
```bash
# Push to GitHub, then on Railway.app:
New Project → Deploy from GitHub → Select repo
```

### Step 2: Get Your URL

Railway automatically gives you a URL. Find it in:
- Railway Dashboard → Your Project → Settings → Domains
- Or run: `railway domain` (if using CLI)

Example URL: `https://assetsscraper-production.up.railway.app`

### Step 3: Hit It From Anywhere!

**From JavaScript (Frontend):**
```javascript
const response = await fetch('https://your-app.up.railway.app/scrape', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ url: 'https://example.com' })
});
const data = await response.json();
```

**From Python:**
```python
import requests
response = requests.post(
    'https://your-app.up.railway.app/scrape',
    json={'url': 'https://example.com'}
)
data = response.json()
```

**From Command Line:**
```bash
curl -X POST https://your-app.up.railway.app/scrape \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

**From ANY language/platform that can make HTTP requests!**

---

## 🎯 Real-World Examples

### From React/Next.js App
```typescript
// app/page.tsx
'use client';

export default function Home() {
  const scrapeWebsite = async () => {
    const res = await fetch('https://your-app.up.railway.app/scrape', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: 'https://example.com' })
    });
    const data = await res.json();
    console.log(data);
  };

  return <button onClick={scrapeWebsite}>Scrape</button>;
}
```

### From v0.dev Workflow
```typescript
// 1. Hit your API to scrape a site
const scraped = await fetch('https://your-app.up.railway.app/scrape', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ url: targetUrl })
}).then(r => r.json());

// 2. Use scraped data to build v0 prompt
const prompt = `
  Recreate this website using React + Tailwind:
  Title: ${scraped.data.meta.title}
  Colors: ${scraped.data.tokens.colors.primary}
  Content: ${scraped.data.content.headings}
`;

// 3. Send to v0.dev
const v0Response = await fetch('https://api.v0.dev/v1/chats', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_V0_KEY',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ message: prompt })
});
```

### From Backend API
```javascript
// Express.js endpoint
app.post('/clone-website', async (req, res) => {
  const { url } = req.body;
  
  // Call your Railway API
  const scraped = await fetch('https://your-app.up.railway.app/scrape', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url })
  }).then(r => r.json());
  
  res.json(scraped);
});
```

### From Zapier/Make/n8n
1. Add "HTTP Request" module
2. Method: POST
3. URL: `https://your-app.up.railway.app/scrape`
4. Headers: `Content-Type: application/json`
5. Body: `{"url": "https://example.com"}`

---

## 📚 Complete Examples

See [API_USAGE_EXAMPLES.md](API_USAGE_EXAMPLES.md) for examples in:
- JavaScript/TypeScript
- Python
- Go
- Rust
- Ruby
- PHP
- cURL
- And more!

---

## 🔐 Optional: Add Authentication

If you want to restrict access, add this to `main.py`:

```python
from fastapi import Header, HTTPException

async def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != "your-secret-key":
        raise HTTPException(status_code=401, detail="Invalid API Key")

@app.post("/scrape", dependencies=[Depends(verify_api_key)])
async def scrape_endpoint(request: ScrapeRequest):
    # existing code...
```

Then set `API_KEY` in Railway environment variables and call with:

```bash
curl -X POST https://your-app.up.railway.app/scrape \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-key" \
  -d '{"url": "https://example.com"}'
```

---

## ✅ Summary

1. **Deploy to Railway** → Get public URL
2. **Make HTTP POST requests** to `/scrape` endpoint
3. **From ANY language/platform** that can make HTTP requests
4. **No special setup required** - just standard HTTP!

**Your API is accessible from:**
- ✅ Web browsers (fetch, axios)
- ✅ Mobile apps (HTTP clients)
- ✅ Backend services (any language)
- ✅ No-code tools (Zapier, Make, n8n)
- ✅ Command line (curl)
- ✅ Serverless functions (Vercel, Netlify)
- ✅ Literally anywhere that can make HTTP requests!

🎉 **That's it!** Your scraper is now a public API that anyone can use.
