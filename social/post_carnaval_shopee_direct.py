"""
🎉 Post Feed: Carnaval Shopee Banner (Direct Publish)
Bypasses the video-only status polling for image Feed posts.
"""
import os
import time
import shutil
import requests
from dotenv import load_dotenv

def run_carnaval_shopee_direct():
    load_dotenv()

    IG_TOKEN = os.getenv("IG_ACCESS_TOKEN")
    IG_BUSINESS_ID = os.getenv("IG_BUSINESS_ID")

    print("\n" + "="*60)
    print("🎭 POST DE FEED: CARNAVAL SHOPEE - PUBLICAÇÃO DIRETA")
    print("="*60)

    # A imagem já foi uploadada e validada com sucesso na tentativa anterior
    # URL pública confirmada:
    image_url = "https://guiadodesconto.com.br/social/carnaval_shopee_1770729313.png"

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

    base_url = f"https://graph.facebook.com/v21.0/{IG_BUSINESS_ID}"

    # Passo 1: Criar Media Container (Imagem)
    print("📦 Criando container de imagem...")
    container_resp = requests.post(f"{base_url}/media", data={
        "image_url": image_url,
        "caption": caption,
        "access_token": IG_TOKEN
    })
    container_data = container_resp.json()
    print(f"   Resposta: {container_data}")

    if "id" not in container_data:
        print(f"❌ Erro ao criar container: {container_data}")
        return False

    creation_id = container_data["id"]
    print(f"✅ Container criado: {creation_id}")

    # Passo 2: Para IMAGENS, aguardar apenas 5 segundos e publicar direto
    # (status_code polling é necessário apenas para vídeos/Reels)
    print("⏳ Aguardando 5 segundos para processamento da imagem...")
    time.sleep(5)

    # Passo 3: Publicar
    print("📲 Publicando no Feed do Instagram...")
    publish_resp = requests.post(f"{base_url}/media_publish", data={
        "creation_id": creation_id,
        "access_token": IG_TOKEN
    })
    publish_data = publish_resp.json()
    print(f"   Resposta: {publish_data}")

    if "id" in publish_data:
        print(f"\n🏆 POST PUBLICADO COM SUCESSO! (Post ID: {publish_data['id']})")

        # Arquivar o banner da fila
        fila_path = "social/fila/banner_carnaval_shopee.png"
        postados_dir = "social/postados"
        if os.path.exists(fila_path):
            os.makedirs(postados_dir, exist_ok=True)
            dest = os.path.join(postados_dir, f"banner_carnaval_shopee_{int(time.time())}.png")
            shutil.move(fila_path, dest)
            print(f"📦 Banner arquivado: {os.path.basename(dest)}")

        return True
    else:
        print(f"❌ Erro na publicação: {publish_data}")
        return False

if __name__ == "__main__":
    run_carnaval_shopee_direct()
