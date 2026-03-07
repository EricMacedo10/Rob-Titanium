import os
from dotenv import load_dotenv
from infra.upload_logic import upload_to_hostinger

def force_upload():
    load_dotenv(override=True) # Force variables from .env to override shell env
    print("🚀 TITANIUM FORCE ASSET UPLOAD")
    
    ftp_host = os.getenv('FTP_HOST')
    ftp_user = os.getenv('FTP_USER')
    ftp_pass = os.getenv('FTP_PASS')
    env_mode = os.getenv('ENV_MODE', 'STAGING').upper()
    
    if not all([ftp_host, ftp_user, ftp_pass]):
        print("❌ Erro: Credenciais FTP não encontradas no .env")
        return

    if env_mode == 'STAGING':
        assets = [
            ('site/js/app.js',           'js/app.js'),
            ('site/js/family-widget.js', 'js/family-widget.js'),
            ('site/css/style.css',       'css/style.css'),
            ('site/css/titanium-security.css', 'css/titanium-security.css'),
            ('site/images/hero-asset.png', 'images/hero-asset.png'),
            ('site/images/hero-bg-portuguese.png', 'images/hero-bg-portuguese.png'),
            ('site/index_staging.html',  'index_staging.html'),
            ('site/index_staging.html',  'index.html'),
        ]
    else:
        assets = [
            ('site/js/app.js',           'js/app.js'),
            ('site/js/family-widget.js', 'js/family-widget.js'),
            ('site/css/style.css',       'css/style.css'),
            ('site/css/titanium-security.css', 'css/titanium-security.css'),
            ('site/images/hero-asset.png', 'images/hero-asset.png'),
            ('site/images/hero-bg-portuguese.png', 'images/hero-bg-portuguese.png'),
            ('site/index.html',          'index.html'),
        ]

    for local, remote in assets:
        if os.path.exists(local):
            print(f"\n>>> Subindo: {local} -> {remote}")
            upload_to_hostinger(local, ftp_host, ftp_user, ftp_pass, remote_path=remote)
        else:
            print(f"⚠️ Aviso: Arquivo não encontrado: {local}")

    print("\n✅ ASSETS ESTRUTURAIS SINCRONIZADOS!")

if __name__ == "__main__":
    force_upload()
