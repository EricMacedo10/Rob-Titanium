import os
import ftplib
from dotenv import load_dotenv

load_dotenv()

def audit_root():
    ftp_host = os.getenv("FTP_HOST")
    ftp_user = os.getenv("FTP_USER")
    ftp_pass = os.getenv("FTP_PASS")

    try:
        session = ftplib.FTP(ftp_host, ftp_user, ftp_pass, timeout=60)
        print(f"✅ Conectado como: {ftp_user}")
        print(f"📍 PWD Atual: {session.pwd()}")
        
        print("\n--- Conteúdo da Raiz ---")
        session.retrlines('LIST')

        session.quit()
    except Exception as e:
        print(f"❌ Erro audit: {e}")

if __name__ == "__main__":
    audit_root()
