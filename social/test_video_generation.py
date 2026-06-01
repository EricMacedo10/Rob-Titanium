import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from core.video_generator import VideoGenerator

def test_reel():
    print("🚀 Iniciando Teste da Máquina de Reels...")
    gen = VideoGenerator()
    
    test_img = "https://cf.shopee.com.br/file/br-11134207-820m8-mlpploslju2u99"
    test_price = "89,90"
    print("\n--- Gerando REEL ---")
    output_reel = gen.generate_video(
        product_url=test_img,
        price=test_price,
        store_type="shopee",
        output_filename="meu_primeiro_reel.mp4",
        video_type="reel"
    )
    
    print("\n--- Gerando STORY ---")
    output_story = gen.generate_video(
        product_url=test_img,
        price=test_price,
        store_type="shopee",
        output_filename="meu_primeiro_story.mp4",
        video_type="story"
    )
    
    print("\n✅ Arquivos Gerados com Sucesso!")

if __name__ == "__main__":
    test_reel()
