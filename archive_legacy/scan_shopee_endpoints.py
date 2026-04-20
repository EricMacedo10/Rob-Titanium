import hashlib
import time
import json
import requests

import os

APP_ID = os.getenv("SHOPEE_APP_ID", "YOUR_APP_ID")
APP_SECRET = os.getenv("SHOPEE_SECRET", "YOUR_APP_SECRET")

# Variações de Endpoints comuns da Shopee Affiliate API
endpoints = [
    "https://open-api.affiliate.shopee.com.br/v2/api/graphql",
    "https://open-api.affiliate.shopee.com.br/graphql",
    "https://open-api.affiliate.shopee.com.br/api/v1/graphql",
    "https://open-api.affiliate.shopee.com/v2/api/graphql" # Global
]

def test_endpoint(url):
    timestamp = int(time.time())
    query = "{ productOfferV2(keyword:\"teste\", limit:1) { nodes { productName } } }"
    body = json.dumps({"query": query, "variables": {}}, separators=(',', ':'))
    
    factor = f"{APP_ID}{timestamp}{body}{APP_SECRET}"
    signature = hashlib.sha256(factor.encode("utf-8")).hexdigest()
    
    headers = {
        "Authorization": f"SHA256 Credential={APP_ID},Timestamp={timestamp},Signature={signature}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers, data=body, timeout=5)
        return response.status_code, response.text[:100]
    except Exception as e:
        return 0, str(e)

if __name__ == "__main__":
    print("Iniciando Varredura de Endpoints Shopee...")
    for url in endpoints:
        status, text = test_endpoint(url)
        print(f"URL: {url}")
        print(f"STATUS: {status} | RESPOSTA: {text.strip()}")
        print("-" * 30)
