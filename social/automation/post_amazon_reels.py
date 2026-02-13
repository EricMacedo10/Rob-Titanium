import os
import sys
import time
import shutil
from dotenv import load_dotenv

# Ajuste de PATH para encontrar os módulos locais (Senior Workflow Resilience)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from social.core.instagram_client import InstagramClient
from social.core.uploader import ResilientUploader

def post_amazon_reels():
    load_dotenv()
    # Forca modo PRODUCAO para esta execucao especifica (Senior Workflow)
    os.environ['ENV_MODE'] = 'PRODUCTION'
    
    print("\n" + "="*60)
    print("--- TITANIUM SENIOR WORKFLOW - AMAZON REELS (PROD) ---")
    print("="*60)
    
    # 1. Configurações
    video_path = "social/fila/Amazon_ofertas_do_dia.mp4"
    postados_dir = "social/postados"
    
    # Legenda estratégica Amazon
    caption = (
        "🚀 OFERTAS DO DIA AMAZON: OS MELHORES PREÇOS ESTÃO AQUI! 📦\n\n"
        "A nossa curadoria não para! O Robô Titanium encontrou os descontos mais quentes do dia na Amazon. De tecnologia a itens para sua casa, selecionamos o que há de melhor para você economizar de verdade. 🔥📉\n\n"
        "🌐 guiadodesconto.com.br\n"
        "🔗 Link na Bio para as ofertas!\n\n"
        "#Amazon #OfertasDoDia #Descontos #Promoção #Achadinhos #Tecnologia #Casa #RoboTitanium #Economia #PreçoBaixo"
    )
    
    # Credenciais
    ig_token = os.getenv("IG_ACCESS_TOKEN")
    ig_business_id = os.getenv("IG_BUSINESS_ID")
    ftp_config = {
        "host": os.getenv("FTP_HOST"),
        "user": os.getenv("FTP_USER"),
        "pass": os.getenv("FTP_PASS")
    }
    
    # 2. Pre-Check (Defensivo)
    if not os.path.exists(video_path):
        print(f"--- ERRO CRITICO: Video nao encontrado em {video_path}")
        return False
        
    print(f"--- Video detectado: {video_path} ({os.path.getsize(video_path)} bytes)")
    
    if not ig_token or not ig_business_id:
        print("--- ERRO CRITICO: Credenciais do Instagram ausentes no .env")
        return False

    # 3. Execução
    uploader = ResilientUploader(ftp_config=ftp_config)
    instagram = InstagramClient(ig_token, ig_business_id)
    
    print("--- Iniciando fase de upload publico...")
    # Nome remoto unico para evitar cache
    timestamp = int(time.time())
    remote_video_name = f"amazon_reels_{timestamp}.mp4"
    remote_cover_name = f"amazon_reels_{timestamp}.jpg"
    
    # Gerar capa localmente se nao existir
    cover_path = video_path.replace(".mp4", "_cover.jpg")
    if not os.path.exists(cover_path):
        try:
            from social.utils.video_cover import extract_cover
            extract_cover(video_path, cover_path)
            print(f"--- Capa gerada em {cover_path}")
        except Exception as e:
            print(f"--- Alerta: Falha ao gerar capa: {e}. Prosseguindo sem capa personalizada.")
            cover_path = None
    
    # Upload Video
    public_video_url = uploader.upload(video_path, remote_video_name)
    
    # Upload Cover
    public_cover_url = uploader.upload(cover_path, remote_cover_name) if (cover_path and os.path.exists(cover_path)) else None
    
    if not public_video_url:
        print("--- FALHA: Nao foi possivel obter uma URL publica para o video.")
        return False
        
    print(f"--- URL Publica Video: {public_video_url}")
    if public_cover_url:
        print(f"--- URL Publica Capa: {public_cover_url}")
        
    print("--- Iniciando postagem no Instagram Reels...")
    success = instagram.post_reels(public_video_url, caption, cover_url=public_cover_url)
    
    # 4. Finalizacao
    if success:
        print("--- SUCESSO! Postagem concluida em PRODUCAO.")
        os.makedirs(postados_dir, exist_ok=True)
        
        files_to_move = [video_path]
        if cover_path and os.path.exists(cover_path):
            files_to_move.append(cover_path)
            
        for f in files_to_move:
            if not os.path.exists(f): continue
            dest_path = os.path.join(postados_dir, os.path.basename(f))
            if os.path.exists(dest_path):
                name, ext = os.path.splitext(os.path.basename(f))
                dest_path = os.path.join(postados_dir, f"{name}_{timestamp}{ext}")
            shutil.move(f, dest_path)
        
        print(f"--- Arquivos arquivados em: {postados_dir}")
        return True
    else:
        print("--- FALHA: Ocorreu um erro durante a postagem no Instagram.")
        return False

if __name__ == "__main__":
    post_amazon_reels()
