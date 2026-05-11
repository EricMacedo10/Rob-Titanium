import os
import csv
import json
import time
import requests
import hashlib
import re
import random
from dotenv import load_dotenv

load_dotenv()

# Configurações de Caminho
STATE_FILE = "social/state_csv.json"
CSV_FILE = "BatchProductLinks.csv"
QUEUE_DIR = "social/fila"
POSTED_DIR = "social/postados"
SHOPEE_APP_ID = os.getenv("SHOPEE_APP_ID")
SHOPEE_SECRET = os.getenv("SHOPEE_SECRET")

from social.core.image_generator import ImageGenerator
from scraper.datafeed_shopee import get_datafeed_products

def get_posted_titles():
    """Le titulos ja postados e na fila para evitar duplicidade no feed."""
    titles = set()
    
    # 1. Verificar o que já foi postado
    if os.path.exists(POSTED_DIR):
        for f in os.listdir(POSTED_DIR):
            if f.endswith('.json'):
                try:
                    with open(os.path.join(POSTED_DIR, f), 'r', encoding='utf-8') as j:
                        data = json.load(j)
                        if 'title' in data:
                            titles.add(data['title'].lower().strip())
                except: continue
                
    # 2. Verificar o que já está na fila esperando postagem
    if os.path.exists(QUEUE_DIR):
        for f in os.listdir(QUEUE_DIR):
            if f.endswith('.json'):
                try:
                    with open(os.path.join(QUEUE_DIR, f), 'r', encoding='utf-8') as j:
                        data = json.load(j)
                        if 'title' in data:
                            titles.add(data['title'].lower().strip())
                except: continue
                
    return titles

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f: return json.load(f)
        except: pass
    return {"last_index": 0, "source": "csv"}

def save_state(state):
    with open(STATE_FILE, 'w') as f: json.dump(state, f, indent=4)

def run():
    print(f"\n{'='*60}")
    print("TITANIUM SOCIAL: GERACAO DE FILA (MODO 100K DATAFEED)")
    print(f"{'='*60}")
    
    state = load_state()
    posted_titles = get_posted_titles()
    batch_size = 5 
    
    products = []
    source_used = "datafeed"

    # 1. TENTAR DATAFEED 100K
    try:
        print("[Datafeed] Buscando melhores achados de INVERNO no pool de 100K...")
        raw_products = get_datafeed_products(max_items=2000)
        
        winter_keywords = ["jaqueta", "casaco", "moletom", "cardigan", "sobretudo", "parka", "tricot", "poncho", "cachecol", "bota", "inverno", "frio", "manga longa", "gola alta", "peluciada", "peluciado"]
        
        for p in raw_products:
            title_lower = p['titulo'].lower().strip()
            
            # FILTRO DE INVERNO EXCLUSIVO PARA O INSTAGRAM
            if not any(wk in title_lower for wk in winter_keywords):
                continue
                
            if title_lower not in posted_titles:
                products.append({
                    "id": p['id_interno'],
                    "name": p['titulo'],
                    "price": str(p['preco']),
                    "url": p['url_produto'],
                    "offer": p['link_afiliado'],
                    "image_api": None 
                })
        
        if not products:
            print("[Aviso] Nenhum produto novo no Datafeed. Recorrendo ao CSV.")
            source_used = "csv"
    except Exception as e:
        print(f"[Erro Datafeed] {e}. Recorrendo ao CSV.")
        source_used = "csv"

    # 2. FALLBACK CSV
    if source_used == "csv":
        print("[CSV] Lendo Curadoria BatchProductLinks.csv...")
        try:
            with open(CSV_FILE, mode='r', encoding='utf-8-sig') as f:
                lines = f.readlines()[1:] 
                csv_pool = []
                for line in lines:
                    clean_line = line.strip()
                    if not clean_line: continue
                    if clean_line.startswith('"') and clean_line.endswith('"'):
                        clean_line = clean_line[1:-1]
                    clean_line = clean_line.replace('""', '"')
                    parts = next(csv.reader([clean_line]))
                    if len(parts) >= 8:
                        title = parts[1].strip()
                        if title.lower().strip() not in posted_titles:
                            csv_pool.append({
                                "id": parts[0].strip(),
                                "name": title,
                                "price": parts[2].strip(),
                                "url": parts[-2].strip(),
                                "offer": parts[-1].strip()
                            })
                
                start_idx = state.get("last_index", 0)
                products = csv_pool[start_idx:]
                if not products: 
                    print("[CSV] Fim do arquivo. Reiniciando.")
                    state["last_index"] = 0
                    products = csv_pool
        except Exception as e:
            print(f"[Erro CSV] {e}")
            return

    # 3. PROCESSAMENTO DO BATCH
    batch = products[:batch_size]
    print(f"Selecionados {len(batch)} itens via {source_used.upper()} para processamento.")
    
    gen = ImageGenerator(assets_path="site/images")
    os.makedirs(QUEUE_DIR, exist_ok=True)
    
    success_count = 0
    for item in batch:
        img_url = None
        search_q = " ".join(item['name'].split()[:6])
        print(f"Buscando imagem Elite para: {search_q}...")
        
        from core.shopee_api import get_shopee_image_api
        try:
            img_url = get_shopee_image_api(search_q)
        except: pass

        if not img_url:
            print("   -> Usando Scraper de imagem (Fallback)...")
            try:
                res = requests.get(item['url'], headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
                m = re.search(r'property="og:image" content="(.*?)"', res.text)
                if m: img_url = m.group(1)
            except: pass

        if img_url:
            base_name = f"shopee_{int(time.time())}_{success_count}"
            path = os.path.join(QUEUE_DIR, f"{base_name}.jpg")
            json_path = os.path.join(QUEUE_DIR, f"{base_name}.json")
            
            try:
                final_link = item['offer']
                if source_used == "csv" or "utm_source" not in final_link:
                    from core.link_builder import build_affiliate_link
                    final_link = build_affiliate_link(item['offer'], "shopee")
                
                gen.generate_premium_reel_frame(item['name'], item['price'], img_url, "shopee", path)
                
                with open(json_path, 'w', encoding='utf-8') as mj:
                    json.dump({
                        "id": item['id'],
                        "title": item['name'], 
                        "price": item['price'], 
                        "link": final_link,
                        "source": source_used
                    }, mj, ensure_ascii=False)
                
                print(f"OK -> {os.path.basename(path)}")
                success_count += 1
            except Exception as e:
                print(f"Erro na geracao: {e}")
        else:
            print("Imagem nao encontrada. Pulando item.")

    if source_used == "csv":
        state["last_index"] = state.get("last_index", 0) + batch_size
    state["source"] = source_used
    save_state(state)
    
    print(f"\nCiclo concluido: {success_count} novas artes na fila social.")

if __name__ == "__main__":
    run()
