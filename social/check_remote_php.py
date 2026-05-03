import ftplib
import os
from dotenv import load_dotenv

load_dotenv()

ftp_host = os.getenv('FTP_HOST')
ftp_user = os.getenv('FTP_USER')
ftp_pass = os.getenv('FTP_PASS')

try:
    ftp = ftplib.FTP(ftp_host, ftp_user, ftp_pass, timeout=60)
    for p in ["public_html", "www"]:
        try:
            ftp.cwd(f"/{p}")
            break
        except:
            continue
    
    print("Remote bot_instagram.php content (first 100 lines):")
    lines = []
    ftp.retrlines('RETR bot_instagram.php', lines.append)
    for line in lines[:100]:
        print(line)
    
    ftp.quit()

except Exception as e:
    print(f"[ERRO] {e}")
