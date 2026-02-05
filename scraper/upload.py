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
        print(f"   📍 Diretório inicial (pwd): {pwd}")

        # Tenta entrar na pasta public_html se existir (Padrão Hostinger)
        paths_to_try = [
            'public_html',
            'domains/guiadodesconto.com.br/public_html',
            'www'
        ]
        
        entered = False
        for p in paths_to_try:
            try:
                session.cwd(p)
                print(f"   📂 Entrou em: {p} (PWD: {session.pwd()})")
                entered = True
                break
            except:
                continue
        
        if not entered:
            print("   ⚠️  Nenhuma das pastas padrão (public_html, domains...) foi encontrada. Ficando na raiz.")
        else:
            # Se estivermos em modo STAGING, entrar na subpasta de teste
            env_mode = os.getenv('ENV_MODE', 'STAGING').upper()
            if env_mode == "STAGING":
                try:
                    session.cwd("teste")
                    print(f"   🧪 Modo STAGING: Entrou na subpasta 'teste' (PWD: {session.pwd()})")
                except:
                    try:
                        session.mkd("teste")
                        session.cwd("teste")
                        print(f"   🧪 Modo STAGING: Criou e entrou na subpasta 'teste'")
                    except Exception as e:
                        print(f"   ⚠️ Falha ao entrar na pasta de staging: {e}")

        # List files for debugging (using LIST for more detail)
        print(f"   📂 Listando arquivos no diretório...")
        files_detailed = []
        session.retrlines('LIST', files_detailed.append)
        for line in files_detailed:
            print(f"      {line}")
        
        # Check if data.json exists in the list (for logging only)
        # We don't need to delete, STOR overwrites.
        if any('data.json' in line for line in files_detailed):
            print(f"   ✅ data.json já existe no servidor (será sobrescrito)")
        else:
            print(f"   ⚠️  data.json não encontrado (será criado)")
        
        # Navegar ou Criar Pasta (social/)
        if '/' in remote_path:
            folder = remote_path.split('/')[0]
            try:
                session.cwd(folder)
            except:
                print(f"   📁 Criando pasta remota: {folder}")
                session.mkd(folder)
                session.cwd(folder)
            remote_filename = remote_path.split('/')[-1]
        else:
            remote_filename = remote_path

        # Upload the file
        print(f"   📤 Enviando arquivo como {remote_filename}...")
        with open(local_file_path, 'rb') as file:
            result = session.storbinary(f'STOR {remote_filename}', file)
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
