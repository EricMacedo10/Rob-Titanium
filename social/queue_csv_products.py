import os
import csv
import json
import time
import requests
import hashlib
import re
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv

load_dotenv()

STATE_FILE = "social/state_csv.json"
CSV_FILE = "BatchProductLinks.csv"
QUEUE_DIR = "social/fila"
SHOPEE_APP_ID = os.getenv("SHOPEE_APP_ID")
SHOPEE_SECRET = os.getenv("SHOPEE_SECRET")

from social.core.image_generator import ImageGenerator

def get_shopee_image_api(keyword):
    if not SHOPEE_APP_ID or not SHOPEE_SECRET: return None
    url = "https://open-api.affiliate.shopee.com.br/graphql"
    timestamp = int(time.time())
    query = "query productOfferV2($keyword: String, $limit: Int) { productOfferV2(keyword: $keyword, limit: $limit) { nodes { imageUrl } } }"
    payload = {"query": query, "variables": {"keyword": keyword, "limit": 1}}
    payload_str = json.dumps(payload, separators=(',', ':'))
    signature = hashlib.sha256(f"{SHOPEE_APP_ID}{timestamp}{payload_str}{SHOPEE_SECRET}".encode('utf-8')).hexdigest()
    headers = {"Content-Type": "application/json", "Authorization": f"SHA256 Credential={SHOPEE_APP_ID}, Signature={signature}, Timestamp={timestamp}"}
    try:
        resp = requests.post(url, headers=headers, data=payload_str, timeout=10)
        nodes = resp.json().get("data", {}).get("productOfferV2", {}).get("nodes", [])
        return nodes[0].get("imageUrl") if nodes else None
    except: return None

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f: return json.load(f)
    return {"last_index": 0}

def save_state(state):
    with open(STATE_FILE, 'w') as f: json.dump(state, f, indent=4)

def run():
    print("[Titanium Elite] Iniciando Parser Customizado para CSV Complexo...")
    state = load_state()
    
    products = []
    try:
        with open(CSV_FILE, mode='r', encoding='utf-8-sig') as f:
            lines = f.readlines()[1:] # Pula cabecalho
            for line in lines:
                # Limpa aspas externas e quebra por virgula
                clean_line = line.strip().strip('"')
                parts = clean_line.split(',')
                if len(parts) >= 8:
                    products.append({
                        "id": parts[0].strip(),
                        "name": parts[1].strip(),
                        "price": parts[2].replace('"', '').strip(),
                        "url": parts[-2].strip(), # Product Link costuma ser o penultimo
                        "offer": parts[-1].strip() # Offer Link o ultimo
                    })
    except Exception as e:
        print(f"Erro Leitura: {e}")
        return

    start_idx = state["last_index"]
    batch_size = 5
    end_idx = min(start_idx + batch_size, len(products))
    
    if start_idx >= len(products):
        print("Ciclo completo. Reiniciando.")
        state["last_index"] = 0
        save_state(state)
        return

    print(f"Processando {start_idx} a {end_idx} de {len(products)}...")
    batch = products[start_idx:end_idx]
    gen = ImageGenerator(assets_path="site/images")
    os.makedirs(QUEUE_DIR, exist_ok=True)
    
    success_count = 0
    for item in batch:
        # Limpeza para busca
        search_q = " ".join(item['name'].split()[:5])
        print(f"Buscando: {search_q}...")
        
        img_url = get_shopee_image_api(search_q)
        
        if not img_url:
            print("Tentando Fallback Scraper...")
            try:
                res = requests.get(item['url'], headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
                m = re.search(r'property="og:image" content="(.*?)"', res.text)
                if m: img_url = m.group(1)
            except: pass

        if img_url:
            base_name = f"shopee_{int(time.time())}_{success_count}"
            path = os.path.join(QUEUE_DIR, f"{base_name}.jpg")
            json_path = os.path.join(QUEUE_DIR, f"{base_name}.json")
            try:
                gen.generate_post(item['name'], item['price'], img_url, "shopee", path)
                with open(json_path, 'w', encoding='utf-8') as mj:
                    json.dump({"title": item['name'], "price": item['price'], "link": item['offer']}, mj, ensure_ascii=False)
                print(f"OK -> {os.path.basename(path)}")
                success_count += 1
            except Exception as e: print(f"Erro: {e}")
        else: print("Imagem nao encontrada.")

    state["last_index"] = end_idx
    save_state(state)
    print(f"Concluido: {success_count} artes prontas na fila.")

if __name__ == "__main__":
    run()
