import os
from PIL import Image, ImageOps, ImageEnhance

def rebrand_banner(source_path, logo_path, output_path, target_color_rgb):
    if not os.path.exists(source_path):
        print(f"Error: Source {source_path} not found")
        return

    # 1. Load the Master Template (The ML Box banner which is clean)
    img = Image.open(source_path).convert("RGBA")
    
    # 2. Color Transformation (Yellow to Orange/Amazon)
    # Since it's yellow, we can use a colorize or just a hue shift
    # For simplicity and quality, we'll overlay a color layer with 'multiply' or 'overlay' mode
    # Or just adjust the image data
    data = img.getdata()
    new_data = []
    for item in data:
        # If it's yellow-ish (high R and G), shift it towards Orange (reduce G)
        r, g, b, a = item
        if r > 150 and g > 150: # Yellow range
            # Adjust G to make it more orange (Amazon is approx 255, 153, 0)
            # ML is approx 255, 230, 0
            new_g = int(g * 0.65)
            new_data.append((r, new_g, b, a))
        else:
            new_data.append(item)
    img.putdata(new_data)

    # 3. Paste Amazon Logo over the previous branding
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        # Resize logo to fit the box area
        logo.thumbnail((250, 150), Image.Resampling.LANCZOS)
        
        # Determine position (center-bottom area of the box)
        # In the ML template, the handshake is roughly in the middle of the box
        pos = ((img.width - logo.width) // 2, img.height - logo.height - 250)
        
        # Paste with alpha
        img.paste(logo, pos, logo)

    # 4. Final Save
    img.convert("RGB").save(output_path, "JPEG", quality=95)
    print(f"✅ Clean Amazon Banner created: {output_path}")

if __name__ == "__main__":
    rebrand_banner(
        "site/images/banner_carnaval_mercadolivre.png",
        "site/images/logo-amazon.png",
        "site/images/banner_carnaval_amazon.png",
        (255, 153, 0)
    )
