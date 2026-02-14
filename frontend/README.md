# Website Scraper Frontend

Beautiful web interface for the Website Scraper API.

## 🚀 Quick Start

### Option 1: Open Directly
Just open `index.html` in your browser!

```bash
open frontend/index.html
```

### Option 2: Serve with Python
```bash
cd frontend
python3 -m http.server 8080
# Visit http://localhost:8080
```

### Option 3: Serve with Node
```bash
cd frontend
npx serve
```

## 📝 Features

- ✨ Beautiful, modern UI
- 🎯 Pre-filled with test URL (The Picnic Basket)
- 📊 Overview with stats cards
- 📝 Content extraction results
- 🖼️ Image gallery
- 🎨 Color palette visualization
- 🔤 Font family detection
- 📄 Metadata display
- 💾 Raw JSON viewer with copy button
- 📱 Fully responsive

## 🎨 Customization

Edit `script.js` to change the API endpoint:

```javascript
const API_URL = 'https://your-api.railway.app/scrape';
```

## 🌐 Deploy Frontend

### Deploy to Netlify
1. Drag and drop the `frontend` folder to netlify.com
2. Done!

### Deploy to Vercel
```bash
cd frontend
vercel
```

### Deploy to GitHub Pages
1. Push `frontend` folder to GitHub
2. Enable GitHub Pages in repo settings
3. Select `main` branch and `/frontend` folder

## 📋 Files

- `index.html` - Main HTML structure
- `styles.css` - All styling
- `script.js` - API integration and UI logic
- `README.md` - This file
