import os
import ftplib
import sys
from dotenv import load_dotenv

# Adiciona diretorio infra ao path para usar a logica de blindagem
sys.path.append(os.path.join(os.path.dirname(__file__), 'infra'))
from upload_logic import upload_to_hostinger

load_dotenv()

def sync_titanium_production():
    """
    DEPLOY FINAL + AI RADAR: Sincroniza a Boutique Titanium 
    com o sistema de Radar de Tendencias Inteligente.
    """
    print("============================================================")
    print("TITANIUM PRODUCTION DEPLOY v12.8 - RADAR READY")
    print("============================================================")

    ftp_host = os.getenv("FTP_HOST")
    ftp_user = os.getenv("FTP_USER")
    ftp_pass = os.getenv("FTP_PASS")

    if not all([ftp_host, ftp_user, ftp_pass]):
        print("[!] Erro: Credenciais FTP nao encontradas no .env")
        return

    # MODO FORCADO: PRODUCTION
    os.environ['ENV_MODE'] = 'PRODUCTION'

    # Lista de arquivos Core
    files_to_sync = [
        ("site/ads.txt", "ads.txt"),
        ("site/index.html", "index.html"),
        ("site/blog.html", "blog.html"),
        ("site/sobre.html", "sobre.html"),
        ("site/privacidade.html", "privacidade.html"),
        ("site/termos.html", "termos.html"),
        ("site/ai_reviews.json", "ai_reviews.json"),  # NOVO: Radar de Tendencias
        ("site/track_clicks.php", "track_clicks.php"),
        ("site/js/app.js", "js/app.js"),
        ("site/css/style.css", "css/style.css"),
        ("site/favicon.ico", "favicon.ico"),
        ("site/specialist.json", "specialist.json"),  # NOVO: Seleção da Especialista
        ("site/data.json", "data.json")               # Garantir sincronia do feed
    ]

    # Adicionar dinamicamente todos os artigos da pasta blog
    blog_dir = 'site/blog'
    if os.path.exists(blog_dir):
        for article in os.listdir(blog_dir):
            if article.endswith('.html'):
                files_to_sync.append((f"site/blog/{article}", f"blog/{article}"))

    print(f"[Info] Iniciando Sincronizacao de {len(files_to_sync)} arquivos...")

    success_count = 0
    for local, remote in files_to_sync:
        if os.path.exists(local):
            print(f"\n>>> Sincronizando: {remote}")
            if upload_to_hostinger(local, ftp_host, ftp_user, ftp_pass, remote_path=remote):
                success_count += 1
        else:
            print(f"\n[!] Arquivo nao encontrado: {local}")

    print("\n" + "============================================================")
    print(f"RESULTADO: {success_count}/{len(files_to_sync)} arquivos em producao!")
    print(f"RADAR DE TENDENCIAS ATIVO: https://guiadodesconto.com.br")
    print("============================================================")

if __name__ == "__main__":
    sync_titanium_production()
