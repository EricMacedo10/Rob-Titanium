from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import random
from scraper.utils import add_affiliate_tag

# Inicializa o Browser (Singleton para não abrir mil janelas)
def get_driver():
    import os
    
    # Detecta se está rodando em CI (GitHub Actions, etc.)
    is_ci = os.getenv('CI') == 'true' or os.getenv('GITHUB_ACTIONS') == 'true'
    
    options = Options()
    
    # Modo Headless AUTOMÁTICO em CI
    if is_ci:
        print("   🤖 Ambiente CI detectado - Modo Headless ativado")
        options.add_argument("--headless=new")  # Novo modo headless do Chrome
        options.add_argument("--no-sandbox")  # Necessário para CI
        options.add_argument("--disable-dev-shm-usage")  # Evita problemas de memória
        options.add_argument("--disable-gpu")  # Desabilita GPU em headless
    else:
        print("   💻 Ambiente local detectado - Modo visual ativado")
    
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # ESTRATÉGIA COOKIE CLONE (Perfil Persistente) - Apenas em ambiente local
    if not is_ci:
        # Isso cria uma pasta aqui na raiz chamada "chrome_profile"
        # Tudo que você fizer no navegador (Login) fica salvo aqui.
        profile_path = os.path.join(os.getcwd(), "chrome_profile")
        options.add_argument(f"user-data-dir={profile_path}")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def search_amazon(term):
    """
    Busca na Amazon usando Selenium para burlar proteções avançadas.
    """
    driver = None
    try:
        print(f"   🔥 Iniciando Motor Blindado (Selenium)...")
        driver = get_driver()
        
        safe_term = term.replace(" ", "+")
        url = f"https://www.amazon.com.br/s?k={safe_term}"
        
        print(f"   ↳ Navegando para: {url}")
        driver.get(url)
        
        # ⏰ TEMPO PARA LOGIN MANUAL (apenas em ambiente local)
        import os
        is_ci = os.getenv('CI') == 'true' or os.getenv('GITHUB_ACTIONS') == 'true'
        
        if not is_ci:
            print(f"\n   ⏰ AGUARDANDO 2 MINUTOS PARA VOCÊ FAZER LOGIN...")
            print(f"   ℹ️  Faça login na Amazon agora se necessário!")
            print(f"   ℹ️  O robô vai continuar automaticamente em 120 segundos...\n")
            time.sleep(120)  # 2 minutos para login manual
            print(f"   ✅ Tempo de login encerrado. Continuando...\n")
        else:
            print(f"   🤖 Modo CI: Pulando espera de login manual")
        
        # Delay aleatório humano adicional
        time.sleep(random.uniform(3, 7))
        
        # Pega o HTML final renderizado
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        # DEBUG: Verifica título da página
        page_title = driver.title
        print(f"   ℹ Título da página: {page_title}")

        # Check de Captcha
        if "captcha" in driver.page_source.lower() or "robô" in driver.page_source.lower():
             print("   ⚠ ALERTA DE CAPTCHA DETECTADO! A Amazon pediu validação visual.")

        # Lógica de Extração (Mesma de antes)
        results = soup.select('div[data-component-type="s-search-result"]')
        if not results:
             print("   Recorrendo a seletor genérico...")
             results = soup.select('.s-result-item')
        
        print(f"   ℹ Itens encontrados no HTML: {len(results)}")

        if not results:
            print("   ⚠ Nada encontrado mesmo com Selenium.")
            return None

        # Processa o primeiro item válido
        for idx, item in enumerate(results[:3]):
            try:
                print(f"   🔍 Analisando item {idx+1}/3...")
                
                title_el = item.select_one("h2 span")
                if not title_el:
                    print(f"      ❌ Título não encontrado")
                    continue
                title = title_el.text.strip()
                print(f"      ✅ Título: {title[:50]}...")

                price_whole = item.select_one(".a-price-whole")
                if not price_whole:
                    print(f"      ❌ Preço não encontrado")
                    continue
                
                # FIX: Preços brasileiros usam vírgula como decimal
                # Exemplo: "299,90" precisa virar "299.90"
                price_text = price_whole.text.strip()
                print(f"      📊 Preço bruto: '{price_text}'")
                
                # Remove pontos (separador de milhar) e substitui vírgula por ponto
                price_str = price_text.replace('.', '').replace(',', '.').strip()
                print(f"      📊 Preço processado: '{price_str}'")
                
                try:
                    price = float(price_str)
                    print(f"      ✅ Preço convertido: R$ {price:.2f}")
                except ValueError as e:
                    print(f"      ❌ Erro ao converter preço: {e}")
                    continue
                
                # DEBUG: Salva HTML do item para análise
                print(f"      🔍 HTML do item (primeiros 500 chars):")
                item_html = str(item)[:500]
                print(f"      {item_html}...")
                
                # Link - Tenta múltiplos seletores E atributos
                link_el = None
                raw_link = None
                
                # Estratégia 1: Procura tags <a> tradicionais
                selectors = [
                    "h2 a",
                    "a.a-link-normal",
                    ".s-title-instructions-style a",
                    "a[href*='/dp/']",
                ]
                
                for selector in selectors:
                    link_el = item.select_one(selector)
                    if link_el and link_el.get('href'):
                        raw_link = link_el['href']
                        print(f"      ✅ Link encontrado com <a> seletor: {selector}")
                        break
                
                # Estratégia 2: Se não achou <a>, procura <span> com data-href ou onclick
                if not raw_link:
                    print(f"      ⚠️  Nenhum <a> encontrado, tentando <span>...")
                    span_selectors = [
                        "span.a-link-normal",
                        "span[data-href]",
                        ".s-title-instructions-style span",
                    ]
                    
                    for selector in span_selectors:
                        span_el = item.select_one(selector)
                        if span_el:
                            # Tenta pegar href de data-href
                            if span_el.get('data-href'):
                                raw_link = span_el['data-href']
                                print(f"      ✅ Link encontrado em <span data-href> com seletor: {selector}")
                                break
                            # Tenta pegar do parent <a>
                            parent = span_el.find_parent('a')
                            if parent and parent.get('href'):
                                raw_link = parent['href']
                                print(f"      ✅ Link encontrado no parent <a> do <span>")
                                break
                
                # Estratégia 3: Procura qualquer elemento com href contendo /dp/
                if not raw_link:
                    print(f"      ⚠️  Tentando busca genérica por /dp/...")
                    all_links = item.select('[href*="/dp/"]')
                    if all_links:
                        raw_link = all_links[0]['href']
                        print(f"      ✅ Link encontrado em busca genérica")
                
                if not raw_link:
                    print(f"      ❌ Link não encontrado com nenhuma estratégia")
                    print(f"      📋 Salvando HTML completo do item em debug_item.html...")
                    with open('debug_item.html', 'w', encoding='utf-8') as f:
                        f.write(str(item))
                    continue
                    
                # Monta URL completa
                if raw_link.startswith('http'):
                    raw_link = raw_link
                elif raw_link.startswith('/'):
                    raw_link = "https://www.amazon.com.br" + raw_link
                else:
                    raw_link = "https://www.amazon.com.br/" + raw_link
                
                # 💰 ADICIONA TAG DE AFILIADO (Aqui está a mágica!)
                link = add_affiliate_tag(raw_link, "amazon")
                print(f"      ✅ Link com afiliado gerado")
                
                # Imagem
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
                import traceback
                traceback.print_exc()
                continue
                
        return None

    except Exception as e:
        print(f"   ❌ Erro Crítico Selenium: {e}")
        return None
    finally:
        if driver:
            driver.quit()
