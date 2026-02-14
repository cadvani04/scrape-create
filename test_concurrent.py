"""
Test concurrent requests to the API
"""

import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

API_URL = "https://scrape-create-production.up.railway.app/scrape"

def scrape_sync(url, request_num):
    """Synchronous scraping request"""
    start = time.time()
    try:
        response = requests.post(
            API_URL,
            json={"url": url, "save_assets": False},
            timeout=120
        )
        elapsed = time.time() - start
        
        if response.status_code == 200:
            return {
                "request": request_num,
                "url": url,
                "status": "success",
                "time": elapsed,
                "data": response.json()
            }
        else:
            return {
                "request": request_num,
                "url": url,
                "status": "failed",
                "time": elapsed,
                "error": f"HTTP {response.status_code}"
            }
    except Exception as e:
        elapsed = time.time() - start
        return {
            "request": request_num,
            "url": url,
            "status": "error",
            "time": elapsed,
            "error": str(e)
        }

def test_concurrent_sync(num_requests=3):
    """Test concurrent requests using ThreadPoolExecutor"""
    
    print(f"\n🧪 Testing {num_requests} concurrent requests...")
    print("=" * 60)
    
    # Test URLs
    urls = [
        "https://example.com",
        "https://example.org",
        "https://example.net"
    ]
    
    start_time = time.time()
    
    # Submit concurrent requests
    with ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = []
        for i in range(num_requests):
            url = urls[i % len(urls)]
            future = executor.submit(scrape_sync, url, i+1)
            futures.append(future)
        
        # Collect results
        results = []
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            
            status_emoji = "✅" if result["status"] == "success" else "❌"
            print(f"{status_emoji} Request #{result['request']}: {result['status']} - {result['time']:.1f}s - {result['url']}")
    
    total_time = time.time() - start_time
    
    print("=" * 60)
    print(f"\n📊 Results:")
    print(f"   Total time: {total_time:.1f}s")
    print(f"   Average time per request: {total_time/num_requests:.1f}s")
    
    successful = sum(1 for r in results if r["status"] == "success")
    print(f"   Successful: {successful}/{num_requests}")
    
    if successful == num_requests:
        print(f"\n✅ All {num_requests} concurrent requests handled successfully!")
        print(f"   Your API can handle multiple requests at once! 🎉")
    else:
        print(f"\n⚠️  Only {successful}/{num_requests} requests succeeded.")
        print(f"   The API may need optimization for higher concurrency.")
    
    return results

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🔥 CONCURRENT REQUEST TEST")
    print("=" * 60)
    
    # Test 1: Light load (3 concurrent)
    print("\n📝 Test 1: Light load (3 concurrent requests)")
    test_concurrent_sync(3)
    
    # Test 2: Medium load (5 concurrent)
    print("\n\n📝 Test 2: Medium load (5 concurrent requests)")
    test_concurrent_sync(5)
    
    print("\n" + "=" * 60)
    print("✅ Concurrent testing complete!")
    print("=" * 60)
