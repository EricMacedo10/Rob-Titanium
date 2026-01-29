import ftplib
import os

def upload_to_hostinger(local_file_path, ftp_host, ftp_user, ftp_pass, remote_path='public_html/data.json'):
    """
    Envia o arquivo data.json atualizado para a Hostinger via FTP.
    """
    if not ftp_user or ftp_user == "seu_usuario_ftp":
        print("⚠ FTP não configurado. O arquivo foi salvo apenas localmente.")
        return False

    print(f"🚀 Iniciando upload para {ftp_host}...")
    
    try:
        session = ftplib.FTP(ftp_host, ftp_user, ftp_pass)
        
        # Force delete existing file to ensure update
        try:
            print(f"🗑️ Removendo arquivo antigo: {remote_path}")
            session.delete(remote_path)
        except Exception:
            print("ℹ Arquivo não existia ou falha ao remover (prosseguindo...)")

        file = open(local_file_path, 'rb')
        session.storbinary(f'STOR {remote_path}', file)
        file.close()
        
        # Verify size
        try:
            size_on_server = session.size(remote_path)
            print(f"📦 Tamanho no Servidor: {size_on_server} bytes")
        except:
            pass
            
        session.quit()
        print("✅ Upload concluído com sucesso! O site foi atualizado.")
        return True
    except Exception as e:
        print(f"❌ Erro no upload FTP: {e}")
        return False
