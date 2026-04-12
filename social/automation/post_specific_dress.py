
import os
import sys
import json
import time
from glob import glob
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv

# Path setup
PROJECT_ROOT = r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium"
sys.path.insert(0, PROJECT_ROOT)

from social.core.instagram_client import InstagramClient
from social.core.uploader import ResilientUploader

def process_user_images():
    fila_dir = os.path.join(PROJECT_ROOT, "social", "fila")
    output_dir = os.path.join(PROJECT_ROOT, "social", "postados", f"manga_japonesa_{int(time.time())}")
    os.makedirs(output_dir, exist_ok=True)
    
    # Locate files: vestido_01.png, vestido_02.png etc
    patterns = ["vestido_*.png", "vestido_*.jpg", "vestido_*.jpeg"]
    all_images = []
    for pattern in patterns:
        all_images.extend(glob(os.path.join(fila_dir, pattern)))
    
    # Sort logically
    def sort_key(s):
        import re
        nums = re.findall(r'\d+', s)
        return int(nums[-1]) if nums else 0
        
    images = sorted(all_images, key=sort_key)
    
    if not images:
        return []

    logo_shopee_path = os.path.join(PROJECT_ROOT, "site", "images", "logo-shopee.png")
    font_path = "C:\\Windows\\Fonts\\arialbd.ttf"
    
    try:
        font_price = ImageFont.truetype(font_path, 100)
        font_title = ImageFont.truetype(font_path, 40)
    except:
        font_price = font_title = ImageFont.load_default()

    processed_paths = []
    price = "43,65"
    title_text = "VESTIDO MANGA JAPONESA"

    for i, img_path in enumerate(images):
        print(f"🔄 Processando imagem {i+1}...")
        img = Image.open(img_path).convert("RGBA")
        img = img.resize((1080, 1080), Image.Resampling.LANCZOS)
        draw = ImageDraw.Draw(img)

        # Logo Shopee
        if i > 0 and os.path.exists(logo_shopee_path):
            logo = Image.open(logo_shopee_path).convert("RGBA")
            logo.thumbnail((200, 80), Image.Resampling.LANCZOS)
            img.paste(logo, (50, 50), logo)

        # Price Badge
        price_text = f"R$ {price}"
        text_w = font_price.getlength(price_text)
        badge_w, badge_h = int(text_w + 60), 140
        badge_x, badge_y = 50, 850
        
        overlay = Image.new('RGBA', img.size, (0,0,0,0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=20, fill=(238, 77, 45, 230))
        img = Image.alpha_composite(img, overlay)
        
        draw = ImageDraw.Draw(img)
        draw.text((badge_x + 30, badge_y + 20), price_text, font=font_price, fill=(255, 255, 255))
        draw.text((50, badge_y - 60), title_text.upper(), font=font_title, fill=(255, 255, 255), stroke_width=2, stroke_fill=(0,0,0))

        # Save
        out_path = os.path.join(output_dir, f"manga_japa_{i:02d}.jpg")
        img.convert("RGB").save(out_path, "JPEG", quality=85)
        processed_paths.append(out_path)
        
    return processed_paths

def run_post():
    load_dotenv(os.path.join(PROJECT_ROOT, ".env"))
    
    processed = process_user_images()
    if not processed:
        print("❌ Nenhuma imagem encontrada na fila para postar.")
        return

    uploader = ResilientUploader(
        ftp_config={
            "host": os.getenv("FTP_HOST"),
            "user": os.getenv("FTP_USER"),
            "pass": os.getenv("FTP_PASS")
        }
    )
    
    public_urls = []
    for i, path in enumerate(processed):
        print(f"🔄 Uploading {i+1}/{len(processed)}...")
        url = uploader.upload(path, f"manga_japa_{i}_{int(time.time())}.jpg", force_cloud=False)
        if url:
            public_urls.append(url)
        else:
            print("❌ Falha no upload.")
            return

    caption = (
        "🌟 EXCLUSIVIDADE TITANIUM: VESTIDO MIDI MANGA JAPONESA 👗✨\n\n"
        "Elegância e conforto em um único look! O nosso Vestido Tubinho Midi em Malha Canelada Blush é aquela peça versátil que valoriza a silhueta com modernidade e delicadeza.\n\n"
        "🎨 Cores disponíveis: Preto, Chocolate, Nude, Verde Militar, Vermelho, Branco, Azul Royal e mais! (Com e sem bolso disponível).\n\n"
        "✅ Destaques:\n"
        "• Manga Japonesa (Design moderno)\n"
        "• Tecido Ribana/Malha Canelada (Toque macio)\n"
        "• Corte Tubinho Ajustado\n"
        "• Sem bojo (Conforto total)\n\n"
        "🔥 PREÇO PROMOCIONAL SHOPEE:\n"
        "🥇 Apenas R$ 43,65! 🔥\n\n"
        "⚠️ *Imagens ilustrativas. Confira as variações reais no link.*\n\n"
        "💬 QUER O LINK DIRETO AGORA? 💬\n"
        "Comente \"QUERO\" e receba o link com segurança na sua DM! 📲🛡️\n\n"
        "#RoboTitanium #ModaFeminina #VestidoMidi #MangaJaponesa #LookDoDia #ShopeeBrasil #ModaCasual #VestidoTubinho"
    )
    
    client = InstagramClient(os.getenv("IG_ACCESS_TOKEN"), os.getenv("IG_BUSINESS_ID"))
    success = client.post_carousel(public_urls, caption)
    
    if success:
        print("\n🏆 POSTAGEM REALIZADA COM SUCESSO!")
        # Clear original images to avoid re-posting
        for f in glob(os.path.join(PROJECT_ROOT, "social", "fila", "vestido_*")):
             try: os.remove(f)
             except: pass
    else:
        print("\n❌ Falha ao postar.")

if __name__ == "__main__":
    run_post()
