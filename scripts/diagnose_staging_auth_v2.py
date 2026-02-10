import os
import ftplib
from dotenv import load_dotenv

def diagnose_staging_ftp():
    load_dotenv()
    FTP_HOST = os.getenv("FTP_HOST")
    FTP_USER = os.getenv("FTP_USER")
    FTP_PASS = os.getenv("FTP_PASS")

    try:
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        print(f"✅ Conectado ao FTP como {FTP_USER}")

        print(f"🏠 Home Directory: {ftp.pwd()}")
        
        # List items in root
        print("📁 Root Listing:")
        print(ftp.nlst())

        # Check for domains folder
        target = "domains/guiadodesconto.com.br/public_html/teste"
        print(f"\n🚀 Navegando para: {target}")
        try:
            ftp.cwd(target)
            print(f"✅ Atual Dir: {ftp.pwd()}")
            files = ftp.nlst()
            print(f"📄 Arquivos: {files}")
            
            for f in [".htaccess", ".htpasswd"]:
                if f in files:
                    print(f"\n📝 Conteúdo de {f}:")
                    lines = []
                    ftp.retrlines(f"RETR {f}", lines.append)
                    for l in lines:
                        print(f"   {l}")
        except Exception as e:
            print(f"❌ Erro ao acessar {target}: {e}")

        ftp.quit()
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    diagnose_staging_ftp()
