"""
🚀 Deploy Site to Hostinger via FTP
Professional deployment script with retry logic and error handling
"""
import ftplib
import os
import time
from pathlib import Path
from typing import List, Tuple
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
SITE_DIR = Path('site')
REMOTE_DIR = 'public_html'
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

# Exclusions - data.json is managed by update-offers workflow
EXCLUDE_PATTERNS = [
    '.git', '.github', 'node_modules', '*.pyc', '__pycache__',
    '.DS_Store', '.env', 'Thumbs.db', 'data.json'
]

def should_exclude(path: Path) -> bool:
    """Check if file/dir should be excluded"""
    for pattern in EXCLUDE_PATTERNS:
        if pattern.startswith('*'):
            if path.name.endswith(pattern[1:]):
                return True
        elif pattern in str(path):
            return True
    return False

def upload_file_with_retry(ftp: ftplib.FTP, local_path: Path, remote_path: str) -> bool:
    """Upload a single file with retry logic"""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            with open(local_path, 'rb') as file:
                ftp.storbinary(f'STOR {remote_path}', file)
            return True
        except Exception as e:
            if attempt < MAX_RETRIES:
                print(f"   ⚠️  Attempt {attempt} failed: {e}")
                print(f"   🔄 Retrying in {RETRY_DELAY}s...")
                time.sleep(RETRY_DELAY)
            else:
                print(f"   ❌ Failed after {MAX_RETRIES} attempts: {e}")
                return False
    return False

def ensure_remote_dir(ftp: ftplib.FTP, remote_dir: str) -> bool:
    """Create remote directory if it doesn't exist"""
    try:
        ftp.cwd(remote_dir)
        return True
    except ftplib.error_perm:
        # Directory doesn't exist, create it
        try:
            ftp.mkd(remote_dir)
            ftp.cwd(remote_dir)
            return True
        except Exception as e:
            print(f"   ❌ Error creating directory {remote_dir}: {e}")
            return False

def clean_obsolete_files(ftp: ftplib.FTP, local_dir: Path, remote_dir: str = '.'):
    """
    Remove files from server that don't exist locally.
    Preserves data.json (managed by update-offers workflow).
    """
    print("\n🧹 Cleaning obsolete files...")
    
    # Files to preserve (never delete)
    PRESERVE = ['data.json', 'deploy_debug.txt', '.htaccess']
    
    try:
        # Get list of remote files
        remote_files = []
        ftp.retrlines('LIST', lambda x: remote_files.append(x))
        
        deleted = 0
        for line in remote_files:
            parts = line.split()
            if len(parts) < 9:
                continue
            
            name = ' '.join(parts[8:])  # Handle filenames with spaces
            is_dir = line.startswith('d')
            
            # Skip preserved files
            if name in PRESERVE:
                continue
                
            local_path = local_dir / name
            
            # If file doesn't exist locally, delete from server
            if not local_path.exists():
                try:
                    if is_dir:
                        # Recursively delete directory
                        print(f"   🗑️  Deleting obsolete dir: {name}/")
                        try:
                            ftp.rmd(name)
                        except:
                            pass  # Non-empty dirs will fail, that's ok
                    else:
                        print(f"   🗑️  Deleting obsolete file: {name}")
                        ftp.delete(name)
                        deleted += 1
                except Exception as e:
                    print(f"   ⚠️  Could not delete {name}: {e}")
        
        print(f"   ✅ Cleaned {deleted} obsolete files")
        return deleted
        
    except Exception as e:
        print(f"   ⚠️  Cleanup error: {e}")
        return 0

