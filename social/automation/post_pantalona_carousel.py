
import os
import sys
import json
import time
from glob import glob
from PIL import Image
from dotenv import load_dotenv

# Configuração de caminhos
PROJECT_ROOT = r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium"
sys.path.insert(0, PROJECT_ROOT)

from social.core.instagram_client import InstagramClient
from social.core.uploader import ResilientUploader

def run_pantalona_carousel():
    load_dotenv(os.path.join(PROJECT_ROOT, ".env"))
    
    IG_TOKEN = os.getenv("IG_ACCESS_TOKEN")
    IG_BUSINESS_ID = os.getenv("IG_BUSINESS_ID")
    
    if not IG_TOKEN or not IG_BUSINESS_ID:
        print("❌ Erro: Credenciais do Instagram não configuradas no .env")
        return

    # 1. Localizar arquivos na pasta fila
    fila_dir = os.path.join(PROJECT_ROOT, "social", "fila")
    
    # Busca por padrões numerados pantalona_01, pantalona_02...
    patterns = ["pantalona_*.webp", "pantalona_*.jpg", "pantalona_*.png", "pantalona_*.jpeg"]
    all_images = []
    for pattern in patterns:
        all_images.extend(glob(os.path.join(fila_dir, pattern)))
    
    # Ordenar numericamente para respeitar a sequência
    images = sorted(all_images)
    
    if not images:
        print("❌ Nenhuma imagem encontrada na pasta fila com o prefixo 'pantalona_'")
        return

    print(f"\n" + "="*50)
    print(f"🎬 INICIANDO CARROSSEL TITANIUM: {len(images)} SLIDES")
    print("="*50)

    # 2. Inicializar Uploader
    uploader = ResilientUploader(
        ftp_config={
            "host": os.getenv("FTP_HOST"),
            "user": os.getenv("FTP_USER"),
            "pass": os.getenv("FTP_PASS")
        },
        imgbb_api_key=os.getenv("IMGBB_API_KEY")
    )
    
    public_urls = []
    temp_files = []
    
    try:
        # Loop de processamento e upload
        for i, img_path in enumerate(images):
            basename = os.path.basename(img_path)
            print(f"🔄 [{i+1}/{len(images)}] Processando {basename}...")
            
            # Conversão para JPEG (Garante compatibilidade total com Meta Graph API)
            temp_jpg = os.path.join(fila_dir, f"catalog_tmp_{i}_{int(time.time())}.jpg")
            with Image.open(img_path) as img:
                rgb_img = img.convert('RGB')
                rgb_img.save(temp_jpg, "JPEG", quality=90)
            
            temp_files.append(temp_jpg)
            
            # Upload para Nuvem (ImgBB recomendado para álbuns de carrossel)
            # Forçamos cloud para garantir que a Meta consiga baixar rapidamente sem restrições de host
            public_url = uploader.upload(temp_jpg, f"pantalona_slide_{i}_{int(time.time())}.jpg", force_cloud=True)
            
            if public_url:
                public_urls.append(public_url)
                print(f"   ✅ Upload OK: {public_url}")
            else:
                print(f"   ❌ Falha crítica no upload do slide {i+1}. Abortando.")
                return

        # 3. Publicar via InstagramClient (Versão Atualizada v2026 com Suporte a Carousel)
        caption = (
            "🌟 PERSPECTIVA TITANIUM: O LOOKBOOK DA PANTALONA PERFEITA! 👖✨\n\n"
            "Diga olá à versatilidade! A nossa Pantalona de Alfaiataria Premium não é apenas uma calça, é a peça que faltava para elevar o seu estilo em qualquer ocasião. Do escritório ao jantar, do casual ao chic.\n\n"
            "Deslize para o lado ➡️ e confira como esse modelo valoriza cada silhueta. Mostramos hoje o poder das nossas curvas, a sofisticação da maturidade e a atitude urbana em um único catálogo! 🧥💎\n\n"
            "✅ Por que amamos esta peça?\n"
            "• Cintura Alta com elástico invisível\n"
            "• Corte Alfaiataria (Caimento impecável)\n"
            "• Tecido Premium de alta durabilidade\n\n"
            "💰 MONERES PREÇOS ENCONTRADOS:\n"
            "🥇 Mercado Livre: R$ 47,43 (Premium)\n"
            "🧡 Shopee: R$ 67,20 (Kit 3 unidades)\n"
            "📦 Amazon: R$ 74,90 (Wide Leg)\n\n"
            "🔥 QUER O LINK COM DESCONTO AGORA? 🔥\n"
            "Comente \"EU QUERO\" e o Robô Titanium enviará o link direto com rastreio de segurança para a sua DM! 📲🛡️\n\n"
            "#GuiaDoDesconto #RoboTitanium #ModaFeminina #Pantalona #Lookbook #Diversidade #AmazonBrasil #ShopeeBR #MercadoLivre"
        )
        
        client = InstagramClient(IG_TOKEN, IG_BUSINESS_ID)
        success = client.post_carousel(public_urls, caption)
        
        if success:
            print("\n🏆 CARROSSEL E CATALOGO PUBLICADOS COM SUCESSO NO FEED!")
            
            # Opcional: Arquivar originais para evitar duplicatas (mantendo schedule limpo)
            postados_dir = os.path.join(PROJECT_ROOT, "social", "postados")
            os.makedirs(postados_dir, exist_ok=True)
            for img in images:
                try:
                    import shutil
                    shutil.move(img, os.path.join(postados_dir, os.path.basename(img)))
                except:
                    pass
        else:
            print("\n❌ Falha na publicação do carrossel no Instagram.")

    except Exception as e:
        print(f"\n❌ Erro imprevisto no fluxo: {e}")
    finally:
        # Limpeza de arquivos temporários
        print("\n🧹 Limpando arquivos temporários de upload...")
        for f in temp_files:
            if os.path.exists(f):
                os.remove(f)

if __name__ == "__main__":
    run_pantalona_carousel()
