import os
import ftplib
import io
from pathlib import Path
from dotenv import load_dotenv

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def deploy_htaccess_bypass():
    print("🚀 TITANIUM SOCIAL: Configurando Bypass Anti-Bloqueio (Hostinger) 🚀")
    load_dotenv()
    
    ftp_host = os.getenv('FTP_HOST')
    ftp_user = os.getenv('FTP_USER')
    ftp_pass = os.getenv('FTP_PASS')
    
    if not all([ftp_host, ftp_user, ftp_pass]):
        print("❌ FTP credentials missing!")
        return False
        
    htaccess_content = """# Titanium Social Bot - Meta Bypass Rule
# Permite que os servidores do Instagram/Facebook baixem os videos sem serem bloqueados
<IfModule mod_setenvif.c>
    SetEnvIfNoCase User-Agent "^facebookexternalhit" allow_facebook
    SetEnvIfNoCase User-Agent "^Instagram" allow_facebook
</IfModule>

<Limit GET POST HEAD>
    Order Allow,Deny
    Allow from all
    Allow from env=allow_facebook
</Limit>
"""
    
    print(f"📡 Conectando ao servidor {ftp_host}...")
    try:
        ftp = ftplib.FTP(ftp_host, ftp_user, ftp_pass, timeout=60)
        
        for p in ["public_html", "www"]:
            try:
                ftp.cwd(f"/{p}")
                print(f"✅ Web root encontrado: /{p}")
                break
            except:
                continue
                
        # Fazendo o upload do .htaccess
        file_obj = io.BytesIO(htaccess_content.encode('utf-8'))
        ftp.storbinary('STOR .htaccess', file_obj)
        print("✅ Arquivo .htaccess atualizado com sucesso no servidor!")
        
        ftp.quit()
        return True
    except Exception as e:
        print(f"❌ Erro ao configurar o bypass: {e}")
        return False

if __name__ == "__main__":
    deploy_htaccess_bypass()
