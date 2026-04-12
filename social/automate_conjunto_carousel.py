import os
from PIL import Image, ImageDraw, ImageFont

def create_conjunto_carousel():
    # Caminhos das imagens geradas
    brain_dir = r"C:\Users\ericm\.gemini\antigravity\brain\72eab431-44e7-4cd8-88ea-9256fd10080a"
    output_dir = r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium\social\fila"
    os.makedirs(output_dir, exist_ok=True)

    # Imagens Geradas (Ajustar caminhos com base nos IDs gerados)
    images = [
        {"path": os.path.join(brain_dir, "wife_conjunto_alfaiataria_lounge_1775754026034.png"), "title": "Elegância & Praticidade: O Conjunto que define o seu Verão!", "price": None, "type": "cover"},
        {"path": os.path.join(brain_dir, "wife_conjunto_alfaiataria_cafe_1775754042595.png"), "title": "", "price": "59,99"},
        {"path": os.path.join(brain_dir, "wife_conjunto_alfaiataria_garden_1775754057705.png"), "title": "", "price": "59,99"},
        {"path": os.path.join(brain_dir, "wife_conjunto_alfaiataria_boutique_1775754072622.png"), "title": "", "price": "59,99"},
        # Adicionar imagem bônus (última) - CTA
        {"path": os.path.join(brain_dir, "wife_conjunto_alfaiataria_boutique_1775754072622.png"), "title": "Aproveite! Edição Limitada", "price": None, "type": "cta"},
    ]

    logo_shopee_path = r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium\site\images\logo-shopee.png"
    font_path = "C:\\Windows\\Fonts\\arialbd.ttf"
    
    try:
        font_price = ImageFont.truetype(font_path, 90)
        font_title = ImageFont.truetype(font_path, 45)
        font_main_title = ImageFont.truetype(font_path, 65)
        font_cta = ImageFont.truetype(font_path, 40)
    except:
        font_price = font_title = font_main_title = font_cta = ImageFont.load_default()

    for i, item in enumerate(images):
        if not os.path.exists(item["path"]):
            print(f"ERRO: Arquivo não encontrado: {item['path']}")
            continue
            
        img = Image.open(item["path"]).convert("RGBA")
        
        # Redimensionar para 1080x1080 (Se não estiver)
        img = img.resize((1080, 1080), Image.Resampling.LANCZOS)
        
        draw = ImageDraw.Draw(img)
        
        # Adicionar Logo Shopee (nos slides de produto)
        if item.get("price") and os.path.exists(logo_shopee_path):
            logo = Image.open(logo_shopee_path).convert("RGBA")
            logo.thumbnail((250, 100), Image.Resampling.LANCZOS)
            img.paste(logo, (50, 50), logo)

        # Adicionar Preço e Título
        if item.get("type") == "cover":
            # Título da Capa - Overlay escuro na base
            overlay = Image.new('RGBA', img.size, (0,0,0,0))
            odraw = ImageDraw.Draw(overlay)
            odraw.rectangle([0, 700, 1080, 1080], fill=(0, 0, 0, 150))
            img = Image.alpha_composite(img, overlay)
            
            draw = ImageDraw.Draw(img)
            text = item["title"].upper()
            wrapped_text = "CONJUNTO ALFAIATARIA\nOMBRO ÚNICO\nCINTURA MARCADA"
            draw.multiline_text((540, 890), wrapped_text, font=font_main_title, fill=(255, 255, 255), anchor="mm", align="center", stroke_width=2, stroke_fill=(0,0,0))
        
        elif item.get("type") == "cta":
            # Texto de CTA Centralizado
            cta_text = "Comente 'QUERO'\npara o Link! 🔗"
            
            overlay = Image.new('RGBA', img.size, (0,0,0,0))
            odraw = ImageDraw.Draw(overlay)
            odraw.rectangle([0, 0, 1080, 1080], fill=(0, 0, 0, 120))
            img = Image.alpha_composite(img, overlay)
            
            draw = ImageDraw.Draw(img)
            draw.multiline_text((540, 500), cta_text, font=font_main_title, fill=(255, 255, 255), anchor="mm", align="center", stroke_width=4, stroke_fill=(238, 77, 45))
            draw.text((540, 700), "Aproveite a oferta Shopee!", font=font_cta, fill=(255, 255, 255), anchor="mm")
            
        elif item["price"]:
            # Badge de Preço
            price_text = f"R$ {item['price']}"
            text_w = font_price.getlength(price_text)
            badge_w, badge_h = int(text_w + 60), 130
            badge_x, badge_y = 50, 850
            
            overlay = Image.new('RGBA', img.size, (0,0,0,0))
            overlay_draw = ImageDraw.Draw(overlay)
            overlay_draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=20, fill=(238, 77, 45, 240)) # Laranja Shopee
            img = Image.alpha_composite(img, overlay)
            
            draw = ImageDraw.Draw(img)
            draw.text((badge_x + 30, badge_y + 20), price_text, font=font_price, fill=(255, 255, 255))
            
            # Título do Slide (Removido conforme solicitado)
            if item.get("title"):
                title_text = item["title"].upper()
                draw.text((50, badge_y - 80), title_text, font=font_title, fill=(255, 255, 255), stroke_width=3, stroke_fill=(0,0,0))

        # Salvar
        output_path = os.path.join(output_dir, f"conjunto_post_{i:02d}.jpg")
        img.convert("RGB").save(output_path, "JPEG", quality=95)
        print(f"Salvo: {output_path}")

if __name__ == "__main__":
    create_conjunto_carousel()
