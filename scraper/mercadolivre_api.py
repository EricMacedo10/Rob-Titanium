"""
Mercado Livre Scraper (Selenium Version)
Substitui a API pública depreciada (403 Forbidden).
"""
import logging
import time
import requests
from typing import Dict, List
from bs4 import BeautifulSoup
from urllib.parse import urlencode

from scraper.browser import get_driver
from scraper import meli_token_manager 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def search_via_api(query: str, token: str = None, limit: int = 3) -> List[Dict]:
    """Busca produtos usando a API Oficial do Mercado Livre"""
    """Busca produtos usando a API Oficial do Mercado Livre"""
    """Busca produtos usando a API Oficial do Mercado Livre"""
    try:
        url = "https://api.mercadolibre.com/sites/MLB/search"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": "https://www.mercadolivre.com.br/",
            "Origin": "https://www.mercadolivre.com.br",
            "Sec-Ch-Ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site"
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"
            
        params = {
            "q": query,
            "sort": "price_asc",
            "limit": limit,
            "status": "active"
        }
        
        # Primeira tentativa (com token, se fornecido)
        response = requests.get(url, headers=headers, params=params)
        
        # Se der Forbidden/Unauthorized e tínhamos token, tenta sem token (Anônimo)
        if token and response.status_code in [401, 403]:
            logger.warning(f"[ML API] Token recusado ({response.status_code}). Tentando anonimamente...")
            headers.pop("Authorization", None)
            response = requests.get(url, headers=headers, params=params)
            
        if response.status_code != 200:
            logger.error(f"[ML API] Erro: {response.text}")
            return []
            
        data = response.json()
        items = []
        
        for result in data.get("results", []):
            try:
                # Affiliate Link
                permalink = result.get("permalink")
                try:
                    params_aff = {
                        'matt_tool': '188269638',
                        'matt_word': query,
                        'matt_source': 'guiadodesconto',
                        'tracking_id': f"gdd-{int(time.time())}", 
                        '_Sort': 'price_asc'
                    }
                    separator = "&" if "?" in permalink else "?"
                    affiliate_link = f"{permalink}{separator}{urlencode(params_aff)}"
                except:
                    affiliate_link = permalink
                
                # Image High Res
                image = result.get("thumbnail", "").replace("-I.jpg", "-O.jpg")
                
                items.append({
                    "id_interno": 2,
                    "id_original": result.get("id"),
                    "titulo": result.get("title"),
                    "preco": float(result.get("price")),
                    "loja": "Mercado Livre",
                    "link_afiliado": affiliate_link,
                    "imagem": image,
                    "disponivel": True
                })
            except Exception as e:
                continue
                
        logger.info(f"[ML API] Found {len(items)} products")
        return items
    except Exception as e:
        logger.error(f"[ML API] Failed: {e}")
        return []

def search_mercadolivre(query: str, limit: int = 3) -> List[Dict]:
    # 1. Tenta via API Oficial (Se tiver token)
    try:
        token = meli_token_manager.get_valid_token()
        if token:
            logger.info(f"[ML] Usando API Oficial para: {query}")
            results = search_via_api(query, token, limit)
            if results: 
                return results
            else:
                logger.warning("[ML] API retornou 0, tentando Selenium...")
    except Exception as e:
        logger.warning(f"[ML] API falhou ({e}), tentando Selenium...")

    # 2. Fallback Selenium
    driver = None
    try:
        logger.info(f"[ML] Starting Selenium Search for: {query}")
        driver = get_driver(headless=True)
        
        # Ordenar por menor preço: _OrderId_PRICE
        url = f"https://lista.mercadolivre.com.br/{query.replace(' ', '-')}_OrderId_PRICE"
        driver.get(url)
        
        # Wait for content
        time.sleep(5)
        
        # Anti-Bot Check: If redirected to Home, try searching via Input
        current_url = driver.current_url
        logger.info(f"[ML] Current URL: {current_url}")
        
        if "mercadolivre.com.br/" in current_url and "lista." not in current_url and "search" not in current_url:
            logger.warning("[ML] Redirected to Home/Generic Page. Attempting Search Bar Fallback...")
            try:
                from selenium.webdriver.common.by import By
                from selenium.webdriver.common.keys import Keys
                
                search_input = driver.find_element(By.CSS_SELECTOR, "input.nav-search-input")
                search_input.clear()
                search_input.send_keys(query)
                search_input.send_keys(Keys.RETURN)
                
                time.sleep(5)
                logger.info(f"[ML] Fallback URL: {driver.current_url}")
            except Exception as e:
                logger.error(f"[ML] Fallback Search Failed: {e}")
                
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        
        # Debug: Check if we are blocked
        page_title = soup.title.string if soup.title else "No Title"
        logger.info(f"[ML] Page Title: {page_title}")
        
        products = []
        
        # Try finding cards (support multiple layouts)
        cards = soup.select('.poly-card') # New 2024 layout
        if not cards:
             cards = soup.select('li.ui-search-layout__item') # Classic List 
        if not cards:
             cards = soup.select('div.ui-search-result__wrapper') # Grid
             
        logger.info(f"[ML] Cards found: {len(cards)}")
             
        for item in cards:
            if len(products) >= limit: break
            
            try:
                # 1. Title & Link
                # Poly layout: a.poly-component__title
                title_el = item.select_one('.poly-component__title') or \
                           item.select_one('.ui-search-item__group__element.ui-search-link') or \
                           item.select_one('a.ui-search-link')
                           
                if not title_el: continue
                
                title = title_el.get_text(strip=True)
                permalink = title_el.get('href', '')
                
                # 2. Price
                price_el = item.select_one('.poly-price__current .andes-money-amount__fraction') or \
                           item.select_one('.ui-search-price__part .andes-money-amount__fraction')
                           
                if not price_el: 
                    # Try finding any price
                    price_el = item.select_one('.andes-money-amount__fraction')
                    
                if not price_el: continue
                
                price_str = price_el.get_text(strip=True).replace('.', '')
                price = float(price_str)
                
                # 3. Image
                img_el = item.select_one('.poly-component__picture') or \
                         item.select_one('.ui-search-result__image img') or \
                         item.select_one('img')
                
                image = ""
                if img_el:
                     image = img_el.get('data-src') or img_el.get('src') or ''
                
                # 4. Affiliate Link Generation
                try:
                    params = {
                        'matt_tool': '188269638',
                        'matt_word': query,
                        'matt_source': 'guiadodesconto',
                        'tracking_id': f"gdd-{int(time.time())}", 
                        '_Sort': 'price_asc'
                    }
                    separator = "&" if "?" in permalink else "?"
                    affiliate_link = f"{permalink}{separator}{urlencode(params)}"
                except:
                    affiliate_link = permalink

                products.append({
                    "id_interno": 2,
                    "id_original": f"ml_{int(time.time()*1000)}", 
                    "titulo": title,
                    "preco": price,
                    "loja": "Mercado Livre",
                    "link_afiliado": affiliate_link,
                    "imagem": image,
                    "disponivel": True
                })
                
            except Exception as e:
                logger.warning(f"[ML] Error parsing item: {e}")
                continue
                
        logger.info(f"[ML] Found {len(products)} products")
        return products
        
    except Exception as e:
        logger.error(f"[ML] Fatal error: {e}")
        return []
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    items = search_mercadolivre("iPhone 15")
    for i in items: print(f"{i['titulo']} - R$ {i['preco']}")
