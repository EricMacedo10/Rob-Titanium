import json
import os
import sys
from urllib.parse import urlparse, parse_qs, urlunparse, urlencode

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

TARGET_TAG = "an_18318830863"
OFERTAS_FILE = 'social/ofertas.json'

def shield_url(url):
    if not url or 'shopee.com.br' not in url:
        return url

    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    # Injeção/Substituição atômica da Tag
    params['utm_source'] = [TARGET_TAG]
    
    # Remove mmp_pid se existir para evitar redundância desnecessária (opcional, mas limpa o link)
    if 'mmp_pid' in params:
        del params['mmp_pid']

    # Reconstrói a URL
    new_query = urlencode(params, doseq=True)
    new_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    ))
    
    return new_url

def audit_ofertas():
    if not os.path.exists(OFERTAS_FILE):
        print(f"Erro: {OFERTAS_FILE} não encontrado.")
        return

    with open(OFERTAS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    modified = False
    for hashtag, link in data.items():
        new_link = shield_url(link)
        if new_link != link:
            print(f"Fixing {hashtag}: {link} -> {new_link}")
            data[hashtag] = new_link
            modified = True

    if modified:
        with open(OFERTAS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("social/ofertas.json auditado e corrigido.")
    else:
        print("social/ofertas.json já está 100% íntegro.")

if __name__ == "__main__":
    audit_ofertas()
