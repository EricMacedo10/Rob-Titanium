# -*- coding: utf-8 -*-
"""
Producao: 100% Shopee Exclusive - Vestuario e Beleza
Minerador de Alta Performance focado na API Oficial Shopee v2.
"""

import os
import sys
import json
import time

# Adiciona o diretorio raiz ao path para importar modulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from engines.shopee_affiliate import search_shopee
except ImportError:
    # Caso esteja rodando de dentro da pasta scraper
    from scraper.engines.shopee_affiliate import search_shopee

def run_production_miner():
    print("[Titanium] INICIANDO MINERACAO SHOPEE GOLD: MODA & BELEZA")
    
    # Mix Estrategico: 50% MODA | 50% BELEZA
    targets = [
        {"q": "calca pantalona alfaiataria feminina", "tag": "#pantalona"},
        {"q": "conjunto alfaiataria feminino colete calca", "tag": "#alfaiataria"},
        {"q": "vestido midi canelado fenda", "tag": "#vestido"},
        {"q": "body poliamida feminino decote quadrado", "tag": "#body"},
        {"q": "blazer feminino max alongado", "tag": "#blazer"},
        {"q": "calca jeans wide leg cintura alta", "tag": "#jeans"},
        {"q": "tshirt basica algodao premium feminina", "tag": "#pima"},
        {"q": "conjunto moletinho casual feminino vip", "tag": "#conforto"},
        {"q": "saia midi alfaiataria fenda", "tag": "#executiva"},
        {"q": "vestido longo festa fluido", "tag": "#festa"},
        {"q": "kit pinceis maquiagem profissional kabuki", "tag": "#maquiagem"},
        {"q": "serum facial vitamina c anti idade", "tag": "#skincare"},
        {"q": "paleta de sombras cores neutras matte", "tag": "#beleza"},
        {"q": "kit skincare facial limpeza profunda", "tag": "#rosto"},
        {"q": "mascara de cilios volume intenso", "tag": "#olhar"},
        {"q": "base maquiagem alta cobertura matte", "tag": "#make"},
        {"q": "batom liquido matte longa duracao", "tag": "#labios"},
        {"q": "secador de cabelo profissional potente", "tag": "#cabelo"},
        {"q": "chapinha prancha nano titanium original", "tag": "#alisado"},
        {"q": "perfume feminino importado fragrancia doce", "tag": "#perfume"}
    ]

    production_database = []
    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../site/data.json'))
    
    try:
        for idx, target in enumerate(targets):
            print(f"[{idx+1}/{len(targets)}] Minerando Shopee: {target['q']}")
            
            try:
                # Buscamos 6 itens por termo para garantir volume total de ~120 produtos
                res_shp_list = search_shopee(target['q'], limit=6)
                
                for res_shp in res_shp_list:
                    prod_shp = {
                        "id": f"shp_{int(time.time() * 1000)}_{len(production_database)}",
                        "title": res_shp['titulo'],
                        "price": float(res_shp['preco']),
                        "old_price": round(float(res_shp['preco']) * 1.45, 2),
                        "discount": 45,
                        "store": "Shopee",
                        "category": "fashion_beauty",
                        "image": res_shp['imagem'],
                        "link": res_shp['link_afiliado'],
                        "tags": [target['tag']],
                        "reason": "Top Tendencia Boutique",
                        "added_date": time.strftime("%Y-%m-%d")
                    }
                    production_database.append(prod_shp)
                    print(f"   [OK] {prod_shp['title'][:40]}...")
            except Exception as e:
                print(f"   [!] Erro API Shopee: {e}")
                
            time.sleep(1.5) # Protecao de taxa API

            # Salva de tempos em tempos
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(production_database, f, indent=4, ensure_ascii=False)
                
        print(f"\n[SUCESSO] {len(production_database)} produtos carregados no catalogo!")
        print(f"Arquivo data.json atualizado em: {output_path}")

    except Exception as grand_error:
        print(f"ERRO FATAL: {grand_error}")

if __name__ == "__main__":
    run_production_miner()
