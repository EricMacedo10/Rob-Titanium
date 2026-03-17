import os
import ftplib
from dotenv import load_dotenv

load_dotenv()

def sync_staging():
    ftp_host = os.getenv("FTP_HOST")
    ftp_user = os.getenv("FTP_USER")
    ftp_pass = os.getenv("FTP_PASS")

    try:
        session = ftplib.FTP(ftp_host, ftp_user, ftp_pass, timeout=60)
        print(f"✅ Conectado: {ftp_user}")
        
        # Muda para pasta teste
        session.cwd("/teste")
        print("📁 Navegado para /teste")

        files = [
            ("site/index_staging.html", "index.html"),
            ("site/index_staging.html", "index_staging.html"),
            ("site/css/style.css", "css/style.css"),
            ("site/js/app.js", "js/app.js"),
            ("site/data.json", "data.json"),
            ("site/js/family-widget.js", "js/family-widget.js"),
            ("site/images/hero-bg-portuguese.png", "images/hero-bg-portuguese.png")
        ]

        print(f"🚀 Iniciando upload de {len(files)} arquivos...")

        for local, remote in files:
            print(f"📤 Subindo: {local} -> {remote}")
            with open(local, "rb") as file:
                # Trata subpastas remota (js/app.js -> cwd to /teste/js)
                if "/" in remote:
                    folder, filename = remote.split("/")
                    try:
                        session.cwd(f"/teste/{folder}")
                    except:
                        session.mkd(f"/teste/{folder}")
                        session.cwd(f"/teste/{folder}")
                    
                    session.storbinary(f"STOR {filename}", file)
                    session.cwd("/teste")
                else:
                    session.storbinary(f"STOR {remote}", file)
        
        session.quit()
        print("🏁 Sincronização v12 concluída!")

    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    sync_staging()
