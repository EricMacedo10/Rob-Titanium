# -*- coding: utf-8 -*-
import os
import sys
import json
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from engines.mercadolivre import search_mercadolivre
from engines.meli_api import format_ml_product_for_site
from core.browser import get_driver

def fix_ml():
    print("👗 RECUPERANDO LOTES DO MERCADO LIVRE (FIX)...")
    
    targets = [
        {"q": "calca pantalona alfaiataria feminina", "tag": "#pantalona"},
        {"q": "conjunto alfaiataria feminino colete calca", "tag": "#alfaiataria"},
        {"q": "vestido midi canelado fenda", "tag": "#vestido"},
        {"q": "blazer feminino max alongado", "tag": "#blazer"},
        {"q": "calca jeans wide leg cintura alta", "tag": "#jeans"},
        {"q": "vestido longo fluido elegante", "tag": "#vestido"},
        {"q": "blusa tricot feminino modal", "tag": "#tricot"},
        {"q": "saia midi alfaiataria fenda", "tag": "#saia"},
        {"q": "camisa social feminina manga longa", "tag": "#camisa"},
        {"q": "jaqueta couro ecologico feminina", "tag": "#couro"}
    ]

    data_path = 'site/data.json'
    with open(data_path, 'r', encoding='utf-8') as f:
        db = json.load(f)

    # Remove ML antigos pra nao duplicar (caso tenha sobrado algum lixo)
    db = [item for item in db if item.get('store') != 'Mercado Livre']
    
    driver = get_driver(headless=True)
    ml_items = []

    try:
        for t in targets:
            print(f"🔍 ML: {t['q']}...")
            res = search_mercadolivre(t['q'], driver, max_price=350)
            if res:
                # O search_mercadolivre agora retorna dict com 'title', 'price', 'image', 'link', 'source'
                prod = format_ml_product_for_site(res, search_term=t['tag'])
                if prod.get('image') and not prod['image'].endswith('.svg'):
                    ml_items.append(prod)
                    print(f"✅ Sucesso: {prod['title'][:30]}")
            time.sleep(2)
        
        # Merge
        db.extend(ml_items)
        
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(db, f, indent=4, ensure_ascii=False)
            
        print(f"✨ Pronto! {len(ml_items)} itens do Mercado Livre reinjetados com sucesso.")

    finally:
        driver.quit()

if __name__ == "__main__":
    fix_ml()
