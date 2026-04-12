import hmac
import hashlib
import time
import json
import requests

# CREDENCIAIS DO PRINT (Revisado: O -> 0 e X -> X)
APP_ID = "18318830863"
APP_SECRET = "04546A3D5KC664BG6SDHB0EMNTUMSX07"
ENDPOINT = "https://open-api.affiliate.shopee.com.br/v2/api/graphql"

def get_shopee_products(keyword="moda feminina", limit=5):
    timestamp = int(time.time())
    
    # Query GraphQL v2
    query = """query($keyword:String,$limit:Int){productOfferV2List(page:1,limit:$limit,keyword:$keyword,sortType:"sales_volume",sortOrder:"desc"){nodes{itemId,productName,imageUrl,price,salesVolume,offerLink}}}"""
    
    variables = {
        "keyword": keyword,
        "limit": limit
    }
    
    # IMPORTANTE: JSON Compacto para Assinatura (Sem espaços: separators=(',',':'))
    body = json.dumps({"query": query, "variables": variables}, separators=(',', ':'))
    
    # V2 BASE STRING (GraphQL Direct): AppID + Timestamp + Payload + Secret
    factor = f"{APP_ID}{timestamp}{body}{APP_SECRET}"
    
    # IMPORTANTE: Shopee GraphQL v2 usa SHA256 Simples, NAO HMAC
    signature = hashlib.sha256(factor.encode("utf-8")).hexdigest()
    
    # Headers Oficiais V2 (Formato Credential=, Timestamp=, Signature=)
    headers = {
        "Authorization": f"SHA256 Credential={APP_ID},Timestamp={timestamp},Signature={signature}",
        "Content-Type": "application/json"
    }
    
    print(f"[Titanium API] Tentando conexao V2 com AppID: {APP_ID}...")
    
    try:
        response = requests.post(ENDPOINT, headers=headers, data=body, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            if "errors" in result:
                print("ERRO retornado pela API da Shopee:")
                print(json.dumps(result["errors"], indent=2))
                return None
            
            return result.get("data", {}).get("productOfferV2List", {}).get("nodes", [])
        else:
            print(f"FALHA na conexao HTTP: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"ERRO de execucao: {e}")
        return None

if __name__ == "__main__":
    products = get_shopee_products()
    
    if products:
        print("\nCONEXAO ESTABELECIDA! Top 5 Moda Feminina (U7D):\n")
        print("-" * 60)
        for i, p in enumerate(products, 1):
            price_reais = float(p['price']) / 100000 if isinstance(p['price'], (int, float, str)) and float(p['price']) > 1000 else p['price']
            print(f"{i}. {p['productName'][:50]}...")
            print(f"   Vendas: {p['salesVolume']} | Preço: R$ {price_reais}")
            print(f"   Link Afiliado: {p['offerLink']}")
            print("-" * 60)
    else:
        print("\n⚠️ O teste falhou. Verifique se o AppID/Secret estão ativos ou se há restrição de IP.")
