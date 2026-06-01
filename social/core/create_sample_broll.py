import os
from moviepy import ColorClip

def create_sample_broll():
    output_path = os.path.join(os.path.dirname(__file__), "..", "assets", "broll", "sample.mp4")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Criar um clipe de cor slida (azul bem escuro/cinza) de 5 segundos, 1080x1920
    clip = ColorClip(size=(1080, 1920), color=(40, 44, 52), duration=5)
    clip = clip.with_fps(24)
    clip.write_videofile(output_path, codec="libx264", audio=False)
    print(f"Sample broll criado em: {output_path}")

if __name__ == "__main__":
    create_sample_broll()
