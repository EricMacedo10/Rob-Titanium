import ftplib
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Arquivos a sincronizar: (local, remoto)
# Adicionamos instagram_posts.json para alimentar a página instagram.html
_FILES_TO_SYNC = [
    (Path('social/ofertas.json'),          'ofertas.json'),
    (Path('site/instagram_posts.json'),    'instagram_posts.json'),
]

def sync_ofertas():
    """
    Sincroniza via FTP:
      - social/ofertas.json  → servidor (bot de DM)
      - site/instagram_posts.json → servidor (página instagram.html)

    Retorna True se PELO MENOS ofertas.json foi enviado com sucesso.
    """
    ftp_host = os.getenv('FTP_HOST')
    ftp_user = os.getenv('FTP_USER')
    ftp_pass = os.getenv('FTP_PASS')

    if not all([ftp_host, ftp_user, ftp_pass]):
        print("[ERRO] FTP credentials missing!")
        return False

    ofertas_path = Path('social/ofertas.json')
    if not ofertas_path.exists():
        print("[ERRO] social/ofertas.json not found!")
        return False

    try:
        ftp = ftplib.FTP(ftp_host, ftp_user, ftp_pass, timeout=60)
        print("[OK] Connected to FTP")

        # Navegar para o web root
        web_root_found = False
        for p in ["public_html", "www"]:
            try:
                ftp.cwd(f"/{p}")
                print(f"[OK] Found web root: /{p}")
                web_root_found = True
                break
            except Exception:
                continue

        if not web_root_found:
            print("[AVISO] Web root não encontrado. Usando raiz FTP.")

        ofertas_ok = False
        for local_path, remote_name in _FILES_TO_SYNC:
            if not local_path.exists():
                print(f"[AVISO] Arquivo local não encontrado, pulando: {local_path}")
                continue
            try:
                with open(local_path, 'rb') as f:
                    ftp.storbinary(f'STOR {remote_name}', f)
                print(f"[OK] {remote_name} enviado para o servidor.")
                if remote_name == 'ofertas.json':
                    ofertas_ok = True
            except Exception as upload_err:
                print(f"[ERRO] Falha ao enviar {remote_name}: {upload_err}")

        ftp.quit()
        return ofertas_ok

    except Exception as e:
        print(f"[ERRO] Error during sync: {e}")
        return False

if __name__ == "__main__":
    sync_ofertas()

