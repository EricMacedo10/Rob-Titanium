import ftplib
import os

def upload_to_hostinger(local_file_path, ftp_host, ftp_user, ftp_pass, remote_path='data.json'):
    """
    Envia o arquivo data.json atualizado para a Hostinger via FTP.
    """
    if not ftp_user or ftp_user == "seu_usuario_ftp":
        print("⚠ FTP não configurado. O arquivo foi salvo apenas localmente.")
        return False

    print(f"🚀 Iniciando upload para {ftp_host}...")
    print(f"   📁 Arquivo local: {local_file_path}")
    print(f"   📍 Destino remoto: {remote_path}")
    
    # Verify local file exists and show size
    if not os.path.exists(local_file_path):
        print(f"   ❌ ERRO: Arquivo local não existe: {local_file_path}")
        return False
    
    file_size = os.path.getsize(local_file_path)
    print(f"   📦 Tamanho do arquivo: {file_size} bytes")
    
    try:
        print(f"   🔌 Conectando ao FTP...")
        session = ftplib.FTP(ftp_host, ftp_user, ftp_pass, timeout=60)
        print(f"   ✅ Conectado!")
        
        # Show current directory
        pwd = session.pwd()
        print(f"   📍 Diretório atual (pwd): {pwd}")
        
        # List files before upload
        print(f"   📂 Listando arquivos no diretório...")
        files_before = []
        session.retrlines('NLST', files_before.append)
        if 'data.json' in files_before:
            print(f"   ✅ data.json existe no servidor")
        else:
            print(f"   ⚠️  data.json NÃO existe no servidor ainda")
        
        # Upload the file
        print(f"   📤 Enviando arquivo...")
        with open(local_file_path, 'rb') as file:
            result = session.storbinary(f'STOR {remote_path}', file)
            print(f"   📨 Resposta do servidor: {result}")
        
        # Verify file was uploaded - check size
        print(f"   🔍 Verificando upload...")
        try:
            remote_size = session.size(remote_path)
            print(f"   📦 Tamanho no servidor: {remote_size} bytes")
            if remote_size == file_size:
                print(f"   ✅ Tamanhos conferem!")
            else:
                print(f"   ⚠️  ATENÇÃO: Tamanhos diferentes! Local: {file_size}, Remoto: {remote_size}")
        except:
            print(f"   ⚠️  Não foi possível verificar tamanho remoto")
        
        session.quit()
        print("✅ Upload concluído com sucesso! O site foi atualizado.")
        return True
        
    except Exception as e:
        print(f"❌ Erro no upload FTP: {e}")
        import traceback
        traceback.print_exc()
        return False
