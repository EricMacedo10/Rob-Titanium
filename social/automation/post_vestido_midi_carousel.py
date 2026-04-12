
import os
import sys
import json
import time
from glob import glob
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv

# Configuração de caminhos
PROJECT_ROOT = r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium"
sys.path.insert(0, PROJECT_ROOT)

from social.core.instagram_client import InstagramClient
from social.core.uploader import ResilientUploader

def prepare_images():
    # Caminhos das imagens geradas por IA
    brain_dir = r"C:\Users\ericm\.gemini\antigravity\brain\c7dd95c4-5e9f-4f89-9cda-3d6f90bb4d05"
    output_dir = os.path.join(PROJECT_ROOT, "social", "fila")
    os.makedirs(output_dir, exist_ok=True)

    images = [
        {"path": os.path.join(brain_dir, "vestido_midi_tricot_capa_1774429803400.png"), "title": "Capa", "price": None},
        {"path": os.path.join(brain_dir, "vestido_midi_tricot_textura_1774429817850.png"), "title": "Textura Ribbed Premium", "price": "39,90"},
        {"path": os.path.join(brain_dir, "vestido_midi_tricot_detalhe_fenda_v2_1774429880725.png"), "title": "Elegância na Fenda Lateral", "price": "39,90"},
        {"path": os.path.join(brain_dir, "vestido_midi_tricot_lifestyle_v2_1774429894985.png"), "title": "Conforto & Sofisticação", "price": "39,90"},
    ]

    logo_shopee_path = os.path.join(PROJECT_ROOT, "site", "images", "logo-shopee.png")
    font_path = "C:\\Windows\\Fonts\\arialbd.ttf"
    
    try:
        font_price = ImageFont.truetype(font_path, 100)
        font_title = ImageFont.truetype(font_path, 40)
        font_cta = ImageFont.truetype(font_path, 35)
    except:
        font_price = font_title = font_cta = ImageFont.load_default()

    processed_images = []
    for i, item in enumerate(images):
        img = Image.open(item["path"]).convert("RGBA")
        
        # Redimensionar para 1080x1080 (Padrão Feed)
        img = img.resize((1080, 1080), Image.Resampling.LANCZOS)
        
        draw = ImageDraw.Draw(img)
        
        # Adicionar Logo Shopee (se não for a capa)
        if i > 0 and os.path.exists(logo_shopee_path):
            logo = Image.open(logo_shopee_path).convert("RGBA")
            logo.thumbnail((200, 80), Image.Resampling.LANCZOS)
            img.paste(logo, (50, 50), logo)

        # Adicionar Preço e Título (se não for a capa)
        if item["price"]:
            price_text = f"R$ {item['price']}"
            text_w = font_price.getlength(price_text)
            badge_w, badge_h = int(text_w + 60), 140
            badge_x, badge_y = 50, 850
            
            overlay = Image.new('RGBA', img.size, (0,0,0,0))
            overlay_draw = ImageDraw.Draw(overlay)
            overlay_draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=20, fill=(238, 77, 45, 230)) # Laranja Shopee
            img = Image.alpha_composite(img, overlay)
            
            draw = ImageDraw.Draw(img)
            draw.text((badge_x + 30, badge_y + 20), price_text, font=font_price, fill=(255, 255, 255))
            draw.text((50, badge_y - 60), item["title"].upper(), font=font_title, fill=(255, 255, 255), stroke_width=2, stroke_fill=(0,0,0))

        if i == len(images) - 1:
            cta_text = "Comente 'QUERO' para receber o link! 🔗"
            draw.text((50, 1000), cta_text, font=font_cta, fill=(255, 255, 255), stroke_width=2, stroke_fill=(238, 77, 45))

        output_path = os.path.join(output_dir, f"vestido_midi_{i:02d}.jpg")
        img.convert("RGB").save(output_path, "JPEG", quality=85) # Um pouco mais de compressão
        processed_images.append(output_path)
    
    return processed_images

def run_vestido_carousel():
    load_dotenv(os.path.join(PROJECT_ROOT, ".env"))
    
    IG_TOKEN = os.getenv("IG_ACCESS_TOKEN")
    IG_BUSINESS_ID = os.getenv("IG_BUSINESS_ID")
    
    if not IG_TOKEN or not IG_BUSINESS_ID:
        print("❌ Erro: Credenciais do Instagram não configuradas.")
        return

    print("\n🎨 PREPARANDO IMAGENS DO VESTIDO MIDI...")
    images = prepare_images()
    
    if not images:
        print("❌ Falha ao preparar imagens.")
        return

    print(f"\n" + "="*50)
    print(f"🎬 INICIANDO CARROSSEL VESTIDO MIDI: {len(images)} SLIDES")
    print("="*50)

    uploader = ResilientUploader(
        ftp_config={
            "host": os.getenv("FTP_HOST"),
            "user": os.getenv("FTP_USER"),
            "pass": os.getenv("FTP_PASS")
        },
        imgbb_api_key=os.getenv("IMGBB_API_KEY")
    )
    
    public_urls = []
    
    try:
        for i, img_path in enumerate(images):
            print(f"🔄 [{i+1}/{len(images)}] Uploading {os.path.basename(img_path)}...")
            public_url = uploader.upload(img_path, f"vestido_midi_slide_{i}_{int(time.time())}.jpg", force_cloud=False)
            
            if public_url:
                public_urls.append(public_url)
                print(f"   ✅ Upload OK: {public_url}")
            else:
                print(f"   ❌ Falha no upload do slide {i+1}. Abortando.")
                return

        caption = (
            "✨ ELEGÂNCIA VERÃO: O VESTIDO MIDI QUE VOCÊ DESEJAVA! 👗☀️\n\n"
            "Conheça o nosso Vestido Midi em Tricot Canelado com Fenda Lateral! A combinação perfeita entre o conforto do Modal e a sofisticação da fenda que valoriza cada passo.\n\n"
            "Deslize para o lado ➡️ e sinta a textura premium desse tecido que se molda ao seu corpo com perfeição. Do churrasco casual ao jantar elegante.\n\n"
            "🌟 Por que você vai amar:\n"
            "• Tricot Canelado Premium (Toque macio)\n"
            "• Fenda Lateral (Charme e movimento)\n"
            "• Comprimento Midi (O queridinho do momento)\n\n"
            "💰 PREÇO EXCLUSIVO SHOPEE:\n"
            "🔥 Apenas R$ 39,90! 🔥\n\n"
            "💬 QUER O LINK DIRETO AGORA? 💬\n"
            "Comente \"QUERO\" e o Robô Titanium enviará o link com segurança para a sua DM agora mesmo! 📲🛡️\n\n"
            "#RoboTitanium #ModaFeminina #VestidoMidi #Tricot #LookVerao #ShopeeBrasil #ModaCasual #VestidoCanelado"
        )
        
        client = InstagramClient(IG_TOKEN, IG_BUSINESS_ID)
        success = client.post_carousel(public_urls, caption)
        
        if success:
            print("\n🏆 CARROSSEL PUBLICADO COM SUCESSO NO INSTAGRAM!")
        else:
            print("\n❌ Falha na publicação do carrossel.")

    except Exception as e:
        print(f"\n❌ Erro imprevisto: {e}")

if __name__ == "__main__":
    run_vestido_carousel()
