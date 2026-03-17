# -*- coding: utf-8 -*-
"""
Mercado Livre Affiliate Link Builder
Módulo para construir links de afiliado do Mercado Livre

Este módulo NÃO depende da API de busca (que pode ter rate limit).
Usa apenas o User ID obtido via OAuth para construir os parâmetros de tracking.

Autor: Robô Titanium
Data: 2026-01-20
"""

from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
from core.tokens import load_tokens

# Cache do User ID
_CACHED_USER_ID = None


def get_affiliate_user_id():
    """
    Obtém o User ID do afiliado a partir dos tokens salvos.
    
    Returns:
        str: User ID ou None
    """
    global _CACHED_USER_ID
    
    if _CACHED_USER_ID:
        return _CACHED_USER_ID
    
    tokens = load_tokens()
    if tokens and 'user_id' in tokens:
        _CACHED_USER_ID = str(tokens['user_id'])
        print(f"[ML Affiliate] User ID carregado: {_CACHED_USER_ID}")
        return _CACHED_USER_ID
    
    print("[ML Affiliate] AVISO: User ID não encontrado nos tokens. Usando fallback.")
    return "188269638" # ID fixo do afiliado ericmacedo


def build_ml_affiliate_link(product_url, keyword=None):
    """
    Constrói URL de afiliado do Mercado Livre.
    
    Adiciona parâmetros de tracking do programa de afiliados:
    - matt_tool: ID do afiliado (seu User ID)
    - matt_word: Palavra-chave da busca
    - matt_source: Origem do tráfego
    
    Args:
        product_url: URL original do produto ML
        keyword: Palavra-chave da busca (opcional)
        
    Returns:
        str: URL com parâmetros de afiliado
    """
    user_id = get_affiliate_user_id()
    
    if not user_id:
        print("[ML Affiliate] ERRO: Não foi possível obter User ID")
        print("[ML Affiliate] Execute primeiro: python scraper/meli_auth_flow.py")
        return product_url
    
    # Limpar URL existente de parâmetros anteriores
    parsed = urlparse(product_url)
    
    # Parâmetros de tracking do ML Afiliados
    affiliate_params = {
        "matt_tool": user_id,
        "matt_word": keyword or "oferta",
        "matt_source": "guiadodesconto",
        "tracking_id": f"gdd-{user_id}"
    }
    
    # Manter parâmetros existentes e adicionar os de afiliado
    existing_params = parse_qs(parsed.query)
    
    # Converter para formato simples (parse_qs retorna listas)
    for key, value in existing_params.items():
        if isinstance(value, list):
            existing_params[key] = value[0]
    
    # Merge: parâmetros de afiliado sobrescrevem existentes
    all_params = {**existing_params, **affiliate_params}
    
    # Reconstruir URL
    new_query = urlencode(all_params, doseq=False)
    affiliate_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    ))
    
    return affiliate_url


def format_ml_product_for_site(product_data, search_term=None):
    """
    Formata produto do ML para o padrão do site (data.json).
    
    Args:
        product_data: Dados brutos do produto (do scraper)
        search_term: Termo usado na busca
        
    Returns:
        dict: Produto formatado para o site
    """
    # Obter dados básicos
    title = product_data.get('title', 'Produto sem título')
    price = product_data.get('price', 0)
    image = product_data.get('image', '')
    original_url = product_data.get('url', '')
    
    # Construir link de afiliado
    affiliate_link = build_ml_affiliate_link(original_url, keyword=search_term)
    
    # Calcular desconto (se tiver preço original)
    old_price = product_data.get('old_price', price)
    if old_price and old_price > price:
        discount = int(((old_price - price) / old_price) * 100)
    else:
        discount = 10  # Desconto padrão se não tiver informação
        old_price = price * 1.1  # Simula preço antigo
    
    # Formatar para o padrão do site
    formatted = {
        "id": f"ml_{hash(original_url) % 1000000}",
        "title": title,
        "price": float(price),
        "old_price": f"{old_price:.2f}",
        "discount": discount,
        "store": "Mercado Livre",
        "category": "ofertas",
        "tags": [search_term.lower()] if search_term else [],
        "image": image,
        "link": affiliate_link,
        "reason": "Oferta Verificada",
        "votes": 0,
        "added_date": "2026-03-17"
    }
    
    # Verificação
    user_id = get_affiliate_user_id()
    if user_id and user_id in affiliate_link:
        print(f"[ML Affiliate] Link gerado com sucesso!")
        print(f"   User ID {user_id} confirmado no link")
    else:
        print(f"[ML Affiliate] AVISO: Verificar link de afiliado")
    
    return formatted


# ============================================================
# TESTES
# ============================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("TESTE DO MÓDULO ML AFFILIATE LINK BUILDER")
    print("="*60)
    
    # Teste 1: Obter User ID
    print("\n[Teste 1] Obtendo User ID...")
    user_id = get_affiliate_user_id()
    if user_id:
        print(f"[OK] User ID: {user_id}")
    else:
        print("[ERRO] User ID não encontrado")
        exit(1)
    
    # Teste 2: Construir link de afiliado
    print("\n[Teste 2] Construindo link de afiliado...")
    test_url = "https://www.mercadolivre.com.br/fone-bluetooth-teste/p/MLB12345678"
    affiliate_url = build_ml_affiliate_link(test_url, keyword="fone bluetooth")
    
    print(f"URL Original: {test_url}")
    print(f"URL Afiliado: {affiliate_url}")
    
    # Verificar se contém user_id
    if user_id in affiliate_url:
        print(f"\n[OK] Link contém User ID {user_id}")
    else:
        print(f"\n[ERRO] Link não contém User ID")
    
    # Teste 3: Formatar produto simulado
    print("\n[Teste 3] Formatando produto para o site...")
    mock_product = {
        "title": "Fone de Ouvido Bluetooth XYZ",
        "price": 89.90,
        "image": "https://example.com/image.jpg",
        "url": "https://www.mercadolivre.com.br/fone-xyz/p/MLB99999999"
    }
    
    formatted = format_ml_product_for_site(mock_product, search_term="fone bluetooth")
    
    print(f"Produto formatado:")
    print(f"  Titulo: {formatted['title']}")
    print(f"  Preco: R$ {formatted['price']}")
    print(f"  Link: {formatted['link'][:70]}...")
    print(f"  Store: {formatted['store']}")
