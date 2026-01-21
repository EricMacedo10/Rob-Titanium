"""
Utilitários para o Robô Titanium
Funções auxiliares para manipulação de links de afiliado
"""

from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from scraper.settings import AFFILIATE_TAGS


def add_affiliate_tag(url, store):
    """
    Adiciona o tag de afiliado ao URL de acordo com a loja.
    
    Args:
        url (str): URL original do produto
        store (str): Nome da loja ('amazon', 'shopee', 'mercadolivre')
    
    Returns:
        str: URL com tag de afiliado adicionado
    """
    if store not in AFFILIATE_TAGS:
        return url
    
    affiliate_id = AFFILIATE_TAGS[store]
    
    if store == "amazon":
        return add_amazon_tag(url, affiliate_id)
    elif store == "shopee":
        return add_shopee_tag(url, affiliate_id)
    elif store == "mercadolivre":
        return add_mercadolivre_tag(url, affiliate_id)
    
    return url


def add_amazon_tag(url, tag):
    """
    Adiciona o tag de afiliado da Amazon ao URL.
    Formato: ?tag=seu-tag-20
    
    Exemplo:
        Input:  https://amazon.com.br/produto/dp/B08XYZ
        Output: https://amazon.com.br/produto/dp/B08XYZ?tag=guiadodesco00-20
    """
    # Parse da URL
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    
    # Adiciona ou substitui o parâmetro 'tag'
    query_params['tag'] = [tag]
    
    # Reconstrói a query string
    new_query = urlencode(query_params, doseq=True)
    
    # Reconstrói a URL completa
    new_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    ))
    
    return new_url


def add_shopee_tag(url, tag):
    """
    Adiciona o tag de afiliado da Shopee ao URL.
    NOTA: Shopee requer API ou gerador manual.
    Por enquanto, retorna URL original.
    """
    # TODO: Implementar quando tivermos acesso à API
    return url


def add_mercadolivre_tag(url, tag):
    """
    Adiciona o tag de afiliado do Mercado Livre ao URL.
    NOTA: ML usa sistema de perfil social, não parâmetro direto.
    Por enquanto, retorna URL original.
    """
    # TODO: Usar gerador manual ou API do ML
    return url


def clean_amazon_url(url):
    """
    Limpa URL da Amazon removendo parâmetros desnecessários,
    mantendo apenas o essencial + tag de afiliado.
    
    Exemplo:
        Input:  https://amazon.com.br/dp/B08XYZ?ref=sr_1_1&keywords=test&tag=guiadodesco00-20
        Output: https://amazon.com.br/dp/B08XYZ?tag=guiadodesco00-20
    """
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    
    # Mantém apenas o parâmetro 'tag' se existir
    cleaned_params = {}
    if 'tag' in query_params:
        cleaned_params['tag'] = query_params['tag']
    
    new_query = urlencode(cleaned_params, doseq=True)
    
    new_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    ))
    
    return new_url
