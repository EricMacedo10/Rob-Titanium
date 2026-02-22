import requests
import os
from dotenv import load_dotenv

load_dotenv()

def test_v3():
    token = os.getenv("LOMADEE_APP_TOKEN")
    source_id = os.getenv("LOMADEE_SOURCE_ID")
    # Publisher ID from index_staging meta is 2324685
    publisher_id = "2324685"
    
    url = f"https://api.lomadee.com/v3/{token}/offer/_search"
    params = {
        "sourceId": source_id,
        "publisherId": publisher_id,
        "keyword": "mouse",
        "size": 1
    }
    
    print(f"Testing V3 API: {url}")
    try:
        r = requests.get(url, params=params, timeout=10)
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            import json
            print(json.dumps(r.json(), indent=2))
        else:
            print(r.text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_v3()
