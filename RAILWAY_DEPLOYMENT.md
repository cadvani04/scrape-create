# Railway Deployment Guide

## ✅ This WILL work on Railway!

The scraper is fully configured for Railway deployment with Playwright support.

## 🚀 Quick Deploy to Railway

### Method 1: Railway CLI (Recommended)

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up
```

### Method 2: GitHub Integration

1. Push this repo to GitHub
2. Go to [railway.app](https://railway.app)
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-detect Python and deploy!

## ⚙️ Configuration

### Required Environment Variables

Railway automatically provides `$PORT` - no configuration needed!

### Optional Environment Variables

Add these in Railway dashboard under "Variables":

```bash
# Increase if scraping slow sites
DEFAULT_TIMEOUT=90000

# For production optimization
WORKERS=2
```

## 📝 Build Configuration

The `railway.toml` file handles everything:

```toml
[build]
buildCommand = "pip install -r requirements.txt && playwright install --with-deps chromium"

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
```

**Key Points:**
- `--with-deps` installs all system dependencies for Chromium
- Healthcheck endpoint ensures Railway knows when app is ready
- Automatic restarts on failure

## 🧪 Testing After Deployment

Once deployed, Railway gives you a URL like: `https://your-app.up.railway.app`

Test it:

```bash
curl -X POST https://your-app.up.railway.app/scrape \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "timeout": 60000
  }'
```

Or visit the interactive docs:
```
https://your-app.up.railway.app/docs
```

## 🐛 Troubleshooting

### If build fails:

1. **Check build logs** in Railway dashboard
2. **Ensure Python version** - Railway uses Python 3.11+ by default (compatible)
3. **Memory issues** - Upgrade to Railway's paid plan if needed (Chromium needs ~512MB)

### If Playwright fails:

The error will be clear in logs. Usually means:
- Missing system deps → Fixed by `--with-deps` flag ✅
- Out of memory → Upgrade plan
- Timeout → Increase `DEFAULT_TIMEOUT` env var

### If timeouts occur:

Railway's free tier has request timeouts. For long-running scrapes:
1. Increase timeout in request: `"timeout": 90000`
2. Upgrade to Railway Pro for better limits
3. Or use background job processing

## 💰 Cost Estimate

- **Starter Plan**: $5/month - Perfect for this use case
- **Chromium**: ~200-300MB memory usage
- **Build time**: ~2-3 minutes (Playwright install)
- **Cold start**: ~5-10 seconds

## 🎯 Production Checklist

- [x] `railway.toml` configured
- [x] Health check endpoint (`/health`)
- [x] Environment variable support (`$PORT`)
- [x] Playwright with system deps (`--with-deps`)
- [x] Proper error handling
- [x] Timeout configuration
- [x] CORS enabled (for frontend integration)

## 🔐 Security Notes

1. **Rate limiting** - Consider adding rate limiting in production
2. **Authentication** - Add API keys if needed:

```python
from fastapi import Header, HTTPException

async def verify_token(x_api_key: str = Header()):
    if x_api_key != os.environ.get("API_KEY"):
        raise HTTPException(status_code=401)
```

3. **URL validation** - Already using Pydantic's `HttpUrl` ✅

## 📊 Monitoring

Railway provides:
- Request logs
- Error tracking
- Memory/CPU usage
- Automatic deploys on git push

## 🚀 Advanced: Custom Domain

In Railway dashboard:
1. Go to Settings → Networking
2. Add custom domain
3. Update DNS records as shown
4. Done!

## Example Production Usage

```javascript
// Frontend integration
const scrapeWebsite = async (url) => {
  const response = await fetch('https://your-app.up.railway.app/scrape', {
    method: 'POST',
    headers: { 
      'Content-Type': 'application/json',
      // 'X-API-Key': 'your-secret-key'  // if you add auth
    },
    body: JSON.stringify({ 
      url,
      save_assets: false,  // Set to false for faster response
      timeout: 60000 
    })
  });
  
  return await response.json();
};
```

## 🎉 You're Ready!

This configuration is **production-ready** and **Railway-optimized**. Just deploy and it will work!

**Questions?** Check Railway docs or the main README.md
