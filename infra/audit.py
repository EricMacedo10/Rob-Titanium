
import json
import os
from urllib.parse import urlparse, parse_qs

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
        elif 'Shopee' in store:
            # Check if it's already a tagged shortlink or has utm parameters
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
    print(f"   [Shopee] UTM Sources: {list(shopee_tags)}")
    
    print("\n🚀 Verificação de Imagens e Títulos:")
    empty_images = [p['title'] for p in data if not p.get('image')]
    if empty_images:
        print(f"   ❌ Produtos sem imagem: {len(empty_images)}")
    else:
        print("   ✅ Todas as imagens estão presentes.")

    print("\n" + "="*60)

if __name__ == "__main__":
    audit_production_data('temp_prod_data.json')
