import os
import sys
import json
import time
import shutil
from dotenv import load_dotenv
from datetime import datetime

# Adicionar o diretório raiz ao path para garantir os imports locais
sys.path.append(os.getcwd())

from social.core.instagram_client import InstagramClient
from social.core.uploader import ResilientUploader

def run_manual_post():
    load_dotenv()
    
    IG_TOKEN = os.getenv("IG_ACCESS_TOKEN")
    IG_BUSINESS_ID = os.getenv("IG_BUSINESS_ID")
    
    print("\n" + "="*60)
    print("🌹 POSTAGEM MANUAL - DIA INTERNACIONAL DA MULHER 🌹")
    print("="*60)
    
    # 1. Alvos
    fila_dir = os.path.join("social", "fila")
    postados_dir = os.path.join("social", "postados")
    image_name = "2026-03-08_Feliz_Dia_Internacional_Da_Mulher.png"
    local_image = os.path.join(fila_dir, image_name)
    
    if not os.path.exists(local_image):
        print(f"❌ Erro: Imagem {image_name} não encontrada em {fila_dir}/")
        # Listar arquivos para ajudar o usuário se falhar
        if os.path.exists(fila_dir):
            print(f"📂 Arquivos na fila: {os.listdir(fila_dir)}")
        return

    # 2. Legenda Poética
    caption = (
        "🌸 Feliz Dia Internacional da Mulher! 💖\n\n"
        "Hoje celebramos a força, a determinação e a sensibilidade de todas as mulheres "
        "que transformam o mundo com sua presença. Vocês são inspiração, coragem e luz em nossas vidas. ✨\n\n"
        "Para todas as nossas seguidoras, parceiras e amigas: que seu dia seja repleto de carinho "
        "e reconhecimento. Vocês merecem o melhor todos os dias! 💐💎\n\n"
        "#DiaInternacionalDaMulher #Mulher #8DeMarço #Inspiração #Homenagem #GuiaDoDesconto #RobôTitanium"
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
    
    # 4. Upload
    print("☁️ Enviando imagem para nuvem...")
    # Usar .jpg como destino para compatibilidade máxima com Meta
    remote_name = f"homenagem_mulher_{int(time.time())}.jpg"
    
    # Converter para JPEG se necessário (ResilientUploader não faz auto-conversão, mas post_scheduled_feed.py faz)
    # Vamos importar o PIL aqui para garantir
    from PIL import Image
    import io
    
    temp_jpg_path = os.path.join(fila_dir, f"temp_homenagem_{int(time.time())}.jpg")
    try:
        with Image.open(local_image) as img:
            rgb_img = img.convert('RGB')
            rgb_img.save(temp_jpg_path, format="JPEG", quality=95)
        
        public_url = uploader.upload(temp_jpg_path, remote_name)
    except Exception as e:
        print(f"❌ Erro ao processar imagem: {e}")
        return

    if public_url:
        print("📲 Publicando no Instagram...")
        success = instagram.post_image(public_url, caption)
        
        if success:
            print("\n🏆 HOMENAGEM PUBLICADA COM SUCESSO!")
            
            # 5. Arquivamento
            os.makedirs(postados_dir, exist_ok=True)
            today = datetime.now().strftime("%Y-%m-%d")
            dest_name = image_name if image_name.startswith(today) else f"{today}_{image_name}"
            
            shutil.move(local_image, os.path.join(postados_dir, dest_name))
            print(f"📦 Imagem arquivada em postados/")
            
            # 6. Log
            log_path = os.path.join(postados_dir, "post_log.json")
            logs = []
            if os.path.exists(log_path):
                with open(log_path, "r", encoding="utf-8") as f:
                    try:
                        logs = json.load(f)
                    except:
                        logs = []
            
            logs.append({
                "data": today,
                "type": "manual_homenagem",
                "imagem": image_name,
                "url": public_url,
                "timestamp": datetime.now().isoformat()
            })
            
            with open(log_path, "w", encoding="utf-8") as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)
            
        else:
            print("❌ Falha na publicação final no Instagram.")
    else:
        print("❌ Falha no upload da imagem.")
        
    # Limpeza
    if os.path.exists(temp_jpg_path):
        os.remove(temp_jpg_path)

if __name__ == "__main__":
    run_manual_post()
