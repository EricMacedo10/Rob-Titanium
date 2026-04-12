import os
from PIL import Image, ImageDraw, ImageFont

def create_macaquinho_carousel():
    brain_dir = r"C:\Users\ericm\.gemini\antigravity\brain\f966bf98-002e-4486-819d-9c8ea153be13"
    output_dir = r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium\social\fila"
    os.makedirs(output_dir, exist_ok=True)

    # Preço Oficial
    price = "104,50"
    
    images = [
        {"path": os.path.join(brain_dir, "model_shaper_01_diversity_1775854774008.png"), "title": "CONCURSO DE CURVAS: MODELADOR PREMIUM 💎", "price": None, "type": "cover"},
        {"path": os.path.join(brain_dir, "model_shaper_01_diversity_1775854774008.png"), "title": "", "price": price},
        {"path": os.path.join(brain_dir, "model_shaper_02_diversity_black_1775854798591.png"), "title": "", "price": price},
        {"path": os.path.join(brain_dir, "model_shaper_03_diversity_asian_1775854827323.png"), "title": "", "price": price},
        {"path": os.path.join(brain_dir, "model_shaper_04_diversity_brunette_1775854850441.png"), "title": "", "price": price},
        {"path": os.path.join(brain_dir, "model_shaper_04_diversity_brunette_1775854850441.png"), "title": "COMENTE 'QUERO'\nPARA O LINK! 🔗", "price": None, "type": "cta"},
    ]

    logo_shopee_path = r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium\site\images\logo-shopee.png"
    font_path = "C:\\Windows\\Fonts\\arialbd.ttf"
    font_simple = "C:\\Windows\\Fonts\\arial.ttf"
    
    try:
        font_price = ImageFont.truetype(font_path, 90)
        font_main_title = ImageFont.truetype(font_path, 60)
        font_disclaimer = ImageFont.truetype(font_simple, 25)
    except:
        font_price = font_main_title = font_disclaimer = ImageFont.load_default()

    for i, item in enumerate(images):
        if not os.path.exists(item["path"]):
            continue

        img = Image.open(item["path"]).convert("RGBA")
        draw = ImageDraw.Draw(img)
        
        # Adicionar Logo Shopee (nos slides de produto)
        if item.get("price") and os.path.exists(logo_shopee_path):
            logo = Image.open(logo_shopee_path).convert("RGBA")
            logo.thumbnail((250, 100), Image.Resampling.LANCZOS)
            img.paste(logo, (50, 50), logo)

        # Capa e CTA
        if item.get("type") == "cover":
            text = item["title"]
            draw.multiline_text((img.width//2, 150), text, font=font_main_title, fill=(255, 255, 255), anchor="mm", align="center", stroke_width=4, stroke_fill=(238, 77, 45))
        
        elif item.get("type") == "cta":
            cta_text = item["title"]
            draw.multiline_text((img.width//2, img.height//2), cta_text, font=font_main_title, fill=(255, 255, 255), anchor="mm", align="center", stroke_width=4, stroke_fill=(238, 77, 45))
            
        elif item.get("price"):
            # Badge de Preço
            price_text = f"R$ {item['price']}"
            text_w = font_price.getlength(price_text)
            badge_w, badge_h = int(text_w + 60), 130
            badge_x, badge_y = 50, img.height - 230
            
            overlay = Image.new('RGBA', img.size, (0,0,0,0))
            overlay_draw = ImageDraw.Draw(overlay)
            overlay_draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=20, fill=(238, 77, 45, 240)) # Laranja Shopee
            img = Image.alpha_composite(img, overlay)
            
            draw = ImageDraw.Draw(img)
            draw.text((badge_x + 30, badge_y + 20), price_text, font=font_price, fill=(255, 255, 255))

        # Disclaimer no rodapé
        disclaimer = "* imagem ilustrativa"
        dis_w = font_disclaimer.getlength(disclaimer)
        draw.text((img.width - dis_w - 50, img.height - 50), disclaimer, font=font_disclaimer, fill=(255, 255, 255), stroke_width=1, stroke_fill=(0,0,0))

        # Salvar
        output_path = os.path.join(output_dir, f"macaquinho_post_{i:02d}.jpg")
        img.convert("RGB").save(output_path, "JPEG", quality=95)
        print(f"Salvo: {output_path}")

if __name__ == "__main__":
    create_macaquinho_carousel()
