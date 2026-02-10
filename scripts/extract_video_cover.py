from moviepy import VideoFileClip
import os

def extract_cover(video_path, output_path):
    print(f"🖼️ Extraindo capa do vídeo: {video_path}")
    try:
        clip = VideoFileClip(video_path)
        # Pega o frame em 1 segundo (ou na metade se for muito curto)
        t = min(1.0, clip.duration / 2)
        clip.save_frame(output_path, t=t)
        clip.close()
        print(f"✅ Capa extraída: {output_path}")
        return True
    except Exception as e:
        print(f"💥 Erro ao extrair capa: {e}")
        return False

if __name__ == "__main__":
    extract_cover("social/fila/Oferta Certa Carnaval_reels.mp4", "social/fila/Oferta Certa Carnaval_cover.jpg")
