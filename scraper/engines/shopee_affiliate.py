"""
Shopee Affiliate API Integration
Implementa autenticação SHA256, geração de links, BUSCA de produtos
e RELATÓRIO DE CONVERSÕES (vendas) via API Oficial.
"""

import hashlib
import time
import requests
import json
import re
from datetime import datetime, timedelta, timezone
from typing import Optional, List, Dict
from core.settings import SHOPEE_APP_ID, SHOPEE_SECRET, SHOPEE_API_URL


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

    def get_conversion_report(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 100
    ) -> List[Dict]:
        """
        Relatório de Conversões em Tempo Real (Real-Time Report).
        Usa os argumentos e campos REAIS confirmados via GraphQL introspection.
        Args corretos: purchaseTimeStart / purchaseTimeEnd (Unix Int64)
        Se start_time não for informado, busca as últimas 24 horas.
        """
        if end_time is None:
            end_time = datetime.now(timezone.utc)
        if start_time is None:
            start_time = end_time - timedelta(hours=24)

        start_ts = int(start_time.timestamp())
        end_ts   = int(end_time.timestamp())

        query = """
        query(
            $purchaseTimeStart: Int64,
            $purchaseTimeEnd: Int64,
            $limit: Int
        ) {
            conversionReport(
                purchaseTimeStart: $purchaseTimeStart,
                purchaseTimeEnd: $purchaseTimeEnd,
                limit: $limit
            ) {
                nodes {
                    conversionId
                    conversionStatus
                    purchaseTime
                    clickTime
                    estimatedTotalCommission
                    netCommission
                    totalCommission
                    cappedCommission
                    utmContent
                    productType
                }
                pageInfo {
                    hasNextPage
                    scrollId
                }
            }
        }
        """
        payload = {
            "query": query,
            "variables": {
                "purchaseTimeStart": start_ts,
                "purchaseTimeEnd":   end_ts,
                "limit":             limit
            }
        }

        data = self._send_request(payload)
        if not data:
            return []

        nodes = (
            data.get("data", {})
                .get("conversionReport", {})
                .get("nodes", [])
        )
        conversions = []
        for node in nodes:
            try:
                # purchaseTime vem como Unix timestamp (Int64)
                purchase_ts = node.get("purchaseTime", 0)
                purchase_dt = (
                    datetime.fromtimestamp(purchase_ts, tz=timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
                    if purchase_ts else "N/A"
                )
                conversions.append({
                    "conversion_id":           str(node.get("conversionId", "")),
                    "conversion_status":       node.get("conversionStatus", "pending"),
                    "purchase_time":           purchase_dt,
                    "estimated_commission":    node.get("estimatedTotalCommission", "0"),
                    "net_commission":          node.get("netCommission", "0"),
                    "total_commission":        node.get("totalCommission", "0"),
                    "capped_commission":       node.get("cappedCommission", "0"),
                    "utm_content":             node.get("utmContent", ""),
                    "product_type":            node.get("productType", ""),
                })
            except Exception as e:
                print(f"⚠️ Error parsing conversion node: {e}")
                continue

        return conversions

    def get_validated_report(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 100
    ) -> List[Dict]:
        """
        Relatório Validado — ATENÇÃO: a API exige `validationId: Int64!` obrigatório.
        Este ID representa um período de validação específico gerado pela Shopee.
        Por enquanto retorna lista vazia com aviso. Implementação futura:
        descobrir endpoint de listagem de validationIds disponíveis.
        """
        print("⚠️ [ValidatedReport] Requer validationId (Int64!) — desabilitado temporariamente.")
        print("   → Use o conversionReport para monitoramento em tempo real.")
        return []


# --- Funções Públicas ---

def get_shopee_affiliate_link(search_term: str) -> str:
    try:
        api = ShopeeAffiliateAPI()
        return api.build_affiliate_url(search_term)
    except:
        return f"https://shopee.com.br/search?keyword={search_term.replace(' ', '+')}"

def search_shopee(query: str, limit: int = 3) -> list:
    """Função principal de busca (Via API Oficial)"""
    print(f"[Shopee] Searching for '{query}' via API...")
    try:
        api = ShopeeAffiliateAPI()
        # API Oficial APROVADA - Validado em 29/01/2026
        results = api.search_products(query, limit=limit)
        
        if results:
            print(f"[Shopee] Found {len(results)} items via API")
            return results
        else:
            print("[Shopee] API returned 0 items.")
            return []
        
    except Exception as e:
        print(f"[Shopee] API Search Failed: {e}")
        return []

if __name__ == "__main__":
    print("🧪 Testing Shopee API...")
    results = search_shopee("iPhone 15")
    for r in results:
        print(f"- {r['titulo']} | R$ {r['preco']:.2f} | Img: {r['imagem']} | Link: {r['link_afiliado']}")
