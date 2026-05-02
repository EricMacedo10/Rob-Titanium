import ftplib
import os
from dotenv import load_dotenv

load_dotenv()

ftp_host = os.getenv('FTP_HOST')
ftp_user = os.getenv('FTP_USER')
ftp_pass = os.getenv('FTP_PASS')

try:
    ftp = ftplib.FTP(ftp_host, ftp_user, ftp_pass, timeout=60)
    print("[OK] Connected to FTP")

    # Navigate to root
    for p in ["public_html", "www"]:
        try:
            ftp.cwd(f"/{p}")
            print(f"[OK] Found web root: /{p}")
            break
        except:
            continue

    # Download bot_debug.log
    with open('bot_debug_remote.log', 'wb') as f:
        ftp.retrbinary('RETR bot_debug.log', f.write)
    print("[OK] bot_debug.log downloaded!")

    ftp.quit()

except Exception as e:
    print(f"[ERRO] {e}")
