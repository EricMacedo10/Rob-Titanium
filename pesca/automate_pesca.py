"""
Pesca Titanium — Script Principal de Automação
==============================================
Robô completamente independente do bot de moda Titanium.
Publica Reels + Stories na conta @pescatitanium.

Variáveis de ambiente (todas prefixadas com PESCA_):
  PESCA_IG_ACCESS_TOKEN   → Token de longa duração da Pesca Titanium
  PESCA_IG_BUSINESS_ID    → ID do negócio IG da Pesca Titanium
  PESCA_PAGE_ID           → ID da Página do Facebook da Pesca Titanium
  PESCA_IMGBB_API_KEY     → Chave do ImgBB / Tmpfiles para CDN
  PESCA_SHOPEE_DATAFEED_URLS → URLs do feed CSV de produtos de pesca

Ativado pelos workflows:
  .github/workflows/pesca_reels_stories_auto.yml
  .github/workflows/pesca_social_auto.yml
"""

import os
import json
import time
import uuid
import sys

from dotenv import load_dotenv

# ── Garante encoding UTF-8 no runner do GitHub Actions ──────────────────────
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# ── Adiciona raiz do projeto ao path ────────────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

load_dotenv()

# ── Diretórios de estado exclusivos da Pesca ────────────────────────────────
BASE_DIR    = os.path.dirname(__file__)
QUEUE_DIR   = os.path.join(BASE_DIR, "fila")
POSTED_DIR  = os.path.join(BASE_DIR, "postados")
OFERTAS_PATH = os.path.join(BASE_DIR, "ofertas_pesca.json")

os.makedirs(QUEUE_DIR,  exist_ok=True)
os.makedirs(POSTED_DIR, exist_ok=True)

# ── Lock file separado do bot de moda (nunca conflita) ──────────────────────
LOCK_FILE = os.path.join(
    os.path.dirname(__file__), "..", "state", "pesca_post.lock"
)
LOCK_FILE = os.path.abspath(LOCK_FILE)

# ── Hashtags do nicho de pesca ───────────────────────────────────────────────
HASHTAGS_PESCA = (
    "#PescaTitanium #PescaEsportiva #PescaBrasil "
    "#CarretilhaSHIMANO #VaraDePesca #IscaArtificial "
    "#PescadorBrasileiro #TudoDePesca #PescaOnline "
    "#AcessoriosDePesca #PescaEmFamilia #FishingBrasil"
)


# ────────────────────────────────────────────────────────────────────────────
# Helpers
# ────────────────────────────────────────────────────────────────────────────

def _acquire_lock() -> bool:
    """Adquire o lock de postagem. Retorna False se já houver uma em andamento."""
    if os.path.exists(LOCK_FILE):
        age = time.time() - os.path.getmtime(LOCK_FILE)
        if age > 600:  # Lock obsoleto (>10 min) — remove e continua
            print(f"⚠️  Lock obsoleto ({age:.0f}s). Removendo...")
            os.remove(LOCK_FILE)
        else:
            print(f"🔒 BLOQUEADO: Já existe postagem PESCA em andamento! ({age:.0f}s)")
            return False

    os.makedirs(os.path.dirname(LOCK_FILE), exist_ok=True)
    with open(LOCK_FILE, "w") as f:
        f.write(str(time.time()))
    return True


def _release_lock():
    """Libera o lock de postagem."""
    if os.path.exists(LOCK_FILE):
        try:
            os.remove(LOCK_FILE)
        except Exception:
            pass


def _get_posted_titles() -> set:
    """Retorna o conjunto de títulos já postados (de pesca/postados/ e pesca/fila/)."""
    titles = set()
    for directory in [POSTED_DIR, QUEUE_DIR]:
        if not os.path.exists(directory):
            continue
        for fname in os.listdir(directory):
            if fname.endswith('.json'):
                try:
                    with open(os.path.join(directory, fname), 'r', encoding='utf-8') as jf:
                        data = json.load(jf)
                        if 'title' in data:
                            titles.add(data['title'].lower().strip())
                except Exception:
                    continue
    return titles


