import os
import time
from PIL import Image, ImageDraw, ImageFont
from social.instagram_client import InstagramClient
from social.uploader import ResilientUploader
from dotenv import load_dotenv

def run_story_launch_post():
    load_dotenv()
    
    # Configurações
    IG_TOKEN = os.getenv("IG_ACCESS_TOKEN")
    IG_BUSINESS_ID = os.getenv("IG_BUSINESS_ID")
    
    print("\n" + "="*60)
    print("🚀 EXECUTANDO POST DE STORY: LANÇAMENTO OFICIAL - v1147")
    print("="*60)
    
    # 1. Alvos
    postados_dir = "social/postados"
    banner_name = "promo_lancamento_v1143.png"
    local_image = os.path.join(postados_dir, banner_name)
    
    if not os.path.exists(local_image):
        # Fallback se não estiver em postados ainda (segurança)
        local_image = os.path.join("social/fila", banner_name)
        if not os.path.exists(local_image):
            print(f"❌ Erro: Banner {banner_name} não encontrado.")
            return

    # 2. Processamento da Imagem (Overlay de Texto)
    print("🎨 Adicionando hashtags e link ao Story...")
    try:
        img = Image.open(local_image).convert("RGBA")
        
        # Se a imagem não for 1080x1920 (proporção Story), vamos criar um canvas Story e centralizar
        story_canvas = Image.new("RGBA", (1080, 1920), (12, 12, 12, 255))
        
        # Redimensionar imagem original para caber com folga
        img.thumbnail((1000, 1000), Image.Resampling.LANCZOS)
        img_x = (1080 - img.width) // 2
        img_y = (1920 - img.height) // 2 - 100
        story_canvas.paste(img, (img_x, img_y), img)
        
        draw = ImageDraw.Draw(story_canvas)
        try:
            font_path = "C:\\Windows\\Fonts\\arialbd.ttf"
            font_link = ImageFont.truetype(font_path, 60)
            font_tags = ImageFont.truetype(font_path, 40)
        except:
            font_link = font_tags = ImageFont.load_default()
            
        # Adicionar Link
        link_text = "guiadodesconto.com.br"
        link_w = draw.textlength(link_text, font=font_link)
        draw.text(((1080 - link_w)//2, img_y + img.height + 100), link_text, font=font_link, fill=(255, 153, 0))
        
        # Adicionar Hashtags
        tags_text = "#Economia #SiteNovo #OfertaCerta"
        tags_w = draw.textlength(tags_text, font=font_tags)
        draw.text(((1080 - tags_w)//2, img_y + img.height + 180), tags_text, font=font_tags, fill=(200, 200, 200))

        story_path = "social/temp_story_launch.png"
        story_canvas.convert("RGB").save(story_path, "JPEG", quality=95)
        print("✅ Imagem de Story com overlay gerada.")
        
    except Exception as e:
        print(f"❌ Erro ao processar imagem: {e}")
        return

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
    print("☁️ Enviando Story para a nuvem...")
    public_url = uploader.upload(story_path, f"launch_story_{int(time.time())}.png")
    
    if public_url:
        # 5. Publicação no Story
        print("📲 Publicando nos Stories do Instagram...")
        success = instagram.post_story(public_url, is_video=False)
        
        if success:
            print("🏆 POST DE STORY REALIZADO COM SUCESSO!")
            if os.path.exists(story_path):
                os.remove(story_path)
        else:
            print("❌ Falha na publicação no Instagram.")
    else:
        print("❌ Falha no upload da imagem.")

if __name__ == "__main__":
    run_story_launch_post()
