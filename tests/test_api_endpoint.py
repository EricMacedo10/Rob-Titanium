import requests
import json
import sys

def test_api():
    print("🚀 TESTING LOCAL API ENDPOINT...")
    url = "http://localhost:5000/api/search"
    params = {"q": "iphone 15"}
    
    try:
        print(f"📡 Sending GET request to {url}...")
        response = requests.get(url, params=params, timeout=30)
        
        print(f"📥 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ API RESPONSE RECEIVED!")
            print(f"   Query: {data.get('query')}")
            
            results = data.get('results', [])
            print(f"   Total Results: {len(results)}")
            
            for i, item in enumerate(results):
                print(f"\n   📦 ITEM #{i+1}")
                print(f"      Store: {item.get('store')} (Original: {item.get('loja')})")
                print(f"      Title: {item.get('title')}")
                print(f"      Price: {item.get('price')}")
                print(f"      Link:  {item.get('link')[:50]}...")
                
            if len(results) == 0:
                print("\n⚠️ WARNING: Results array is empty!")
        else:
            print(f"❌ API Error: {response.text}")
            
    except Exception as e:
        print(f"❌ CONNECTION ERROR: {e}")
        print("   Is the Flask server running? (python main.py)")

if __name__ == "__main__":
    test_api()
