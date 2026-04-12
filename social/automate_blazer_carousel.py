import os
from PIL import Image, ImageDraw, ImageFont

def create_blazer_carousel():
    # Caminhos das imagens geradas
    brain_dir = r"C:\Users\ericm\.gemini\antigravity\brain\c242a9e4-4ab5-4233-8443-d4b5d8698771"
    output_dir = r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium\social\fila"
    os.makedirs(output_dir, exist_ok=True)

    images = [
        {"path": os.path.join(brain_dir, "blazer_carousel_cover_bg_1775670066471.png"), "title": "O Blazer que não pode faltar no seu closet!", "price": None, "type": "cover"},
        {"path": os.path.join(brain_dir, "wife_blazer_office_v2_1775669562328.png"), "title": "Elegância Total para o Trabalho", "price": "108,30"},
        {"path": os.path.join(brain_dir, "wife_blazer_urban_v2_1775669581276.png"), "title": "Look Urbano e Sofisticado", "price": "108,30"},
        {"path": os.path.join(brain_dir, "wife_blazer_luxury_lounge_1775669884443.png"), "title": "Sofisticação para Eventos", "price": "108,30"},
        {"path": os.path.join(brain_dir, "wife_blazer_boutique_1775669908563.png"), "title": "Estilo que Impressiona", "price": "108,30"},
        {"path": os.path.join(brain_dir, "blazer_carousel_cta_bg_1775670085597.png"), "title": "Não perca essa oferta!", "price": None, "type": "cta"},
    ]

    logo_shopee_path = r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium\site\images\logo-shopee.png"
    font_path = "C:\\Windows\\Fonts\\arialbd.ttf"
    
    try:
        font_price = ImageFont.truetype(font_path, 90)
        font_title = ImageFont.truetype(font_path, 45)
        font_main_title = ImageFont.truetype(font_path, 60)
        font_cta = ImageFont.truetype(font_path, 40)
    except:
        font_price = font_title = font_main_title = font_cta = ImageFont.load_default()

    for i, item in enumerate(images):
        img = Image.open(item["path"]).convert("RGBA")
        draw = ImageDraw.Draw(img)
        
        # Adicionar Logo Shopee (nos slides de produto)
        if item.get("price") and os.path.exists(logo_shopee_path):
            logo = Image.open(logo_shopee_path).convert("RGBA")
            # Deixar logo branca/mais clara ou manter original
            logo.thumbnail((250, 100), Image.Resampling.LANCZOS)
            img.paste(logo, (50, 50), logo)

        # Adicionar Preço e Título
        if item.get("type") == "cover":
            # Título da Capa Centralizado
            text = item["title"].upper()
            wrapped_text = "O BLAZER QUE\nNÃO PODE FALTAR\nNO SEU CLOSET!"
            draw.multiline_text((540, 540), wrapped_text, font=font_main_title, fill=(255, 255, 255), anchor="mm", align="center", stroke_width=4, stroke_fill=(238, 77, 45))
        
        elif item.get("type") == "cta":
            # Texto de CTA Centralizado
            cta_text = "Comente 'QUERO'\npara receber o link! 🔗"
            draw.multiline_text((540, 540), cta_text, font=font_main_title, fill=(255, 255, 255), anchor="mm", align="center", stroke_width=4, stroke_fill=(238, 77, 45))
            draw.text((540, 700), "Aproveite agora!", font=font_cta, fill=(255, 255, 255), anchor="mm", stroke_width=2, stroke_fill=(0,0,0))
            
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
            
            # Título do Slide
            draw.text((50, badge_y - 70), item["title"].upper(), font=font_title, fill=(255, 255, 255), stroke_width=3, stroke_fill=(0,0,0))

        # Salvar
        output_path = os.path.join(output_dir, f"blazer_post_{i:02d}.jpg")
        img.convert("RGB").save(output_path, "JPEG", quality=95)
        print(f"Salvo: {output_path}")

if __name__ == "__main__":
    create_blazer_carousel()
