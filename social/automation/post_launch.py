import os
import time
import shutil
from social.core.instagram_client import InstagramClient
from social.utils.video_utils import image_to_video
from social.core.uploader import ResilientUploader
from dotenv import load_dotenv

def run_launch_post():
    load_dotenv()
    
    # Configurações
    IG_TOKEN = os.getenv("IG_ACCESS_TOKEN")
    IG_BUSINESS_ID = os.getenv("IG_BUSINESS_ID")
    ENV_MODE = "PRODUCTION" # Forçando produção para o post oficial
    
    print("\n" + "="*60)
    print("🚀 EXECUTANDO POST DE LANÇAMENTO OFICIAL - v1145")
    print("="*60)
    
    # 1. Alvos
    fila_dir = "social/fila"
    postados_dir = "social/postados"
    banner_name = "promo_lancamento_v1143.png"
    local_image = os.path.join(fila_dir, banner_name)
    
    if not os.path.exists(local_image):
        print(f"❌ Erro: Banner {banner_name} não encontrado na fila.")
        return

    # 2. Legenda Premium (Solicitada pelo Usuário)
    caption = (
        "🚀 O NOVO GUIA DO DESCONTO CHEGOU! 💎\n\n"
        "Estamos de cara nova e com o 'motor' mais potente do que nunca. "
        "O Robô Titanium foi atualizado para trazer a melhor experiência de economia para você!\n\n"
        "✅ O QUE MUDOU?\n"
        "• Visual Premium: Navegação ultra-rápida e intuitiva.\n"
        "• Comparação Inteligente: Compare preços entre Amazon, Mercado Livre e Shopee em segundos.\n"
        "• Segurança Blindada: Implementamos protocolos de proteção de última geração para que "
        "sua navegação seja 100% segura e confiável.\n\n"
        "Economizar com inteligência e segurança nunca foi tão fácil. O site novo já está no ar!\n\n"
        "🔗 Link na Bio para conferir agora!\n\n"
        "#GuiaDoDesconto #EconomiaInteligente #Ofertas #Amazon #MercadoLivre #Shopee #SegurançaDigital #SiteNovo"
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
    local_video = "social/temp_launch_video.mp4"
    
    # 4. Processamento de Vídeo (Zoom Effect)
    print("🎬 Gerando Reels Cinematográfico...")
    if image_to_video(local_image, local_video):
        
        # 5. Upload e Postagem
        print("☁️ Enviando mídia para nuvem...")
        public_url = uploader.upload(local_video, f"launch_reels_{int(time.time())}.mp4")
        
        if public_url:
            print("📲 Publicando no Instagram...")
            success = instagram.post_reels(public_url, caption)
            
            if success:
                print("🏆 POST DE LANÇAMENTO REALIZADO COM SUCESSO!")
                
                # 6. Arquivamento
                os.makedirs(postados_dir, exist_ok=True)
                shutil.move(local_image, os.path.join(postados_dir, banner_name))
                print(f"📦 Banner arquivado.")
                
                # Limpeza
                if os.path.exists(local_video):
                    os.remove(local_video)
            else:
                print("❌ Falha na publicação final no Instagram.")
        else:
            print("❌ Falha no upload da mídia.")
    else:
        print("❌ Falha na geração do vídeo.")

if __name__ == "__main__":
    run_launch_post()
