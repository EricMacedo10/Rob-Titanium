# -*- coding: utf-8 -*-
"""
Produção: 100 Ofertas - Vestuário Feminino 
Minerador de Larga Escala (Mercado Livre & Shopee) Especializado em Roupas.
"""

import os
import sys
import json
import time

# Adiciona o diretório raiz ao path para importar módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from engines.mercadolivre import search_mercadolivre
from engines.meli_api import format_ml_product_for_site
from engines.shopee_affiliate import search_shopee
from core.browser import get_driver

def run_production_clothing_miner():
    print("💎 INICIANDO PRODUÇÃO 100 PEÇAS: VESTUÁRIO FEMININO 👗")
    
    # 25 Buscas Cirúrgicas * 4 itens cada = 100 Ofertas de Roupas
    # Foco total em Conversão, Estilo e Tamanhos
    targets = [
        {"q": "calca pantalona alfaiataria feminina", "tag": "#pantalona"},
        {"q": "conjunto alfaiataria feminino colete calca", "tag": "#alfaiataria"},
        {"q": "vestido midi canelado fenda", "tag": "#vestido"},
        {"q": "body poliamida feminino decote quadrado", "tag": "#body"},
        {"q": "blazer feminino max alongado", "tag": "#blazer"},
        {"q": "calca jeans wide leg cintura alta", "tag": "#jeans"},
        {"q": "vestido longo fluido elegante", "tag": "#vestido"},
        {"q": "tshirt básica algodão premium feminina", "tag": "#tshirt"},
        {"q": "conjunto moletinho casual feminino vip", "tag": "#moletinho"},
        {"q": "blusa tricot feminino modal", "tag": "#tricot"},
        {"q": "saia midi alfaiataria fenda", "tag": "#saia"},
        {"q": "camisa social feminina manga longa", "tag": "#camisa"},
        {"q": "jaqueta jeans feminina over", "tag": "#jaqueta"},
        {"q": "cardigan feminino longo tricot", "tag": "#cardigan"},
        {"q": "calca legging montaria peluciada", "tag": "#legging"},
        {"q": "vestido tubinho midi elegante", "tag": "#tubinho"},
        {"q": "macaquinho feminino transpassado", "tag": "#macaquinho"},
        {"q": "jaqueta couro ecologico feminina", "tag": "#couro"},
        {"q": "short alfaiataria cintura alta", "tag": "#short"},
        {"q": "blusa ombro a ombro ciganinha", "tag": "#blusa"}
    ]

    production_database = []
    
    # Inicia motor do Mercado Livre
    driver = get_driver(headless=True)
    
    try:
        for idx, target in enumerate(targets):
            print(f"\n[{idx+1}/{len(targets)}] 👗 Procurando Roupas para: {target['q']}")
            
            # --- 1. Busca Mercado Livre (Foco em Qualidade/Full) ---
            try:
                res_ml = search_mercadolivre(target['q'], driver, max_price=299)
                if res_ml: 
                    prod_ml = format_ml_product_for_site(res_ml, search_term=target['tag'])
                    prod_ml['category'] = "roupas_ml"
                    prod_ml['added_date'] = "2026-03-20"
                    production_database.append(prod_ml)
                    print(f"✅ ML Encontrou: {prod_ml['title'][:40]}...")
            except Exception as e:
                print(f"⚠️ Erro ML: {e}")
                
            time.sleep(2) # Proteção Antiblock
            
            # --- 2. Busca Shopee (Foco em Preço/Volume, buscamos 2-3 por termo) ---
            try:
                res_shp_list = search_shopee(target['q'], limit=3)
                for res_shp in res_shp_list:
                    prod_shp = {
                        "id": f"shp_{int(time.time() * 1000)}_{len(production_database)}",
                        "title": res_shp['titulo'],
                        "price": float(res_shp['preco']),
                        "old_price": f"{float(res_shp['preco']) * 1.35:.2f}",
                        "discount": 35,
                        "store": "Shopee",
                        "category": "roupas_shopee",
                        "image": res_shp['imagem'],
                        "link": res_shp['link_afiliado'],
                        "tags": [target['tag']],
                        "reason": "Trend Verão/Inverno",
                        "added_date": "2026-03-20"
                    }
                    production_database.append(prod_shp)
                    print(f"✅ Shopee Encontrou: {prod_shp['title'][:40]}...")
            except Exception as e:
                print(f"⚠️ Erro Shopee: {e}")
                
            time.sleep(3) # Proteção Antiblock API

            # Salva o arquivo de tempos em tempos para não perder dados se a luz cair!
            output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../site/data.json'))
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(production_database, f, indent=4, ensure_ascii=False)
                
        print(f"\n✨ SUCESSO! {len(production_database)} Peças de Vestuário geradas para Produção!")
        print(f"📂 Arquivo MESTRE atualizado em: {output_path}")

    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    run_production_clothing_miner()
