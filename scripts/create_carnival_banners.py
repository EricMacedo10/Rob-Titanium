import os
from PIL import Image, ImageDraw, ImageFont

def create_festive_banner(brand, title, output_path, bg_color, text_color):
    # Constants
    width, height = 800, 600
    
    # 1. Create Base Background with Gradient
    base = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(base)
    
    # Add simple festive pattern (Circles/Confetti)
    import random
    colors = [(255, 255, 255), (255, 200, 0), (0, 255, 200), (255, 0, 255)]
    for _ in range(100):
        x = random.randint(0, width)
        y = random.randint(0, height)
        r = random.randint(5, 15)
        draw.ellipse([x-r, y-r, x+r, y+r], fill=random.choice(colors))

    # 2. Add Brand Logo
    logo_path = f"site/images/logo-{brand}.png"
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        logo.thumbnail((200, 100), Image.Resampling.LANCZOS)
        base.paste(logo, (20, 20), logo)

    # 3. Add Campaign Text
    try:
        font_path = "C:\\Windows\\Fonts\\arialbd.ttf"
        font_main = ImageFont.truetype(font_path, 80)
        font_sub = ImageFont.truetype(font_path, 40)
    except:
        font_main = font_sub = ImageFont.load_default()

    # Draw centered text with shadow
    text = "CARNAVAL"
    sub_text = "DE OFERTAS"
    
    tw = draw.textlength(text, font=font_main)
    sw = draw.textlength(sub_text, font=font_sub)
    
    # Shadow
    draw.text(((width-tw)//2 + 5, height//2 - 60 + 5), text, font=font_main, fill=(0,0,0))
    draw.text(((width-tw)//2, height//2 - 60), text, font=font_main, fill=(255,255,255))
    
    draw.text(((width-sw)//2 + 3, height//2 + 40 + 3), sub_text, font=font_sub, fill=(0,0,0))
    draw.text(((width-sw)//2, height//2 + 40), sub_text, font=font_sub, fill=(255,255,255))

    # 4. Save
    base.save(output_path, "PNG")
    print(f"✅ Banner created: {output_path}")

if __name__ == "__main__":
    # Create the 3 banners
    create_festive_banner("amazon", "Carnaval Amazon", "site/images/banner_carnaval_amazon.png", (255, 153, 0), (255, 255, 255))
    create_festive_banner("mercadolivre", "Carnaval ML", "site/images/banner_carnaval_mercadolivre.png", (255, 230, 0), (51, 51, 51))
    create_festive_banner("shopee", "Carnaval Shopee", "site/images/banner_carnaval_shopee.png", (238, 77, 45), (255, 255, 255))
