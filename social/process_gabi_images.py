import os
import json
from PIL import Image, ImageDraw, ImageFont

def process_gabi_carousel():
    # Caminhos das imagens geradas por IA (caminhos absolutos conforme retorno da ferramenta)
    base_dir = r"C:\Users\ericm\.gemini\antigravity\brain\77986c9f-30e3-40da-8a95-3dd5293ea29a"
    output_dir = r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium\social\fila"
    os.makedirs(output_dir, exist_ok=True)

    # Nomes dos arquivos gerados (substitua pelos nomes reais se necessário, mas vou usar os padronizados)
    image_files = [
        "fashion_gabi_capa_1774994218111.png",
        "fashion_gabi_blonde_1774994238545.png",
        "fashion_gabi_brunette_1774994260037.png",
        "fashion_gabi_plus_size_1774994277285.png",
        "fashion_gabi_black_1774994295680.png",
        "fashion_gabi_mature_1774994315896.png"
    ]

    items = [
        {"path": os.path.join(base_dir, f), "title": "Conjunto Gabi Alfaiataria", "price": "65,99"}
        for f in image_files
    ]
    # Ajustar o primeiro para "Capa" (sem preço no badge talvez)
    items[0]["title"] = "Elegância & Estilo"
    items[0]["price"] = None

    logo_shopee_path = r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium\site\images\logo-shopee.png"
    font_path = "C:\\Windows\\Fonts\\arialbd.ttf"
    
    try:
        font_price = ImageFont.truetype(font_path, 100)
        font_title = ImageFont.truetype(font_path, 45)
        font_cta = ImageFont.truetype(font_path, 35)
    except:
        font_price = font_title = font_cta = ImageFont.load_default()

    for i, item in enumerate(items):
        if not os.path.exists(item["path"]):
            print(f"❌ Imagem não encontrada: {item['path']}")
            continue

        img = Image.open(item["path"]).convert("RGBA")
        
        # Redimensionar para 1080x1350 (formato Reels/Feed Instagram Portrait)
        # Se a imagem for quadrada (1024x1024), vamos centralizar ou preencher
        target_size = (1080, 1350)
        # Resize mantendo proporção e preenchendo
        img_aspect = img.width / img.height
        target_aspect = target_size[0] / target_size[1]
        
        if img_aspect > target_aspect: # Imagem é mais larga que o alvo
            new_height = target_size[1]
            new_width = int(new_height * img_aspect)
        else:
            new_width = target_size[0]
            new_height = int(new_width / img_aspect)
            
        img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Crop para o centro
        left = (new_width - target_size[0]) / 2
        top = (new_height - target_size[1]) / 2
        right = (new_width + target_size[0]) / 2
        bottom = (new_height + target_size[1]) / 2
        img = img_resized.crop((left, top, right, bottom))

        draw = ImageDraw.Draw(img)
        
        # Adicionar Logo Shopee (em todos exceto talvez a capa, ou em todos)
        if os.path.exists(logo_shopee_path):
            logo = Image.open(logo_shopee_path).convert("RGBA")
            logo.thumbnail((180, 70), Image.Resampling.LANCZOS)
            img.paste(logo, (target_size[0] - 220, 50), logo)

        # Adicionar Preço e Título
        if item["price"]:
            price_text = f"R$ {item['price']}"
            text_w = font_price.getlength(price_text)
            badge_w, badge_h = int(text_w + 60), 140
            badge_x, badge_y = 50, 1100 # Parte inferior
            
            # Badge Shopee Style (Laranja)
            overlay = Image.new('RGBA', img.size, (0,0,0,0))
            overlay_draw = ImageDraw.Draw(overlay)
            overlay_draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=25, fill=(238, 77, 45, 240))
            img = Image.alpha_composite(img, overlay)
            
            draw = ImageDraw.Draw(img)
            draw.text((badge_x + 30, badge_y + 20), price_text, font=font_price, fill=(255, 255, 255))
            
            # Título acima do preço
            draw.text((55, badge_y - 70), item["title"].upper(), font=font_title, fill=(255, 255, 255), stroke_width=2, stroke_fill=(0,0,0))
        elif i == 0:
            # Texto especial para a capa
            draw.text((50, 1000), "CONJUNTO GABI", font=font_price, fill=(255, 255, 255), stroke_width=3, stroke_fill=(238, 77, 45))
            draw.text((55, 1110), "ALFAIATARIA PREMIUM", font=font_title, fill=(255, 255, 255), stroke_width=2, stroke_fill=(0,0,0))

        # Aviso de imagens ilustrativas (Small text bottom right)
        notice_text = "Imagens Ilustrativas / I.A."
        try:
            font_small = ImageFont.truetype(font_path, 20)
        except:
            font_small = ImageFont.load_default()
        
        draw.text((target_size[0] - 250, target_size[1] - 40), notice_text, font=font_small, fill=(200, 200, 200), stroke_width=1, stroke_fill=(0,0,0))

        # Adicionar CTA no último slide
        if i == len(items) - 1:
            cta_text = "Comente 'QUERO' para o link! 🔗"
            draw.text((50, 1220), cta_text, font=font_cta, fill=(255, 255, 255), stroke_width=2, stroke_fill=(238, 77, 45))

        # Salvar na fila
        output_path = os.path.join(output_dir, f"gabi_post_{i:02d}.jpg")
        img.convert("RGB").save(output_path, "JPEG", quality=95)
        print(f"Salvo: {output_path}")

if __name__ == "__main__":
    process_gabi_carousel()
