"""
Lomadee API Scraper Engine (v3)
Implementa busca de ofertas via API Oficial da Lomadee (Lomadee V3)
"""

import requests
import logging
import os
import urllib.parse
import json
from typing import List, Dict
from core.settings import LOMADEE_APP_TOKEN, LOMADEE_SOURCE_ID

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def search_lomadee(query: str, limit: int = 10) -> List[Dict]:
    """
    Busca ofertas na Lomadee usando a NOVA API (v4/Beta 2025).
    Retorna lista formatada para o padrão do Robô Titanium.
    """
    if not LOMADEE_APP_TOKEN:
        logger.error("Lomadee APP TOKEN not configured. Check .env file.")
        return []

    # O sourceId agora é opcional na busca ou injetado via headers em algumas versões,
    # mas mantemos o LOMADEE_SOURCE_ID nas configurações caso precise gerar links manuais.

    # Novo Endpoint Oficial (Baseado nos docs de 2025)
    url = "https://api-beta.lomadee.com.br/affiliate/products"
    
    headers = {
        "x-api-key": LOMADEE_APP_TOKEN,
        "Accept": "application/json"
    }

    params = {
        "search": query,
        "limit": limit,
        "page": 1
    }

    print(f"[Lomadee] Buscando '{query}' via Nova API (Header Auth)...")

    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        
        if response.status_code != 200:
            logger.error(f"Lomadee API error: {response.status_code} - {response.text}")
            return []

        data = response.json()
        # A estrutura nova coloca os itens em "data"
        products_data = data.get("data", [])
        
        results = []
        for product in products_data:
            try:
                # Na nova API, o preço está em options[0].pricing[0].price
                options = product.get("options", [])
                if not options: continue
                
                main_option = options[0]
                pricing = main_option.get("pricing", [])
                if not pricing: continue
                
                price = pricing[0].get("price", 0)
                
                # Imagem: images[0].url
                images = product.get("images", [])
                image_url = images[0].get("url", "") if images else ""

                # Generate Affiliate Link (Deeplink)
                # Standard Lomadee structure: https://redir.lomadee.com/v2/deeplink?sourceId={sourceId}&url={encodedUrl}
                direct_url = product.get("url", "")
                encoded_url = urllib.parse.quote(direct_url)
                affiliate_url = f"https://redir.lomadee.com/v2/deeplink?sourceId={LOMADEE_SOURCE_ID}&url={encoded_url}"

                results.append({
                    "id_interno": product.get("id", product.get("_id", 0)),
                    "titulo": product.get("name", "Produto Lomadee"),
                    "preco": float(price),
                    "loja": "Lomadee", # Standardized for filtering
                    "link_afiliado": affiliate_url, 
                    "imagem": image_url,
                    "disponivel": product.get("available", True)
                })
            except Exception as e:
                logger.warning(f"Erro ao processar produto Lomadee: {e}")
                continue

        if results:
            print(f"[Lomadee] Encontrados {len(results)} itens via Nova API")
        else:
            print("[Lomadee] Nova API retornou 0 itens.")
            
        return results

    except Exception as e:
        logger.error(f"Lomadee API exception: {e}")
        return []

if __name__ == "__main__":
    print("🧪 Testando Lomadee NEW API Structure...")
    # Teste prático
    res = search_lomadee("mouse", limit=1)
    for p in res:
        print(f">> {p['titulo']} | R$ {p['preco']} | {p['loja']}")
