import json
import time
import os
import random
from dotenv import load_dotenv
load_dotenv()

from core.settings import TARGETS
from core.arbitrator import ArbitroDePreco
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
        print(f"\n--- [{i+1}/{len(selected_targets)}] Minerando Shopee: {term} ---")
        
        try:
            # Foco Exclusivo: Shopee API Titanium
            from scraper.engines.shopee_affiliate import search_shopee
            res = search_shopee(term, limit=10) # Aumentado para 10 para compensar outras lojas

            if res and len(res) > 0:
                for prod in res:
                    if prod and prod.get('preco') and prod.get('preco') != float('inf'):
                        analise = {"motivo": f"Curadoria Titanium: {term}"}
                        formatted = _format_product_for_site(prod, analise, i, target.get('category', 'all'))
                        new_products.append(formatted)
                print(f"✅ Shopee Encontrou {len(res)} itens para {term}")
            else:
                print(f"⚠️ Nenhum produto Shopee para {term}")
                
        except Exception as e:
            print(f"❌ Erro ao buscar {term}: {e}")
            
        # Delay anti-ban (mais curto pois a API da Shopee é robusta)
        time.sleep(random.uniform(1, 2))
        
    return new_products

def main():
    print("🚀 INICIANDO ATUALIZAÇÃO AUTOMÁTICA: BOUTIQUE TITANIUM (SHOPEE EXCLUSIVE)")
    
    # Ensure site directory exists
    os.makedirs('site', exist_ok=True)
    
    # 1. Update ML Trends (DESATIVADO - BOUTIQUE SHOPEE)
    print(">>> Status: Mercado Livre Trends Desativado (Boutique Shopee Exclusive)")
        
    # 2. Update Manual Targets
    print("\n>>> Executando Minerador de Alta Precisão (Shopee)...")
    fixed_products = []
    try:
        fixed_products = update_manual_targets()
    except Exception as e:
        print(f"❌ Erro fatal durante a busca de targets: {e}")
    
    # 3. Merge Strategies
    final_list = []
    
    if fixed_products:
        print(f"\nConsolidando {len(fixed_products)} novas ofertas extraídas...")
        
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                current_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            current_data = []
            
        # Strategy: 
        # - Keep recent Shopee verified products
        # - Discard old products to refresh the boutique
        
        # Filtramos para manter apenas Shopee se houver resquícios
        current_shopee = [p for p in current_data if p.get('store', '').lower() == 'shopee']
        
        # Create set of normalized titles for fast lookup
        seen_titles = {str(p.get('title', '')).lower().strip() for p in current_shopee}
        
        unique_new = []
        for p in fixed_products:
            p_title = str(p.get('title', '')).lower().strip()
            # Validate image and title
            if not p.get('image') or not p_title:
                continue

            if p_title not in seen_titles:
                unique_new.append(p)
                seen_titles.add(p_title) 
                
        final_list = current_shopee[:12] + unique_new # Mantém 12 antigos + novos
        
        # Final Filtering & Sanitation
        sanitized_list = []
        final_seen = set()
        
        for p in final_list:
            # 1. Validation Logic
            title = p.get('title')
            price = p.get('price')
            link = p.get('link') or p.get('link_afiliado')
            image = p.get('image') or p.get('imagem')
            
            # Skip INVALID products
            if not title: continue
            if not price or price == float('inf') or price <= 0: continue
            if not link or "http" not in link: continue
            if not image or "http" not in image: continue
            
            # 2. Duplicate Prevention
            norm_title = title.lower().strip()
            if norm_title in final_seen: continue
            final_seen.add(norm_title)
            
            # 3. Standardize Keys & Forced Store Name
            p['image'] = image 
            p['link'] = link   
            p['store'] = 'Shopee'
            
            sanitized_list.append(p)
            
        final_list = sanitized_list

        print(f"\n✨ SUCESSO! Catálogo Titanium 100% Shopee com {len(final_list)} produtos.")
        
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
    env_mode = os.getenv('ENV_MODE', 'PRODUCTION')
    
    print(f"   DEBUG: Host={'Configurado' if ftp_host else 'MISSING'}, User={'Configurado' if ftp_user else 'MISSING'}, Env={env_mode}")

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
