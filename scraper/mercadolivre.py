# -*- coding: utf-8 -*-
"""
Mercado Livre Scraper
Extrai informações de produtos do Mercado Livre
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import random

def scrape_mercadolivre(url, driver):
    """
    Scrape de produto do Mercado Livre
    
    Args:
        url: URL do produto ou busca
        driver: Instância do Selenium WebDriver
        
    Returns:
        dict com dados do produto ou None se falhar
    """
    try:
        print(f"[ML] Acessando: {url}")
        driver.get(url)
        
        # Aguardar carregamento da página
        time.sleep(random.uniform(3, 5))
        
        # Aguardar elemento de preço carregar
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".ui-pdp-price__second-line"))
            )
        except:
            print("[ML] Timeout aguardando preço")
            return None
        
        # Parse HTML com BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Extrair dados
        title = extract_title(soup)
        price = extract_price(soup)
        image = extract_image(soup)
        product_url = driver.current_url  # URL real após redirecionamentos
        
        if not title or not price:
            print("[ML] Dados incompletos")
            return None
        
        product_data = {
            'title': title,
            'price': price,
            'image': image,
            'url': product_url,
            'source': 'Mercado Livre'
        }
        
        print(f"[ML] Produto encontrado: {title} - R$ {price}")
        return product_data
        
    except Exception as e:
        print(f"[ML] Erro no scraping: {e}")
        return None


def extract_title(soup):
    """Extrai título do produto"""
    try:
        # Seletor principal
        title_elem = soup.select_one('.ui-pdp-title')
        if title_elem:
            return title_elem.get_text(strip=True)
        
        # Fallback: h1
        h1 = soup.find('h1')
        if h1:
            return h1.get_text(strip=True)
        
        return None
    except Exception as e:
        print(f"[ML] Erro extraindo título: {e}")
        return None


def extract_price(soup):
    """Extrai preço do produto"""
    try:
        # Seletor principal: preço atual (segunda linha)
        price_fraction = soup.select_one('.ui-pdp-price__second-line .andes-money-amount__fraction')
        price_cents = soup.select_one('.ui-pdp-price__second-line .andes-money-amount__cents')
        
        if price_fraction:
            # Montar preço completo
            fraction_text = price_fraction.get_text(strip=True)
            cents_text = price_cents.get_text(strip=True) if price_cents else "00"
            
            # Remover pontos de milhar e converter
            fraction_text = fraction_text.replace('.', '')
            price_str = f"{fraction_text}.{cents_text}"
            
            return float(price_str)
        
        # Fallback: qualquer preço
        any_fraction = soup.select_one('.andes-money-amount__fraction')
        if any_fraction:
            fraction_text = any_fraction.get_text(strip=True).replace('.', '')
            return float(fraction_text)
        
        return None
    except Exception as e:
        print(f"[ML] Erro extraindo preço: {e}")
        return None


def extract_image(soup):
    """Extrai URL da imagem principal"""
    try:
        # Seletor principal
        img_elem = soup.select_one('.ui-pdp-image')
        if img_elem and img_elem.get('src'):
            return img_elem['src']
        
        # Fallback: primeira imagem do produto
        img_gallery = soup.select_one('.ui-pdp-gallery__figure__image')
        if img_gallery and img_gallery.get('src'):
            return img_gallery['src']
        
        return None
    except Exception as e:
        print(f"[ML] Erro extraindo imagem: {e}")
        return None


def search_mercadolivre(query, driver, max_price=1000):
    """
    Busca produtos no Mercado Livre
    
    Args:
        query: Termo de busca
        driver: Instância do Selenium WebDriver
        max_price: Preço máximo (parte inteira)
        
    Returns:
        dict com dados do primeiro produto válido ou None
    """
    try:
        # Construir URL de busca
        search_url = f"https://lista.mercadolivre.com.br/{query.replace(' ', '-')}"
        print(f"[ML] Buscando: {query}")
        
        driver.get(search_url)
        time.sleep(random.uniform(3, 5))
        
        # Aguardar resultados (Poly layout)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".poly-card"))
            )
        except:
            print("[ML] Timeout aguardando resultados")
            return None
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Encontrar produtos (Poly layout)
        products = soup.select('.poly-card')
        
        if not products:
            print("[ML] Nenhum produto encontrado na pagina")
            return None
        
        print(f"[ML] Encontrados {len(products)} produtos")
        
        for idx, product in enumerate(products[:5], 1):  # Verificar até 5 produtos
            try:
                print(f"[ML] Analisando produto {idx}...")
                
                # Extrair link do produto (Poly layout)
                link_elem = product.select_one('.poly-component__title')
                if not link_elem or not link_elem.get('href'):
                    print(f"[ML] Produto {idx}: link nao encontrado")
                    continue
                
                product_url = link_elem['href']
                
                # Extrair título
                title = link_elem.get_text(strip=True)
                
                # Extrair preço da listagem (Poly layout)
                price_elem = product.select_one('.poly-price__current .andes-money-amount__fraction')
                if not price_elem:
                    print(f"[ML] Produto {idx}: preco nao encontrado")
                    continue
                
                price_text = price_elem.get_text(strip=True).replace('.', '')
                price = float(price_text)
                
                print(f"[ML] Produto {idx}: {title[:40]}... - R$ {price}")
                
                # Verificar se está dentro do limite
                if int(price) <= max_price:
                    print(f"[ML] Produto {idx} aprovado! (R$ {price} <= R$ {max_price})")
                    # Scrape completo do produto
                    return scrape_mercadolivre(product_url, driver)
                else:
                    print(f"[ML] Produto {idx} rejeitado (R$ {price} > R$ {max_price})")
            
            except Exception as e:
                print(f"[ML] Erro processando produto {idx}: {e}")
                continue
        
        print(f"[ML] Nenhum produto encontrado abaixo de R$ {max_price}")
        return None
        
    except Exception as e:
        print(f"[ML] Erro na busca: {e}")
        return None
