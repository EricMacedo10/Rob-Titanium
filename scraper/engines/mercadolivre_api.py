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

from core.browser import get_driver
# meli_token_manager was moved to core.tokens
from core import tokens as meli_token_manager 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def search_via_api(query: str, token: str = None, limit: int = 3) -> List[Dict]:
    """
    Busca produtos usando Requests + Headers (Simulação de Browser).
    Bypass no bloqueio da API Oficial e mais leve que Selenium.
    """
    try:
        # URL de Busca (HTML)
        url = f"https://lista.mercadolivre.com.br/{query.replace(' ', '-')}_OrderId_PRICE_ASC"
        
        # Headers "Mágicos" validados em testes (Bypass WAF)
        # Headers Validated for 2026
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "pt-BR,pt;q=0.9",
            "Referer": "https://www.mercadolivre.com.br/",
        }
        
        session = requests.Session()
        session.headers.update(headers)
        
        logger.info(f"[ML Optimized] Fetching: {url}")
        response = session.get(url, timeout=15)
        
        if response.status_code != 200:
            logger.error(f"[ML Optimized] Failed: {response.status_code}")
            return []
            
        # Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")
        items = []
        
        # Seletores compatíveis com layouts 2024/2025
        cards = soup.select('.poly-card') or \
                soup.select('.ui-search-result__wrapper') or \
                soup.select('.ui-search-layout__item') or \
                soup.select('div[class*="ui-search-result"]')
                
        logger.info(f"[ML Optimized] Cards found: {len(cards)}")
        
        for item in cards:
            if len(items) >= limit: break
            try:
                # 1. Title & Link
                title_el = item.select_one('.poly-component__title') or \
                           item.select_one('.ui-search-item__group__element.ui-search-link') or \
                           item.select_one('a.ui-search-link')
                           
                if not title_el: continue
                title = title_el.get_text(strip=True)
                permalink = title_el.get('href', '')
                
                # 2. Price
                price_el = item.select_one('.poly-price__current .andes-money-amount__fraction') or \
                           item.select_one('.ui-search-price__part .andes-money-amount__fraction') or \
                           item.select_one('.andes-money-amount__fraction')
                           
                if not price_el: continue
                price = float(price_el.get_text(strip=True).replace('.', ''))
                
                # 3. Image
                img_el = item.select_one('.poly-component__picture') or \
                         item.select_one('.ui-search-result__image img') or \
                         item.select_one('img')
                image = img_el.get('data-src') or img_el.get('src') or ''
                
                # 4. Construir Link Afiliado Manualmente (Não precisamos depender da API para isso)
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

                items.append({
                    "id_interno": 2,
                    "id_original": f"ml_{int(time.time()*1000)}_{len(items)}",
                    "titulo": title,
                    "preco": price,
                    "loja": "Mercado Livre",
                    "link_afiliado": affiliate_link,
                    "imagem": image,
                    "disponivel": True
                })
            except Exception as e:
                continue
                
        return items
        
    except Exception as e:
        logger.error(f"[ML Optimized] Error: {e}")
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
        logger.info(f"[ML] Starting Selenium Nuclear Search for: {query}")
        driver = get_driver(headless=True)
        
        # 1. Start from Home to get cookies and bypass direct list page block
        driver.get("https://www.mercadolivre.com.br/")
        time.sleep(4)
        
        try:
            from selenium.webdriver.common.by import By
            from selenium.webdriver.common.keys import Keys
            
            # Find search bar
            search_input = driver.find_element(By.CSS_SELECTOR, "input.nav-search-input")
            search_input.clear()
            search_input.send_keys(query)
            # Add a small organic delay
            time.sleep(1)
            search_input.send_keys(Keys.RETURN)
            
            # Wait for results
            time.sleep(6)
            
            # Sort by price if possible
            try:
                # Try clicking sort dropdown - this is layout dependent
                # For now, let's just stick with the search results as they are
                pass
            except:
                pass
                
        except Exception as e:
            logger.error(f"[ML] Home Search Bar Failed: {e}")
            # Fallback to direct URL if home search fails
            url = f"https://lista.mercadolivre.com.br/{query.replace(' ', '-')}_OrderId_PRICE_ASC"
            driver.get(url)
            time.sleep(7)
                
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        
        # Debug: Check if we are blocked
        page_title = soup.title.string if soup.title else "No Title"
        logger.info(f"[ML] Page Title: {page_title} | URL: {driver.current_url}")
        
        products = []
        
        # Try finding cards with VERY generic selectors
        cards = soup.select('.poly-card') or \
                soup.select('.ui-search-result__wrapper') or \
                soup.select('.ui-search-layout__item') or \
                soup.select('.ui-search-result') or \
                soup.select('div[class*="ui-search-result"]')
             
        logger.info(f"[ML] Cards found: {len(cards)}")
             
        for item in cards:
            if len(products) >= limit: break
            
            try:
                # 1. Title & Link
                title_el = item.select_one('.poly-component__title') or \
                           item.select_one('.ui-search-item__group__element.ui-search-link') or \
                           item.select_one('.ui-search-link') or \
                           item.select_one('a[href*="click"]') or \
                           item.select_one('a[href*="p/MLB"]')
                           
                if not title_el: continue
                
                title = title_el.get_text(strip=True)
                permalink = title_el.get('href', '')
                if not permalink or "mercadolivre" not in permalink:
                     # Check parent or child for link
                     link_el = item.select_one('a')
                     permalink = link_el.get('href', '') if link_el else permalink
                
                # 2. Price
                price_el = item.select_one('.poly-price__current .andes-money-amount__fraction') or \
                           item.select_one('.ui-search-price__part .andes-money-amount__fraction') or \
                           item.select_one('.andes-money-amount__fraction')
                           
                if not price_el: continue
                
                price_str = price_el.get_text(strip=True).replace('.', '').replace(',', '.')
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
                    "id_original": f"ml_{int(time.time()*1000)}_{len(products)}", 
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