def _update_ofertas(hashtag_id: str, affiliate_link: str):
    """Atualiza o ofertas_pesca.json com o link mais recente."""
    try:
        if os.path.exists(OFERTAS_PATH):
            with open(OFERTAS_PATH, 'r', encoding='utf-8') as f:
                ofertas = json.load(f)
        else:
            ofertas = {}

        ofertas[hashtag_id]      = affiliate_link
        ofertas["#latest_story"] = affiliate_link  # Bot de comentários usa esta chave

        with open(OFERTAS_PATH, 'w', encoding='utf-8') as f:
            json.dump(ofertas, f, indent=4, ensure_ascii=False)

        print(f"✅ ofertas_pesca.json atualizado com {hashtag_id}")
    except Exception as e:
        print(f"⚠️  Não foi possível atualizar ofertas_pesca.json: {e}")


def _mark_as_posted(safe_id: str, product: dict, post_type: str):
    """Salva o registro do produto postado em pesca/postados/."""
    record = {
        "id":        product.get('id_interno', safe_id),
        "title":     product['titulo'],
        "price":     product['preco'],
        "timestamp": time.time(),
        "type":      post_type
    }
    path = os.path.join(POSTED_DIR, f"{safe_id}.json")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(record, f, indent=4, ensure_ascii=False)


# ────────────────────────────────────────────────────────────────────────────
# Automação Principal
# ────────────────────────────────────────────────────────────────────────────

