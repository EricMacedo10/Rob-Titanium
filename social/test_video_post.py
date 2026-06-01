import os
import ftplib
import time
from pathlib import Path
from dotenv import load_dotenv

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from social.core.instagram_client import InstagramClient

def upload_to_ftp(local_file_path, filename):
    print(f"📤 Fazendo upload de {filename} para Hostinger...")
    ftp_host = os.getenv('FTP_HOST')
    ftp_user = os.getenv('FTP_USER')
    ftp_pass = os.getenv('FTP_PASS')
    
    ftp = ftplib.FTP(ftp_host, ftp_user, ftp_pass, timeout=60)
    
    for p in ["public_html", "www"]:
        try:
            ftp.cwd(f"/{p}")
            break
        except:
            continue
            
    with open(local_file_path, 'rb') as f:
        ftp.storbinary(f'STOR {filename}', f)
        
    ftp.quit()
    print(f"✅ Upload concluído! URL: https://{ftp_host}/{filename}")
    return f"https://{ftp_host}/{filename}"

def run_test_post():
    load_dotenv()
    client = InstagramClient(
        access_token=os.getenv("IG_ACCESS_TOKEN"),
        business_id=os.getenv("IG_BUSINESS_ID"),
        page_id=os.getenv("PAGE_ID")
    )
    
    reel_path = os.path.join(os.path.dirname(__file__), "temp_videos", "meu_primeiro_reel.mp4")
    story_path = os.path.join(os.path.dirname(__file__), "temp_videos", "meu_primeiro_story.mp4")
    
    if not os.path.exists(reel_path):
        print("❌ Arquivo meu_primeiro_reel.mp4 não encontrado.")
        return
        
    if not os.path.exists(story_path):
        print("❌ Arquivo meu_primeiro_story.mp4 não encontrado.")
        return

    # 1. Upload Reels
    reel_url = upload_to_ftp(reel_path, "test_reel_titanium.mp4")
    
    # 2. Upload Story
    story_url = upload_to_ftp(story_path, "test_story_titanium.mp4")
    
    print("\n⏳ Aguardando 10 segundos para o servidor DNS/CDN da Hostinger propagar os arquivos...")
    time.sleep(10)
    
    # 3. Postar Reels
    print("\n🎬 Disparando Postagem de REELS...")
    caption = "Vestido Elegante Feminino - Coleção Exclusiva ✨\n\nPor apenas R$ 89,90!\n\nComente QUERO para receber o link VIP no seu direct! 🛍️\n\n#ModaFeminina #ShopeeBR #VestidoLongo #LookDoDia #TitaniumBoutique"
    client.post_reels(video_url=reel_url, caption=caption)
    
    # 4. Postar Story
    print("\n🎬 Disparando Postagem de STORY...")
    client.post_story(media_url=story_url, is_video=True)
    
    print("\n🚀 Teste Completo finalizado. Verifique o seu Instagram pelo celular!")

if __name__ == "__main__":
    run_test_post()
