import os
import ftplib
from dotenv import load_dotenv

load_dotenv()

def staging_sync():
    ftp_host = os.getenv("FTP_HOST")
    ftp_user = os.getenv("FTP_USER")
    ftp_pass = os.getenv("FTP_PASS")
    
    # Pasta de destino na Hostinger para o ambiente de teste
    STAGING_DIR = "/teste"

    try:
        session = ftplib.FTP(ftp_host, ftp_user, ftp_pass, timeout=60)
        print(f"✅ Conectado para STAGING: {ftp_user}")
        
        # Garantir que a pasta /teste existe e entrar nela
        try:
            session.cwd(STAGING_DIR)
        except:
            print(f"📁 Criando pasta staging: {STAGING_DIR}")
            session.mkd(STAGING_DIR)
            session.cwd(STAGING_DIR)
        
        # Estrutura de pastas internas
        subfolders = ["css", "js", "images", "admin"]
        for f in subfolders:
            try:
                session.mkd(f)
                print(f"📁 Subpasta criada: {f}")
            except:
                pass # Já existe

        # Mapeamento de arquivos (Local -> Remoto relativo ao /teste)
        files = {
            "site/index.html": "index.html",
            "site/css/style.css": "css/style.css",
            "site/js/app.js": "js/app.js",
            "site/js/family-widget.js": "js/family-widget.js",
            "site/admin/monitoring_dashboard.html": "admin/monitoring_dashboard.html",
            "site/track_clicks.php": "track_clicks.php",
            "site/admin/affiliate_status.json": "admin/affiliate_status.json",
            "site/admin/affiliate_status.js": "admin/affiliate_status.js",
            "site/admin/analytics.json": "admin/analytics.json",
            "site/admin/analytics.js": "admin/analytics.js",
            ".htaccess": ".htaccess" # Se houver proteção de pasta
        }

        # Banners (Opcional: sincronizar apenas os necessários para economizar banda)
        image_dir = "site/images"
        if os.path.exists(image_dir):
            for f in os.listdir(image_dir):
                if f.endswith((".png", ".jpg", ".webp")):
                    files[os.path.join(image_dir, f)] = f"images/{f}"

        print(f"🚀 Iniciando upload de {len(files)} arquivos para STAGING...")

        for local, remote in files.items():
            if not os.path.exists(local):
                print(f"⚠️ Pulando (não existe local): {local}")
                continue
                
            print(f"📤 Subindo: {remote}")
            with open(local, "rb") as file:
                # Tratar subpastas no caminho remoto
                if "/" in remote:
                    parts = remote.split("/")
                    filename = parts[-1]
                    subpath = "/".join(parts[:-1])
                    
                    # Entra na subpasta relativa ao /teste
                    session.cwd(f"{STAGING_DIR}/{subpath}")
                    session.storbinary(f"STOR {filename}", file)
                    session.cwd(STAGING_DIR)
                else:
                    session.storbinary(f"STOR {remote}", file)
        
        session.quit()
        print(f"🏁 Sincronização STAGING concluída em guiadodesconto.com.br{STAGING_DIR}")
        print(f"🔗 Acesse: http://teste.guiadodesconto.com.br")

    except Exception as e:
        print(f"❌ Erro no Sync Staging: {e}")

if __name__ == "__main__":
    staging_sync()
