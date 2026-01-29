import ftplib
import os
import time

MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

def upload_to_hostinger(local_file_path, ftp_host, ftp_user, ftp_pass, remote_filename='data.json'):
    """
    Envia o arquivo data.json atualizado para a Hostinger via FTP.
    O usuário FTP já inicia em public_html, então upload direto.
    Inclui retry automático para lidar com timeouts.
    """
    if not ftp_user or ftp_user == "seu_usuario_ftp":
        print("⚠ FTP não configurado. O arquivo foi salvo apenas localmente.")
        return False

    for attempt in range(1, MAX_RETRIES + 1):
        print(f"🚀 Tentativa {attempt}/{MAX_RETRIES} - Upload para {ftp_host}...")
        
        try:
            session = ftplib.FTP(ftp_host, ftp_user, ftp_pass, timeout=120)
            current_dir = session.pwd()
            print(f"✅ Conectado! Diretório: {current_dir}")
            
            # Force delete existing file to ensure update
            try:
                session.delete(remote_filename)
                print(f"🗑️ Arquivo antigo removido")
            except Exception:
                print("ℹ Arquivo não existia (prosseguindo...)")

            # Upload directly (user already in public_html)
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
            print(f"⚠️ Erro na tentativa {attempt}: {e}")
            if attempt < MAX_RETRIES:
                print(f"⏳ Aguardando {RETRY_DELAY}s antes de tentar novamente...")
                time.sleep(RETRY_DELAY)
            else:
                print(f"❌ Falha após {MAX_RETRIES} tentativas.")
                return False
    
    return False


