import json
import os
import sys
from urllib.parse import urlparse, parse_qs, urlunparse, urlencode

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Lazy import da API Shopee
try:
    from scraper.engines.shopee_affiliate import ShopeeAffiliateAPI
    _shopee_api_available = True
except ImportError:
    _shopee_api_available = False

# Cache em memória para evitar chamadas duplicadas na mesma execução
_shortlink_cache: dict = {}

TARGET_TAG = "an_18318830863"
OFERTAS_FILE = 'social/ofertas.json'


def _shield_url_via_api(url: str) -> str:
    """
    [MÉTODO PRIMÁRIO]
    Gera Short Link oficial da Shopee (s.shopee.com.br) com subId de afiliado.
    """
    global _shortlink_cache
    if url in _shortlink_cache:
        return _shortlink_cache[url]
    try:
        api = ShopeeAffiliateAPI()
        short = api.generate_short_link(url, sub_id=TARGET_TAG)
        if short:
            _shortlink_cache[url] = short
            return short
    except Exception as e:
        print(f"  [ShortLink] ❌ Erro: {e}")
    return None


def shield_url(url: str) -> str:
    """
    Nuclear Shield v4.0 — Auditoria de links do ofertas.json.
    Primário: ShortLink Oficial Shopee | Fallback: utm_source
    """
    if not url or 'shopee.com.br' not in url:
        return url

    # Evita reprocessar Short Links já válidos
    if 's.shopee.com.br' in url:
        return url

    # Tentativa via API
    if _shopee_api_available:
        short = _shield_url_via_api(url)
        if short:
            return short

    # Fallback: utm_source
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    params['utm_source'] = [TARGET_TAG]
    if 'mmp_pid' in params:
        del params['mmp_pid']
    new_query = urlencode(params, doseq=True)
    return urlunparse((
        parsed.scheme, parsed.netloc, parsed.path,
        parsed.params, new_query, parsed.fragment
    ))

def audit_ofertas():
    modo = "ShortLink Oficial (API)" if _shopee_api_available else "UTM Source (Fallback)"
    print(f"\n{'='*60}")
    print(f"SHIELD: AUDITANDO ofertas.json | MODO: {modo}")
    print(f"{'='*60}")

    if not os.path.exists(OFERTAS_FILE):
        print(f"❌ Erro: {OFERTAS_FILE} não encontrado.")
        return

    with open(OFERTAS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    modified = False
    fixed_count = 0
    already_ok = 0
    for hashtag, link in data.items():
        new_link = shield_url(link)
        if new_link != link:
            print(f"  ✅ Blindado [{hashtag}]: ...{link[-40:]} → {new_link}")
            data[hashtag] = new_link
            modified = True
            fixed_count += 1
        else:
            already_ok += 1

    if modified:
        with open(OFERTAS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"\n✅ {fixed_count} link(s) blindados. {already_ok} já estavam OK.")
        print("social/ofertas.json auditado e corrigido.")
    else:
        print(f"\n✅ Todos os {already_ok} links já estão 100% íntegros.")
        print("social/ofertas.json já está 100% íntegro.")
    print("="*60)

if __name__ == "__main__":
    audit_ofertas()
