import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_premium_banner(brand, highlight_path, output_path, brand_name):
    width, height = 1000, 1000  # High res for premium feel
    
    # 1. Background Gradient (Warm/Festive)
    base = Image.new('RGB', (width, height), (255, 120, 0)) # Base orange
    draw = ImageDraw.Draw(base)
    
    # Simple radial gradient effect
    for i in range(width // 2, 0, -2):
        color = (255, min(255, 120 + (width//2 - i)//2), 0)
        draw.ellipse([width//2 - i, height//2 - i, width//2 + i, height//2 + i], outline=color, width=2)

    # 2. Add Festive Elements (Confetti/Streamers)
    confetti_colors = [(255, 255, 255), (255, 215, 0), (0, 255, 255), (255, 0, 255), (0, 255, 0)]
    for _ in range(150):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(5, 15)
        draw.rectangle([x, y, x+size, y+size], fill=random.choice(confetti_colors))
        # Streamers (lines)
        if random.random() > 0.7:
            draw.line([x, y, x+random.randint(20, 50), y+random.randint(20, 50)], fill=random.choice(confetti_colors), width=3)

    # 3. Add Central Highlight (The 3D Brand Element)
    if os.path.exists(highlight_path):
        highlight = Image.open(highlight_path).convert("RGBA")
        # Scale to central focus
        highlight.thumbnail((700, 700), Image.Resampling.LANCZOS)
        
        # Add shadow for the highlight
        shadow = Image.new("RGBA", highlight.size, (0, 0, 0, 80))
        base.paste(shadow, ((width - highlight.width)//2 + 20, (height - highlight.height)//2 + 50 + 20), shadow)
        
        base.paste(highlight, ((width - highlight.width)//2, (height - highlight.height)//2 + 50), highlight)

    # 4. Premium Text "CARNAVAL DE OFERTAS"
    try:
        font_path = "C:\\Windows\\Fonts\\arialbd.ttf"
        font_top = ImageFont.truetype(font_path, 110)
        font_brand = ImageFont.truetype(font_path, 80)
    except:
        font_top = font_brand = ImageFont.load_default()

    def draw_premium_text(text, y, font, fill):
        # Outline/Shadow for 3D effect
        tw = draw.textlength(text, font=font)
        x = (width - tw) // 2
        # Multiple layers for depth
        for offset in range(10, 0, -1):
            draw.text((x + offset, y + offset), text, font=font, fill=(0, 0, 0, 100))
        draw.text((x, y), text, font=font, fill=fill)

    draw_premium_text("CARNAVAL DE OFERTAS", 100, font_top, (255, 215, 0)) # Gold
    draw_premium_text(brand_name.upper(), 230, font_brand, (255, 255, 255))

    # 5. Save
    # We save as PNG first then convert if needed, but the web likes PNG/JPG
    base.convert("RGB").save(output_path, "JPEG", quality=95)
    print(f"✅ Premium Banner created: {output_path}")

if __name__ == "__main__":
    # Create ML and Shopee versions
    create_premium_banner(
        "mercadolivre", 
        "site/images/highlight-mercadolivre.png", 
        "site/images/banner_carnaval_mercadolivre.png", 
        "Mercado Livre"
    )
    create_premium_banner(
        "shopee", 
        "site/images/highlight-shopee.png", 
        "site/images/banner_carnaval_shopee.png", 
        "Shopee"
    )
