"""
Shopee Affiliate API Integration
Implementa autenticação SHA256 e geração de short links para afiliados Shopee
"""

import hashlib
import time
import requests
import json
from typing import Optional, Dict
from scraper.settings import SHOPEE_APP_ID, SHOPEE_SECRET, SHOPEE_API_URL


class ShopeeAffiliateAPI:
    """
    Cliente para Shopee Open Platform GraphQL API
    Implementa autenticação SHA256 para geração de links de afiliado
    """
    
    def __init__(self, app_id: str = None, secret: str = None):
        """
        Inicializa o cliente Shopee API
        
        Args:
            app_id: Shopee App ID (usa settings se não fornecido)
            secret: Shopee Secret (usa settings se não fornecido)
        """
        self.app_id = app_id or SHOPEE_APP_ID
        self.secret = secret or SHOPEE_SECRET
        # Endpoint validado via debug
        self.api_url = "https://open-api.affiliate.shopee.com.br/graphql"
        
        if not self.app_id or not self.secret:
            raise ValueError("Shopee credentials not configured. Check .env file.")
    
    def generate_signature(self, timestamp: int, payload_str: str) -> str:
        """
        Gera assinatura SHA256 para autenticação (Não-HMAC)
        
        Algorithm: SHA256(Credential + Timestamp + Payload + Secret)
        """
        # Formato exato da documentação
        base_string = f"{self.app_id}{timestamp}{payload_str}{self.secret}"
        
        # SHA256 simples (Hash do conteúdo concatenado)
        signature = hashlib.sha256(base_string.encode('utf-8')).hexdigest()
        
        return signature
    
    def generate_short_link(self, url: str, sub_id: str = "") -> Optional[str]:
        """
        Gera short link de afiliado via Shopee API
        Uses validated Schema B: ShortLinkInput!
        """
        timestamp = int(time.time())
        
        # Correção Validada: O tipo correto do argumento é ShortLinkInput!
        query = """
        mutation($input: ShortLinkInput!) {
            generateShortLink(input: $input) {
                shortLink
            }
        }
        """
        
        variables = {
            "input": {
                "originUrl": url,
                "subId": sub_id or f"gdd-{timestamp}"
            }
        }
        
        payload = {
            "query": query,
            "variables": variables
        }
        
        # IMPORTANTE: JSON minificado para assinatura (separators sem espaço)
        payload_str = json.dumps(payload, separators=(',', ':'))
        
        signature = self.generate_signature(timestamp, payload_str)
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"SHA256 Credential={self.app_id}, Signature={signature}, Timestamp={timestamp}"
        }
        
        try:
            # Envia 'data=payload_str' para garantir que o corpo seja idêntico ao usado na assinatura
            response = requests.post(
                self.api_url,
                headers=headers,
                data=payload_str,
                timeout=10
            )
            
            # Não levantar exceção em 4xx/5xx ainda para ler o corpo de erro
            # response.raise_for_status() 
            
            data = response.json()
            
            # Verificar erros de negócio no nível raiz
            if "errors" in data:
                print(f"❌ Shopee GraphQL Error: {data['errors']}")
                return None
            
            # Extrair resultado
            result = data.get("data", {}).get("generateShortLink", {})
            
            if not result:
                print(f"⚠️ Empty response structure: {data}")
                return None
                
            if result.get("error"):
                error = result["error"]
                print(f"❌ Shopee API Logic Error: {error.get('code')} - {error.get('message')}")
                return None
            
            short_link = result.get("shortLink")
            
            if short_link:
                print(f"✅ Shopee short link generated: {short_link}")
                return short_link
            else:
                print("⚠️ No short link returned in successful response")
                return None
                
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON response: {response.text}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Request Error: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")
            return None
    
    def build_affiliate_url(self, search_term: str) -> str:
        """
        Constrói URL de busca Shopee e gera short link de afiliado
        
        Args:
            search_term: Termo de busca
            
        Returns:
            Short link de afiliado ou URL de busca padrão
        """
        # URL de busca Shopee com ordenação por menor preço
        base_url = "https://shopee.com.br/search"
        search_url = f"{base_url}?keyword={search_term.replace(' ', '+')}&sortBy=price"
        
        # Tentar gerar short link
        short_link = self.generate_short_link(search_url)
        
        # Retornar short link ou URL padrão
        return short_link if short_link else search_url


# Função helper para uso rápido
def get_shopee_affiliate_link(search_term: str) -> str:
    """
    Função helper para gerar link de afiliado Shopee
    
    Args:
        search_term: Termo de busca
        
    Returns:
        Link de afiliado Shopee
    """
    try:
        api = ShopeeAffiliateAPI()
        return api.build_affiliate_url(search_term)
    except Exception as e:
        print(f"⚠️ Fallback to direct URL: {e}")
        # Fallback: URL direta sem afiliado
        return f"https://shopee.com.br/search?keyword={search_term.replace(' ', '+')}"


if __name__ == "__main__":
    # Teste rápido
    print("🧪 Testando Shopee Affiliate API (Production Code)...")
    
    if SHOPEE_APP_ID and SHOPEE_SECRET:
        api = ShopeeAffiliateAPI()
        
        # Teste: Gerar short link para 'decoração'
        term = "decoração casa"
        print(f"\n🔗 Generating link for '{term}'...")
        
        link = api.build_affiliate_url(term)
        print(f"👉 Concluded Link: {link}")
    else:
        print("❌ Credentials not configured/loaded.")
