import json
import time
import os
import random
from dotenv import load_dotenv
load_dotenv()

from core.settings import TARGETS
from core.arbitrator import ArbitroDePreco
from scraper.engines.ml_trends import update_site_with_trends
from infra.upload_logic import upload_to_hostinger
from core.phrases import generate_dynamic_phrases

DATA_FILE = 'site/data.json'

def _format_product_for_site(prod, analise, index, category):
    """Auxiliar para formatar produto para o data.json"""
    return {
        "id": f"prod_{int(time.time())}_{index}_{random.randint(0, 999)}",
        "title": prod.get('titulo', prod.get('nome', 'Sem Título')), 
        "price": prod['preco'],
        "old_price": prod['preco'] * 1.25, 
        "discount": 20,
        "store": prod['loja'],
        "category": category,
        "image": prod.get('imagem', prod.get('image', '')), 
        "link": prod.get('link', prod.get('link_afiliado', '')),
        "reason": analise.get('motivo', 'Melhor oferta encontrada')
    }

def update_manual_targets():
    """
    Scrape products defined in TARGETS list (settings.py)
    """
    print("\n" + "="*60)
    print("ATUALIZANDO TARGETS DEFINIDOS")
    print("="*60)
    
    arbitro = ArbitroDePreco()
    new_products = []
    
    # --- NOVO: Embaralhar e selecionar targets aleatórios ---
    max_targets_per_run = 15
    selected_targets = random.sample(TARGETS, min(len(TARGETS), max_targets_per_run))
    print(f"\n🎲 Sorteando {len(selected_targets)} termos de um total de {len(TARGETS)} cadastrados...")
    # --------------------------------------------------------
    
    for i, target in enumerate(selected_targets):
        term = target['term']
        store_target = target.get('store', 'all')
        print(f"\n--- [{i+1}/{len(selected_targets)}] Buscando: {term} (Loja: {store_target}) ---")
        
        try:
            # Respect store targeting
            # --- Mercado Livre: [REMOVIDO POR SOLICITAÇÃO - FOCO 50/50 AMAZON/SHOPEE] ---
            if store_target == 'mercadolivre':
                continue # Pula ML
            elif store_target == 'lomadee':
                from scraper.engines.lomadee_api import search_lomadee
                res = search_lomadee(term, limit=5)
                if res and len(res) > 0:
                    for prod in res:
                        if prod and prod.get('preco') and prod.get('preco') != float('inf'):
                            analise = {"motivo": f"Oferta Direta Lomadee para {term}"}
                            formatted = _format_product_for_site(prod, analise, i, target.get('category', 'all'))
                            new_products.append(formatted)
                    continue # Skip general processing for this target
            elif store_target == 'shopee':
                import asyncio
                from scraper.engines.shopee_affiliate import search_shopee
                res = search_shopee(term, limit=5)
                if res and len(res) > 0:
                    for prod in res:
                        if prod and prod.get('preco') and prod.get('preco') != float('inf'):
                            analise = {"motivo": f"Oferta Direta Shopee para {term}"}
                            formatted = _format_product_for_site(prod, analise, i, target.get('category', 'all'))
                            new_products.append(formatted)
                    continue # Skip general processing for this target
            elif store_target == 'amazon':
                # Use Arbitro but specifically for Amazon (it handles the loop)
                import asyncio
                res = asyncio.run(arbitro.buscar_amazon(term))
                prod = res if res and res.get('disponivel') else None
                analise = {"motivo": f"Oferta Direta Amazon para {term}"}
            else:
                # DEFAULT: Cross-store arbitration (IA chooses best)
                resultado = arbitro.processar_pedido(term)
                prod = resultado.get('melhor_produto') if resultado else None
                analise = resultado.get('analise_ia', {}) if resultado else {}
            
            if prod and prod.get('preco') and prod.get('preco') != float('inf'):
                formatted = _format_product_for_site(prod, analise, i, target.get('category', 'geral'))
                new_products.append(formatted)
                print(f"✅ Encontrado: {formatted['title'][:40]}... (R$ {formatted['price']})")
            else:
                print(f"⚠️ Nenhum produto encontrado para {term}")
                
        except Exception as e:
            print(f"❌ Erro ao buscar {term}: {e}")
            
        # Delay anti-ban
        time.sleep(random.uniform(2, 5))
        
    return new_products

