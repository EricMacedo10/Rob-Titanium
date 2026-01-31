"""
🚀 Deploy Site to Hostinger via FTP (Robust Version)
Updates:
- Enforces root directory (/) to avoid path confusion
- Explicit verification of critical files
- Preserves data.json
"""
import ftplib
import os
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Configuration
SITE_DIR = Path('site')
MAX_RETRIES = 3
RETRY_DELAY = 5

# Files to exclude from upload/cleanup
EXCLUDE_PATTERNS = [
    '.git', '.github', 'node_modules', '*.pyc', '__pycache__',
    '.DS_Store', '.env', 'Thumbs.db', 'data.json', 'notifications.json'
]

def should_exclude(path: Path) -> bool:
    for pattern in EXCLUDE_PATTERNS:
        if pattern.startswith('*'):
            if path.name.endswith(pattern[1:]): return True
        elif pattern in str(path):
            return True
    return False

def upload_file_with_retry(ftp: ftplib.FTP, local_path: Path, remote_base: str) -> bool:
    """Uploads file to correct remote path, ensuring folders exist"""
    # Calculate remote path relative to site root
    rel_path = local_path.relative_to(SITE_DIR).as_posix()
    
    # If file is at root of site/, it goes to /
    # If file is site/css/style.css, it goes to /css/style.css
    if '/' in rel_path:
        remote_dir = os.path.dirname(rel_path)
        remote_file = os.path.basename(rel_path)
    else:
        remote_dir = "" # Root
        remote_file = rel_path

    # Ensure remote dir exists
    if remote_dir:
        parts = remote_dir.split('/')
        current = ""
        for part in parts:
            current = f"{current}/{part}" if current else part
            try:
                ftp.cwd(f"/{current}")
            except:
                try:
                    ftp.mkd(f"/{current}")
                except: pass

    # Upload
    remote_full_path = f"/{rel_path}"
    print(f"📤 Uploading: {rel_path} -> {remote_full_path}")
    
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            with open(local_path, 'rb') as f:
                ftp.storbinary(f'STOR {remote_full_path}', f)
            return True
        except Exception as e:
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
            else:
                print(f"   ❌ Failed to upload {rel_path}: {e}")
                return False

def main():
    print("=" * 60)
    print("🚀 DEPLOY SITE TO HOSTINGER (ROBUST)")
    print("=" * 60)
    
    ftp_host = os.getenv('FTP_HOST')
    ftp_user = os.getenv('FTP_USER')
    ftp_pass = os.getenv('FTP_PASS')
    
    if not all([ftp_host, ftp_user, ftp_pass]):
        print("❌ FTP credentials missing!")
        return False

    try:
        ftp = ftplib.FTP(ftp_host, ftp_user, ftp_pass, timeout=120)
        print("✅ Connected to FTP")
        
        # Enforce Root
        ftp.cwd("/")
        print("✅ Root directory enforced: /")

        uploadeds = 0
        faileds = 0

        # Walk through site directory
        for root, dirs, files in os.walk(SITE_DIR):
            # Remove excluded dirs in-place
            dirs[:] = [d for d in dirs if not should_exclude(Path(root)/d)]
            
            for file in files:
                local_path = Path(root) / file
                if should_exclude(local_path):
                    continue
                
                if upload_file_with_retry(ftp, local_path, ""):
                    uploadeds += 1
                else:
                    faileds += 1

        print("-" * 60)
        print(f"📊 Summary: {uploadeds} uploaded, {faileds} failed")
        
        # Verification
        print("\n🔎 Verificando arquivos críticos:")
        critical_files = ['index.html', 'js/app.js', 'css/style.css']
        all_ok = True
        
        for crit in critical_files:
            try:
                if '/' in crit:
                    d, f = crit.rsplit('/', 1)
                    ftp.cwd(f"/{d}")
                    files_list = []
                    ftp.retrlines('LIST', files_list.append)
                    found = any(f in l for l in files_list)
                else:
                    ftp.cwd("/")
                    files_list = []
                    ftp.retrlines('LIST', files_list.append)
                    found = any(crit in l for l in files_list)
                
                if found:
                    print(f"   ✅ {crit} encontrado")
                else:
                    print(f"   ❌ {crit} NÃO encontrado")
                    all_ok = False
            except Exception as e:
                print(f"   ❌ Erro ao verificar {crit}: {e}")
                all_ok = False

        ftp.quit()
        return all_ok and faileds == 0

    except Exception as e:
        print(f"\n❌ Deployment failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
