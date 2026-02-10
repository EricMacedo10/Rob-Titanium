import os
import sys
from dotenv import load_dotenv

# Add social to path to import ImageGenerator
sys.path.append(os.path.join(os.getcwd(), 'social'))

try:
    from image_generator import ImageGenerator
except ImportError:
    # If standard import fails, try relative to root
    from social.image_generator import ImageGenerator

def run_test():
    print(f"\n{'='*20} SENIOR IMAGE SERVICE TEST {'='*20}")
    
    # 1. Initialize Generator
    assets = os.path.join(os.getcwd(), "site", "images")
    if not os.path.exists(assets):
        print(f"❌ Assets path error: {assets} not found")
        return

    gen = ImageGenerator(assets_path=assets)
    print(f"[INIT]      ✅ ImageGenerator ready (Assets: {assets})")

    # 2. Mock Data for Test
    product = "PRODUTO TESTE SENIOR - Verificação de Sistema"
    price = "99,90"
    # Use a reliable public image for testing (Google logo)
    img_url = "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png"
    output = "scripts/test_senior_banner.jpg"

    # 3. Generate
    print(f"[GENERATE]  Attempting to create: {output}...")
    try:
        gen.generate_post(
            product_title=product,
            price=price,
            image_url=img_url,
            store_type="amazon",
            output_path=output
        )
        
        if os.path.exists(output):
            size = os.path.getsize(output)
            print(f"[SUCCESS]   ✅ Banner generated ({size} bytes)")
            print(f"[FILE]      Path: {os.path.abspath(output)}")
        else:
            print("❌ Banner script finished but file is missing")
            
    except Exception as e:
        print(f"❌ Generation FAILED: {e}")

if __name__ == "__main__":
    run_test()
