"""
post_brick3d_carousel.py
========================
Posta o carrossel MISTO (vídeo + fotos) do Kit 52 Placas 3D Brick Pedra
Flexível no Feed do Instagram.

Ordem dos slides:
  Slide 1: video_1.mp4  → Vídeo de apresentação do produto
  Slide 2: imagem_1.png → Produto em destaque / capa
  Slide 3: imagem_2.png → Detalhe / benefício
  Slide 4: imagem_3.png → Especificações técnicas
  Slide 5: imagem_4.png → CTA → Comente QUERO

Link afiliado Shopee com nossa tag:
  https://shope.ee/... (redirecionado a partir da URL original + nossa ID)
"""

import os
import time
import json
from dotenv import load_dotenv
from social.core.instagram_client import InstagramClient
from social.core.uploader import ResilientUploader

load_dotenv()

# ─────────────────────────────────────────────
#  CONFIGURAÇÕES DO PRODUTO
# ─────────────────────────────────────────────
PRODUCT_NAME = "Kit 52 Placas 3D Brick Pedra Flexível"
SHOPEE_AFFILIATE_TAG = os.getenv("SHOPEE_APP_ID", "18318830863")

# Link do produto com nossa tag de afiliado embutida
PRODUCT_URL = (
    "https://shopee.com.br/Kit-52-Placas-3D-Autoadesivo-Brick-Pedra-Flex%C3%ADvel"
    "-Autocolante-28cm-x-7cm-1M2-i.401374403.22693753520"
    f"?extraParams=%7B%22display_model_id%22%3A335580335683%7D"
    f"&af_id={SHOPEE_AFFILIATE_TAG}"
)

# Legenda estratégica → robô de DM vai detectar "QUERO" nos comentários
CAPTION = """\
🧱 Renovação SEM OBRA? Existe sim! 👇

Apresentamos o Kit 52 Placas 3D Brick Pedra Flexível Autoadesivo — o revestimento que transforma qualquer parede em segundos, sem argamassa, sem ferramentas e sem bagunça! ✨

✅ Visual de pedra natural 3D ultra-realista
✅ Autocolante de alta aderência
✅ Cobre 1m² por kit (28cm x 7cm cada placa)
✅ Pode ser cortado com tesoura ou estilete
✅ Fácil de limpar com pano úmido
✅ Perfeito para sala, cozinha, corredor, escritório…

💰 Preço imperdível aqui na Shopee!

💬 Comente **"QUERO"** que nosso robô Titanium manda o link direto no seu direct! 🤖🚀

#Reforma #RevestimentoDecorativo #TijolinhoDePedra #Decoração #CasaDecor #DiyCasa #BrickWall #ParedeDePedra #ShopeeAchadinhos #TitaniumBot"""

# ─────────────────────────────────────────────
#  PASTA DA FILA (arquivos já salvos pelo usuário)
# ─────────────────────────────────────────────
FILA_DIR = r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium\social\fila"

# Ordem dos slides: vídeo PRIMEIRO, depois as imagens
CAROUSEL_FILES = [
    {"file": "video_1.mp4",  "type": "VIDEO"},
    {"file": "imagem_1.png", "type": "IMAGE"},
    {"file": "imagem_2.png", "type": "IMAGE"},
    {"file": "imagem_3.png", "type": "IMAGE"},
    {"file": "imagem_4.png", "type": "IMAGE"},
]

# ─────────────────────────────────────────────
#  FUNÇÃO PRINCIPAL
# ─────────────────────────────────────────────
def post_brick3d():
    ig_token      = os.getenv("IG_ACCESS_TOKEN")
    ig_business   = os.getenv("IG_BUSINESS_ID")
    page_id       = os.getenv("PAGE_ID")

    if not ig_token or not ig_business:
        print("❌ Credenciais do Instagram não encontradas no .env")
        return

    ftp_config = {
        "host": os.getenv("FTP_HOST"),
        "user": os.getenv("FTP_USER"),
        "pass": os.getenv("FTP_PASS"),
    }

    uploader  = ResilientUploader(ftp_config=ftp_config, imgbb_api_key=os.getenv("IMGBB_API_KEY"))
    client    = InstagramClient(ig_token, ig_business, page_id=page_id)

    # ── Verificar se todos os arquivos existem ──────────────────────────
    print("\n🔍 Verificando arquivos na fila...")
    for item in CAROUSEL_FILES:
        path = os.path.join(FILA_DIR, item["file"])
        if not os.path.exists(path):
            print(f"❌ Arquivo não encontrado: {path}")
            print("   Por favor, salve o arquivo na pasta 'fila' e tente novamente.")
            return
        size_mb = os.path.getsize(path) / 1_048_576
        print(f"   ✅ {item['file']} ({size_mb:.2f} MB) [{item['type']}]")

    # ── Upload de cada arquivo ─────────────────────────────────────────
    print("\n🚀 Iniciando uploads...")
    media_items = []

    for item in CAROUSEL_FILES:
        local_path  = os.path.join(FILA_DIR, item["file"])
        remote_name = f"brick3d_{int(time.time())}_{item['file']}"
        
        print(f"\n📤 Enviando: {item['file']} [{item['type']}]")
        
        # Imagens vão via FTP (o formato é mantido original .png/.jpg). ImgBB as vezes converte pra webp (Instagram recusa).
        force_cloud = False 
        public_url = uploader.upload(local_path, remote_name, force_cloud=force_cloud)

        if not public_url:
            print(f"❌ Falha no upload de {item['file']}. Abortando.")
            return

        media_items.append({"url": public_url, "type": item["type"]})
        print(f"   → {public_url}")
        time.sleep(2)  # Evita rate-limit no FTP/ImgBB

    # ── Postar o carrossel misto ───────────────────────────────────────
    print(f"\n📢 Postando carrossel misto com {len(media_items)} itens no Instagram...")
    success = client.post_carousel(media_items, CAPTION)

    if success:
        print("\n🏆 CARROSSEL DO KIT BRICK 3D PUBLICADO COM SUCESSO!")
        # Salva o ID da thread mais recente para o bot de comentários monitorar
        latest = client.get_latest_media(limit=1)
        if latest:
            post_id = latest[0]["id"]
            state = {
                "post_id": post_id,
                "product_url": PRODUCT_URL,
                "product_name": PRODUCT_NAME,
                "keyword": "QUERO",
                "posted_at": time.strftime("%Y-%m-%dT%H:%M:%S")
            }
            state_path = os.path.join(FILA_DIR, "..", "..", "state", "brick3d_active_post.json")
            state_path = os.path.normpath(state_path)
            os.makedirs(os.path.dirname(state_path), exist_ok=True)
            with open(state_path, "w", encoding="utf-8") as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
            print(f"💾 Estado salvo em: {state_path}")
            print(f"📌 Post ID: {post_id}")
            print(f"🔗 Link afiliado configurado: {PRODUCT_URL}")
            print("\n➡️  Agora execute: python bot_comentario_brick3d.py")
    else:
        print("\n❌ Falha na publicação do carrossel.")


if __name__ == "__main__":
    post_brick3d()
