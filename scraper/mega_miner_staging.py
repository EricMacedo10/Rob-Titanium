# -*- coding: utf-8 -*-
"""
Minerador de Larga Escala - Titanium Shopee Exclusive
Este script busca produtos na Shopee e os formata para a vitrine.
"""

import os
import sys
import json
import time

# Adiciona o diretório raiz ao path para importar os módulos internos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from engines.shopee_affiliate import search_shopee

def run_mega_miner():
    print("💎 INICIANDO MEGA MINERADOR SHOPEE - TITANIUM 🛡️")
    
    # Alvos Estratégicos (Transferidos para Shopee)
    targets = [
        {"query": "conjunto alfaiataria feminino luxo", "tag": "#alfaiataria"},
        {"query": "vestido midi festa elegante", "tag": "#vestido"},
        {"query": "calca pantalona linho premium", "tag": "#pantalona"},
        {"query": "blazer feminino alfaiataria forrado", "tag": "#blazer"},
        {"query": "body poliamida decote quadrado", "tag": "#body"},
        {"query": "conjunto moletinho casual feminino", "tag": "#conjunto"},
        {"query": "tshirt algodao premium feminina", "tag": "#basico"},
        {"query": "vestido canelado midi fenda", "tag": "#fenda"},
        {"q": "bolsa feminina couro sintetico luxo", "tag": "#bolsa"},
        {"q": "relogio feminino dourado presente", "tag": "#relogio"},
        {"q": "kit pincel maquiagem profissional", "tag": "#make"},
        {"q": "perfume feminino importado original", "tag": "#perfume"}
    ]

    final_results = []

    try:
        for target in targets:
            query_str = target.get('query') or target.get('q')
            print(f"🔍 Minerando Shopee: {query_str}...")
            
            try:
                res_list = search_shopee(query_str, limit=3)
                for res in res_list:
                    product = {
                        "id": f"shp_{int(time.time() * 1000)}_{len(final_results)}",
                        "title": res['titulo'],
                        "price": float(res['preco']),
                        "old_price": f"{float(res['preco']) * 1.3:.2f}",
                        "discount": 30,
                        "store": "Shopee",
                        "category": "geral",
                        "image": res['imagem'],
                        "link": res['link_afiliado'],
                        "tags": [target['tag']],
                        "reason": "Seleção Titanium",
                        "added_date": time.strftime("%Y-%m-%d")
                    }
                    final_results.append(product)
                    print(f"✅ Adicionado: {product['title'][:40]}...")
            except Exception as e:
                print(f"❌ Erro em {query_str}: {e}")
            
            time.sleep(2)

        # Salvar o Resultado Final (Staging)
        output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data_fashion_staging.json'))
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(final_results, f, indent=4, ensure_ascii=False)
            
        print(f"\n✨ SUCESSO! {len(final_results)} itens minerados com foco 100% Shopee.")

    except Exception as e:
        print(f"🚨 Erro no Minerador: {e}")

if __name__ == "__main__":
    run_mega_miner()


if __name__ == "__main__":
    run_mega_fashion_miner()
