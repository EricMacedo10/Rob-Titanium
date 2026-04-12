import os
import json
from PIL import Image, ImageDraw, ImageFont

def create_carousel():
    # Caminhos das imagens geradas por IA
    base_dir = r"C:\Users\ericm\.gemini\antigravity\brain\ebc53408-e506-4694-80b0-fd7d62852be4"
    output_dir = r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium\social\fila"
    os.makedirs(output_dir, exist_ok=True)

    images = [
        {"path": os.path.join(base_dir, "capa_carrossel_moda_1774111679890.png"), "title": "Capa", "price": None},
        {"path": os.path.join(base_dir, "modelo_alfaiataria_luxo_1774111695830.png"), "title": "Conjunto Alfaiataria Super Luxo", "price": "65,99"},
        {"path": os.path.join(base_dir, "modelo_jaqueta_couro_1774111711794.png"), "title": "Jaqueta de Couro Ecológico", "price": "63,92"},
        {"path": os.path.join(base_dir, "modelo_pantalona_estilo_1774111726484.png"), "title": "Calça Pantalona Alfaiataria", "price": "124,90"},
        {"path": os.path.join(base_dir, "modelo_blazer_premium_1774111743219.png"), "title": "Blazer Max Alongado", "price": "99,90"},
        {"path": os.path.join(base_dir, "modelo_vestido_tricot_1774111758825.png"), "title": "Vestido Midi Tricot Canelado", "price": "39,90"},
    ]

    logo_shopee_path = r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium\site\images\logo-shopee.png"
    font_path = "C:\\Windows\\Fonts\\arialbd.ttf"
    
    try:
        font_price = ImageFont.truetype(font_path, 100)
        font_title = ImageFont.truetype(font_path, 40)
        font_cta = ImageFont.truetype(font_path, 35)
    except:
        font_price = font_title = font_cta = ImageFont.load_default()

    for i, item in enumerate(images):
        img = Image.open(item["path"]).convert("RGBA")
        draw = ImageDraw.Draw(img)
        
        # Adicionar Logo Shopee (se não for a capa)
        if i > 0 and os.path.exists(logo_shopee_path):
            logo = Image.open(logo_shopee_path).convert("RGBA")
            logo.thumbnail((200, 80), Image.Resampling.LANCZOS)
            img.paste(logo, (50, 50), logo)

        # Adicionar Preço e Título (se não for a capa)
        if item["price"]:
            # Badge de Preço (Glassmorphism style)
            price_text = f"R$ {item['price']}"
            text_w = font_price.getlength(price_text)
            badge_w, badge_h = int(text_w + 60), 140
            badge_x, badge_y = 50, 850
            
            # Retângulo semi-transparente
            overlay = Image.new('RGBA', img.size, (0,0,0,0))
            overlay_draw = ImageDraw.Draw(overlay)
            overlay_draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=20, fill=(238, 77, 45, 230)) # Laranja Shopee
            img = Image.alpha_composite(img, overlay)
            
            draw = ImageDraw.Draw(img)
            draw.text((badge_x + 30, badge_y + 20), price_text, font=font_price, fill=(255, 255, 255))
            
            # Título
            draw.text((50, badge_y - 60), item["title"].upper(), font=font_title, fill=(255, 255, 255), stroke_width=2, stroke_fill=(0,0,0))

        # Adicionar CTA no último slide
        if i == len(images) - 1:
            cta_text = "Comente 'QUERO' para receber os links! 🔗"
            draw.text((50, 1000), cta_text, font=font_cta, fill=(255, 255, 255), stroke_width=2, stroke_fill=(238, 77, 45))

        # Salvar
        output_path = os.path.join(output_dir, f"fashion_post_{i:02d}.jpg")
        img.convert("RGB").save(output_path, "JPEG", quality=95)
        print(f"Salvo: {output_path}")

if __name__ == "__main__":
    create_carousel()
