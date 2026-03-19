# -*- coding: utf-8 -*-
"""
Minerador de Moda Feminina via API - Titanium Specialized Scraper
Este script busca os 10 produtos de moda feminina via API Oficial do Mercado Livre
e os formata especificamente para o site de Staging.
"""

import os
import sys
import json
import requests
from urllib.parse import quote

# Adiciona o diretório raiz ao path para importar os módulos internos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from engines.meli_api import format_ml_product_for_site

def run_fashion_api_miner():
    print("👗 INICIANDO MINERADOR DE MODA FEMININA VIA API - TITANIUM 🛡️")
    
    # Categorias e Termos de Busca Quentes
    fashion_targets = [
        {"query": "conjunto alfaiataria feminino colete e calca", "tag": "#alfaiataria"},
        {"query": "vestido midi canelado feminino", "tag": "#vestido"},
        {"query": "calca pantalona alfaiataria cintura alta", "tag": "#pantalona"},
        {"query": "body poliamida feminino manga longa", "tag": "#body"},
        {"query": "conjunto moletinho feminino casual premium", "tag": "#conjunto"},
        {"query": "blazer feminino oversized alfaiataria", "tag": "#blazer"},
        {"query": "calca jeans wide leg feminina tendencia", "tag": "#jeans"},
        {"query": "vestido longo floral fluido feminino", "tag": "#floral"},
        {"query": "tshirt feminina algodao premium pima", "tag": "#basico"},
        {"query": "tricot feminino conjunto blusa e calca", "tag": "#tricot"}
    ]

    fashion_results = []
    
    # 1. Tentar obter o token de acesso (Client Credentials ou Manual)
    # Nota: Usaremos a busca PÚBLICA primeiro pois é mais rápida e estável para 10 itens
    for target in fashion_targets:
        print(f"\n🔍 Buscando via API: {target['query']}...")
        
        # URL de busca do ML (Pública)
        search_url = f"https://api.mercadolibre.com/sites/MLB/search?q={quote(target['query'])}&limit=5"
        
        try:
            resp = requests.get(search_url)
            if resp.status_code == 200:
                data = resp.json()
                results = data.get('results', [])
                
                # Filtrar o melhor candidato (abaixo de R$ 250 e com boa reputação se possível)
                for item in results:
                    price = item.get('price', 0)
                    if price > 30 and price <= 250:
                        # Extrair os dados necessários no formato esperado pelo format_ml_product_for_site
                        product_data = {
                            "title": item.get('title'),
                            "price": price,
                            "image": item.get('thumbnail').replace("-I.", "-O."), # Converte para imagem original
                            "url": item.get('permalink'),
                            "old_price": item.get('original_price') or price * 1.2
                        }
                        
                        formatted = format_ml_product_for_site(product_data, search_term=target['tag'])
                        formatted['category'] = "moda_feminina"
                        fashion_results.append(formatted)
                        print(f"✅ API Encontrou: {formatted['title'][:50]}... por R$ {formatted['price']}")
                        break # Pega apenas o primeiro válido
            else:
                print(f"⚠️ Erro API ({resp.status_code}) para '{target['query']}'")
        except Exception as e:
            print(f"❌ Erro na requisição: {e}")

    # Salvar os resultados para o Staging
    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data_fashion_staging.json'))
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(fashion_results, f, indent=4, ensure_ascii=False)
        
    print(f"\n✨ SUCESSO via API! {len(fashion_results)} tesouros de moda minerados.")
    print(f"📂 Arquivo gerado: {output_path}")

if __name__ == "__main__":
    run_fashion_api_miner()
