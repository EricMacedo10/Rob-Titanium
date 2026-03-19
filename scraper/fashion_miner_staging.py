# -*- coding: utf-8 -*-
"""
Minerador de Moda Feminina - Titanium Specialized Scraper
Este script busca os 10 produtos de moda feminina mais quentes no Mercado Livre
e os formata especificamente para o site de Staging (teste.guiadodesconto.com.br).
"""

import os
import sys
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Adiciona o diretório raiz ao path para importar os módulos internos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from engines.mercadolivre import search_mercadolivre
from engines.meli_api import format_ml_product_for_site

def run_fashion_miner():
    print("👗 INICIANDO MINERADOR DE MODA FEMININA - TITANIUM 🛡️")
    
    # Configuração do WebDriver (Headless para rodar em background)
    chrome_options = Options()
    # chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Categorias e Termos de Busca Quentes (Baseados na análise de mercado)
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
    
    try:
        for target in fashion_targets:
            print(f"\n🔍 Minerando: {target['query']}...")
            # Busca no Mercado Livre com limite de preço realista para alta conversão (até R$ 250)
            product = search_mercadolivre(target['query'], driver, max_price=250)
            
            if product:
                # Formata com a inteligência de links de afiliado
                formatted = format_ml_product_for_site(product, search_term=target['tag'])
                # Ajusta a categoria para o Staging
                formatted['category'] = "moda_feminina"
                fashion_results.append(formatted)
                print(f"✅ Adicionado: {formatted['title'][:50]}...")
            else:
                print(f"⚠️ Nenhum resultado ideal para '{target['query']}'")
            
            time.sleep(2) # Pausa amigável entre buscas

        # Salvar os resultados para o Staging
        output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data_fashion_staging.json'))
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(fashion_results, f, indent=4, ensure_ascii=False)
            
        print(f"\n✨ SUCESSO! {len(fashion_results)} tesouros de moda minerados.")
        print(f"📂 Arquivo gerado: {output_path}")

    finally:
        driver.quit()

if __name__ == "__main__":
    run_fashion_miner()
