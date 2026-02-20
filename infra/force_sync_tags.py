import ftplib
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def force_upload():
    host = os.getenv('FTP_HOST')
    user = os.getenv('FTP_USER')
    password = os.getenv('FTP_PASS')
    
    files_to_upload = [
        Path('site/index.html'),
        Path('site/obrigado.html')
    ]
    
    try:
        ftp = ftplib.FTP(host, user, password)
        print("✅ Connected to FTP")
        
        # Try to find the root
        for p in ["public_html", "www", ""]:
            try:
                if p: ftp.cwd(f"/{p}")
                else: ftp.cwd("/")
                print(f"📂 Current Dir: {ftp.pwd()}")
                break
            except: continue
            
        for local_file in files_to_upload:
            if not local_file.exists():
                print(f"❌ Local file not found: {local_file}")
                continue
                
            filename = local_file.name
            print(f"📤 Uploading {filename}...")
            with open(local_file, 'rb') as f:
                ftp.storbinary(f'STOR {filename}', f)
            print(f"✅ Success: {filename}")
            
        ftp.quit()
        print("🏁 Force Sync Complete")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    force_upload()
