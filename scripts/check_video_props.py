from moviepy import VideoFileClip
import os

def check_video(path):
    if not os.path.exists(path):
        print(f"File {path} not found")
        return
    
    try:
        clip = VideoFileClip(path)
        print(f"Resolution: {clip.w}x{clip.h}")
        print(f"Duration: {clip.duration}s")
        print(f"FPS: {clip.fps}")
        clip.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_video("social/fila/Oferta Certa Carnaval.mp4")
