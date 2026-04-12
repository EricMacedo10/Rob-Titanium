import hashlib
import time
import json
import requests

APP_ID = "18318830863"
APP_SECRET = "O4546A3D5KC664BG6SDHBOEMNTUMSXO7"

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
