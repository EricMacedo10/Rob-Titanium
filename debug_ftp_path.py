
import ftplib
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def print_separator(char='-', length=60):
    print(char * length)

def list_directory(ftp, header_msg):
    print_separator()
    print(f"📂 {header_msg}")
    print(f"📍 PWD: {ftp.pwd()}")
    print_separator()
    
    try:
        lines = []
        ftp.dir(lines.append)
        for line in lines:
            print(line)
        if not lines:
            print("(Directory is empty)")
    except Exception as e:
        print(f"❌ Error listing directory: {e}")

def main():
    print("🕵️‍♂️ HOSTINGER FTP PATHFINDER")
    print("============================================================")
    
    ftp_host = os.getenv('FTP_HOST')
    ftp_user = os.getenv('FTP_USER')
    ftp_pass = os.getenv('FTP_PASS')
    
    if not all([ftp_host, ftp_user, ftp_pass]):
        print("❌ Missing FTP credentials in .env")
        return

    try:
        print(f"📡 Connecting to {ftp_host}...")
        ftp = ftplib.FTP(ftp_host, ftp_user, ftp_pass, timeout=120)
        ftp.set_pasv(True)
        print("✅ Connected!")
        
        # 1. Inspect Initial Login Directory
        list_directory(ftp, "INITIAL LOGIN DIRECTORY")
        
        # 2. Try to go UP one level
        print("\n⬆️  Attempting to go UP (..)...")
        try:
            ftp.cwd('..')
            list_directory(ftp, "PARENT DIRECTORY (Level -1)")
        except Exception as e:
            print(f"❌ Could not go up: {e}")

        # 3. Try to go UP another level
        print("\n⬆️  Attempting to go UP AGAIN (../..)...")
        try:
            ftp.cwd('..')
            list_directory(ftp, "GRANDPARENT DIRECTORY (Level -2)")
        except Exception as e:
            print(f"❌ Could not go up again: {e}")
            
        # 4. Search for 'domains' folder (common in Hostinger)
        # We are likely at the highest level we can reach now. Let's look around.
        
        print("\n🔍 Analyzing structure...")
        
        ftp.quit()
        print("\n✅ Pathfinder finished.")

    except Exception as e:
        print(f"\n❌ Fatal Error: {e}")

if __name__ == "__main__":
    main()
