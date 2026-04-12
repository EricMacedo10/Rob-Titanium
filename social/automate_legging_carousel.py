import os
import json
from PIL import Image, ImageDraw, ImageFont

def create_carousel():
    # Caminhos das imagens geradas por IA
    base_dir = r"C:\Users\ericm\.gemini\antigravity\brain\b6aba381-d961-41ea-ac66-b12ede4198fe"
    output_dir = r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium\social\fila"
    os.makedirs(output_dir, exist_ok=True)

    images = [
        {"path": os.path.join(base_dir, "legging_cover_v1_1775499398303.png"), "title": "Calça Legging Fitness com Bolso", "subtitle": "Estilo & Praticidade", "price": None},
        {"path": os.path.join(base_dir, "legging_blonde_v1_1775499413226.png"), "title": "Flexibilidade Extrema", "subtitle": "A liberdade que você precisa", "price": "36,90"},
        {"path": os.path.join(base_dir, "legging_plussize_v1_1775499427684.png"), "title": "Modelagem Perfeita", "subtitle": "Cintura alta para suporte total", "price": "36,90"},
        {"path": os.path.join(base_dir, "legging_brunette_v1_1775499441625.png"), "title": "Estilo para o Dia a Dia", "subtitle": "Versatilidade e Conforto", "price": "36,90"},
        {"path": os.path.join(base_dir, "legging_blackwoman_v2_fullbody_1775499888366.png"), "title": "Squat-Proof", "subtitle": "Segurança em cada movimento", "price": "36,90"},
        {"path": os.path.join(base_dir, "legging_mature_v1_1775499469717.png"), "title": "Praticidade com Bolso", "subtitle": "Seu celular sempre à mão", "price": "36,90"},
    ]

    logo_amazon_path = r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium\site\images\logo-amazon.png"
    font_path = "C:\\Windows\\Fonts\\arialbd.ttf"
    
    try:
        font_price = ImageFont.truetype(font_path, 90)
        font_title = ImageFont.truetype(font_path, 50)
        font_subtitle = ImageFont.truetype(font_path, 35)
        font_cta = ImageFont.truetype(font_path, 40)
    except:
        font_price = font_title = font_subtitle = font_cta = ImageFont.load_default()

    for i, item in enumerate(images):
        if not os.path.exists(item["path"]):
            print(f"ERRO: Arquivo não encontrado: {item['path']}")
            continue
            
        img = Image.open(item["path"]).convert("RGBA")
        draw = ImageDraw.Draw(img)
        
        # Adicionar Logo Amazon
        if os.path.exists(logo_amazon_path):
            logo = Image.open(logo_amazon_path).convert("RGBA")
            logo.thumbnail((250, 100), Image.Resampling.LANCZOS)
            img.paste(logo, (50, 50), logo)

        # Adicionar Preço (Badge Azul Amazon Style ou Laranja Destaque)
        if item["price"]:
            price_text = f"R$ {item['price']}"
            text_w = font_price.getlength(price_text)
            badge_w, badge_h = int(text_w + 60), 120
            badge_x, badge_y = 50, 880
            
            # Retângulo semi-transparente
            overlay = Image.new('RGBA', img.size, (0,0,0,0))
            overlay_draw = ImageDraw.Draw(overlay)
            # Cor Amazon Prime/Blue: (35, 47, 62, 230) ou Laranja Amazon: (255, 153, 0, 230)
            overlay_draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=20, fill=(255, 153, 0, 230))
            img = Image.alpha_composite(img, overlay)
            
            draw = ImageDraw.Draw(img)
            draw.text((badge_x + 30, badge_y + 15), price_text, font=font_price, fill=(255, 255, 255))
            
            # Título e Subtítulo
            draw.text((50, badge_y - 120), item["title"].upper(), font=font_title, fill=(255, 255, 255), stroke_width=2, stroke_fill=(0,0,0))
            draw.text((50, badge_y - 60), item["subtitle"], font=font_subtitle, fill=(255, 255, 255), stroke_width=1, stroke_fill=(0,0,0))
        else:
            # Título na Capa
            draw.text((50, 850), item["title"].upper(), font=font_title, fill=(255, 255, 255), stroke_width=3, stroke_fill=(0,0,0))
            draw.text((50, 920), item["subtitle"], font=font_subtitle, fill=(255, 255, 255), stroke_width=2, stroke_fill=(0,0,0))

        # Adicionar CTA no último slide
        if i == len(images) - 1:
            cta_text = "Comente 'QUERO' e te envio o link 🔗"
            # Overlay para CTA
            overlay_cta = Image.new('RGBA', img.size, (0,0,0,0))
            octa_draw = ImageDraw.Draw(overlay_cta)
            octa_draw.rectangle([0, 1000, 1080, 1080], fill=(0, 0, 0, 180))
            img = Image.alpha_composite(img, overlay_cta)
            
            draw = ImageDraw.Draw(img)
            draw.text((150, 1020), cta_text, font=font_cta, fill=(255, 255, 255))

        # Salvar
        output_path = os.path.join(output_dir, f"legging_post_{i:02d}.jpg")
        img.convert("RGB").save(output_path, "JPEG", quality=95)
        print(f"Salvo: {output_path}")

if __name__ == "__main__":
    create_carousel()
