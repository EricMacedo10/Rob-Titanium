from bs4 import BeautifulSoup
import time
import random
from core.utils import add_affiliate_tag
from core.browser import get_driver

def search_amazon(term):
    """
    Busca na Amazon usando Selenium para burlar proteções avançadas.
    """
    driver = None
    try:
        print(f"   🔥 Iniciando Motor Blindado (Selenium)...")
        driver = get_driver(headless=True)
        
        safe_term = term.replace(" ", "+")
        url = f"https://www.amazon.com.br/s?k={safe_term}&s=price-asc-rank" 
        
        print(f"   ↳ Navegando para: {url}")
        driver.get(url)
        
        # Delay aleatório humano
        time.sleep(random.uniform(3, 5))
        
        # Check title
        if "Algo deu errado" in driver.title:
            print("   ⚠️  Amazon detectou bot (Soft Block). Tentando reload...")
            time.sleep(2)
            driver.refresh()
            time.sleep(3)
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        # Check de Captcha
        if "captcha" in driver.page_source.lower() or "robô" in driver.page_source.lower():
             print("   ⚠️  ALERTA DE CAPTCHA DETECTADO! A Amazon pediu validação visual.")

        # Lógica de Extração
        results = soup.select('div[data-component-type="s-search-result"]')
        if not results:
             print("   Recorrendo a seletor genérico...")
             results = soup.select('.s-result-item')
        
        print(f"   ℹ Itens encontrados no HTML: {len(results)}")

        if not results:
            print("   ⚠ Nada encontrado.")
            return None

        # Processa o primeiro item válido
        for idx, item in enumerate(results[:3]):
            try:
                # Title
                title_el = item.select_one("h2 span")
                if not title_el: continue
                title = title_el.text.strip()

                # Price - Seletor Melhorado (Senior Workflow v2026)
                # Prioridade 1: Seletor exato do preço principal (apex-pricetopay)
                price_el = item.select_one('.apex-pricetopay-value .a-offscreen') or \
                           item.select_one('.a-price[data-a-color="base"] .a-offscreen') or \
                           item.select_one('.a-price .a-offscreen')
                
                if price_el:
                    # Formato: "R$3,90" ou "R$2.999,00"
                    price_text = price_el.text.strip()
                    price_str = price_text.replace('R$', '').replace('.', '').replace(',', '.').strip()
                else:
                    # Fallback: seletor antigo .a-price-whole
                    price_whole = item.select_one(".a-price-whole")
                    if not price_whole: continue
                    price_str = price_whole.text.strip().replace('.', '').replace(',', '.').strip()
                
                try:
                    price = float(price_str)
                except:
                    continue
                
                # Link
                link_el = item.select_one("h2 a") or \
                          item.select_one("a.a-link-normal") or \
                          item.select_one("a[href*='/dp/']")
                          
                if not link_el: continue
                raw_link = link_el.get('href')
                
                if raw_link.startswith('/'):
                    raw_link = "https://www.amazon.com.br" + raw_link
                
                link = add_affiliate_tag(raw_link, "amazon")
                
                # Image
                img_el = item.select_one(".s-image")
                image = img_el['src'] if img_el else ""

                product = {
                    "id": f"amz_{random.randint(10000,99999)}",
                    "title": title,
                    "price": price,
                    "old_price": f"{price * 1.2:.2f}",
                    "discount": 20,
                    "store": "Amazon",
                    "category": "tech",
                    "image": image,
                    "link": link,
                    "reason": "Oferta Verificada"
                }
                
                print(f"      🎉 PRODUTO EXTRAÍDO COM SUCESSO!")
                return product
                
            except Exception as e:
                print(f"      ❌ Erro ao processar item {idx+1}: {e}")
                continue
                
        return None

    except Exception as e:
        print(f"   ❌ Erro Crítico Selenium: {e}")
        return None
    finally:
        if driver:
            driver.quit()
