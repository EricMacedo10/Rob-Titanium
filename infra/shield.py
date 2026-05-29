import json
import os
import re
import sys
from urllib.parse import urlparse, parse_qs, urlunparse, urlencode

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Lazy import da API Shopee (evita crash se o módulo não estiver disponível)
try:
    from scraper.engines.shopee_affiliate import ShopeeAffiliateAPI
    _shopee_api_available = True
except ImportError:
    _shopee_api_available = False

# Cache local de Short Links para evitar chamadas duplicadas à API durante uma mesma execução
_shortlink_cache: dict = {}

# Configurações de Elite
TARGET_TAG = "an_18318830863"
SHIELD_VERSION = "v4.0-ShortLink"
FILES_TO_SHIELD = [
    'site/data.json',
    'site/specialist.json',
    'site/ai_reviews.json',
    'social/ofertas.json',
    'site/data_sensual.json',
    'site/ai_reviews_sensual.json',
    'site/specialist_sensual.json'
]

def _shield_url_via_api(url: str) -> str:
    """
    [MÉTODO PRIMÁRIO - v4.0]
    Gera um Short Link oficial da Shopee via API (s.shopee.com.br).
    Este é o único método que garante o crédito de comissão de afiliado.
    Usa cache em memória para evitar chamadas duplicadas na mesma execução.
    """
    global _shortlink_cache

    if url in _shortlink_cache:
        return _shortlink_cache[url]

    try:
        api = ShopeeAffiliateAPI()
        short_link = api.generate_short_link(url, sub_id=TARGET_TAG)
        if short_link:
            print(f"  [ShortLink] ✅ {url[:60]}... → {short_link}")
            _shortlink_cache[url] = short_link
            return short_link
        else:
            print(f"  [ShortLink] ⚠️  API não retornou link para {url[:60]}... Usando fallback.")
    except Exception as e:
        print(f"  [ShortLink] ❌ Erro na API: {e}. Usando fallback utm_source.")

    return None


def _shield_url_via_utm(url: str) -> str:
    """
    [MÉTODO DE FALLBACK - Legado]
    Injeta utm_source para rastreamento do Google Analytics.
    ATENÇÃO: Não garante comissão Shopee. Usar apenas se a API não estiver disponível.
    """
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    params['utm_source'] = [TARGET_TAG]
    new_query = urlencode(params, doseq=True)
    return urlunparse((
        parsed.scheme, parsed.netloc, parsed.path,
        parsed.params, new_query, parsed.fragment
    ))


def shield_url(url: str) -> str:
    """
    🛡️ Nuclear Shield v4.0 - Blindagem Atômica de Comissão.
    PRIORIDADE 1: Gera Short Link oficial via API Shopee (s.shopee.com.br) — garante comissão real.
    FALLBACK:     Injeta utm_source — garante rastreamento GA, mas NÃO garante comissão Shopee.
    """
    if not url or 'shopee.com.br' not in url:
        return url

    # Se o link já é um Short Link da Shopee, não reprocessa
    if 's.shopee.com.br' in url:
        print(f"  [ShortLink] ✅ Link já é um Short Link. Ignorando.")
        return url

    # Tentativa via API oficial (Método Primário)
    if _shopee_api_available:
        short = _shield_url_via_api(url)
        if short:
            return short

    # Fallback: injeção de utm_source
    print(f"  [Fallback] Injetando utm_source em: {url[:60]}...")
    return _shield_url_via_utm(url)

def apply_nuclear_shield():
    print("="*60)
    print(f"SHIELD: INICIANDO BLINDAGEM NUCLEAR TITANIUM ({SHIELD_VERSION})")
    if _shopee_api_available:
        print("MODO: ShortLink Oficial (API Shopee) — Comissão 100% Garantida")
    else:
        print("MODO: UTM Source (Fallback) — ATENÇÃO: Comissão pode não ser creditada!")
    print("="*60)

    total_fixed = 0

    for file_path in FILES_TO_SHIELD:
        if not os.path.exists(file_path):
            print(f"WARN: {file_path} nao encontrado. Pulando...")
            continue

        print(f"INFO: Auditando {file_path}...")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            modified = False
            
            # Handle list of objects (like data.json)
            if isinstance(data, list):
                for item in data:
                    original_link = item.get('link', '')
                    if not original_link and 'product_url' in item:
                        original_link = item['product_url']
                    
                    shielded_link = shield_url(original_link)
                    
                    if original_link != shielded_link:
                        if 'link' in item: item['link'] = shielded_link
                        if 'product_url' in item: item['product_url'] = shielded_link
                        modified = True
                        total_fixed += 1
            
            # Handle simple dictionary (like ofertas.json)
            elif isinstance(data, dict):
                for key, original_link in data.items():
                    shielded_link = shield_url(original_link)
                    if original_link != shielded_link:
                        data[key] = shielded_link
                        modified = True
                        total_fixed += 1

            if modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                print(f"SUCCESS: {file_path} BLINDADO com sucesso.")
            else:
                print(f"OK: {file_path} ja estava 100% integro.")

        except Exception as e:
            print(f"ERROR: Erro ao blindar {file_path}: {e}")

    print("="*60)
    print(f"STATS: {total_fixed} links corrigidos.")
    print("SHIELD: SISTEMA BLINDADO E PRONTO PARA DEPLOY.")
    print("="*60)
    
    return True

if __name__ == "__main__":
    apply_nuclear_shield()
