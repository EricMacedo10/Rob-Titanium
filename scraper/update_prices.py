#!/usr/bin/env python3
"""
==============================================
 TITANIUM SHOPEE PRICE AUDITOR (Exclusive v2026)
 Auditor de preços focado 100% na API Shopee.
==============================================
"""
import json
import os
import sys
import time
from datetime import datetime

# Adiciona o diretório pai ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from engines.shopee_affiliate import search_shopee
except ImportError:
    print("⚠️  Módulo Shopee não encontrado em engines/shopee_affiliate.py")
    sys.exit(1)

# Caminhos
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_JSON_PATH = os.path.join(PROJECT_ROOT, 'site', 'data.json')

def update_shopee_prices():
    print("=" * 60)
    print("🛡️ TITANIUM SHOPEE AUDITOR - Sincronização de Preços")
    print("=" * 60)

    if not os.path.exists(DATA_JSON_PATH):
        print(f"❌ Erro: data.json não encontrado em {DATA_JSON_PATH}")
        return

    try:
        with open(DATA_JSON_PATH, 'r', encoding='utf-8') as f:
            deals = json.load(f)
    except Exception as e:
        print(f"❌ Erro ao ler JSON: {e}")
        return

    print(f"📦 Analisando {len(deals)} itens no catálogo...")

    # PURGA: Remove qualquer coisa que NÃO seja Shopee ou Amazon (expulsando intrusos)
    shopee_only = [d for d in deals if d.get('store', '').lower() == 'shopee']
    
    if len(shopee_only) < len(deals):
        print(f"🧹 PURGA CONCLUÍDA: {len(deals) - len(shopee_only)} intrusos (Amazon/ML) removidos.")

    updated_deals = []
    
    for i, deal in enumerate(shopee_only):
        title = deal.get('title', 'Sem título')[:40]
        print(f"[{i+1}/{len(shopee_only)}] Auditando: {title}...")
        
        try:
            # Busca o item novamente para ver se o preço mudou
            api_res = search_shopee(deal.get('title'), limit=1)
            
            if api_res:
                new_data = api_res[0]
                old_price = float(deal.get('price', 0))
                new_price = float(new_data['preco'])
                
                if abs(new_price - old_price) > 0.01:
                    print(f"   📉 Mudança detectada: R$ {old_price} -> R$ {new_price}")
                    deal['price'] = new_price
                    deal['old_price'] = round(new_price * 1.35, 2)
                else:
                    print("   ✅ Preço estável.")
                
                # Sincroniza Link e Imagem (Garante que o link de afiliado esteja fresco)
                deal['link'] = new_data['link_afiliado']
                deal['image'] = new_data['imagem']
            else:
                print("   ⚠️ Item não encontrado na API (Fora de estoque?)")
            
            updated_deals.append(deal)
            
        except Exception as e:
            print(f"   ❌ Erro na auditoria: {e}")
            updated_deals.append(deal)

        time.sleep(1.5) # Proteção de taxa de requisição

    # Salva o arquivo purificado e atualizado
    with open(DATA_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(updated_deals, f, ensure_ascii=False, indent=4)

    print(f"\n" + "=" * 60)
    print(f"✨ AUDITORIA CONCLUÍDA!")
    print(f"📊 Catálogo 100% Shopee com {len(updated_deals)} itens auditados.")
    print("=" * 60)

if __name__ == "__main__":
    update_shopee_prices()
