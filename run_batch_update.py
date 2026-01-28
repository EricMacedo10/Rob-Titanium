
import json
import time
import os
import random
from scraper.settings import TARGETS
from scraper.arbitro_preco import ArbitroDePreco
from scraper.ml_trends import update_site_with_trends
from scraper.upload import upload_to_hostinger

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
        # - PREVENT DUPLICATES: Check if new fixed product is already in trends
        
        trends_only = [p for p in current_data if str(p.get('id', '')).startswith('trend_')]
        
        # Create set of normalized titles from trends for fast lookup
        trend_titles = {str(p.get('title', '')).lower().strip() for p in trends_only}
        
        unique_fixed = []
        for p in fixed_products:
            p_title = str(p.get('title', '')).lower().strip()
            # Validate image and title
            if not p.get('image') or not p_title:
                continue

            if p_title not in trend_titles:
                unique_fixed.append(p)
                trend_titles.add(p_title) # Prevent internal duplicates too
            else:
                print(f"⚠️ Duplicata removida: {p.get('title')}")
                
        final_list = trends_only + unique_fixed
        
        # Final sanity check: remove items with no image just in case
        final_list = [p for p in final_list if p.get('image')]
        
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(final_list, f, ensure_ascii=False, indent=4)
            
        print(f"✅ {DATA_FILE} atualizado com sucesso!")
        print(f"   Trends: {len(trends_only)}")
        print(f"   Fixos: {len(fixed_products)}")
        print(f"   Total: {len(final_list)}")
    
    # 4. Upload to Hostinger
    print("\n>>> Iniciando Upload FTP...")
    ftp_host = os.getenv('FTP_HOST')
    ftp_user = os.getenv('FTP_USER')
    ftp_pass = os.getenv('FTP_PASS')
    
    if ftp_host and ftp_user and ftp_pass:
        upload_to_hostinger(DATA_FILE, ftp_host, ftp_user, ftp_pass)
    else:
        print("⚠️ Credenciais FTP não encontradas. Upload pulado.")

    print("\n🏁 EXECUÇÃO CONCLUÍDA!")

if __name__ == "__main__":
    main()
