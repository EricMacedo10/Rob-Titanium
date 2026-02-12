import os
import ftplib
from dotenv import load_dotenv

def upload_discoverer():
    load_dotenv()
    FTP_HOST = os.getenv("FTP_HOST")
    FTP_USER = os.getenv("FTP_USER")
    FTP_PASS = os.getenv("FTP_PASS")

    try:
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        
        target_dir = "/teste"
        ftp.cwd(target_dir)
        
        with open("scripts/path_discover.php", "rb") as f:
            ftp.storbinary("STOR path.php", f)
        
        print("✅ path.php uploaded to /teste")
        ftp.quit()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    upload_discoverer()
