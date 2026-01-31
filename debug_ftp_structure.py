import os
import ftplib
from dotenv import load_dotenv

load_dotenv()

def explore_ftp():
    ftp_host = os.getenv("FTP_HOST")
    ftp_user = os.getenv("FTP_USER")
    ftp_pass = os.getenv("FTP_PASS")

    print(f"Conectando a {ftp_host}...")
    try:
        session = ftplib.FTP(ftp_host, ftp_user, ftp_pass, timeout=60)
        print("Conectado!")
        
        def list_recursive(path, depth=0):
            if depth > 2: return
            try:
                session.cwd(path)
                current = session.pwd()
                print("  " * depth + f"📁 {current}")
                items = session.nlst()
                for item in items:
                    if item in [".", ".."]: continue
                    list_recursive(item, depth + 1)
                session.cwd("..")
            except:
                # Provavelmente é um arquivo
                # print("  " * depth + f"📄 {path}")
                pass

        print("Explorando diretórios:")
        list_recursive("/")
        
        session.quit()
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    explore_ftp()
