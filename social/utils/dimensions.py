from PIL import Image
import os

images = [
    'site/images/banner_carnaval_amazon.png',
    'site/images/banner_carnaval_mercadolivre.png',
    'site/images/banner_carnaval_shopee.png'
]

print("--- Image Dimensions Report ---")
for img_path in images:
    if os.path.exists(img_path):
        with Image.open(img_path) as img:
            w, h = img.size
            print(f"{img_path}: {w}x{h} (Ratio: {w/h:.2f})")
    else:
        print(f"File not found: {img_path}")
