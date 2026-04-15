import os
import csv
import json
import time
import requests
import hashlib
from dotenv import load_dotenv

load_dotenv()

CSV_FILE = "BatchProductLinks.csv"
OUTPUT_JSON = "site/specialist.json"
SHOPEE_APP_ID = os.getenv("SHOPEE_APP_ID")
SHOPEE_SECRET = os.getenv("SHOPEE_SECRET")

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

def build_specialist_collection():
    print("[Titanium Curator] Iniciando: Gerando Selecao da Especialista...")
    
    products = []
    try:
        with open(CSV_FILE, mode='r', encoding='utf-8-sig') as f:
            lines = f.readlines()[1:] # Pula cabeçalho
            for line in lines:
                clean_line = line.strip()
                if not clean_line: continue
                if clean_line.startswith('"') and clean_line.endswith('"'):
                    clean_line = clean_line[1:-1]
                clean_line = clean_line.replace('""', '"')
                
                parts = next(csv.reader([clean_line]))
                
                if len(parts) >= 8:
                    
                    price_str = parts[2].strip()
                    try:
                        price = float(price_str.replace('"', '').replace('.', '').replace(',', '.'))
                    except:
                        price = 99.99
                        
                    products.append({
                        "id_interno": parts[0].strip(),
                        "titulo": parts[1].strip(),
                        "preco": price,
                        "url_produto": parts[-2].strip(), 
                        "link_afiliado": parts[-1].strip(),
                        "desconto": 25, # Desconto fixo simulado para a curadoria
                        "loja": "Shopee"
                    })
    except Exception as e:
        print(f"Erro Leitura CSV: {e}")
        return

    import random
    # Roleta Premium: Seleciona 24 achados aleatórios do universo do CSV
    if len(products) > 24:
        top_picks = random.sample(products, 24)
    else:
        top_picks = products # Fallback de proteção
        
    curated_data = []

    print(f"[Curator] Processando {len(top_picks)} itens para a vitrine Platinum...")

    for item in top_picks:
        search_q = " ".join(item['titulo'].split()[:5])
        img_url = get_shopee_image_api(search_q)
        
        # Fallback de imagem genérica caso falhe (para não quebrar a vitrine)
        if not img_url:
            img_url = "https://guiadodesconto.com.br/images/fashion-hero.png"

        from core.link_builder import build_affiliate_link
        final_link = build_affiliate_link(item['link_afiliado'], "shopee")

        curated_data.append({
            "id": f"specialist_{item['id_interno']}",
            "title": item['titulo'],
            "price": item['preco'],
            "old_price": item['preco'] * 1.25, # Cria um preço antigo cenográfico
            "discount": item['desconto'],
            "image": img_url,
            "link": final_link,
            "store": item['loja'],
            "category": "Premium"
        })
        print(f"Adicionado: {item['titulo'][:30]}...")
        time.sleep(0.5) # Pausa para não estourar rate limit da API

    os.makedirs("site", exist_ok=True)
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(curated_data, f, ensure_ascii=False, indent=4)
        
    print(f"SUCESSO! Vitrine gerada: {OUTPUT_JSON} com {len(curated_data)} produtos.")

if __name__ == "__main__":
    build_specialist_collection()