def run_pesca_automation():
    print("=" * 65)
    print("🎣  PESCA TITANIUM — MÁQUINA DE REELS + STORIES  🎣")
    print("=" * 65)

    # ── 0. Lock anti-duplicação ──────────────────────────────────────────────
    if not _acquire_lock():
        sys.exit(1)

    try:
        # ── 1. Lê flags de execução ──────────────────────────────────────────
        post_reel  = os.getenv("POST_REEL",  "true").lower() == "true"
        post_story = os.getenv("POST_STORY", "true").lower() == "true"
        print(f"⚙️  Reels: {post_reel} | Stories: {post_story}")

        # ── 2. Seleciona produto de pesca não postado ainda ──────────────────
        from pesca.datafeed_pesca import get_pesca_products

        posted_titles = _get_posted_titles()
        print(f"\n[1] Buscando produtos de pesca (já postados: {len(posted_titles)})...")
        raw_products = get_pesca_products(max_items=3000)

        chosen_product = None
        for p in raw_products:
            if p['titulo'].lower().strip() not in posted_titles:
                chosen_product = p
                break

        if not chosen_product:
            print("❌ Nenhum produto de pesca novo encontrado. Amplie o datafeed.")
            sys.exit(1)

        print(f"✅ Produto selecionado: {chosen_product['titulo']} (R$ {chosen_product['preco']})")

        # ── 3. Obtém imagem do produto ───────────────────────────────────────
        image_url = chosen_product.get('imagem_url', '')

        # Fallback: busca via API da Shopee se o datafeed não trouxe imagem
        if not image_url:
            print("🔍 Imagem não encontrada no datafeed — buscando via Shopee API...")
            try:
                from core.shopee_api import get_shopee_image_api
                image_url = get_shopee_image_api(chosen_product['titulo'])
            except Exception as e:
                print(f"⚠️  Shopee API indisponível: {e}")

        if not image_url:
            print("❌ Não foi possível obter imagem para este produto.")
            sys.exit(1)

        # ── 4. Gera vídeos ───────────────────────────────────────────────────
        from pesca.video_generator_pesca import PescaVideoGenerator

        gen     = PescaVideoGenerator()
        safe_id = str(uuid.uuid4())[:8]

        reel_url  = None
        story_url = None

        # Uploader: usa PESCA_IMGBB_API_KEY (separado) ou fallback para IMGBB_API_KEY
        from social.core.uploader import ResilientUploader

        pesca_imgbb_key = (
            os.getenv("PESCA_IMGBB_API_KEY") or
            os.getenv("IMGBB_API_KEY")
        )
        uploader = ResilientUploader(
            ftp_config=None,          # GitHub Actions bloqueia FTP — força CDN
            imgbb_api_key=pesca_imgbb_key
        )

        if post_reel:
            print(f"\n[2] Gerando REEL de pesca...")
            reel_path = gen.generate_video(
                product_url=image_url,
                price=str(chosen_product['preco']),
                product_title=chosen_product['titulo'],
                output_filename=f"pesca_reel_{safe_id}.mp4",
                video_type="reel"
            )
            print("[3] Enviando REEL via Cloud CDN...")
            reel_url = uploader.upload(reel_path, f"pesca_reel_{safe_id}.mp4", force_cloud=True)
            if not reel_url:
                print("❌ Falha crítica no upload do Reel. Abortando.")
                sys.exit(1)

        if post_story:
            print(f"\n[2b] Gerando STORY de pesca...")
            story_path = gen.generate_video(
                product_url=image_url,
                price=str(chosen_product['preco']),
                product_title=chosen_product['titulo'],
                output_filename=f"pesca_story_{safe_id}.mp4",
                video_type="story"
            )
            print("[3b] Enviando STORY via Cloud CDN...")
            story_url = uploader.upload(story_path, f"pesca_story_{safe_id}.mp4", force_cloud=True)
            if not story_url:
                print("❌ Falha crítica no upload do Story. Abortando.")
                sys.exit(1)

        # ── 5. Aguarda propagação CDN ────────────────────────────────────────
        print("\n⏳ Aguardando propagação CDN (12s)...")
        time.sleep(12)

        # ── 6. Conecta ao Instagram API (conta Pesca Titanium) ───────────────
        print("\n[4] Conectando à API do Instagram — Pesca Titanium...")
        from social.core.instagram_client import InstagramClient

        client = InstagramClient(
            access_token=os.getenv("PESCA_IG_ACCESS_TOKEN"),
            business_id=os.getenv("PESCA_IG_BUSINESS_ID"),
            page_id=os.getenv("PESCA_PAGE_ID")
        )

        # ── 7. Monta caption temática de pesca ───────────────────────────────
        price_fmt     = f"{float(chosen_product['preco']):.2f}".replace('.', ',')
        affiliate_link = (
            chosen_product.get('link_afiliado') or
            chosen_product.get('url_produto', '')
        )
        hashtag_id = f"#pesca_{safe_id}"

        caption = (
            f"🎣 {chosen_product['titulo']}\n\n"
            f"Por apenas R$ {price_fmt}!\n\n"
            f"🔗 Link do produto na bio ou comente QUERO que mando no direct! 🎣\n\n"
            f"📦 Produto disponível na Shopee com entrega rápida!\n\n"
            f"{HASHTAGS_PESCA} {hashtag_id}"
        )

        # ── 8. Atualiza o mapa de ofertas (para bot de comentários) ──────────
        _update_ofertas(hashtag_id, affiliate_link)

        # ── 9. Publica no Instagram ──────────────────────────────────────────
        if post_reel and reel_url:
            print("\n🎬 Publicando REEL na @pescatitanium...")
            client.post_reels(video_url=reel_url, caption=caption)

        if post_story and story_url:
            print("\n📱 Publicando STORY na @pescatitanium...")
            client.post_story(media_url=story_url, is_video=True)

        # ── 10. Marca produto como postado ───────────────────────────────────
        _mark_as_posted(safe_id, chosen_product, "pesca_reel_story")

        print("\n🏆 Pesca Titanium — Automação concluída com sucesso!")
        print(f"   Produto: {chosen_product['titulo']}")
        print(f"   Hashtag: {hashtag_id}")

    finally:
        _release_lock()


# ────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_pesca_automation()
