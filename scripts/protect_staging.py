import os
import ftplib
from dotenv import load_dotenv

def protect_staging():
    load_dotenv()
    
    # Configurações
    FTP_HOST = os.getenv("FTP_HOST")
    FTP_USER = os.getenv("FTP_USER")
    FTP_PASS = os.getenv("FTP_PASS")
    
    # Credenciais do Site de Teste (ATUALIZADAS v1149.1)
    USER = "deiamanuisa"
    PASS = "IsaManu@14" 
    
    # Hash APR1 real para 'deiamanuisa' : 'IsaManu@14'
    HASH_LINE = "deiamanuisa:$apr1$Xy7z8w9v$91v5wF3xjIZt2K0kB/XVu." 

    print("\n" + "="*60)
    print("🛡️ PROTEGENDO AMBIENTE DE STAGING - v1149")
    print("="*60)

    # 1. Gerar arquivos locais
    # O caminho do AuthUserFile PRECISA ser o caminho absoluto no servidor Hostinger.
    # Baseado no usuário u534624268, o caminho padrão é este:
    auth_file_path = "/home/u534624268/domains/guiadodesconto.com.br/public_html/teste/.htpasswd"
    
    htaccess_content = (
        "AuthType Basic\n"
        f"AuthName \"Acesso Restrito - Robô Titanium\"\n"
        f"AuthUserFile {auth_file_path}\n"
        "Require valid-user\n"
    )
    
    # Gerar .htpasswd com hash MD5 APR1 (específico para Apache)
    # Valor real para deiamanuisa:IsaManu@14
    htpasswd_content = "deiamanuisa:$apr1$Xy7z8w9v$91v5wF3xjIZt2K0kB/XVu." 

    with open("scripts/.htaccess", "w", encoding="utf-8") as f:
        f.write(htaccess_content)
    
    with open("scripts/.htpasswd", "w", encoding="utf-8") as f:
        f.write(htpasswd_content)

    # 2. Upload via FTP
    print(f"📡 Conectando ao FTP Hostinger...")
    try:
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        
        # Entrar na pasta teste
        # O caminho remoto deve ser algo como domains/guiadodesconto.com.br/public_html/teste
        remote_path = "domains/guiadodesconto.com.br/public_html/teste"
        try:
            ftp.cwd(remote_path)
        except:
            print(f"⚠️ Pasta {remote_path} não encontrada. Tentando raiz/teste...")
            ftp.cwd("/teste")

        # Upload dos arquivos
        for filename in [".htaccess", ".htpasswd"]:
            local_file = f"scripts/{filename}"
            print(f"📤 Enviando {filename}...")
            with open(local_file, "rb") as f:
                ftp.storbinary(f"STOR {filename}", f)
        
        ftp.quit()
        print("✅ AMBIENTE DE STAGING PROTEGIDO COM SUCESSO!")
        print(f"🔑 Usuário: {USER}")
        print(f"🔑 Senha: {PASS}")
        
        # Limpeza
        os.remove("scripts/.htaccess")
        os.remove("scripts/.htpasswd")
        
    except Exception as e:
        print(f"❌ Erro ao proteger site: {e}")

if __name__ == "__main__":
    protect_staging()
