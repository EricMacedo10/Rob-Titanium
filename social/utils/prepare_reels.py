from moviepy import VideoFileClip, ColorClip, CompositeVideoClip
import os

def prepare_for_reels(input_path, output_path):
    print(f"🔧 Preparando vídeo para Reels: {input_path}")
    
    try:
        # 1. Carregar clipe
        clip = VideoFileClip(input_path)
        
        # 2. Configurar dimensões do Reels (1080x1920)
        target_w = 1080
        target_h = 1920
        
        # Redimensionar o vídeo original para caber na largura do reels (1080)
        # Mantendo o aspect ratio original (1920x1080 -> 1080x607.5)
        clip_resized = clip.resized(width=target_w)
        
        # Criar um fundo (pode ser preto ou um gradiente festivo)
        # Vou usar preto para ser seguro, mas centralizado
        bg = ColorClip(size=(target_w, target_h), color=(0, 0, 0)).with_duration(clip.duration)
        
        # Compor: Vídeo centralizado no Reels
        final_clip = CompositeVideoClip([
            bg,
            clip_resized.with_position('center')
        ])
        
        # 3. Renderizar (Codec h264, 30fps)
        final_clip.write_videofile(
            output_path,
            fps=30,
            codec='libx264',
            audio_codec='aac',
            threads=4,
            preset='slow'
        )
        
        clip.close()
        final_clip.close()
        
        print(f"✅ Vídeo otimizado para Reels: {output_path}")
        return True
    except Exception as e:
        print(f"💥 Erro na preparação do Reels: {e}")
        return False

if __name__ == "__main__":
    input_video = "social/fila/Oferta Certa Carnaval.mp4"
    output_video = "social/fila/Oferta Certa Carnaval_reels.mp4"
    prepare_for_reels(input_video, output_video)
