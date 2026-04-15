"""
Utilitários para o Robô Titanium - Shopee Elite (v3.2.0)
Funções auxiliares para manipulação de links Shopee
"""

from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from core.settings import AFFILIATE_TAGS


def add_affiliate_tag(url, store):
    """
    Adiciona o tag de afiliado ao URL de acordo com a loja.
    Focado exclusivamente em Shopee.
    
    Args:
        url (str): URL original do produto
        store (str): Nome da loja ('shopee')
    
    Returns:
        str: URL com tag de afiliado adicionado
    """
    if store != "shopee":
        return url
        
    affiliate_id = AFFILIATE_TAGS.get("shopee", "")
    return add_shopee_tag(url, affiliate_id)


def add_shopee_tag(url, tag):
    """
    Adiciona o tag de afiliado da Shopee ao URL.
    NOTA: Shopee requer geração via API Deep Link para ser efetivo.
    """
    # A geração real ocorre no scraper/engines/shopee_affiliate.py
    return url
