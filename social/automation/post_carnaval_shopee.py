"""
🎉 Post Feed: Carnaval Shopee Banner
Segue o Senior Workflow: Upload Resiliente + Publicação + Arquivamento
"""
import os
import time
import shutil
from social.core.instagram_client import InstagramClient
from social.utils.video_utils import image_to_video
from social.core.uploader import ResilientUploader
from dotenv import load_dotenv

def run_carnaval_shopee_post():
    load_dotenv()

    # Configurações
    IG_TOKEN = os.getenv("IG_ACCESS_TOKEN")
    IG_BUSINESS_ID = os.getenv("IG_BUSINESS_ID")
    ENV_MODE = os.getenv("ENV_MODE", "STAGING").upper()

    print("\n" + "="*60)
    print("🎭 POST DE FEED: CARNAVAL SHOPEE - PRODUÇÃO")
    print("="*60)

    # 1. Banner na fila
    fila_dir = "social/fila"
    postados_dir = "social/postados"
    banner_name = "banner_carnaval_shopee.png"
    local_image = os.path.join(fila_dir, banner_name)

    if not os.path.exists(local_image):
        print(f"❌ Erro: Banner {banner_name} não encontrado na fila.")
        return

    print(f"✅ Banner encontrado: {local_image}")

    # 2. Legenda Carnaval Shopee 🎉
    caption = (
        "🎭🔥 CARNAVAL DE OFERTAS NA SHOPEE! 🔥🎭\n\n"
        "A folia começou e os preços despencaram! 🎊\n"
        "Aproveite promoções IMPERDÍVEIS em todas as categorias "
        "com frete grátis e cupons exclusivos! 💸✨\n\n"
        "🛒 Eletrônicos com até 70% OFF\n"
        "👗 Moda e Acessórios por preços de Carnaval\n"
        "🏠 Casa e Decoração com mega descontos\n"
        "💄 Beleza e Cuidados Pessoais em promoção\n\n"
        "⏰ Corre que é por tempo limitado!\n"
        "👉 Link na bio para garantir as melhores ofertas!\n\n"
        "#Carnaval #Carnaval2026 #Ofertas #Shopee "
        "#PromoçãoDeCarnaval #FoliaDeDescontos "
        "#FreteGrátis #Cupom #Desconto #Economia "
        "#OfertaCerta #GuiaDoDesconto #ComprasOnline "
        "#MelhorPreço #BlackCarnaval #ShopeeCarnaval"
    )

    print(f"\n📝 Legenda preparada ({len(caption)} caracteres)")

    # 3. Verificar modo
    if ENV_MODE != "PRODUCTION":
        print(f"\n🧪 MODO {ENV_MODE}: Simulação ativa. Legenda gerada:")
        print("-"*40)
        print(caption)
        print("-"*40)
        print("Para postar de verdade, defina ENV_MODE=PRODUCTION no .env")
        return

    # 4. Inicializar Componentes
    uploader = ResilientUploader(
        ftp_config={
            "host": os.getenv("FTP_HOST"),
            "user": os.getenv("FTP_USER"),
            "pass": os.getenv("FTP_PASS")
        },
        imgbb_api_key=os.getenv("IMGBB_API_KEY")
    )

    instagram = InstagramClient(IG_TOKEN, IG_BUSINESS_ID)

    # 5. Upload da Imagem
    print("\n☁️ Enviando imagem para a nuvem...")
    public_url = uploader.upload(local_image, f"carnaval_shopee_{int(time.time())}.png")

    if public_url:
        # 6. Publicação no Feed
        print("📲 Publicando no Feed do Instagram...")
        success = instagram.post_image(public_url, caption)

        if success:
            print("\n🏆 POST DE CARNAVAL SHOPEE REALIZADO COM SUCESSO! 🎉")

            # 7. Arquivamento
            os.makedirs(postados_dir, exist_ok=True)
            dest = os.path.join(postados_dir, banner_name)
            if os.path.exists(dest):
                name, ext = os.path.splitext(banner_name)
                dest = os.path.join(postados_dir, f"{name}_{int(time.time())}{ext}")
            shutil.move(local_image, dest)
            print(f"📦 Banner arquivado em: {os.path.basename(dest)}")
        else:
            print("❌ Falha na publicação no Instagram.")
    else:
        print("❌ Falha no upload da imagem.")

if __name__ == "__main__":
    run_carnaval_shopee_post()
