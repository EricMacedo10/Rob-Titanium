import json
import os
import re
from urllib.parse import urlparse, parse_qs, urlunparse, urlencode

# Configurações de Elite
TARGET_TAG = "an_18318830863"
FILES_TO_SHIELD = [
    'site/data.json',
    'site/specialist.json',
    'site/ai_reviews.json'
]

def shield_url(url):
    """
    Aplica a blindagem atômica em uma única URL Shopee.
    Garante que a tag utm_source seja única e correta.
    """
    if not url or 'shopee.com.br' not in url:
        return url

    # Parse da URL para garantir integridade
    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    # Injeção/Substituição atômica da Tag
    params['utm_source'] = [TARGET_TAG]

    # Reconstrói a URL limpa e blindada
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

def apply_nuclear_shield():
    print("="*60)
    print("SHIELD: INICIANDO BLINDAGEM NUCLEAR TITANIUM (v3.8)")
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
