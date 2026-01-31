import os
import ftplib
from dotenv import load_dotenv

load_dotenv()

def sync_seasonal_banners():
    ftp_host = os.getenv("FTP_HOST")
    ftp_user = os.getenv("FTP_USER")
    ftp_pass = os.getenv("FTP_PASS")

    try:
        session = ftplib.FTP(ftp_host, ftp_user, ftp_pass, timeout=60)
        session.cwd("/")
        
        # Garante pasta images
        try:
            session.cwd("images")
        except:
            session.mkd("images")
            session.cwd("images")

        # Banners Sazonais
        seasonal_files = [
            "banner_mochilas_mercadolivre.png",
            "banner_cadernos_shopee.png",
            "banner_volta_aulas_amazon.png"
        ]
        
        image_dir = "site/images"
        for f in seasonal_files:
            local_path = os.path.join(image_dir, f)
            if os.path.exists(local_path):
                print(f"📤 Subindo Sazonal: {f}")
                with open(local_path, "rb") as file:
                    session.storbinary(f"STOR {f}", file)
            else:
                print(f"⚠️  Arquivo não encontrado localmente: {local_path}")

        session.quit()
        print("✅ Banners Sazonais Sincronizados!")

    except Exception as e:
        print(f"❌ Erro sazonal: {e}")

if __name__ == "__main__":
    sync_seasonal_banners()
