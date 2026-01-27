"""
Shopee Affiliate API Integration
Implementa autenticação SHA256, geração de links e BUSCA de produtos via API Oficial
"""

import hashlib
import time
import requests
import json
import re
from typing import Optional, List, Dict
from scraper.settings import SHOPEE_APP_ID, SHOPEE_SECRET, SHOPEE_API_URL


class ShopeeAffiliateAPI:
    """
    Cliente para Shopee Open Platform GraphQL API
    """
    
    def __init__(self, app_id: str = None, secret: str = None):
        self.app_id = app_id or SHOPEE_APP_ID
        self.secret = secret or SHOPEE_SECRET
        self.api_url = "https://open-api.affiliate.shopee.com.br/graphql"
        
        if not self.app_id or not self.secret:
            raise ValueError("Shopee credentials not configured. Check .env file.")
    
    def generate_signature(self, timestamp: int, payload_str: str) -> str:
        """SHA256(Credential + Timestamp + Payload + Secret)"""
        base_string = f"{self.app_id}{timestamp}{payload_str}{self.secret}"
        return hashlib.sha256(base_string.encode('utf-8')).hexdigest()
    
    def _send_request(self, payload: dict) -> Optional[dict]:
        """Helper para enviar requisição autenticada"""
        timestamp = int(time.time())
        # JSON compactado para assinatura
        payload_str = json.dumps(payload, separators=(',', ':'))
        signature = self.generate_signature(timestamp, payload_str)
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"SHA256 Credential={self.app_id}, Signature={signature}, Timestamp={timestamp}"
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, data=payload_str, timeout=10)
            
            # Se a resposta não for JSON valido, lança erro
            try:
                data = response.json()
            except json.JSONDecodeError:
                print(f"❌ Shopee API returned invalid JSON: {response.text[:200]}")
                return None

            if "errors" in data:
                print(f"❌ Shopee GraphQL Error: {data['errors']}")
                return None
                
            return data
        except Exception as e:
            print(f"❌ Connection Error: {e}")
            return None

    def generate_short_link(self, url: str, sub_id: str = "") -> Optional[str]:
        """Gera short link de afiliado"""
        query = """
        mutation($input: ShortLinkInput!) {
            generateShortLink(input: $input) {
                shortLink
            }
        }
        """
        payload = {
            "query": query,
            "variables": {
                "input": {
                    "originUrl": url,
                    "subId": sub_id or f"gdd-{int(time.time())}"
                }
            }
        }
        
        data = self._send_request(payload)
        if data:
            return data.get("data", {}).get("generateShortLink", {}).get("shortLink")
        return None

    def search_products(self, keyword: str, limit: int = 10) -> List[Dict]:
        """
        Busca produtos via API productOfferV2
        Retorna lista formatada para o padrão do robô
        """
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
            }
        }
        """
        payload = {
            "query": query,
            "variables": {
                "keyword": keyword,
                "limit": limit
            }
        }
        
        data = self._send_request(payload)
        if not data:
            return []
            
        nodes = data.get("data", {}).get("productOfferV2", {}).get("nodes", [])
        products = []
        
        for node in nodes:
            try:
                # Normalização de dados
                price = float(node.get("price", 0))
                
                products.append({
                    "id_interno": 0,
                    "titulo": node.get("productName", "Produto Shopee"),
                    "preco": price,
                    "loja": "Shopee",
                    "link_afiliado": node.get("offerLink", ""), # Link JÁ VEM com afiliado!
                    "imagem": node.get("imageUrl", ""),
                    "disponivel": True
                })
            except Exception as e:
                print(f"⚠️ Error parsing node: {e}")
                continue
                
        return products

    def build_affiliate_url(self, search_term: str) -> str:
        """Constrói URL de busca (usado apenas se API falhar, não é o foco principal)"""
        base_url = "https://shopee.com.br/search"
        search_url = f"{base_url}?keyword={search_term.replace(' ', '+')}&sortBy=price"
        short_link = self.generate_short_link(search_url)
        return short_link if short_link else search_url


# --- Funções Públicas ---

def get_shopee_affiliate_link(search_term: str) -> str:
    try:
        api = ShopeeAffiliateAPI()
        return api.build_affiliate_url(search_term)
    except:
        return f"https://shopee.com.br/search?keyword={search_term.replace(' ', '+')}"

def search_shopee(query: str, limit: int = 3) -> list:
    """Função principal de busca (Substitui Selenium)"""
    print(f"[Shopee] Searching for '{query}' via API...")
    try:
        api = ShopeeAffiliateAPI()
        results = api.search_products(query, limit=limit)
        
        print(f"[Shopee] Found {len(results)} items via API")
        return results
        
    except Exception as e:
        print(f"[Shopee] API Search Failed: {e}")
        return []

if __name__ == "__main__":
    print("🧪 Testing Shopee API...")
    results = search_shopee("iPhone 15")
    for r in results:
        print(f"- {r['titulo']} | R$ {r['preco']:.2f} | {r['link_afiliado']}")
