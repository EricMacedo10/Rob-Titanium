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
        print("✅ Conectado ao FTP")

        # Caminhos prováveis
        paths = [
            "public_html/teste",
            "domains/guiadodesconto.com.br/public_html/teste",
            "/teste"
        ]

        for p in paths:
            print(f"\n📁 Tentando caminho: {p}")
            try:
                ftp.cwd(p)
                print(f"✅ Entrou em {p}")
                files = ftp.nlst()
                print(f"📄 Arquivos: {files}")
                
                if ".htaccess" in files:
                    print("✅ .htaccess encontrado")
                    content = []
                    ftp.retrlines(f"RETR .htaccess", content.append)
                    print("📝 Conteúdo .htaccess:")
                    for line in content:
                        print(f"   {line}")
                
                if ".htpasswd" in files:
                    print("✅ .htpasswd encontrado")
                    content = []
                    ftp.retrlines(f"RETR .htpasswd", content.append)
                    print("📝 Conteúdo .htpasswd:")
                    for line in content:
                        print(f"   {line}")
            except Exception as e:
                print(f"❌ Erro em {p}: {e}")

        ftp.quit()
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")

if __name__ == "__main__":
    diagnose_staging_ftp()
