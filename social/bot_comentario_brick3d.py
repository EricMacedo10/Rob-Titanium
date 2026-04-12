"""
bot_comentario_brick3d.py
=========================
Robô de monitoramento de comentários para o post do Kit Brick 3D.

Funcionamento:
  1. Lê o estado do post ativo em state/brick3d_active_post.json
  2. Verifica novos comentários no post a cada 60 segundos
  3. Se detectar a palavra-chave ("QUERO"), faz duas ações:
       a) Resposta pública amigável no comentário
       b) DM privado com o link afiliado do produto
  4. Mantém registro de quem já recebeu DM (evita duplicatas)

Uso:
  python bot_comentario_brick3d.py
  (Deixe rodando em segundo plano enquanto o post estiver ativo)
"""

import os
import json
import time
import sys
from datetime import datetime
from dotenv import load_dotenv
from social.core.instagram_client import InstagramClient

load_dotenv()

# ─────────────────────────────────────────────
#  CONFIGURAÇÕES DO BOT
# ─────────────────────────────────────────────
BASE_DIR       = r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium"
STATE_FILE     = os.path.join(BASE_DIR, "state", "brick3d_active_post.json")
REPLIED_FILE   = os.path.join(BASE_DIR, "state", "brick3d_replied_users.json")

CHECK_INTERVAL = 60        # segundos entre cada verificação
MAX_CYCLES     = 999_999   # Rodar indefinidamente (Ctrl+C para parar)

KEYWORD        = "QUERO"   # Case-insensitive

# Mensagem de resposta pública (comentário)
PUBLIC_REPLY = (
    "Oi! 😍 Vi que você quer! Já tô mandando o link no seu direct agora! "
    "Verifica o seu inbox! 🤖✨ #TitaniumBot"
)

# Mensagem privada (DM) — inclui o link afiliado
DM_TEMPLATE = """Oi! 🎉 Aqui é o Robô Titanium!

Vi que você comentou "QUERO" no nosso post do Kit 52 Placas 3D Brick Pedra Flexível! 🧱✨

🔗 Aqui está o link exclusivo com o melhor preço na Shopee:
{product_url}

💡 Dicas rápidas:
• Aproveite agora antes de esgotar o estoque!
• O frete pode ser grátis para o seu CEP — confira!
• Dúvidas? Responda aqui no direct 😊

🤖 Robô Titanium — Seu assistente de achados incríveis!"""

# ─────────────────────────────────────────────
#  FUNÇÕES AUXILIARES
# ─────────────────────────────────────────────
def load_state():
    """Carrega o estado do post ativo."""
    if not os.path.exists(STATE_FILE):
        print(f"❌ Arquivo de estado não encontrado: {STATE_FILE}")
        print("   Execute primeiro: python social/post_brick3d_carousel.py")
        sys.exit(1)
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_replied():
    """Carrega o conjunto de usuários que já receberam DM."""
    if os.path.exists(REPLIED_FILE):
        with open(REPLIED_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return set(data.get("replied_comment_ids", []))
    return set()


def save_replied(replied_ids: set):
    """Persiste o conjunto de comentários já respondidos."""
    os.makedirs(os.path.dirname(REPLIED_FILE), exist_ok=True)
    with open(REPLIED_FILE, "w", encoding="utf-8") as f:
        json.dump({"replied_comment_ids": list(replied_ids)}, f, indent=2, ensure_ascii=False)


def contains_keyword(text: str, keyword: str) -> bool:
    """Verifica se o texto contém a palavra-chave (case-insensitive, sem acento)."""
    import unicodedata
    def normalize(s):
        return unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower()
    return normalize(keyword) in normalize(text)


def log(msg: str):
    """Log com timestamp."""
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")


# ─────────────────────────────────────────────
#  LOOP PRINCIPAL DO BOT
# ─────────────────────────────────────────────
def run_bot():
    ig_token    = os.getenv("IG_ACCESS_TOKEN")
    ig_business = os.getenv("IG_BUSINESS_ID")
    page_id     = os.getenv("PAGE_ID")

    if not ig_token or not ig_business:
        print("❌ Credenciais do Instagram não encontradas no .env")
        sys.exit(1)

    # Inicializa cliente
    client = InstagramClient(ig_token, ig_business, page_id=page_id)

    # Carrega estado do post
    state       = load_state()
    post_id     = state["post_id"]
    product_url = state["product_url"]
    keyword     = state.get("keyword", KEYWORD)

    print("=" * 60)
    print("🤖 TITANIUM BOT — Monitoramento de Comentários")
    print("=" * 60)
    print(f"📌 Post ID    : {post_id}")
    print(f"🔑 Palavra-chave: '{keyword}'")
    print(f"🔗 Link afiliado: {product_url}")
    print(f"⏱  Intervalo   : {CHECK_INTERVAL}s")
    print("=" * 60)
    print("Pressione Ctrl+C para parar.\n")

    replied_ids = load_replied()
    dm_message  = DM_TEMPLATE.format(product_url=product_url)
    cycle       = 0

    while cycle < MAX_CYCLES:
        cycle += 1
        log(f"🔎 Ciclo #{cycle} — Buscando comentários no post {post_id}...")

        try:
            comments = client.get_comments(post_id)
        except Exception as e:
            log(f"⚠️  Erro ao buscar comentários: {e}")
            time.sleep(CHECK_INTERVAL)
            continue

        new_count = 0
        for comment in comments:
            comment_id = comment.get("id")
            text       = comment.get("text", "")
            username   = comment.get("username") or comment.get("from", {}).get("username", "usuário")

            # Já respondeu esse comentário?
            if comment_id in replied_ids:
                continue

            # Tem a palavra-chave?
            if not contains_keyword(text, keyword):
                continue

            log(f"💬 Comentário detectado de @{username}: \"{text}\"")

            # ── Resposta pública ──────────────────────────────────────
            log(f"   → Enviando resposta pública...")
            try:
                pub_result = client.post_public_reply(comment_id, PUBLIC_REPLY)
                if "id" in pub_result:
                    log(f"   ✅ Resposta pública enviada (ID: {pub_result['id']})")
                else:
                    log(f"   ⚠️  Resposta pública: {pub_result}")
            except Exception as e:
                log(f"   ❌ Erro na resposta pública: {e}")

            # ── DM privado ────────────────────────────────────────────
            log(f"   → Enviando DM privado para @{username}...")
            try:
                dm_result = client.post_private_reply(comment_id, dm_message)
                if "message_id" in dm_result or "recipient_id" in dm_result:
                    log(f"   ✅ DM enviada com sucesso!")
                else:
                    log(f"   ⚠️  DM resultado: {dm_result}")
            except Exception as e:
                log(f"   ❌ Erro no envio de DM: {e}")

            # Marca como respondido independente de falhas parciais
            replied_ids.add(comment_id)
            save_replied(replied_ids)
            new_count += 1

            # Pausa entre ações para evitar rate-limit
            time.sleep(3)

        if new_count == 0:
            log(f"   Nenhum novo comentário com '{keyword}'. Total já respondidos: {len(replied_ids)}")
        else:
            log(f"   ✅ {new_count} novo(s) comentário(s) respondido(s) neste ciclo.")

        log(f"   ⏳ Aguardando {CHECK_INTERVAL}s para o próximo ciclo...\n")
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    try:
        run_bot()
    except KeyboardInterrupt:
        print("\n\n🛑 Bot encerrado pelo usuário. Até logo! 🤖")
