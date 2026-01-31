import os
import ftplib
from dotenv import load_dotenv

load_dotenv()

def audit_remote():
    ftp_host = os.getenv("FTP_HOST")
    ftp_user = os.getenv("FTP_USER")
    ftp_pass = os.getenv("FTP_PASS")

    try:
        session = ftplib.FTP(ftp_host, ftp_user, ftp_pass, timeout=60)
        
        # Testar caminhos
        paths = ["public_html", "domains/guiadodesconto.com.br/public_html", "www"]
        found_base = False
        for p in paths:
            try:
                session.cwd(p)
                print(f"✅ Entrou em: {p}")
                found_base = True
                break
            except:
                continue
        
        if not found_base:
            print("❌ Falha ao encontrar diretório base")
            return

        print(f"📍 PWD Atual: {session.pwd()}")
        
        print("\n--- Arquivos na Raiz ---")
        session.retrlines('LIST')

        try:
            session.cwd("images")
            print(f"\n--- Arquivos em 'images/' (PWD: {session.pwd()}) ---")
            session.retrlines('LIST')
        except:
            print("\n❌ Pasta 'images/' não encontrada na base atual")

        session.quit()
    except Exception as e:
        print(f"❌ Erro audit: {e}")

if __name__ == "__main__":
    audit_remote()