def main():
    print("🚀 INICIANDO ATUALIZAÇÃO AUTOMÁTICA DE OFERTAS")
    
    # Ensure site directory exists
    os.makedirs('site', exist_ok=True)
    
    # 1. Update ML Trends
    print(">>> Executando ML Trends...")
    print("⚠️ ML Trends Temporariamente Desativado (Aguardando Proxy)")
    # try:
    #     # update_site_with_trends reads limits internally and updates data.json
    #     # We perform it first so we have a base
    #     update_site_with_trends(DATA_FILE)
    # except Exception as e:
    #     print(f"❌ Falha ao atualizar trends: {e}")
        
    # 2. Update Manual Targets
    print("\n>>> Executando Targets Manuais...")
    fixed_products = []
    try:
        fixed_products = update_manual_targets()
    except Exception as e:
        print(f"❌ Erro fatal durante a busca de targets: {e}")
    
    # 3. Merge Strategies
    final_list = []
    
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
                
        # 🛡️ TITANIUM BALANCER (v1.4)
        # Garante 50% Shopee e 50% Amazon no catálogo final
        shopee_deals = [p for p in final_list if p.get('store', '').lower() == 'shopee']
        amazon_deals = [p for p in final_list if p.get('store', '').lower() == 'amazon']
        
        print(f"\n⚖️ Balanceando Catálogo (Shopee: {len(shopee_deals)} / Amazon: {len(amazon_deals)})")
        
        # Define o tamanho de cada fatia (ex: 55 total -> 27 de cada)
        target_per_store = 27 
        shopee_balanced = shopee_deals[:target_per_store]
        amazon_balanced = amazon_deals[:target_per_store]
        
        # Intercala os produtos para uma vitrine variada
        balanced_list = []
        for i in range(max(len(shopee_balanced), len(amazon_balanced))):
            if i < len(shopee_balanced): balanced_list.append(shopee_balanced[i])
            if i < len(amazon_balanced): balanced_list.append(amazon_balanced[i])
            
        final_list = balanced_list
        print(f"✅ Catálogo final balanceado com {len(final_list)} produtos.")
        
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(final_list, f, ensure_ascii=False, indent=4)
            
        print(f"✅ {DATA_FILE} atualizado com sucesso!")
        print("\n>>> Gerando Frases Dinâmicas...")
        generate_dynamic_phrases(final_list)
        # --------------------------------------

    # ----------------------------------------------------------------------
    # 4. Fail-Safe & Integrity Check
    # ----------------------------------------------------------------------
    if not final_list:
        print("\n❌ ERRO CRÍTICO: Nenhum produto encontrado (Lista Vazia)!")
        print("   >>> BLOQUEIO DE UPLOAD ATIVADO: Preservando site funcional.")
        print("   Isso pode indicar falha geral nas APIs ou bloqueio de IP.")
        import sys
        sys.exit(1)

    # 5. Upload to Hostinger (Only if we have data)
    print("\n>>> Iniciando Upload FTP...")
    ftp_host = os.getenv('FTP_HOST')
    ftp_user = os.getenv('FTP_USER')
    ftp_pass = os.getenv('FTP_PASS')
    
    print(f"   DEBUG: Host={'Configurado' if ftp_host else 'MISSING'}, User={'Configurado' if ftp_user else 'MISSING'}")

    if ftp_host and ftp_user and ftp_pass:
        # 🛡️ ISOLAMENTO POR AMBIENTE: Sincronizar Arquivos de Dados
        # upload_to_hostinger já roteia para /teste/ automaticamente se ENV_MODE=STAGING
        
        # Upload data.json (Produtos)
        upload_to_hostinger(DATA_FILE, ftp_host, ftp_user, ftp_pass, remote_path='data.json')
        
        # Upload notifications.json (Frases)
        notif_file = 'site/notifications.json'
        if os.path.exists(notif_file):
             upload_to_hostinger(notif_file, ftp_host, ftp_user, ftp_pass, remote_path='notifications.json')

        # Sincronizar Assets Estruturais (separados por ambiente)

        if env_mode == 'STAGING':
            # ⚠️ STAGING: envia apenas para /teste/ — nunca toca em produção
            # index_staging.html é enviado duas vezes: como si mesmo e como index.html
            # (index.html é o default do subdomínio teste.guiadodesconto.com.br)
            assets = [
                ('site/js/app.js',           'js/app.js'),
                ('site/css/style.css',       'css/style.css'),
                ('site/categoria.html',      'categoria.html'),
                ('site/css/categoria.css',   'css/categoria.css'),
                ('site/js/app_categoria.js', 'js/app_categoria.js'),
                ('site/index.html',          'index_staging.html'),
                ('site/index.html',          'index.html'),   # Default page do subdomínio /teste/
            ]
        else:
            # 🛡️ PRODUCTION BLINDAGEM: Nunca envia assets estruturais automaticamente.
            # No modo produção, o robô atualiza APENAS o JSON de ofertas (data.json).
            # Mudanças de layout (HTML/JS/CSS) devem ser feitas via force_asset_upload.py
            assets = []

        asset_pairs = assets if isinstance(assets, list) else assets.items()
        for local, remote in asset_pairs:
            if os.path.exists(local):
                print(f"\n>>> Sincronizando Asset ({env_mode}): {remote}")
                upload_to_hostinger(local, ftp_host, ftp_user, ftp_pass, remote_path=remote)
            else:
                print(f"⚠️ Asset local não encontrado, pulado: {local}")
        
        print("\n✅ SITE ATUALIZADO COM SUCESSO!")
    else:
        print("⚠️ Credenciais FTP não encontradas. Upload pulado.")

    print("\n🏁 EXECUÇÃO CONCLUÍDA com SUCESSO!")

if __name__ == "__main__":
    main()
