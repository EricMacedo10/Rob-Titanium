import os
import re
import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Configuration
SITE_INDEX = "site/index.html"
OUTPUT_JSON = "site/admin/affiliate_status.json"
AMAZON_TAG = os.getenv("AMAZON_AFFILIATE_TAG", "guiadodesco00-20")
ML_TAG = "matt_tool=188269638"
SHOPEE_TAG = "utm_source=an_18318830863"

def monitor_affiliate_links():
    print("Dashboard Integrity Audit - Robô Titanium")
    print("="*60)
    
    if not os.path.exists(SITE_INDEX):
        print(f"❌ Error: {SITE_INDEX} not found.")
        return

    with open(SITE_INDEX, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    results = []
    
    # Target elements: cards with onclick="window.open('...') "
    cards = soup.find_all("div", class_="hub-card")
    print(f"--- Analysis: {len(cards)} main links found.")

    for card in cards:
        onclick = card.get("onclick", "")
        if not onclick: continue
        
        # Extract URL from window.open
        match = re.search(r"window\.open\('([^']+)'", onclick)
        if not match: continue
        
        url = match.group(1)
        store = "unknown"
        if "mercadolivre" in url or "mercadolivre" in str(card.get("class")): store = "Mercado Livre"
        elif "amazon" in url or "amazon" in str(card.get("class")): store = "Amazon"
        elif "shopee" in url or "shopee" in str(card.get("class")): store = "Shopee"
        
        title = card.find("h3").text if card.find("h3") else "No Title"
        
        # Check Tag Integrity
        tag_ok = False
        if store == "Amazon" and AMAZON_TAG in url: tag_ok = True
        elif store == "Mercado Livre" and ML_TAG in url: tag_ok = True
        elif store == "Shopee" and SHOPEE_TAG in url: tag_ok = True
        elif store == "unknown": tag_ok = "n/a"
        
        # Health Check (HTTP Status)
        print(f"--- Testing {store}: {title}...")
        status = 0
        try:
            # Robust headers to mimic a real browser
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache"
            }
            
            # Amazon specifically hates HEAD requests and simple bots. 
            # We use GET with stream=True to be lighter but more "human".
            if store == "Amazon":
                response = requests.get(url, timeout=15, allow_redirects=True, headers=headers, stream=True)
            else:
                response = requests.head(url, timeout=10, allow_redirects=True, headers=headers)
                
            status = response.status_code
            
            msg = ""
            # Se ainda der 503 ou 403 na Amazon, vamos considerar "Manual Check Needed" 
            # mas nao marcar como falha total se o link parece integro
            if store == "Amazon" and status in [503, 403]:
                msg = "Anti-bot da Amazon detectado. Verifique o link manualmente no navegador."
                print(f"   ℹ️ {msg}")
                
        except Exception as e:
            print(f"   ⚠️ Connection Error on {url}: {e}")
            status = "Error"
            msg = f"Connection Error: {e}"
            
        results.append({
            "store": store,
            "title": title,
            "url": url,
            "tag_integrity": tag_ok,
            "http_status": status,
            "message": msg,
            "last_check": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })

    # Save to JSON for future server use
    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as out:
        json.dump(results, out, indent=4, ensure_ascii=False)
        
    # Save to JS for local file:/// use (Bypasses CORS)
    OUTPUT_JS = OUTPUT_JSON.replace(".json", ".js")
    with open(OUTPUT_JS, "w", encoding="utf-8") as out:
        out.write(f"const affiliate_audit_data = {json.dumps(results, indent=4, ensure_ascii=False)};")
        
    print("="*60)
    print(f"✅ Audit Complete. Dashboard updated: {OUTPUT_JSON}")

if __name__ == "__main__":
    monitor_affiliate_links()
