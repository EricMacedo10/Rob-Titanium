import ftplib
import os

def upload_to_hostinger(local_file_path, ftp_host, ftp_user, ftp_pass, remote_filename='data.json'):
    """
    Envia o arquivo data.json atualizado para a Hostinger via FTP.
    O usuário FTP já inicia em public_html, então upload direto.
    """
    if not ftp_user or ftp_user == "seu_usuario_ftp":
        print("⚠ FTP não configurado. O arquivo foi salvo apenas localmente.")
        return False

    print(f"🚀 Iniciando upload para {ftp_host}...")
    
    try:
        session = ftplib.FTP(ftp_host, ftp_user, ftp_pass, timeout=60)
        current_dir = session.pwd()
        print(f"✅ Conectado! Diretório atual: {current_dir}")
        
        # Force delete existing file to ensure update
        try:
            print(f"🗑️ Removendo arquivo antigo: {remote_filename}")
            session.delete(remote_filename)
            print("✅ Arquivo antigo removido")
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
        print(f"❌ Erro no upload FTP: {e}")
        return False


