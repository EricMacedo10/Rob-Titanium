"""
upload_logic.py — Resilient FTP Uploader (Blindagem Titanium)

Supports two modes via ENV_MODE:
  - PRODUCTION: uploads to / (web root = public_html on Hostinger)
  - STAGING:    uploads to /teste/ (maps to teste.guiadodesconto.com.br)

Important: The FTP account connects directly to the web root (public_html).
The /teste folder IS the subdomínio teste.guiadodesconto.com.br.
"""
import ftplib
import os
from dotenv import load_dotenv

load_dotenv()

# --- Path helpers ---

def _get_staging_prefix():
    """Returns the staging folder prefix for remote paths."""
    return "teste"

def _navigate_to_root(session: ftplib.FTP):
    """Navigate back to the absolute FTP root."""
    session.cwd("/")

def _ensure_remote_dir(session: ftplib.FTP, base_dir: str, sub_path: str):
    """
    Navigate from / to base_dir/sub_path, creating directories as needed.
    Returns the final pwd after navigation.
    Example: base_dir='teste', sub_path='js' -> navigates to /teste/js/
    """
    _navigate_to_root(session)
    session.cwd(base_dir)

    if sub_path:
        parts = sub_path.strip("/").split("/")
        for part in parts:
            try:
                session.cwd(part)
            except ftplib.error_perm:
                print(f"   --- Criando pasta remota: {part}")
                session.mkd(part)
                session.cwd(part)

    return session.pwd()


def upload_to_hostinger(local_file_path, ftp_host, ftp_user, ftp_pass, remote_path='data.json'):
    """
    Envia um arquivo via FTP para Hostinger.

    remote_path: relative path from the web root.
                 Examples: 'data.json', 'js/app.js', 'css/style.css', 'index_staging.html'
    """
    if not ftp_user or ftp_user == "seu_usuario_ftp":
        print("--- FTP nao configurado. Arquivo salvo apenas localmente.")
        return False

    env_mode = os.getenv('ENV_MODE', 'STAGING').upper()

    # Determine base_dir (where to upload relative to FTP root)
    if env_mode == "STAGING":
        base_dir = _get_staging_prefix()   # /teste
    else:
        base_dir = None                     # / (web root)

    print(f"--- Iniciando upload ({env_mode}) para {ftp_host}...")
    print(f"   --- Arquivo local:   {local_file_path}")
    print(f"   --- Destino remoto:  /{base_dir + '/' if base_dir else ''}{remote_path}")

    if not os.path.exists(local_file_path):
        print(f"   --- ERRO: Arquivo local nao existe: {local_file_path}")
        return False

    file_size = os.path.getsize(local_file_path)
    print(f"   --- Tamanho local:   {file_size} bytes")

    max_retries = 3
    session = None
    for attempt in range(max_retries):
        try:
            print(f"   --- Tentativa {attempt + 1}/{max_retries} de conexao FTP...")
            session = ftplib.FTP(ftp_host, ftp_user, ftp_pass, timeout=60)
            break
        except Exception as e:
            if attempt == max_retries - 1: raise e
            print(f"   --- ⚠️ Timeout/Erro na conexao ({e}). Tentando novamente em 5s...")
            import time
            time.sleep(5)

    if session:
        print(f"   --- Conectado! PWD inicial: {session.pwd()}")

        # Split remote_path into directory + filename
        if "/" in remote_path:
            remote_dir = "/".join(remote_path.split("/")[:-1])  # e.g. 'js'
            remote_filename = remote_path.split("/")[-1]        # e.g. 'app.js'
        else:
            remote_dir = ""
            remote_filename = remote_path                       # e.g. 'data.json'

        # Navigate to correct destination
        if base_dir:
            final_pwd = _ensure_remote_dir(session, base_dir, remote_dir)
        else:
            # PRODUCTION: navigate from root
            _navigate_to_root(session)
            if remote_dir:
                parts = remote_dir.strip("/").split("/")
                for part in parts:
                    try:
                        session.cwd(part)
                    except ftplib.error_perm:
                        session.mkd(part)
                        session.cwd(part)
            final_pwd = session.pwd()

        print(f"   --- Navegado para:   {final_pwd}")

        # Check if file already exists
        existing = []
        session.retrlines('LIST', existing.append)
        if any(remote_filename in l for l in existing):
            print(f"   --- {remote_filename} ja existe (sera sobrescrito)")
        else:
            print(f"   --- {remote_filename} novo (sera criado)")

        # Upload
        print(f"   --- Enviando arquivo como {remote_filename}...")
        with open(local_file_path, 'rb') as f:
            result = session.storbinary(f'STOR {remote_filename}', f)
        print(f"   --- Resposta do servidor: {result}")

        # Verify size
        try:
            remote_size = session.size(remote_filename)
            print(f"   --- Tamanho no servidor: {remote_size} bytes")
            if remote_size == file_size:
                print(f"   --- ✅ Tamanhos conferem!")
            else:
                print(f"   --- ⚠️ Tamanhos DIFERENTES! Local: {file_size}, Remoto: {remote_size}")
        except Exception:
            print(f"   --- (Verificacao de tamanho nao suportada pelo servidor)")

        session.quit()
        print("--- Upload concluido com sucesso!")
        return True

    except Exception as e:
        import traceback
        print(f"--- ❌ Erro no upload FTP: {e}")
        traceback.print_exc()
        return False
