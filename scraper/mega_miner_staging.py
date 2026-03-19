# -*- coding: utf-8 -*-
"""
Minerador Multi-Loja (ML + Shopee + Amazon) - Dia das Mães Staging
Este script busca os 20 produtos (look completo) nas 3 maiores lojas
e os formata especificamente para o site de Staging.
"""

import os
import sys
import json
import time

# Adiciona o diretório raiz ao path para importar os módulos internos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from engines.mercadolivre import search_mercadolivre
from engines.meli_api import format_ml_product_for_site
from engines.shopee_affiliate import search_shopee
from engines.amazon import search_amazon
from core.browser import get_driver

def run_mega_fashion_miner():
    print("💎 INICIANDO MEGA MINERADOR MULTI-LOJA - TITANIUM 🛡️")
    
    # 1. Definir os Alvos Estratégicos
    targets = {
        "Mercado Livre": [
            {"query": "conjunto alfaiataria feminino luxo", "tag": "#alfaiataria"},
            {"query": "vestido midi festa elegante", "tag": "#vestido"},
            {"query": "calca pantalona linho premium", "tag": "#pantalona"},
            {"query": "blazer feminino alfaiataria forrado", "tag": "#blazer"}
        ],
        "Shopee": [
            {"query": "body poliamida decote quadrado", "tag": "#body"},
            {"query": "conjunto moletinho casual feminino", "tag": "#conjunto"},
            {"query": "tshirt algodao premium feminina", "tag": "#basico"},
            {"query": "vestido canelado midi fenda", "tag": "#fenda"}
        ],
        "Amazon": [
            {"query": "bolsa feminina couro sintetico luxo", "tag": "#bolsa"},
            {"query": "relogio feminino dourado presente", "tag": "#relogio"},
            {"query": "kit pincel maquiagem profissional", "tag": "#make"},
            {"query": "perfume feminino importado original", "tag": "#perfume"}
        ]
    }

    final_results = []
    driver = None

    try:
        # Loop por Loja
        for store, queries in targets.items():
            print(f"\n🚀 TRABALHANDO NA LOJA: {store}...")
            
            for target in queries:
                try:
                    product = None
                    print(f"🔍 Buscando: {target['query']}...")
                    
                    if store == "Mercado Livre":
                        if not driver: driver = get_driver(headless=True)
                        res = search_mercadolivre(target['query'], driver, max_price=300)
                        if res: product = format_ml_product_for_site(res, search_term=target['tag'])
                        
                    elif store == "Shopee":
                        res_list = search_shopee(target['query'], limit=1)
                        if res_list:
                            res = res_list[0]
                            product = {
                                "id": f"shp_{int(time.time() * 1000)}",
                                "title": res['titulo'],
                                "price": float(res['preco']),
                                "old_price": f"{res['preco'] * 1.3:.2f}",
                                "discount": 30,
                                "store": "Shopee",
                                "category": "moda_feminina",
                                "image": res['imagem'],
                                "link": res['link_afiliado'],
                                "tags": [target['tag']],
                                "reason": "Mais Vendido Shopee"
                            }
                            
                    elif store == "Amazon":
                        res = search_amazon(target['query'])
                        if res:
                            product = res
                            product['category'] = "acessorios"
                            product['tags'] = [target['tag']]

                    if product:
                        product['added_date'] = "2026-03-19"
                        final_results.append(product)
                        print(f"✅ Adicionado: {product['title'][:40]}...")
                    
                    time.sleep(2)
                except Exception as e:
                    print(f"❌ Erro em {target['query']}: {e}")

        # Salvar o Resultado Final
        output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data_fashion_staging.json'))
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(final_results, f, indent=4, ensure_ascii=False)
            
        print(f"\n✨ SUCESSO! {len(final_results)} itens de 3 lojas minerados.")

    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    run_mega_fashion_miner()
