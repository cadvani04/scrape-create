"""
Quick test script for the scraper API
"""

import requests
import json

# Test the API
def test_scraper():
    url = "http://localhost:8000"
    
    # Health check
    print("🏥 Testing health endpoint...")
    response = requests.get(f"{url}/health")
    print(f"✅ Health: {response.json()}")
    print()
    
    # Test scraping
    print("🔍 Testing scraper endpoint...")
    print("📝 Scraping https://example.com...")
    
    response = requests.post(
        f"{url}/scrape",
        json={
            "url": "https://example.com",
            "save_assets": True,
            "convert_to_webp": True,
            "timeout": 30000
        },
        timeout=60
    )
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Scraping successful!")
        print(f"📊 Status: {data['status']}")
        print(f"🌐 URL: {data['url']}")
        print(f"⏰ Timestamp: {data['timestamp']}")
        print()
        print("📄 Extracted data:")
        print(f"  - Headings: {len(data['data']['content']['headings'])}")
        print(f"  - Paragraphs: {len(data['data']['content']['paragraphs'])}")
        print(f"  - Images: {data['data']['assets'].get('total_images', 0)}")
        print(f"  - SVGs: {data['data']['assets'].get('total_svgs', 0)}")
        print(f"  - Colors: {len(data['data']['tokens']['colors']['primary'])}")
        print(f"  - Fonts: {len(data['data']['tokens']['fonts']['families'])}")
        print(f"  - Title: {data['data']['meta']['title']}")
        print()
        print("💾 Full response saved to test_output.json")
        
        with open("test_output.json", "w") as f:
            json.dump(data, f, indent=2)
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    try:
        test_scraper()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API. Make sure the server is running:")
        print("   python main.py")
    except Exception as e:
        print(f"❌ Error: {e}")
