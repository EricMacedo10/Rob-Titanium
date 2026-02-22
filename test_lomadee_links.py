import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

def test_product_link():
    headers = {"x-api-key": os.getenv("LOMADEE_APP_TOKEN")}
    params = {
        "search": "mouse gamer",
        "limit": 1,
        "sourceId": os.getenv("LOMADEE_SOURCE_ID")
    }
    url = "https://api-beta.lomadee.com.br/affiliate/products"
    
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2))
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_product_link()
