import json
import os
import sys
from urllib.parse import urlparse, parse_qs

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def audit_production_data(file_path):
    print("="*60)
    print(f"📊 AUDITORIA DE DADOS - ROBÔ TITANIUM (PROD)")
    print("="*60)
    
    if not os.path.exists(file_path):
        print(f"❌ Erro: Arquivo {file_path} não encontrado!")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total = len(data)
    print(f"✅ Total de Produtos: {total}")
    
    stores = {}
    amazon_tags = set()
    shopee_tags = set()
    ml_tags = set()
    
    for p in data:
        store = p.get('store', 'Desconhecido')
        stores[store] = stores.get(store, 0) + 1
        
        link = p.get('link', '')
        parsed = urlparse(link)
        params = parse_qs(parsed.query)
        
        if 'Amazon' in store:
            tag = params.get('tag', ['MISSING'])[0]
            amazon_tags.add(tag)
        if 'Shopee' in store:
            # v4.0: Verifica Short Links oficiais (s.shopee.com.br) OU utm_source
            if 's.shopee.com.br' in link:
                shopee_tags.add('s.shopee.com.br [SHORT_LINK_OFICIAL]')
            else:
                utm = params.get('utm_source', ['MISSING'])[0]
                shopee_tags.add(utm)
        elif 'Mercado Livre' in store:
            tool = params.get('matt_tool', ['MISSING'])[0]
            ml_tags.add(tool)

    print("\n📦 Distribuição por Loja:")
    for store, count in stores.items():
        print(f"   - {store}: {count} ({round(count/total*100, 1)}%)")

    print("\n💰 Auditoria de Affiliate Tracking:")
    
    # Amazon Check
    print(f"   [Amazon] Tags encontradas: {list(amazon_tags)}")
    if 'guiadodesco00-20' in amazon_tags:
        print("      ✅ Amazon Tracking: OK (guiadodesco00-20)")
    else:
        print("      ❌ Amazon Tracking: ALERTA (Tag guiadodesco00-20 não detectada!)")

    # Mercado Livre Check
    print(f"   [ML] Matt Tools encontrados: {list(ml_tags)}")
    if '188269638' in ml_tags:
        print("      ✅ Mercado Livre Tracking: OK (Matt Tool 188269638)")
    else:
        print("     ⚠️ Mercado Livre Tracking: ALERTA (Pode estar usando shortlinks ou redirecionamento JS)")

    # Shopee Check
    print(f"   [Shopee] Tags/Short Links encontrados: {list(shopee_tags)}")
    if any('SHORT_LINK_OFICIAL' in t or 'an_18318830863' in t for t in shopee_tags):
        print("      ✅ Shopee Tracking: OK (Short Link Oficial ou utm_source correto)")
    elif 'MISSING' in shopee_tags and len(shopee_tags) == 1:
        print("      ❌ Shopee Tracking: ALERTA — Nenhum link com tag de afiliado detectado!")
    else:
        print("      ⚠️  Shopee Tracking: Verificar links manualmente.")
    
    print("\n🚀 Verificação de Imagens e Títulos:")
    empty_images = [p['title'] for p in data if not p.get('image')]
    if empty_images:
        print(f"   ❌ Produtos sem imagem: {len(empty_images)}")
    else:
        print("   ✅ Todas as imagens estão presentes.")

    print("\n" + "="*60)

if __name__ == "__main__":
    audit_production_data('temp_prod_data.json')
