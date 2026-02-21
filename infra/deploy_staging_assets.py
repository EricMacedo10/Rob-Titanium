import ftplib
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def main():
    print("🚀 TARGETED STAGING UPLOAD (data.json)")
    ftp_host = os.getenv('FTP_HOST')
    ftp_user = os.getenv('FTP_USER')
    ftp_pass = os.getenv('FTP_PASS')
    
    try:
        ftp = ftplib.FTP(ftp_host, ftp_user, ftp_pass)
        # Caminho da Hostinger
        # Subir um nível para garantir o caminho correto (Hostinger usa public_html ou www)
        paths_to_try = ["/public_html/teste", "/www/teste", "/teste"]
        success_cwd = False
        for p in paths_to_try:
            try:
                ftp.cwd(p)
                print(f"✅ Connected to {p}")
                success_cwd = True
                break
            except:
                continue
        
        if not success_cwd:
            print("❌ Could not find /teste directory")
            return False

        # Upload data.json
        file_to_upload = "site/data.json"
        with open(file_to_upload, 'rb') as f:
            ftp.storbinary('STOR data.json', f)
        print("✅ data.json uploaded to staging")

        ftp.quit()
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    main()
