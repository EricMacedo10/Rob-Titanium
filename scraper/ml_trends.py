# -*- coding: utf-8 -*-
"""
Modulo de Tendencias do Mercado Livre
Busca os termos mais populares via API e gera produtos com links de afiliado

Fluxo:
1. API ML /trends/MLB -> termos populares
2. Selenium busca produtos reais desses termos
3. Gera links com tag de afiliado (matt_tool=188269638)
4. Salva no data.json
"""

import requests
import json
import random
import time
from .meli_token_manager import load_tokens
from .meli_api import build_ml_affiliate_link, get_affiliate_user_id

# Configuracao
MAX_TRENDS = 6  # Numero de tendencias a buscar
DELAY_BETWEEN_SEARCHES = 5  # segundos entre buscas


def get_ml_trends():
    """
    Busca as tendencias do Mercado Livre Brasil via API
    
    Returns:
        list: Lista de termos em alta (keywords)
    """
    tokens = load_tokens()
    if not tokens or 'access_token' not in tokens:
        print("[Tendencias] ERRO: Token nao encontrado")
        return []
    
    access_token = tokens['access_token']
    
    try:
        response = requests.get(
            'https://api.mercadolibre.com/trends/MLB',
            headers={'Authorization': f'Bearer {access_token}'},
            timeout=10
        )
        
        if response.status_code == 200:
            trends = response.json()
            keywords = [t.get('keyword') for t in trends if t.get('keyword')]
            print(f"[Tendencias] {len(keywords)} tendencias encontradas")
            return keywords[:MAX_TRENDS]
        else:
            print(f"[Tendencias] ERRO: Status {response.status_code}")
            return []
            
    except Exception as e:
        print(f"[Tendencias] ERRO: {e}")
        return []


def get_category_trends(category_id):
    """
    Busca tendencias de uma categoria especifica
    
    Args:
        category_id: ID da categoria (ex: MLB1648 para Tecnologia)
        
    Returns:
        list: Lista de termos em alta na categoria
    """
    tokens = load_tokens()
    if not tokens:
        return []
    
    try:
        response = requests.get(
            f'https://api.mercadolibre.com/trends/MLB/{category_id}',
            headers={'Authorization': f'Bearer {tokens["access_token"]}'},
            timeout=10
        )
        
        if response.status_code == 200:
            trends = response.json()
            return [t.get('keyword') for t in trends if t.get('keyword')][:5]
        else:
            return []
            
    except Exception as e:
        print(f"[Tendencias] ERRO categoria {category_id}: {e}")
        return []


def search_product_for_trend(trend_keyword, driver):
    """
    Busca um produto real no ML para um termo de tendencia
    Usa Selenium para scraping
    
    Args:
        trend_keyword: Termo de busca
        driver: WebDriver do Selenium
        
    Returns:
        dict: Dados do produto ou None
    """
    from .mercadolivre import search_mercadolivre
    
    try:
        print(f"[Tendencias] Buscando: {trend_keyword}")
        product = search_mercadolivre(trend_keyword, driver, max_price=5000)
        
        if product:
            # Adicionar link de afiliado
            affiliate_link = build_ml_affiliate_link(product['link'], keyword=trend_keyword)
            product['link'] = affiliate_link
            product['trend_keyword'] = trend_keyword
            print(f"[Tendencias] Encontrado: {product.get('title', '')[:40]}...")
            return product
        else:
            print(f"[Tendencias] Nenhum produto para: {trend_keyword}")
            return None
            
    except Exception as e:
        print(f"[Tendencias] ERRO busca {trend_keyword}: {e}")
        return None


def update_site_with_trends(output_file='site/data.json'):
    """
    Funcao principal: Busca tendencias e atualiza o site
    
    1. Busca tendencias via API
    2. Para cada tendencia, busca produto via Selenium
    3. Gera links de afiliado
    4. Atualiza data.json
    """
    print("\n" + "="*60)
    print("ATUALIZANDO SITE COM TENDENCIAS DO ML")
    print("="*60)
    
    # Verificar User ID
    user_id = get_affiliate_user_id()
    if not user_id:
        print("[ERRO] User ID nao encontrado. Execute meli_auth_flow.py primeiro.")
        return []
    
    print(f"[OK] User ID: {user_id}")
    
    # 1. Buscar tendencias
    print("\n[1] Buscando tendencias...")
    trends = get_ml_trends()
    
    if not trends:
        print("[ERRO] Nenhuma tendencia encontrada")
        return []
    
    print(f"[OK] Tendencias: {', '.join(trends)}")
    
    # 2. Inicializar Selenium
    print("\n[2] Iniciando busca de produtos...")
    from .amazon import get_driver
    driver = get_driver()
    
    products = []
    
    try:
        for i, trend in enumerate(trends):
            print(f"\n--- [{i+1}/{len(trends)}] {trend} ---")
            
            # Delay anti-ban
            if i > 0:
                wait_time = random.uniform(DELAY_BETWEEN_SEARCHES, DELAY_BETWEEN_SEARCHES + 3)
                print(f"[Aguardando {wait_time:.1f}s...]")
                time.sleep(wait_time)
            
            product = search_product_for_trend(trend, driver)
            
            if product:
                # Formatar para o site
                formatted_product = {
                    "id": f"trend_{random.randint(10000, 99999)}",
                    "title": product.get('title', 'Produto ML'),
                    "price": product.get('price', 0),
                    "old_price": str(float(product.get('price', 0)) * 1.2),
                    "discount": 20,
                    "store": "Mercado Livre",
                    "category": "trending",
                    "image": product.get('image', ''),
                    "link": product.get('link', ''),
                    "reason": f"Em Alta: {trend}",
                    "trend_keyword": trend
                }
                products.append(formatted_product)
                
    finally:
        driver.quit()
        print("\n[OK] Browser fechado")
    
    # 3. Atualizar data.json
    if products:
        print(f"\n[3] Salvando {len(products)} produtos de tendencia...")
        
        try:
            # Carregar produtos existentes
            with open(output_file, 'r', encoding='utf-8') as f:
                existing = json.load(f)
        except:
            existing = []
        
        # Remover produtos de tendencia antigos
        existing = [p for p in existing if not p.get('id', '').startswith('trend_')]
        
        # Adicionar novos no inicio
        updated = products + existing
        
        # Salvar
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(updated, f, ensure_ascii=False, indent=4)
        
        print(f"[OK] {output_file} atualizado!")
        print(f"    - Produtos de tendencia: {len(products)}")
        print(f"    - Total de produtos: {len(updated)}")
    
    print("\n" + "="*60)
    print("ATUALIZACAO CONCLUIDA!")
    print("="*60)
    
    return products


# Execucao direta
if __name__ == "__main__":
    update_site_with_trends()
