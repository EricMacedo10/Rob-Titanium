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
            # [v5.0] Usa a API Moderna (ShopeeAffiliateAPI) para gerar ShortLinks oficiais
            # Nunca usa utm_source como afiliado - apenas como rastreamento secundário
            
            # Se já é um shortlink (s.shopee.com.br ou shope.ee), retornar como está
            if 's.shopee.com.br' in url or 'shope.ee' in url:
                return url
            
            try:
                from scraper.engines.shopee_affiliate import ShopeeAffiliateAPI
                api = ShopeeAffiliateAPI()
                short = api.generate_short_link(url)
                if short:
                    return short
                print(f"[LinkBuilder] API nao retornou link. Retornando URL original.")
                return url
            except Exception as e:
                print(f"[LinkBuilder] Erro na API Shopee: {e}. Retornando URL original.")
            
        return url
        
    except Exception as e:
        print(f"Erro ao criar link de afiliado: {e}")
        return url

