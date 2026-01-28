"""
🚀 Deploy Site to Hostinger via FTP
Professional deployment script with retry logic and error handling
"""
import ftplib
import os
import time
from pathlib import Path
from typing import List, Tuple

# Configuration
SITE_DIR = Path('site')
REMOTE_DIR = 'public_html'
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

# Exclusions
EXCLUDE_PATTERNS = [
    '.git', '.github', 'node_modules', '*.pyc', '__pycache__',
    '.DS_Store', '.env', 'Thumbs.db'
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
        # Connect to FTP
        print("\n🔌 Establishing FTP connection...")
        ftp = ftplib.FTP(ftp_host, ftp_user, ftp_pass, timeout=120)
        print("✅ Connected!")
        
        print(f"📍 Initial PWD: {ftp.pwd()}")
        print("📂 Listing root directory:")
        ftp.dir()

        # Check if we are already in public_html
        current_pwd = ftp.pwd()
        if current_pwd == '/public_html' or current_pwd.endswith('/public_html'):
            print(f"\nℹ️  Already in public_html ({current_pwd}). Uploading to current directory.")
            target_dir = '.'
        else:
            target_dir = REMOTE_DIR
            
        # Change to remote directory if needed
        if target_dir != '.':
            print(f"\n📂 Navigating to {target_dir}...")
            ensure_remote_dir(ftp, target_dir)
        
        print(f"📍 Target PWD: {ftp.pwd()}")

        
        # Upload debug file
        with open('deploy_debug.txt', 'w') as f:
            f.write(f'Deployment test: {time.ctime()}')
        with open('deploy_debug.txt', 'rb') as f:
            ftp.storbinary('STOR deploy_debug.txt', f)
        print("✅ debug file uploaded")
        
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
