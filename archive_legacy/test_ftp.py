import os
import ftplib
from dotenv import load_dotenv

load_dotenv()

host = os.getenv('FTP_HOST')
user = os.getenv('FTP_USER')
password = os.getenv('FTP_PASS')

print(f"Buscando diretorios no FTP: {host}")

try:
    ftp = ftplib.FTP(host, user, password)
    print("Conectado! PWD:", ftp.pwd())
    
    print("\n[Raiz /]")
    ftp.retrlines('LIST')
    
    print("\n[Diretorios possíveis para subdomino 'teste']")
    dirs = []
    ftp.retrlines('NLST', dirs.append)
    
    for d in dirs:
        if "teste" in d.lower():
            print(f"  -> Encontrado: /{d}")
            try:
                ftp.cwd(f"/{d}")
                print(f"     [Conteudo de /{d}]")
                ftp.retrlines('LIST')
            except Exception as e:
                print(f"     Erro ao acessar /{d}: {e}")
                
    ftp.quit()
except Exception as e:
    print(f"Erro FTP: {e}")
