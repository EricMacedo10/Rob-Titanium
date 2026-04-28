import os
from moviepy import ImageClip
import logging

# Configuração de Logs Silenciosos para MoviePy para manter o terminal limpo
logging.getLogger('moviepy').setLevel(logging.ERROR)

def image_to_video(image_path, output_path, duration=5, fps=30):
    """
    Converte uma imagem estática (JPG/PNG) em um vídeo MP4 de N segundos.
    Adiciona um efeito sutil de Zoom (Ken Burns) para dinamismo no Reels/Stories.
    """
    print(f"🎬 Convertendo imagem para vídeo com Efeito Zoom: {os.path.basename(image_path)}")
    
    try:
        # 1. Carregar a imagem
        clip = ImageClip(image_path).with_duration(duration)
        
        # 2. Aplicar Efeito de Zoom (Ken Burns)
        # Começa em 100% e vai até 110% do tamanho original
        clip = clip.resized(lambda t: 1 + 0.1 * (t / duration))
        
        # 3. Garantir centralização após o resize
        clip = clip.with_position('center')

        # 4. Renderizar o vídeo (Codec h264 para máxima compatibilidade)
        clip.write_videofile(
            output_path, 
            fps=fps,
            codec='libx264', 
            audio=False, 
            threads=4, 
            logger=None, 
            bitrate="1000k",
            preset='fast' # Rapidez e compressão equilibradas
        )
        
        clip.close()
        
        if os.path.exists(output_path):
            size_mb = os.path.getsize(output_path) / (1024 * 1024)
            print(f"✅ Vídeo 'Titanium Dynamic' gerado ({size_mb:.2f} MB)")
            return True
        return False
            
    except Exception as e:
        print(f"💥 Erro na geração de vídeo dinâmico: {e}")
        return False

if __name__ == "__main__":
    # Teste rápido se executado diretamente
    test_img = "social/temp_post_0.jpg"
    if os.path.exists(test_img):
        image_to_video(test_img, "social/test_conversion.mp4")
    else:
        print(f"Pulei o teste: {test_img} não encontrado.")
