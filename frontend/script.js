const API_URL = 'https://scrape-create-production.up.railway.app/scrape';

let currentData = null;

// DOM Elements
const urlInput = document.getElementById('url-input');
const saveAssetsCheckbox = document.getElementById('save-assets');
const convertWebpCheckbox = document.getElementById('convert-webp');
const scrapeBtn = document.getElementById('scrape-btn');
const loading = document.getElementById('loading');
const error = document.getElementById('error');
const results = document.getElementById('results');
const copyJsonBtn = document.getElementById('copy-json');

// Tab switching
document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
        const tabName = tab.dataset.tab;
        
        // Update active tab
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        
        // Update active content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(`${tabName}-tab`).classList.add('active');
    });
});

// Scrape button handler
scrapeBtn.addEventListener('click', async () => {
    const url = urlInput.value.trim();
    
    if (!url) {
        showError('Please enter a valid URL');
        return;
    }
    
    await scrapeWebsite(url);
});

// Allow Enter key to submit
urlInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        scrapeBtn.click();
    }
});

// Copy JSON button
copyJsonBtn.addEventListener('click', () => {
    const jsonText = document.getElementById('raw-json').textContent;
    navigator.clipboard.writeText(jsonText).then(() => {
        copyJsonBtn.textContent = '✓ Copied!';
        setTimeout(() => {
            copyJsonBtn.textContent = 'Copy JSON';
        }, 2000);
    });
});

async function scrapeWebsite(url) {
    // Show loading
    loading.querySelector('p').textContent = 'Scraping website... This may take 30-60 seconds';
    loading.classList.remove('hidden');
    error.classList.add('hidden');
    results.classList.add('hidden');
    scrapeBtn.disabled = true;
    
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                url: url,
                save_assets: saveAssetsCheckbox.checked,
                convert_to_webp: convertWebpCheckbox.checked,
                timeout: 60000
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        currentData = data;
        
        displayResults(data);
        
    } catch (err) {
        showError(`Failed to scrape website: ${err.message}`);
    } finally {
        loading.classList.add('hidden');
        scrapeBtn.disabled = false;
    }
}

function showError(message) {
    error.textContent = message;
    error.classList.remove('hidden');
    results.classList.add('hidden');
}

function displayResults(data) {
    const { content, assets, tokens, meta } = data.data;
    
    // Update stats
    document.getElementById('stat-headings').textContent = content.headings?.length || 0;
    document.getElementById('stat-paragraphs').textContent = content.paragraphs?.length || 0;
    document.getElementById('stat-images').textContent = assets.images?.length || 0;
    document.getElementById('stat-colors').textContent = 
        (tokens.colors?.primary?.length || 0) + (tokens.colors?.text?.length || 0);
    
    // Overview
    displayOverview(data);
    
    // Content
    displayContent(content);
    
    // Assets
    displayAssets(assets);
    
    // Tokens
    displayTokens(tokens);
    
    // Metadata
    displayMetadata(meta);
    
    // Raw JSON
    document.getElementById('raw-json').textContent = JSON.stringify(data, null, 2);
    
    // Show results
    results.classList.remove('hidden');
}

function displayOverview(data) {
    const { content, assets, tokens, meta } = data.data;
    
    const html = `
        <p><strong>URL:</strong> ${data.url}</p>
        <p><strong>Title:</strong> ${meta.title || 'N/A'}</p>
        <p><strong>Scraped at:</strong> ${new Date(data.timestamp).toLocaleString()}</p>
        <p><strong>Status:</strong> <span style="color: var(--success);">✓ ${data.status}</span></p>
        
        <div style="margin-top: 1.5rem;">
            <strong>Extracted Data:</strong>
            <ul style="margin-top: 0.5rem; padding-left: 1.5rem;">
                <li>${content.headings?.length || 0} headings</li>
                <li>${content.paragraphs?.length || 0} paragraphs</li>
                <li>${content.lists?.length || 0} lists</li>
                <li>${content.navigation?.length || 0} navigation items</li>
                <li>${assets.images?.length || 0} images</li>
                <li>${assets.svgs?.length || 0} SVGs</li>
                <li>${tokens.fonts?.families?.length || 0} font families</li>
                <li>${Object.keys(tokens.css_variables || {}).length} CSS variables</li>
            </ul>
        </div>
    `;
    
    document.getElementById('overview-content').innerHTML = html;
}

function displayContent(content) {
    let html = '';
    
    // Headings
    if (content.headings && content.headings.length > 0) {
        html += '<div class="section-title">📝 Headings</div>';
        content.headings.forEach(h => {
            html += `<div class="list-item"><strong>${h.tag.toUpperCase()}:</strong> ${escapeHtml(h.text)}</div>`;
        });
    }
    
    // Paragraphs
    if (content.paragraphs && content.paragraphs.length > 0) {
        html += '<div class="section-title">📄 Paragraphs</div>';
        content.paragraphs.slice(0, 10).forEach(p => {
            html += `<div class="list-item">${escapeHtml(p.substring(0, 200))}${p.length > 200 ? '...' : ''}</div>`;
        });
        if (content.paragraphs.length > 10) {
            html += `<p style="color: var(--text-light); margin-top: 0.5rem;">...and ${content.paragraphs.length - 10} more</p>`;
        }
    }
    
    // Navigation
    if (content.navigation && content.navigation.length > 0) {
        html += '<div class="section-title">🧭 Navigation</div>';
        content.navigation.forEach(nav => {
            html += `<div class="list-item">${escapeHtml(nav.text)} → ${nav.href || '#'}</div>`;
        });
    }
    
    document.getElementById('content-data').innerHTML = html || '<p>No content extracted</p>';
}

