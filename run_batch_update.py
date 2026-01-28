
import json
import time
import os
import random
from scraper.settings import TARGETS
from scraper.arbitro_preco import ArbitroDePreco
from scraper.ml_trends import update_site_with_trends

DATA_FILE = 'site/data.json'

def update_manual_targets():
    """
    Scrape products defined in TARGETS list (settings.py)
    """
    print("\n" + "="*60)
    print("ATUALIZANDO TARGETS DEFINIDOS")
    print("="*60)
    
    arbitro = ArbitroDePreco()
    new_products = []
    
    for i, target in enumerate(TARGETS):
        term = target['term']
        print(f"\n--- [{i+1}/{len(TARGETS)}] Buscando: {term} ---")
        
        try:
            # Use Arbitro to find best deal across all stores
            resultado = arbitro.processar_pedido(term)
            
            if resultado and 'melhor_produto' in resultado:
                prod = resultado['melhor_produto']
                
                # Format for site/data.json
                formatted = {
                    "id": f"prod_{int(time.time())}_{i}",
                    "title": prod['nome'],
                    "price": prod['preco'],
                    "old_price": prod['preco'] * 1.25, # Fake old price
                    "discount": 20,
                    "store": prod['loja'],
                    "category": target.get('category', 'geral'),
                    "image": prod['imagem'],
                    "link": prod['link'],
                    "reason": resultado.get('analise_ia', {}).get('motivo', 'Melhor oferta encontrada')
                }
                new_products.append(formatted)
                print(f"✅ Encontrado: {formatted['title'][:40]}... (R$ {formatted['price']})")
            else:
                print(f"⚠️ Nenhum produto encontrado para {term}")
                
        except Exception as e:
            print(f"❌ Erro ao buscar {term}: {e}")
            
        # Delay anti-ban
        time.sleep(5)
        
    return new_products

def main():
    print("🚀 INICIANDO ATUALIZAÇÃO AUTOMÁTICA DE OFERTAS")
    
    # Ensure site directory exists
    os.makedirs('site', exist_ok=True)
    
    # 1. Update ML Trends
    print(">>> Executando ML Trends...")
    try:
        # update_site_with_trends reads limits internally and updates data.json
        # We perform it first so we have a base
        update_site_with_trends(DATA_FILE)
    except Exception as e:
        print(f"❌ Falha ao atualizar trends: {e}")
        
    # 2. Update Manual Targets
    print("\n>>> Executando Targets Manuais...")
    fixed_products = update_manual_targets()
    
    # 3. Merge Strategies
    if fixed_products:
        print(f"\nMesclando {len(fixed_products)} novos produtos fixos...")
        
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                current_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            current_data = []
            
        # Strategy: 
        # - Keep recent Trends (id starts with trend_) 
        # - Discard old Fixed products (id starts with prod_) to replace with new ones
        # This prevents accumulation of duplicates
        
        trends_only = [p for p in current_data if str(p.get('id', '')).startswith('trend_')]
        final_list = trends_only + fixed_products
        
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(final_list, f, ensure_ascii=False, indent=4)
            
        print(f"✅ {DATA_FILE} atualizado com sucesso!")
        print(f"   Trends: {len(trends_only)}")
        print(f"   Fixos: {len(fixed_products)}")
        print(f"   Total: {len(final_list)}")
    
    print("\n🏁 EXECUÇÃO CONCLUÍDA!")

if __name__ == "__main__":
    main()
