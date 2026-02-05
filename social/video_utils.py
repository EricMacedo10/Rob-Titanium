import os
from moviepy import ImageClip
import logging

# Configuração de Logs Silenciosos para MoviePy para manter o terminal limpo
logging.getLogger('moviepy').setLevel(logging.ERROR)

def image_to_video(image_path, output_path, duration=5, fps=30):
    """
    Converte uma imagem estática (JPG/PNG) em um vídeo MP4 de N segundos.
    Ideal para transformar artes estáticas em Reels/Stories de vídeo.
    """
    print(f"🎬 Convertendo imagem para vídeo: {os.path.basename(image_path)} -> {os.path.basename(output_path)}")
    
    try:
        # 1. Carregar a imagem como um clip
        clip = ImageClip(image_path).with_duration(duration)
        
        # 2. Configurar FPS (30 é o padrão ouro para Instagram)
        # No moviepy 2.0, some parameters are better passed to write_videofile
        
        # 3. Renderizar o vídeo
        clip.write_videofile(
            output_path, 
            fps=fps,
            codec='libx264', 
            audio=False, 
            threads=4, 
            logger=None, 
            preset='ultrafast'
        )
        
        # 4. Fechar o clip para liberar recursos
        clip.close()
        
        if os.path.exists(output_path):
            size_mb = os.path.getsize(output_path) / (1024 * 1024)
            print(f"✅ Vídeo gerado com sucesso ({size_mb:.2f} MB)")
            return True
        else:
            print("❌ Falha: O arquivo de saída não foi encontrado após o processamento.")
            return False
            
    except Exception as e:
        print(f"💥 Erro crítico na conversão de vídeo: {e}")
        return False

if __name__ == "__main__":
    # Teste rápido se executado diretamente
    test_img = "social/temp_post_0.jpg"
    if os.path.exists(test_img):
        image_to_video(test_img, "social/test_conversion.mp4")
    else:
        print(f"Pulei o teste: {test_img} não encontrado.")
