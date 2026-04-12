import os
import ftplib
from dotenv import load_dotenv

load_dotenv()

host = os.getenv('FTP_HOST')
user = os.getenv('FTP_USER')
password = os.getenv('FTP_PASS')

with open('ftp_out_teste.txt', 'w') as f:
    try:
        ftp = ftplib.FTP(host, user, password)
        ftp.cwd('/teste')
        f.write(f"Conectado! PWD: {ftp.pwd()}\n")
        
        f.write("\n[Raiz /teste/]\n")
        def append_line(line):
            f.write(line + '\n')
        ftp.retrlines('LIST', append_line)
        
        ftp.quit()
    except Exception as e:
        f.write(f"Erro: {e}\n")
