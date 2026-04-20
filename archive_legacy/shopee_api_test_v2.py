import hashlib
import time
import json
import requests

import os

# CREDENCIAIS OFICIAIS
APP_ID = os.getenv("SHOPEE_APP_ID", "YOUR_APP_ID")
APP_SECRET = os.getenv("SHOPEE_SECRET", "YOUR_APP_SECRET")
ENDPOINT = "https://open-api.affiliate.shopee.com.br/v2/api/graphql"

def get_top_selling_feminino():
    timestamp = int(time.time())
    
    # Query baseada na documentação fornecida: productOfferV2
    query = """
    query($keyword:String, $limit:Int, $sortType:Int) {
      productOfferV2(keyword:$keyword, limit:$limit, sortType:$sortType) {
        nodes {
          productName
          priceMin
          priceMax
          sales
          offerLink
          imageUrl
        }
      }
    }
    """
    
    variables = {
        "keyword": "moda feminina",
        "limit": 5,
        "sortType": 2 # ITEM_SOLD_DESC (Mais vendidos)
    }
    
    # JSON Compacto para Assinatura
    body = json.dumps({"query": query, "variables": variables}, separators=(',', ':'))
    
    # Gerando Assinatura SHA256 v2: AppID + Timestamp + Body + Secret
    factor = f"{APP_ID}{timestamp}{body}{APP_SECRET}"
    signature = hashlib.sha256(factor.encode("utf-8")).hexdigest()
    
    headers = {
        "Authorization": f"SHA256 Credential={APP_ID},Timestamp={timestamp},Signature={signature}",
        "Content-Type": "application/json"
    }
    
    print(f"[Titanium API] Consultando Shopee API v2 (AppID: {APP_ID})...")
    
    try:
        response = requests.post(ENDPOINT, headers=headers, data=body, timeout=15)
        
        try:
            result = response.json()
        except:
            print(f"FALHA NO JSON. Status HTTP: {response.status_code}")
            print("Resposta Bruta do Servidor:")
            print(response.text[:500]) # Primeiros 500 chars
            return

        if "errors" in result:
            print("ERRO na API Shopee:")
            print(json.dumps(result["errors"], indent=2))
            return
            
        products = result.get("data", {}).get("productOfferV2", {}).get("nodes", [])
        
        if not products:
            print("Nenhum produto encontrado com os filtros aplicados.")
            return

        print("\n--- TOP 5 MODA FEMININA (Mais Vendidos) ---\n")
        for i, p in enumerate(products, 1):
            print(f"{i}. {p['productName']}")
            print(f"   Vendas: {p.get('sales', 'N/A')}")
            print(f"   Preço: R$ {p.get('priceMin', '??')} a R$ {p.get('priceMax', '??')}")
            print(f"   Link: {p['offerLink']}")
            print("-" * 50)
            
    except Exception as e:
        print(f"Erro na conexao: {e}")

if __name__ == "__main__":
    get_top_selling_feminino()
