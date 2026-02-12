import os
import time
import shutil
from social.core.instagram_client import InstagramClient
from social.utils.video_utils import image_to_video
from social.core.uploader import ResilientUploader
from dotenv import load_dotenv

def run_feed_launch_post():
    load_dotenv()
    
    # Configurações
    IG_TOKEN = os.getenv("IG_ACCESS_TOKEN")
    IG_BUSINESS_ID = os.getenv("IG_BUSINESS_ID")
    ENV_MODE = "PRODUCTION"
    
    print("\n" + "="*60)
    print("🚀 EXECUTANDO POST DE FEED: LANÇAMENTO OFICIAL - v1146")
    print("="*60)
    
    # 1. Alvos
    fila_dir = "social/fila"
    postados_dir = "social/postados"
    banner_name = "promo_lancamento_v1143.png"
    local_image = os.path.join(fila_dir, banner_name)
    
    if not os.path.exists(local_image):
        print(f"❌ Erro: Banner {banner_name} não encontrado na fila.")
        return

    # 2. Legenda Premium
    caption = (
        "✨ O FUTURO DA ECONOMIA CHEGOU! ✨\n\n"
        "É com muito orgulho que apresentamos o NOVO Guia do Desconto. "
        "Não é apenas uma atualização, é uma experiência totalmente reconstruída para quem não abre mão de economizar com inteligência. 💎\n\n"
        "O que você vai encontrar no novo site:\n\n"
        "✅ COMPARADOR TITANIUM: Encontre o menor preço entre Amazon, Mercado Livre e Shopee em segundos. Otimizamos nossos algoritmos para que você nunca mais pague caro.\n"
        "✅ NAVEGAÇÃO PREMIUM: Um visual moderno, leve e focado no que importa: as melhores ofertas na palma da sua mão.\n"
        "✅ SEGURANÇA BLINDADA: Investimos pesado em protocolos de proteção de dados e integridade de links. No Guia do Desconto, sua segurança é prioridade absoluta. 🛡️\n\n"
        "Tudo isso com a credibilidade de quem monitora o mercado 24h por dia para você.\n\n"
        "👉 O site novo já está no ar! Clique no LINK NA BIO e descubra como é fácil economizar com segurança.\n\n"
        "#GuiaDoDesconto #SiteNovo #Economia #Ofertas #Amazon #MercadoLivre #Shopee #Segurança #Tecnologia #Titanium"
    )

    # 3. Inicializar Componentes
    uploader = ResilientUploader(
        ftp_config={
            "host": os.getenv("FTP_HOST"),
            "user": os.getenv("FTP_USER"),
            "pass": os.getenv("FTP_PASS")
        },
        imgbb_api_key=os.getenv("IMGBB_API_KEY")
    )
    
    instagram = InstagramClient(IG_TOKEN, IG_BUSINESS_ID)
    
    # 4. Upload da Imagem
    print("☁️ Enviando imagem para a nuvem...")
    public_url = uploader.upload(local_image, f"launch_feed_{int(time.time())}.png")
    
    if public_url:
        # 5. Publicação no Feed
        print("📲 Publicando no Feed do Instagram...")
        success = instagram.post_image(public_url, caption)
        
        if success:
            print("🏆 POST DE FEED REALIZADO COM SUCESSO!")
            
            # 6. Arquivamento
            os.makedirs(postados_dir, exist_ok=True)
            shutil.move(local_image, os.path.join(postados_dir, banner_name))
            print(f"📦 Banner arquivado.")
        else:
            print("❌ Falha na publicação no Instagram.")
    else:
        print("❌ Falha no upload da imagem.")

if __name__ == "__main__":
    run_feed_launch_post()