def upload_directory(ftp: ftplib.FTP, local_dir: Path, remote_base: str = '') -> Tuple[int, int]:
    """
    Recursively upload directory
    Returns: (files_uploaded, files_failed)
    """
    uploaded = 0
    failed = 0
    
    for item in sorted(local_dir.iterdir()):
        if should_exclude(item):
            continue
        
        remote_path = f"{remote_base}/{item.name}" if remote_base else item.name
        
        if item.is_file():
            # Upload file
            print(f"📤 {item.relative_to(SITE_DIR)} -> {remote_path}")
            if upload_file_with_retry(ftp, item, remote_path):
                uploaded += 1
                print(f"   ✅ Success")
            else:
                failed += 1
        
        elif item.is_dir():
            # Create directory (don't navigate into it)
            print(f"📁 Creating directory: {remote_path}")
            try:
                ftp.mkd(remote_path)
                print(f"   ✅ Directory created")
            except ftplib.error_perm as e:
                # Directory might already exist
                if "exists" in str(e).lower() or "file exists" in str(e).lower():
                    print(f"   ℹ️  Directory already exists")
                else:
                    print(f"   ⚠️  Warning: {e}")
            
            # Upload contents recursively (using absolute paths)
            sub_uploaded, sub_failed = upload_directory(ftp, item, remote_path)
            uploaded += sub_uploaded
            failed += sub_failed
    
    return uploaded, failed

def main():
    print("=" * 60)
    print("🚀 DEPLOY SITE TO HOSTINGER")
    print("=" * 60)
    
    # Get credentials from environment
    ftp_host = os.getenv('FTP_HOST')
    ftp_user = os.getenv('FTP_USER')
    ftp_pass = os.getenv('FTP_PASS')
    
    if not all([ftp_host, ftp_user, ftp_pass]):
        print("❌ FTP credentials not configured!")
        print("   Set FTP_HOST, FTP_USER, FTP_PASS environment variables")
        return False
    
    print(f"\n📡 Connecting to: {ftp_host}")
    print(f"👤 User: {ftp_user}")
    print(f"📂 Local directory: {SITE_DIR.absolute()}")
    print(f"🌐 Remote directory: {REMOTE_DIR}")
    
    try:
        # Connect to FTP with retry
        ftp = None
        for attempt in range(1, 4):
            try:
                print(f"🔌 Tentativa {attempt}/3 - Conectando...")
                ftp = ftplib.FTP(ftp_host, ftp_user, ftp_pass, timeout=120)
                print(f"✅ Conectado! Diretório: {ftp.pwd()}")
                break
            except Exception as e:
                print(f"⚠️  Erro: {e}")
                if attempt < 3:
                    print(f"⏳ Aguardando 5s...")
                    time.sleep(5)
        
        if not ftp:
            print("❌ Falha ao conectar após 3 tentativas")
            return False
        
        # User already starts in /public_html - no navigation needed
        print(f"📍 PWD: {ftp.pwd()}")

        
        # Upload debug file
        with open('deploy_debug.txt', 'w') as f:
            f.write(f'Deployment test: {time.ctime()}')
        with open('deploy_debug.txt', 'rb') as f:
            ftp.storbinary('STOR deploy_debug.txt', f)
        print("✅ debug file uploaded")
        
        # Clean obsolete files before uploading new ones
        clean_obsolete_files(ftp, SITE_DIR)
        
        # Upload files
        print(f"\n📦 Starting file upload...")
        print("-" * 60)
        
        start_time = time.time()
        uploaded, failed = upload_directory(ftp, SITE_DIR)
        duration = time.time() - start_time
        
        print("-" * 60)
        print(f"\n📊 DEPLOYMENT SUMMARY")
        print("=" * 60)
        print(f"✅ Files uploaded: {uploaded}")
        print(f"❌ Files failed: {failed}")
        print(f"⏱️  Duration: {duration:.1f}s")
        print("=" * 60)

        # Verify upload by listing again
        print("\n📂 Final Directory Listing:")
        ftp.dir()
        
        # Close connection
        ftp.quit()
        
        if failed > 0:
            print(f"\n⚠️  Deployment completed with {failed} errors")
            return False
        else:
            print("\n🎉 Deployment successful!")
            return True
        
    except ftplib.error_perm as e:
        print(f"\n❌ FTP Permission Error: {e}")
        print("   Check your FTP credentials and permissions")
        return False
    except Exception as e:
        print(f"\n❌ Deployment failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
