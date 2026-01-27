"""
Mercado Livre Scraper (Selenium Version)
Substitui a API pública depreciada (403 Forbidden).
"""
import logging
import time
from typing import Dict, List
from bs4 import BeautifulSoup
from urllib.parse import urlencode

from scraper.browser import get_driver

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def search_mercadolivre(query: str, limit: int = 3) -> List[Dict]:
    driver = None
    try:
        logger.info(f"[ML] Starting Selenium Search for: {query}")
        driver = get_driver(headless=True)
        
        # Ordenar por menor preço: _OrderId_PRICE
        url = f"https://lista.mercadolivre.com.br/{query.replace(' ', '-')}_OrderId_PRICE"
        driver.get(url)
        
        # Wait for content
        time.sleep(3)
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        products = []
        
        # Try finding cards (support both layouts)
        cards = soup.select('.poly-card') # New layout
        if not cards:
             cards = soup.select('.ui-search-layout__item') # Legacy
             
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