function displayAssets(assets) {
    let html = '';
    
    // Images
    if (assets.images && assets.images.length > 0) {
        html += '<div class="section-title">🖼️ Images</div>';
        html += '<div class="image-grid">';
        assets.images.slice(0, 12).forEach(img => {
            html += `
                <div class="image-card">
                    <img src="${img.url}" alt="${escapeHtml(img.alt || 'Image')}" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%22200%22 height=%22150%22%3E%3Crect fill=%22%23e2e8f0%22 width=%22200%22 height=%22150%22/%3E%3Ctext x=%2250%25%22 y=%2250%25%22 fill=%22%23718096%22 text-anchor=%22middle%22 dy=%22.3em%22%3EImage%3C/text%3E%3C/svg%3E'">
                    <div class="image-info">
                        <div class="image-alt">${escapeHtml(img.alt || 'No alt text')}</div>
                        <div class="image-url">${img.url.substring(0, 50)}...</div>
                    </div>
                </div>
            `;
        });
        html += '</div>';
        if (assets.images.length > 12) {
            html += `<p style="color: var(--text-light); margin-top: 1rem;">...and ${assets.images.length - 12} more images</p>`;
        }
    }
    
    // SVGs
    if (assets.svgs && assets.svgs.length > 0) {
        html += '<div class="section-title">✨ Inline SVGs</div>';
        html += `<p>${assets.svgs.length} inline SVG(s) found</p>`;
    }
    
    document.getElementById('assets-data').innerHTML = html || '<p>No assets extracted</p>';
}

function displayTokens(tokens) {
    let html = '';
    
    // Colors
    if (tokens.colors) {
        const allColors = [
            ...(tokens.colors.primary || []),
            ...(tokens.colors.text || []),
            ...(tokens.colors.background || [])
        ];
        
        if (allColors.length > 0) {
            html += '<div class="section-title">🎨 Color Palette</div>';
            html += '<div class="color-grid">';
            allColors.slice(0, 20).forEach(color => {
                html += `
                    <div class="color-swatch">
                        <div class="color-box" style="background-color: ${color};"></div>
                        <div class="color-value">${color}</div>
                    </div>
                `;
            });
            html += '</div>';
        }
    }
    
    // Fonts
    if (tokens.fonts && tokens.fonts.families && tokens.fonts.families.length > 0) {
        html += '<div class="section-title">🔤 Font Families</div>';
        tokens.fonts.families.forEach(font => {
            html += `<div class="list-item">${escapeHtml(font)}</div>`;
        });
    }
    
    // CSS Variables
    if (tokens.css_variables && Object.keys(tokens.css_variables).length > 0) {
        html += '<div class="section-title">⚙️ CSS Variables</div>';
        Object.entries(tokens.css_variables).slice(0, 20).forEach(([key, value]) => {
            html += `<div class="list-item"><code>${escapeHtml(key)}</code>: ${escapeHtml(value)}</div>`;
        });
    }
    
    document.getElementById('tokens-data').innerHTML = html || '<p>No design tokens extracted</p>';
}

function displayMetadata(meta) {
    let html = `
        <div class="section-title">📄 Basic Info</div>
        <div class="info-card">
            <p><strong>Title:</strong> ${escapeHtml(meta.title || 'N/A')}</p>
            <p><strong>Description:</strong> ${escapeHtml(meta.description || 'N/A')}</p>
            <p><strong>Language:</strong> ${meta.language || 'N/A'}</p>
            <p><strong>Canonical URL:</strong> ${meta.canonical || 'N/A'}</p>
        </div>
    `;
    
    // OpenGraph
    if (meta.opengraph && Object.keys(meta.opengraph).length > 0) {
        html += '<div class="section-title">🌐 OpenGraph Tags</div>';
        html += '<div class="info-card">';
        Object.entries(meta.opengraph).forEach(([key, value]) => {
            html += `<p><strong>${key}:</strong> ${escapeHtml(value)}</p>`;
        });
        html += '</div>';
    }
    
    // Twitter
    if (meta.twitter && Object.keys(meta.twitter).length > 0) {
        html += '<div class="section-title">🐦 Twitter Card</div>';
        html += '<div class="info-card">';
        Object.entries(meta.twitter).forEach(([key, value]) => {
            html += `<p><strong>${key}:</strong> ${escapeHtml(value)}</p>`;
        });
        html += '</div>';
    }
    
    document.getElementById('metadata-data').innerHTML = html;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Auto-run on page load with pre-filled URL
window.addEventListener('load', () => {
    // Optionally auto-scrape the pre-filled URL
    // scrapeBtn.click();
});
