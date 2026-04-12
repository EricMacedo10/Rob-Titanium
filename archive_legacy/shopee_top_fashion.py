import hashlib
import time
import json
import requests

# CREDENCIAIS E ENDPOINT VALIDADOS (Robô Titanium v2.2)
APP_ID = "18318830863"
APP_SECRET = "O4546A3D5KC664BG6SDHBOEMNTUMSXO7"
ENDPOINT = "https://open-api.affiliate.shopee.com.br/graphql"

def get_titanium_top_fashion():
    timestamp = int(time.time())
    
    # Query Profissional baseada na documentação V2
    # sortType 2 = ITEM_SOLD_DESC (Mais Vendidos)
    query = """
    query($keyword: String, $limit: Int, $sortType: Int) {
      productOfferV2(keyword: $keyword, limit: $limit, sortType: $sortType) {
        nodes {
          productName
          sales
          priceMin
          priceMax
          offerLink
          imageUrl
          commissionRate
        }
        pageInfo {
          hasNextPage
        }
      }
    }
    """
    
    variables = {
        "keyword": "moda feminina",
        "limit": 5,
        "sortType": 2
    }
    
    # JSON Compacto para Assinatura (Obrigatório)
    body = json.dumps({"query": query, "variables": variables}, separators=(',', ':'))
    
    # Assinatura SHA256 Direct (Validada no scan anterior)
    factor = f"{APP_ID}{timestamp}{body}{APP_SECRET}"
    signature = hashlib.sha256(factor.encode("utf-8")).hexdigest()
    
    headers = {
        "Authorization": f"SHA256 Credential={APP_ID},Timestamp={timestamp},Signature={signature}",
        "Content-Type": "application/json"
    }
    
    print(f"[Titanium] Consultando Inteligência Shopee...")
    
    try:
        response = requests.post(ENDPOINT, headers=headers, data=body, timeout=15)
        data = response.json()
        
        if "errors" in data:
            print("❌ Erro retornado:")
            print(json.dumps(data["errors"], indent=2))
            return

        products = data.get("data", {}).get("productOfferV2", {}).get("nodes", [])

        print("\nRELATORIO TITANIUM: TOP 5 MODA FEMININA (BEST SELLERS)\n")
        print("=" * 70)
        for i, p in enumerate(products, 1):
            name = p['productName'][:55]
            sales = p.get('sales', 0)
            commission = float(p.get('commissionRate', 0)) * 100
            
            # Formatação de preço (Shopee às vezes manda em centavos ou string)
            p_min = p.get('priceMin', '0')
            
            print(f"{i}. {name}...")
            print(f"   Vendas: {sales} unidades")
            print(f"   Preco: R$ {p_min}")
            print(f"   Comissao: {commission:.1f}%")
            print(f"   Link Seguro: {p['offerLink']}")
            print("-" * 70)
            
    except Exception as e:
        print(f"Erro na extracao: {e}")

if __name__ == "__main__":
    get_titanium_top_fashion()
