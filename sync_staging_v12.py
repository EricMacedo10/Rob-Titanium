import os
import ftplib
import sys
from dotenv import load_dotenv

# Adiciona diretorio infra ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'infra'))
from upload_logic import upload_to_hostinger

load_dotenv()

def sync_titanium_staging():
    """
    Sincroniza a Boutique Titanium (Moda & Beleza) com o site de testes:
    teste.guiadodesconto.com.br - INCLUINDO PAGINAS LEGAIS
    """
    print("="*60)
    print("TITANIUM STAGING SYNC v12.3 - FULL BOUTIQUE PUSH")
    print("="*60)

    ftp_host = os.getenv("FTP_HOST")
    ftp_user = os.getenv("FTP_USER")
    ftp_pass = os.getenv("FTP_PASS")

    if not all([ftp_host, ftp_user, ftp_pass]):
        print("[!] Erro: Credenciais FTP nao encontradas no .env")
        return

    # MODO FORCADA: STAGING
    os.environ['ENV_MODE'] = 'STAGING'

    # Lista de arquivos vitais + Imagens + Paginas Legais
    files_to_sync = [
        # HTML Core
        ("site/index.html", "index.html"),
        ("site/index.html", "index_staging.html"),
        ("site/categoria.html", "categoria.html"),
        
        # Paginas Legais Atualizadas (Shopee Only)
        ("site/sobre.html", "sobre.html"),
        ("site/privacidade.html", "privacidade.html"),
        ("site/termos.html", "termos.html"),
        
        # Dados 
        ("site/data.json", "data.json"),
        ("site/notifications.json", "notifications.json"),
        
        # Estrutura
        ("site/js/app.js", "js/app.js"),
        ("site/css/style.css", "css/style.css"),
        
        # Imagens Hero
        ("site/images/hero-bg-portuguese.png", "images/hero-bg-portuguese.png"),
        ("site/images/hero-asset.png", "images/hero-asset.png"),
        ("site/images/fashion-hero.png", "images/fashion-hero.png"),
        ("site/images/beauty-hero.png", "images/beauty-hero.png"),
        ("site/favicon.ico", "favicon.ico")
    ]

    print(f"[Info] Preparando envio de {len(files_to_sync)} arquivos para /teste/...")

    success_count = 0
    for local, remote in files_to_sync:
        if os.path.exists(local):
            print(f"\n>>> Sincronizando: {remote}")
            if upload_to_hostinger(local, ftp_host, ftp_user, ftp_pass, remote_path=remote):
                success_count += 1
        else:
            print(f"\n[!] Arquivo nao encontrado (pulado): {local}")

    print("\n" + "="*60)
    print(f"RESULTADO: {success_count}/{len(files_to_sync)} arquivos sincronizados!")
    print(f"🚀 BOUTIQUE 100% SHOPEE NO AR: http://teste.guiadodesconto.com.br")
    print("="*60)

if __name__ == "__main__":
    sync_titanium_staging()
