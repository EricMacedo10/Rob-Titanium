import os
import time
import json
import hashlib
import requests
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

APP_ID = os.getenv("SHOPEE_APP_ID")
SECRET = os.getenv("SHOPEE_SECRET")
API_URL = "https://open-api.affiliate.shopee.com.br/graphql"

def generate_signature(timestamp, payload):
    base_string = f"{APP_ID}{timestamp}{payload}{SECRET}"
    return hashlib.sha256(base_string.encode('utf-8')).hexdigest()

def test_product_search(keyword="iphone"):
    print(f"Testing Shopee API search for: {keyword}")
    print(f"App ID: {APP_ID}")
    
    timestamp = int(time.time())
    
    # Query baseada na documentação fornecida pelo usuário
    query = """
    query productOfferV2($keyword: String, $limit: Int) {
        productOfferV2(keyword: $keyword, limit: $limit) {
            nodes {
                productName
                price
                imageUrl
                offerLink
                commissionRate
                shopName
            }
            pageInfo {
                page
                hasNextPage
            }
        }
    }
    """
    
    variables = {
        "keyword": keyword,
        "limit": 5
    }
    
    payload = {
        "query": query,
        "variables": variables
    }
    
    # Payload string para assinatura (importante: separators)
    payload_str = json.dumps(payload, separators=(',', ':'))
    signature = generate_signature(timestamp, payload_str)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"SHA256 Credential={APP_ID}, Signature={signature}, Timestamp={timestamp}"
    }
    
    try:
        print("Sending request...")
        response = requests.post(API_URL, headers=headers, data=payload_str, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print("Response Body:")
        print(response.text)
        
        if response.status_code == 200:
            data = response.json()
            if "errors" in data:
                print("❌ GraphQL Errors:", data["errors"])
            else:
                nodes = data.get("data", {}).get("productOfferV2", {}).get("nodes", [])
                print(f"✅ Success! Found {len(nodes)} products.")
                for p in nodes:
                    print(f"- {p['productName']} ({p['price']}) -> {p['offerLink']}")
                    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_product_search()
