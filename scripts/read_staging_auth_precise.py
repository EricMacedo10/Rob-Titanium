import os
import ftplib
from dotenv import load_dotenv

def read_files_ftp():
    load_dotenv()
    FTP_HOST = os.getenv("FTP_HOST")
    FTP_USER = os.getenv("FTP_USER")
    FTP_PASS = os.getenv("FTP_PASS")

    try:
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        
        target_dir = "/teste"
        ftp.cwd(target_dir)
        print(f"✅ In {target_dir}")

        for filename in [".htaccess", ".htpasswd"]:
            print(f"\n--- {filename} ---")
            lines = []
            try:
                ftp.retrlines(f"RETR {filename}", lines.append)
                for l in lines:
                    print(l)
            except:
                print(f"❌ Could not read {filename}")

        ftp.quit()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    read_files_ftp()
