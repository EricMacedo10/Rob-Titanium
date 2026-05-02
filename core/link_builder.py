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
            # Usa a API Oficial para gerar ShortLinks blindados (Universal Links)
            try:
                from .shopee_api import generate_affiliate_link
                return generate_affiliate_link(url)
            except Exception as e:
                print(f"[LinkBuilder] Erro ao usar API Shopee: {e}")
                tag = AFFILIATE_TAGS.get('shopee', 'an_18318830863')
                # Fallback manual se a API falhar
                from urllib.parse import urlparse, parse_qs, urlunparse, urlencode
                parsed = urlparse(url)
                params = parse_qs(parsed.query)
                params['utm_source'] = [tag]
                new_query = urlencode(params, doseq=True)
                return urlunparse((
                    parsed.scheme,
                    parsed.netloc,
                    parsed.path,
                    parsed.params,
                    new_query,
                    parsed.fragment
                ))
            
        return url
        
    except Exception as e:
        print(f"Erro ao criar link de afiliado: {e}")
        return url

