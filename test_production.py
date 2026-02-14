"""
Test the production deployment on Railway
"""

import requests
import json
import sys
import time

def test_deployment(base_url):
    """Test all endpoints of the deployed API"""
    
    print(f"🧪 Testing deployment at: {base_url}")
    print("=" * 60)
    
    # Remove trailing slash
    base_url = base_url.rstrip('/')
    
    # Test 1: Root endpoint
    print("\n1️⃣  Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print("✅ Root endpoint working!")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
        return False
    
    # Test 2: Health check
    print("\n2️⃣  Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check passed!")
            print(f"   Status: {data.get('status')}")
            print(f"   Timestamp: {data.get('timestamp')}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test 3: API docs
    print("\n3️⃣  Testing API docs...")
    try:
        response = requests.get(f"{base_url}/docs", timeout=10)
        if response.status_code == 200:
            print("✅ API docs accessible!")
            print(f"   Visit: {base_url}/docs")
        else:
            print(f"❌ API docs failed: {response.status_code}")
    except Exception as e:
        print(f"⚠️  API docs error: {e}")
    
    # Test 4: Actual scraping (this will take longer)
    print("\n4️⃣  Testing scraper endpoint (this may take 30-60 seconds)...")
    print("   Scraping https://example.com...")
    
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{base_url}/scrape",
            json={
                "url": "https://example.com",
                "save_assets": False,  # Faster without downloading assets
                "convert_to_webp": False,
                "timeout": 60000
            },
            timeout=120  # 2 minute timeout
        )
        
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Scraping successful! (took {elapsed:.1f}s)")
            print(f"\n📊 Results:")
            print(f"   Status: {data.get('status')}")
            print(f"   URL: {data.get('url')}")
            
            # Extract key metrics
            content = data.get('data', {}).get('content', {})
            assets = data.get('data', {}).get('assets', {})
            tokens = data.get('data', {}).get('tokens', {})
            meta = data.get('data', {}).get('meta', {})
            
            print(f"\n   📝 Content extracted:")
            print(f"      - Headings: {len(content.get('headings', []))}")
            print(f"      - Paragraphs: {len(content.get('paragraphs', []))}")
            print(f"      - Lists: {len(content.get('lists', []))}")
            print(f"      - Navigation items: {len(content.get('navigation', []))}")
            
            print(f"\n   🎨 Assets extracted:")
            print(f"      - Images: {len(assets.get('images', []))}")
            print(f"      - SVGs: {len(assets.get('svgs', []))}")
            
            print(f"\n   🎭 Design tokens:")
            print(f"      - Primary colors: {len(tokens.get('colors', {}).get('primary', []))}")
            print(f"      - Font families: {len(tokens.get('fonts', {}).get('families', []))}")
            print(f"      - CSS variables: {len(tokens.get('css_variables', {}))}")
            
            print(f"\n   📄 Metadata:")
            print(f"      - Title: {meta.get('title')}")
            print(f"      - Description: {meta.get('description')[:50]}..." if meta.get('description') else "      - Description: None")
            
            # Save full response
            output_file = "production_test_result.json"
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"\n   💾 Full response saved to: {output_file}")
            
        else:
            print(f"❌ Scraping failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"❌ Scraping timeout after {time.time() - start_time:.1f}s")
        print("   Try increasing the timeout or check Railway logs")
        return False
    except Exception as e:
        print(f"❌ Scraping error: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 All tests passed! Your API is working perfectly!")
    print(f"\n📚 Interactive docs: {base_url}/docs")
    print(f"🔗 Share this URL with your team: {base_url}")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_production.py <RAILWAY_URL>")
        print("\nExample:")
        print("  python test_production.py https://scrape-create-production.up.railway.app")
        sys.exit(1)
    
    url = sys.argv[1]
    success = test_deployment(url)
    
    sys.exit(0 if success else 1)
