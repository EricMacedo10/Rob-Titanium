import os
import json
import time
import requests
import hashlib
from dotenv import load_dotenv

load_dotenv()

SHOPEE_APP_ID = os.getenv("SHOPEE_APP_ID")
SHOPEE_SECRET = os.getenv("SHOPEE_SECRET")

def get_shopee_image_api(keyword):
    """
    Busca a imagem de um produto na API oficial da Shopee via GraphQL.
    Retorna a URL da imagem do primeiro resultado encontrado.
    """
    if not SHOPEE_APP_ID or not SHOPEE_SECRET:
        print("[ShopeeAPI] Credenciais ausentes.")
        return None
        
    url = "https://open-api.affiliate.shopee.com.br/graphql"
    timestamp = int(time.time())
    
    # Query para buscar ofertas por palavra-chave
    query = """
    query productOfferV2($keyword: String, $limit: Int) {
      productOfferV2(keyword: $keyword, limit: $limit) {
        nodes {
          imageUrl
          productName
        }
      }
    }
    """
    
    variables = {"keyword": keyword, "limit": 1}
    payload = {"query": query, "variables": variables}
    payload_str = json.dumps(payload, separators=(',', ':'))
    
    # Gerar Assinatura (Signature) conforme requisitos da Shopee
    base_string = f"{SHOPEE_APP_ID}{timestamp}{payload_str}{SHOPEE_SECRET}"
    signature = hashlib.sha256(base_string.encode('utf-8')).hexdigest()
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"SHA256 Credential={SHOPEE_APP_ID}, Signature={signature}, Timestamp={timestamp}"
    }
    
    try:
        response = requests.post(url, headers=headers, data=payload_str, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        nodes = data.get("data", {}).get("productOfferV2", {}).get("nodes", [])
        if nodes:
            return nodes[0].get("imageUrl")
        return None
    except Exception as e:
        print(f"[ShopeeAPI] Erro na requisição: {e}")
        return None

def generate_affiliate_link(product_url):
    """
    Usa a API Oficial da Shopee para converter uma URL de produto em um 
    Universal Link (s.shopee.com.br) blindado com o ID de afiliado.
    """
    if not SHOPEE_APP_ID or not SHOPEE_SECRET:
        return product_url
        
    url = "https://open-api.affiliate.shopee.com.br/graphql"
    timestamp = int(time.time())
    
    # Mutação oficial para gerar links curtos (Universal Links)
    query = """
    mutation generateShortLink($originUrls: [String]!) {
      generateShortLink(originUrls: $originUrls) {
        shortLink
      }
    }
    """
    
    variables = {"originUrls": [product_url]}
    payload = {"query": query, "variables": variables}
    payload_str = json.dumps(payload, separators=(',', ':'))
    
    # Assinatura de Segurança
    base_string = f"{SHOPEE_APP_ID}{timestamp}{payload_str}{SHOPEE_SECRET}"
    signature = hashlib.sha256(base_string.encode('utf-8')).hexdigest()
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"SHA256 Credential={SHOPEE_APP_ID}, Signature={signature}, Timestamp={timestamp}"
    }
    
    try:
        response = requests.post(url, headers=headers, data=payload_str, timeout=10)
        data = response.json()
        
        # Extrai o link curto oficial
        results = data.get("data", {}).get("generateShortLink", [])
        if results and results[0].get("shortLink"):
            return results[0]["shortLink"]
            
        return product_url
    except Exception as e:
        print(f"[ShopeeAPI] Erro ao converter link: {e}")
        return product_url
