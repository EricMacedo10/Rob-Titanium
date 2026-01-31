import os
import ftplib
from dotenv import load_dotenv

load_dotenv()

def force_sync():
    ftp_host = os.getenv("FTP_HOST")
    ftp_user = os.getenv("FTP_USER")
    ftp_pass = os.getenv("FTP_PASS")

    try:
        session = ftplib.FTP(ftp_host, ftp_user, ftp_pass, timeout=60)
        print(f"✅ Conectado: {ftp_user}")
        
        # Inicia na raiz /
        session.cwd("/")
        
        # Pastas para garantir
        folders = ["css", "js", "images"]
        for f in folders:
            try:
                session.mkd(f)
                print(f"📁 Pasta criada: {f}")
            except:
                print(f"✅ Pasta já existe: {f}")

        # Arquivos principais
        files = {
            "site/index.html": "index.html",
            "site/css/style.css": "css/style.css",
            "site/js/app.js": "js/app.js",
            "site/js/family-widget.js": "js/family-widget.js"
        }

        # Banners
        image_dir = "site/images"
        for f in os.listdir(image_dir):
            if f.startswith("banner_") and "_" in f and not any(c.isdigit() for c in f.split(".")[0].split("_")[-1]):
                files[os.path.join(image_dir, f)] = f"images/{f}"

        print(f"🚀 Iniciando upload de {len(files)} arquivos...")

        for local, remote in files.items():
            print(f"📤 Subindo: {remote}")
            with open(local, "rb") as file:
                # Se tiver subpasta, muda PWD
                if "/" in remote:
                    folder, filename = remote.split("/")
                    session.cwd(f"/{folder}")
                    session.storbinary(f"STOR {filename}", file)
                    session.cwd("/")
                else:
                    session.storbinary(f"STOR {remote}", file)
        
        session.quit()
        print("🏁 Sincronização FORÇADA concluída!")

    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    force_sync()
