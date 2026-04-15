import urllib.parse
from .settings import AFFILIATE_TAGS

def build_affiliate_link(url, store, keyword=None):
    """
    Recebe uma URL limpa (ex: amazon.com.br/dp/B09B8...)
    Retorna a URL com o parametro de afiliado anexado.
    
    Args:
        url: URL original do produto
        store: Nome da loja (amazon, mercadolivre, shopee)
        keyword: Palavra-chave da busca (opcional, usado no ML)
    """
    try:
        if store == 'amazon':
            tag = AFFILIATE_TAGS.get('amazon', '')
            if not tag or tag == "seutag-20":
                return url # Retorna sem tag se o usuário não configurou
            
            # Adiciona ?tag=guiadodesco00-20
            sep = "&" if "?" in url else "?"
            return f"{url}{sep}tag={tag}"
        
        elif store == 'mercadolivre':
            # Usa o novo módulo de links de afiliado com OAuth
            try:
                from .meli_api import build_ml_affiliate_link
                affiliate_url = build_ml_affiliate_link(url, keyword=keyword)
                return affiliate_url
            except ImportError as e:
                print(f"[LinkBuilder] Módulo meli_api não encontrado: {e}")
                return url
            except Exception as e:
                print(f"[LinkBuilder] Erro ao gerar link ML: {e}")
                return url
            
        elif store == 'shopee':
            tag = AFFILIATE_TAGS.get('shopee', 'an_18318830863')
            if not tag:
                return url
            
            # Adiciona utm_source=an_18318830863
            sep = "&" if "?" in url else "?"
            return f"{url}{sep}utm_source={tag}"
            
        return url
        
    except Exception as e:
        print(f"Erro ao criar link de afiliado: {e}")
        return url

