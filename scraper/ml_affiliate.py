# -*- coding: utf-8 -*-
"""
Mercado Livre Affiliate Link Generator - NEW FLOW
Fluxo usando busca integrada + botao Compartilhar + Resolucao de Link

URL: https://www.mercadolivre.com.br/afiliados/hub#menu-lateral

FLUXO:
1. Acessar pagina de afiliados
2. Buscar produto na barra integrada
3. Clicar no botao "Compartilhar" do primeiro resultado
4. Clicar em "Copiar link" no modal
5. Abrir link em nova aba para resolver para URL completa
6. Extrair link final com tag ericmacedo
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import json
import os
import pyperclip

# Configuracoes
ML_HUB_URL = "https://www.mercadolivre.com.br/afiliados/hub#menu-lateral"
ML_CACHE_FILE = "ml_links_cache.json"


def load_link_cache():
    """Carrega cache de links gerados"""
    try:
        if os.path.exists(ML_CACHE_FILE):
            with open(ML_CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"[ML Affiliate] Erro carregando cache: {e}")
    return {}


def save_link_cache(cache):
    """Salva cache de links gerados"""
    try:
        with open(ML_CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[ML Affiliate] Erro salvando cache: {e}")


def setup_affiliate_hub(driver, wait_for_login=120):
    """
    Configura pagina de afiliados e aguarda login
    """
    print(f"\n{'='*70}")
    print("CONFIGURANDO PAGINA DE AFILIADOS")
    print(f"{'='*70}")
    
    try:
        if "afiliados" in driver.current_url:
            print("[Hub] Ja esta na pagina de afiliados")
            return True
        
        print(f"[Hub] Abrindo {ML_HUB_URL}...")
        driver.get(ML_HUB_URL)
        time.sleep(3)
        
        print(f"[Hub] Aguardando {wait_for_login}s para login...")
        print(f"[Hub] FACA LOGIN se necessario!")
        time.sleep(wait_for_login)
        
        print(f"[Hub] Pronto!")
        return True
        
    except Exception as e:
        print(f"[Hub] ERRO: {e}")
        return False


def search_product_in_hub(driver, search_query, wait_timeout=15):
    """
    Busca produto na barra de busca integrada do Hub de Afiliados
    """
    print(f"\n{'='*70}")
    print(f"BUSCANDO PRODUTO: {search_query}")
    print(f"{'='*70}")
    
    try:
        # Primeiro, limpar qualquer overlay que possa estar bloqueando
        try:
            driver.execute_script("""
                var overlays = document.querySelectorAll('.andes-modal__overlay, [class*="overlay"], [role="dialog"]');
                overlays.forEach(function(o) { o.remove(); });
                var modals = document.querySelectorAll('.andes-modal, .modal');
                modals.forEach(function(m) { m.remove(); });
            """)
        except:
            pass
        
        print("[Busca] Localizando campo de busca...")
        
        search_field = WebDriverWait(driver, wait_timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.andes-form-control__field[placeholder*='Busque']"))
        )
        
        print(f"[Busca] Campo encontrado!")
        
        # Usar JavaScript para interagir com o campo (mais confiavel)
        driver.execute_script("arguments[0].focus();", search_field)
        driver.execute_script("arguments[0].value = '';", search_field)
        time.sleep(0.3)
        
        # Tentar click normal primeiro, se falhar, usar JS
        try:
            search_field.click()
        except:
            driver.execute_script("arguments[0].click();", search_field)
        
        search_field.send_keys(search_query)
        search_field.send_keys(Keys.RETURN)
        
        print(f"[Busca] Busca enviada: {search_query}")
        print(f"[Busca] Aguardando resultados...")
        time.sleep(8)
        
        # Verificar se ha resultados
        print(f"[Busca] Procurando cards de produtos...")
        
        # Procurar por botoes "Compartilhar"
        share_buttons = driver.find_elements(By.XPATH, "//button[.//span[contains(text(), 'Compartilhar')]]")
        
        if share_buttons:
            print(f"[Busca] {len(share_buttons)} produtos encontrados!")
            return True
        
        # Fallback
        cards = driver.find_elements(By.CSS_SELECTOR, "[class*='card'], [class*='item'], [class*='product']")
        
        if cards and len(cards) > 10:
            print(f"[Busca] {len(cards)} elementos encontrados!")
            return True
        
        print(f"[Busca] Nenhum produto encontrado")
        return False
            
    except Exception as e:
        print(f"[Busca] ERRO: {e}")
        return False


def resolve_short_link(driver, short_link):
    """
    Abre o link curto em uma nova aba para resolver para o link completo
    
    Args:
        driver: WebDriver
        short_link: Link curto (ex: https://mercadolivre.com/sec/...)
    
    Returns:
        Link completo com tag ericmacedo ou None
    """
    print(f"\n{'='*70}")
    print("RESOLVENDO LINK CURTO")
    print(f"{'='*70}")
    
    original_handle = driver.current_window_handle
    
    try:
        # Abrir nova aba
        print("[Resolve] Abrindo nova aba...")
        driver.execute_script(f"window.open('{short_link}', '_blank');")
        time.sleep(2)
        
        # Mudar para nova aba
        new_handle = [h for h in driver.window_handles if h != original_handle][0]
        driver.switch_to.window(new_handle)
        
        # Aguardar redirecionamento
        print("[Resolve] Aguardando redirecionamento...")
        time.sleep(5)
        
        # Capturar URL final
        final_url = driver.current_url
        print(f"[Resolve] URL final: {final_url[:80]}...")
        
        # Verificar tag
        if "ericmacedo" in final_url:
            print("[Resolve] Tag 'ericmacedo' CONFIRMADA!")
        else:
            print("[Resolve] AVISO: Tag 'ericmacedo' nao encontrada na URL final")
        
        # Fechar aba
        driver.close()
        
        # Voltar para aba original
        driver.switch_to.window(original_handle)
        print("[Resolve] Voltou para aba principal")
        
        return final_url
        
    except Exception as e:
        print(f"[Resolve] ERRO: {e}")
        # Tentar voltar para aba original
        try:
            driver.switch_to.window(original_handle)
        except:
            pass
        return None


def click_share_and_copy_link(driver, wait_timeout=10):
    """
    Clica no botao Compartilhar do primeiro produto e copia o link
    """
    print(f"\n{'='*70}")
    print("CLICANDO EM COMPARTILHAR E COPIANDO LINK")
    print(f"{'='*70}")
    
    try:
        # Localizar botao Compartilhar
        print("[Share] Localizando botao Compartilhar...")
        
        try:
            share_button = WebDriverWait(driver, wait_timeout).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'Compartilhar')]]"))
            )
            print("[Share] Botao encontrado via XPath!")
        except:
            try:
                share_button = driver.find_element(By.CSS_SELECTOR, "button.andes-button__content")
                print("[Share] Botao encontrado via CSS!")
            except:
                print("[Share] ERRO: Botao Compartilhar nao encontrado")
                return None
        
        # Clicar no botao
        print("[Share] Clicando em Compartilhar...")
        share_button.click()
        time.sleep(2)
        
        # Aguardar modal abrir
        print("[Share] Aguardando modal abrir...")
        
        modal = WebDriverWait(driver, wait_timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[role='dialog'], .modal, [class*='modal']"))
        )
        
        print("[Share] Modal aberto!")
        
        # Localizar botao "Copiar link"
        print("[Share] Localizando botao 'Copiar link'...")
        
        copy_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'Copiar link')]]"))
        )
        
        print("[Share] Botao 'Copiar link' encontrado!")
        
        # Limpar clipboard
        pyperclip.copy("")
        
        # Clicar em Copiar link
        print("[Share] Clicando em 'Copiar link'...")
        copy_button.click()
        time.sleep(1)
        
        # Obter link do clipboard
        short_link = pyperclip.paste()
        
        if short_link and ("mercadolivre" in short_link or "mercado" in short_link):
            print(f"[Share] Link curto copiado: {short_link[:60]}...")
        else:
            print(f"[Share] ERRO: Link invalido ou nao copiado")
            # Fechar modal
            try:
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
            except:
                pass
            return None
        
        # Fechar modal de forma robusta
        print("[Share] Fechando modal...")
        modal_closed = False
        
        # Metodo 1: Botao X
        try:
            close_btn = driver.find_element(By.CSS_SELECTOR, "button[aria-label*='Cerrar'], button[aria-label*='Fechar'], button[aria-label*='Close'], .andes-modal__close-button")
            driver.execute_script("arguments[0].click();", close_btn)
            print("[Share] Modal fechado via botao X (JS)")
            modal_closed = True
        except:
            pass
        
        # Metodo 2: ESC via JavaScript
        if not modal_closed:
            try:
                driver.execute_script("document.dispatchEvent(new KeyboardEvent('keydown', {'key': 'Escape', 'code': 'Escape'}));")
                print("[Share] Enviado ESC via JavaScript")
                modal_closed = True
            except:
                pass
        
        # Metodo 3: Clicar fora do modal (na overlay)
        if not modal_closed:
            try:
                overlay = driver.find_element(By.CSS_SELECTOR, ".andes-modal__overlay")
                driver.execute_script("arguments[0].click();", overlay)
                print("[Share] Clicou na overlay para fechar")
                modal_closed = True
            except:
                pass
        
        # Metodo 4: Remover modal via JavaScript (ultimo recurso)
        if not modal_closed:
            try:
                driver.execute_script("""
                    var modals = document.querySelectorAll('[role="dialog"], .andes-modal, .modal');
                    modals.forEach(function(m) { m.remove(); });
                    var overlays = document.querySelectorAll('.andes-modal__overlay');
                    overlays.forEach(function(o) { o.remove(); });
                """)
                print("[Share] Modal removido via JavaScript")
                modal_closed = True
            except:
                pass
        
        # Aguardar overlay desaparecer
        try:
            WebDriverWait(driver, 5).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, ".andes-modal__overlay"))
            )
            print("[Share] Overlay desapareceu!")
        except:
            # Forcar remocao da overlay
            try:
                driver.execute_script("""
                    var overlays = document.querySelectorAll('.andes-modal__overlay, [class*="overlay"]');
                    overlays.forEach(function(o) { o.style.display = 'none'; o.remove(); });
                """)
                print("[Share] Overlay removida forcadamente via JS")
            except:
                print("[Share] AVISO: Overlay pode ainda estar presente")
        
        time.sleep(1)
        
        return short_link
            
    except Exception as e:
        print(f"[Share] ERRO: {e}")
        import traceback
        traceback.print_exc()
        return None


def generate_affiliate_link(search_query, driver, first_time=False):
    """
    Gera link de afiliado usando o novo fluxo completo
    
    Args:
        search_query: Termo de busca (ex: "PlayStation 5")
        driver: WebDriver
        first_time: Se True, configura o hub e aguarda login
    
    Returns:
        Link de afiliado com tag 'ericmacedo' ou None
    """
    print(f"\n{'='*70}")
    print(f"GERANDO LINK DE AFILIADO: {search_query}")
    print(f"{'='*70}")
    
    # Verificar cache
    cache = load_link_cache()
    cache_key = search_query.lower().strip()
    
    if cache_key in cache:
        print(f"[Cache] Link encontrado no cache!")
        return cache[cache_key]
    
    try:
        # Configurar hub (apenas na primeira vez)
        if first_time:
            if not setup_affiliate_hub(driver):
                print("[ERRO] Falha ao configurar hub de afiliados")
                return None
        
        # Buscar produto
        if not search_product_in_hub(driver, search_query):
            print("[ERRO] Falha ao buscar produto")
            return None
        
        # Clicar em Compartilhar e copiar link curto
        short_link = click_share_and_copy_link(driver)
        
        if not short_link:
            print("[ERRO] Falha ao obter link curto")
            return None
        
        # Resolver link curto para obter URL completa com tag
        full_link = resolve_short_link(driver, short_link)
        
        if full_link:
            # Salvar no cache
            cache[cache_key] = full_link
            save_link_cache(cache)
            
            print(f"\n{'='*70}")
            print("SUCESSO!")
            print(f"{'='*70}")
            
            if "ericmacedo" in full_link:
                print(f"[OK] Tag 'ericmacedo' confirmada!")
            
            print(f"Link: {full_link[:100]}...")
            
            return full_link
        else:
            print("[ERRO] Falha ao resolver link")
            return None
            
    except Exception as e:
        print(f"[ERRO] {e}")
        import traceback
        traceback.print_exc()
        return None


# Compatibilidade com codigo antigo
def setup_linkbuilder_tab(driver, wait_for_login=120):
    """Alias para setup_affiliate_hub"""
    return setup_affiliate_hub(driver, wait_for_login)


def generate_affiliate_link_from_search(search_query, driver, linkbuilder_handle=None):
    """Alias para generate_affiliate_link"""
    return generate_affiliate_link(search_query, driver, first_time=(linkbuilder_handle is None))
