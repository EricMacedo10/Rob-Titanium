import os
import json
import time
import sys
from datetime import datetime
from dotenv import load_dotenv
from social.core.instagram_client import InstagramClient

load_dotenv()

BASE_DIR       = r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium"
STATE_FILE     = os.path.join(BASE_DIR, "state", "conjunto_active_post.json")
REPLIED_FILE   = os.path.join(BASE_DIR, "state", "conjunto_replied_users.json")

CHECK_INTERVAL = 60
MAX_CYCLES     = 999_999
KEYWORD        = "QUERO"

PUBLIC_REPLY = (
    "Oi! 😍 Link saindo do forno! Acabei de enviar no seu direct! "
    "Dá uma olhadinha lá! 🤖✨ #RoboTitanium"
)

DM_TEMPLATE = """✨ Oi! Aqui é o Robô Titanium! ✨

Vi que você amou o Conjunto Alfaiataria Ombro Único! 😍 Ele é realmente incrível e está com um preço imperdível na Shopee.

🔗 **Link Direto para Compra:**
{product_url}

💡 **Dica de Ouro:**
O preço de R$ 59,99 é por tempo limitado! Verifique se há cupons de frete grátis disponíveis no app da Shopee para economizar ainda mais. 🛍️

Dúvidas? Pode me chamar aqui! 😊

🤖 Robô Titanium — Facilitando seus achados!"""

def load_state():
    if not os.path.exists(STATE_FILE):
        return None
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def load_replied():
    if os.path.exists(REPLIED_FILE):
        with open(REPLIED_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return set(data.get("replied_comment_ids", []))
    return set()

def save_replied(replied_ids: set):
    os.makedirs(os.path.dirname(REPLIED_FILE), exist_ok=True)
    with open(REPLIED_FILE, "w", encoding="utf-8") as f:
        json.dump({"replied_comment_ids": list(replied_ids)}, f, indent=2, ensure_ascii=False)

def contains_keyword(text: str, keyword: str) -> bool:
    import unicodedata
    def normalize(s):
        return unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower()
    return normalize(keyword) in normalize(text)

def log(msg: str):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")

def run_bot():
    ig_token    = os.getenv("IG_ACCESS_TOKEN")
    ig_business = os.getenv("IG_BUSINESS_ID")
    page_id     = os.getenv("PAGE_ID")

    client      = InstagramClient(ig_token, ig_business, page_id=page_id)
    
    replied_ids = load_replied()
    cycle       = 0

    print("=" * 60)
    print("🤖 TITANIUM CONJUNTO BOT — Aguardando Post Ativo")
    print("=" * 60)

    while cycle < MAX_CYCLES:
        cycle += 1
        state = load_state()
        
        if not state:
            log("⏳ Aguardando criação do arquivo de estado (post_id)...")
            time.sleep(30)
            continue
            
        post_id     = state["post_id"]
        product_url = state["product_url"]
        keyword     = state.get("keyword", KEYWORD)

        if cycle == 1 or cycle % 10 == 0:
            log(f"📌 Monitorando Post: {post_id}")

        try:
            comments = client.get_comments(post_id)
            new_count = 0
            for comment in comments:
                comment_id = comment.get("id")
                text       = comment.get("text", "")
                username   = comment.get("username") or comment.get("from", {}).get("username") or "usuário"

                if comment_id in replied_ids: continue
                if not contains_keyword(text, keyword): continue

                log(f"💬 Comentário detectado de @{username}")
                client.post_public_reply(comment_id, PUBLIC_REPLY)
                
                dm_message = DM_TEMPLATE.format(product_url=product_url)
                client.post_private_reply(comment_id, dm_message)

                replied_ids.add(comment_id)
                save_replied(replied_ids)
                new_count += 1
                time.sleep(3)
                
            if new_count > 0:
                log(f"✅ {new_count} novos respondidos.")
        except Exception as e:
            log(f"⚠️  Erro: {e}")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    run_bot()
