import os
import json
import time
import sys
from datetime import datetime
from dotenv import load_dotenv
from social.core.instagram_client import InstagramClient

load_dotenv()

BASE_DIR       = r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium"
STATE_FILE     = os.path.join(BASE_DIR, "state", "blazer_active_post.json")
REPLIED_FILE   = os.path.join(BASE_DIR, "state", "blazer_replied_users.json")

CHECK_INTERVAL = 60
MAX_CYCLES     = 999_999
KEYWORD        = "QUERO"

PUBLIC_REPLY = (
    "Oi! 😍 Vi que você quer! Já tô mandando o link no seu direct agora! "
    "Verifica o seu inbox! 🤖✨ #TitaniumBot"
)

DM_TEMPLATE = """Oi! 🎉 Aqui é o Robô Titanium!

Vi que você comentou "QUERO" no nosso post do Blazer Feminino Alongado! 🖤✨

🔗 Aqui está o link exclusivo com o melhor preço na Shopee:
{product_url}

💡 Dicas rápidas:
• Aproveite agora o preço promocional de R$ 108,30!
• O frete pode ser grátis para o seu CEP — confira!
• Dúvidas? Responda aqui no direct 😊

🤖 Robô Titanium — Seu assistente de achados incríveis!"""

def load_state():
    if not os.path.exists(STATE_FILE):
        print(f"❌ Arquivo de estado não encontrado: {STATE_FILE}")
        sys.exit(1)
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

    client = InstagramClient(ig_token, ig_business, page_id=page_id)
    state       = load_state()
    post_id     = state["post_id"]
    product_url = state["product_url"]
    keyword     = state.get("keyword", KEYWORD)

    print("=" * 60)
    print("🤖 TITANIUM BLAZER BOT — Monitoramento Ativo")
    print("=" * 60)
    print(f"📌 Post ID    : {post_id}")
    print(f"🔑 Palavra-chave: '{keyword}'")
    print(f"🔗 Link afiliado: {product_url}")
    print("=" * 60)

    replied_ids = load_replied()
    dm_message  = DM_TEMPLATE.format(product_url=product_url)
    cycle       = 0

    while cycle < MAX_CYCLES:
        cycle += 1
        log(f"🔎 Ciclo #{cycle}...")
        try:
            comments = client.get_comments(post_id)
            new_count = 0
            for comment in comments:
                comment_id = comment.get("id")
                text       = comment.get("text", "")
                username   = comment.get("username") or comment.get("from", {}).get("username", "usuário")

                if comment_id in replied_ids: continue
                if not contains_keyword(text, keyword): continue

                log(f"💬 Comentário detectado de @{username}")
                client.post_public_reply(comment_id, PUBLIC_REPLY)
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
