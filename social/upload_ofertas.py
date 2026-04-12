import ftplib
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def sync_ofertas():
    ftp_host = os.getenv('FTP_HOST')
    ftp_user = os.getenv('FTP_USER')
    ftp_pass = os.getenv('FTP_PASS')

    if not all([ftp_host, ftp_user, ftp_pass]):
        print("❌ FTP credentials missing!")
        return False

    local_file = Path('social/ofertas.json')
    if not local_file.exists():
        print("❌ social/ofertas.json not found!")
        return False

    try:
        ftp = ftplib.FTP(ftp_host, ftp_user, ftp_pass, timeout=60)
        print("✅ Connected to FTP")

        # Navigate to root
        for p in ["public_html", "www"]:
            try:
                ftp.cwd(f"/{p}")
                print(f"✅ Found web root: /{p}")
                break
            except:
                continue

        # Upload ofertas.json
        with open(local_file, 'rb') as f:
            ftp.storbinary('STOR ofertas.json', f)
        print("✅ ofertas.json uploaded to server root!")

        ftp.quit()
        return True

    except Exception as e:
        print(f"❌ Error during sync: {e}")
        return False

if __name__ == "__main__":
    sync_ofertas()
