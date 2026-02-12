# 🧪 Test Your Railway Deployment

## Quick Tests

### 1. Get Your Railway URL

In Railway dashboard, find your URL (something like):
```
https://scrape-create-production.up.railway.app
```

### 2. Test Health Endpoint

```bash
curl https://YOUR-APP.up.railway.app/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-12T..."
}
```

### 3. Test Interactive Docs

Open in browser:
```
https://YOUR-APP.up.railway.app/docs
```

You should see Swagger UI where you can test the API directly!

### 4. Test Actual Scraping

```bash
curl -X POST https://YOUR-APP.up.railway.app/scrape \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "save_assets": false, "timeout": 60000}'
```

**Expected:** JSON response with scraped data (may take 10-30 seconds)

---

## 🐛 Common Issues & Solutions

### Issue: "Playwright not found" error
**Solution:** Check build logs - make sure `playwright install --with-deps chromium` ran successfully

### Issue: Timeout on scraping
**Solution:** Increase timeout in request:
```json
{"url": "https://example.com", "timeout": 90000}
```

### Issue: 500 Internal Server Error
**Solution:** Check Railway logs for specific Python error
- Railway Dashboard → Deployments → View Logs

### Issue: Memory errors
**Solution:** Upgrade to Railway Pro ($5/month) for more RAM

### Issue: Cold start is slow
**Solution:** First request after idle takes ~10 seconds (Playwright initializing). This is normal!

---

## ✅ If Everything Works

You should be able to:
- ✅ Hit `/health` and get `{"status": "healthy"}`
- ✅ Open `/docs` and see interactive API docs
- ✅ POST to `/scrape` and get scraped data back

---

## 📊 Check Railway Logs

In Railway dashboard:
1. Go to your project
2. Click "Deployments"
3. Click latest deployment
4. Click "View Logs"

Look for:
```
✓ Installing Python dependencies
✓ Installing Playwright browsers
✓ Starting server
✓ Application startup complete
```

---

## 🎯 Next Steps

Once confirmed working:
1. Save your Railway URL
2. Use it in your frontend/backend
3. Share with your team
4. Start scraping! 🚀

---

## ❓ Need Help?

Tell me:
1. What error are you seeing?
2. What's in the Railway logs?
3. What happens when you test the endpoints?
