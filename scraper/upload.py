import ftplib
import os

# Hostinger path for guiadodesconto.com.br
TARGET_DIR = 'domains/guiadodesconto.com.br/public_html'

def upload_to_hostinger(local_file_path, ftp_host, ftp_user, ftp_pass, remote_filename='data.json'):
    """
    Envia o arquivo data.json atualizado para a Hostinger via FTP.
    Navega até o diretório correto antes de fazer upload.
    """
    if not ftp_user or ftp_user == "seu_usuario_ftp":
        print("⚠ FTP não configurado. O arquivo foi salvo apenas localmente.")
        return False

    print(f"🚀 Iniciando upload para {ftp_host}...")
    
    try:
        session = ftplib.FTP(ftp_host, ftp_user, ftp_pass, timeout=60)
        print(f"✅ Conectado! PWD inicial: {session.pwd()}")
        
        # Navigate to correct directory (like deploy_site.py does)
        print(f"📂 Navegando para: /{TARGET_DIR}")
        try:
            session.cwd(TARGET_DIR)
            print(f"✅ Diretório encontrado! PWD: {session.pwd()}")
        except ftplib.error_perm as e:
            print(f"❌ Erro ao navegar: {e}")
            session.quit()
            return False
        
        # Force delete existing file to ensure update
        try:
            print(f"🗑️ Removendo arquivo antigo: {remote_filename}")
            session.delete(remote_filename)
            print("✅ Arquivo antigo removido")
        except Exception:
            print("ℹ Arquivo não existia (prosseguindo...)")

        # Upload
        print(f"📤 Enviando: {local_file_path} -> {remote_filename}")
        with open(local_file_path, 'rb') as file:
            session.storbinary(f'STOR {remote_filename}', file)
        
        # Verify size
        try:
            size_on_server = session.size(remote_filename)
            print(f"📦 Tamanho no Servidor: {size_on_server} bytes")
        except:
            pass
            
        session.quit()
        print("✅ Upload concluído com sucesso! O site foi atualizado.")
        return True
    except Exception as e:
        print(f"❌ Erro no upload FTP: {e}")
        return False

