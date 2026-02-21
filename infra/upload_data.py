"""
Upload data.json to staging manually (one-time fix).
The deploy.py script excludes data.json to preserve server state.
"""
import ftplib
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def upload_data_json():
    ftp_host = os.getenv('FTP_HOST')
    ftp_user = os.getenv('FTP_USER')
    ftp_pass = os.getenv('FTP_PASS')

    if not all([ftp_host, ftp_user, ftp_pass]):
        print("❌ FTP credentials missing!")
        return False

    local_file = Path('site/data.json')
    if not local_file.exists():
        print("❌ site/data.json not found!")
        return False

    try:
        ftp = ftplib.FTP(ftp_host, ftp_user, ftp_pass, timeout=60)
        print("✅ Connected to FTP")

        # Discover web root (same logic as deploy.py)
        base_path = "/"
        for p in ["public_html", "www"]:
            try:
                ftp.cwd(f"/{p}")
                base_path = f"/{p}"
                print(f"✅ Found web root: {base_path}")
                break
            except:
                continue
        
        # Navigate to staging subfolder
        staging_path = f"{base_path.rstrip('/')}/teste"
        try:
            ftp.cwd(staging_path)
            print(f"✅ In {staging_path}")
        except:
            print(f"⚠️ {staging_path} not found, trying /teste")
            ftp.cwd("/teste")
            staging_path = "/teste"
            print(f"✅ In {staging_path}")

        # Upload data.json
        with open(local_file, 'rb') as f:
            ftp.storbinary('STOR data.json', f)
        print("✅ data.json uploaded to staging!")

        # Verify
        files = []
        ftp.retrlines('LIST', files.append)
        found = any('data.json' in f for f in files)
        print(f"{'✅' if found else '❌'} Verification: data.json {'found' if found else 'NOT found'}")

        ftp.quit()
        return found

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    upload_data_json()
