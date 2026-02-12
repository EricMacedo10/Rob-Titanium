import os
import ftplib
from dotenv import load_dotenv

load_dotenv()

def verify_remote_content():
    ftp_host = os.getenv("FTP_HOST")
    ftp_user = os.getenv("FTP_USER")
    ftp_pass = os.getenv("FTP_PASS")

    print(f"Conectando a {ftp_host}...")
    try:
        session = ftplib.FTP(ftp_host, ftp_user, ftp_pass, timeout=60)
        session.cwd("/") 
        
        files_to_check = ["index.html", "css/style.css"]
        
        for remote_file in files_to_check:
            print(f"\n--- Verificando: {remote_file} ---")
            try:
                content = []
                session.retrlines(f"RETR {remote_file}", content.append)
                text = "\n".join(content)
                
                if remote_file == "index.html":
                    import re
                    match = re.search(r'href="css/style\.css\?v=([^"]+)"', text)
                    if match:
                        print(f"Versão do CSS no HTML: {match.group(1)}")
                    else:
                        print("Não encontrei a versão do CSS no HTML.")
                
                if remote_file == "css/style.css":
                    if ".btn-search" in text:
                        if "display: none" in text:
                            print("CSS remotamente contém 'display: none' no .btn-search. ✅")
                        else:
                            print("CSS remotamente NÃO contém 'display: none' no .btn-search. ❌")
                    else:
                        print("Não encontrei .btn-search no CSS remoto.")

            except Exception as e:
                print(f"Erro ao ler {remote_file}: {e}")
        
        session.quit()
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    verify_remote_content()
