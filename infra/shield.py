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
    """
    if not url or 'shopee.com.br' not in url:
        return url

    # Pula links curtos que já são domínios de afiliado (confiamos no backend de encurtamento)
    if 's.shopee.com.br' in url or 'shope.ee' in url:
        return url

    # Remove parâmetros de tracking 'sujos' que podem interferir
    url = re.sub(r'[?&](sp_atk|xptdk)=[^&]*', '', url)

    # Parse da URL
    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    # Se já tem utm_source mas é diferente, substitui. Se não tem, adiciona.
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
    print("🛡️  INICIANDO BLINDAGEM NUCLEAR TITANIUM (v3.8)")
    print("="*60)

    total_fixed = 0

    for file_path in FILES_TO_SHIELD:
        if not os.path.exists(file_path):
            print(f"⚠️  Aviso: {file_path} não encontrado. Pulando...")
            continue

        print(f"🔍 Auditando {file_path}...")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            modified = False
            for item in data:
                original_link = item.get('link', '')
                # Suporte para diferentes esquemas de JSON (ai_reviews usa 'link', data usa 'link')
                if not original_link and 'product_url' in item:
                    original_link = item['product_url']
                
                shielded_link = shield_url(original_link)
                
                if original_link != shielded_link:
                    # Atualiza o link no objeto (preservando a chave original)
                    if 'link' in item: item['link'] = shielded_link
                    if 'product_url' in item: item['product_url'] = shielded_link
                    modified = True
                    total_fixed += 1

            if modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                print(f"✅ {file_path} BLINDADO com sucesso.")
            else:
                print(f"✨ {file_path} já estava 100% íntegro.")

        except Exception as e:
            print(f"❌ Erro ao blindar {file_path}: {e}")

    print("="*60)
    print(f"📊 RESUMO DA OPERAÇÃO: {total_fixed} links corrigidos.")
    print("🛡️  SISTEMA BLINDADO E PRONTO PARA DEPLOY.")
    print("="*60)
    
    return True

if __name__ == "__main__":
    apply_nuclear_shield()
