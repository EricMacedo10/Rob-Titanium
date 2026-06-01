import os
import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
import requests

# Diretório de áudios
AUDIO_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

# Lista de áudios Premium (Lo-fi / Aesthetic / Instrumental) sem direitos autorais
AUDIO_LINKS = [
    {
        "nome": "aesthetic_lofi_1.mp3",
        "url": "https://files.freemusicarchive.org/storage-freemusicarchive-org/music/WFMU/Broke_For_Free/Directionless_EP/Broke_For_Free_-_01_-_Night_Owl.mp3"
    },
    {
        "nome": "fashion_upbeat_2.mp3",
        "url": "https://files.freemusicarchive.org/storage-freemusicarchive-org/music/ccCommunity/Jahzzar/Tumbling_Dishes_Like_Old-Man_Wishes/Jahzzar_-_01_-_Siesta.mp3"
    },
    {
        "nome": "luxury_minimalist_3.mp3",
        "url": "https://files.freemusicarchive.org/storage-freemusicarchive-org/music/Creative_Commons/Ketsa/Raising_Frequecy/Ketsa_-_04_-_Dust_Bros.mp3"
    },
    {
        "nome": "chill_vibes_4.mp3",
        "url": "https://files.freemusicarchive.org/storage-freemusicarchive-org/music/no_curator/Tours/Enthusiast/Tours_-_01_-_Enthusiast.mp3"
    }
]

def download_audios():
    print(f"🎵 Iniciando download da Biblioteca de Áudios Premium na pasta: {AUDIO_DIR}")
    
    headers = {"User-Agent": "Mozilla/5.0"}
    
    for audio in AUDIO_LINKS:
        filepath = os.path.join(AUDIO_DIR, audio["nome"])
        
        if os.path.exists(filepath):
            print(f"✅ {audio['nome']} já existe. Pulando...")
            continue
            
        print(f"⬇️ Baixando {audio['nome']}...")
        try:
            resp = requests.get(audio["url"], headers=headers, stream=True, timeout=30)
            if resp.status_code == 200:
                with open(filepath, 'wb') as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"   Salvo com sucesso!")
            else:
                print(f"   ❌ Erro ao baixar (HTTP {resp.status_code})")
        except Exception as e:
            print(f"   ❌ Erro de conexão: {e}")

    print("\n🎧 Download concluído! Sua biblioteca de áudios está pronta para a Máquina de Reels.")

if __name__ == "__main__":
    download_audios()
