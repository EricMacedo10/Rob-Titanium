import sys
import io
import ftplib
import os
from pathlib import Path

# Garante impressão UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def deploy_pesca_bot():
    print("=" * 60)
    print("🚀 TITANIUM PESCA: DEPLOY SÊNIOR CI/CD")
    print("=" * 60)

    ftp_host = os.getenv('FTP_HOST')
    ftp_user = os.getenv('FTP_USER')
    ftp_pass = os.getenv('FTP_PASS')
    
    # Tokens injetados pelo GitHub Actions
    ig_token = os.getenv('PESCA_IG_ACCESS_TOKEN')
    page_id = os.getenv('PESCA_PAGE_ID')

    if not all([ftp_host, ftp_user, ftp_pass]):
        print("❌ Erro: Credenciais de FTP ausentes.")
        return False
        
    if not all([ig_token, page_id]):
        print("❌ Erro: Secrets do Instagram (PESCA_IG_ACCESS_TOKEN ou PESCA_PAGE_ID) ausentes.")
        return False

    local_file = Path("pesca/bot_instagram_pesca.php")
    if not local_file.exists():
        print(f"❌ Erro: Arquivo local não encontrado em {local_file}")
        return False

    # 1. Lê o arquivo original
    print("📝 Lendo código fonte do robô...")
    content = local_file.read_text(encoding="utf-8")
    
    # 2. Injeta os tokens na memória (Segurança: não salva no disco)
    print("🔒 Injetando Secrets no código (Memory Injection)...")
    content = content.replace("COLOQUE_SEU_PESCA_IG_ACCESS_TOKEN_AQUI", ig_token)
    content = content.replace("COLOQUE_SEU_PESCA_PAGE_ID_AQUI", page_id)
    
    # 3. Prepara arquivo temporário em memória para FTP
    memory_file = io.BytesIO(content.encode('utf-8'))

    print(f"\n📡 Conectando ao servidor FTP ({ftp_host})...")
    try:
        ftp = ftplib.FTP(ftp_host, ftp_user, ftp_pass, timeout=60)
        print(f"✅ Conectado ao FTP")

        # Descobrir web root
        base_path = "/"
        for p in ["public_html", "www"]:
            try:
                ftp.cwd(f"/{p}")
                base_path = f"/{p}"
                print(f"✅ Web root encontrado: {base_path}")
                break
            except:
                continue

        remote_name = "bot_instagram_pesca.php"
        print(f"\n📤 Fazendo upload blindado de {remote_name}...")
        
        # Envia arquivo a partir da memória
        ftp.storbinary(f'STOR {remote_name}', memory_file)
        print("   ✅ Upload concluído com sucesso!")

        # Verificação
        print(f"\n🔍 Verificando arquivo no servidor...")
        files = []
        ftp.retrlines('LIST', files.append)
        
        if any(remote_name in f for f in files):
            print(f"   ✅ Arquivo {remote_name} confirmado em produção!")
            ftp.quit()
            print("=" * 60)
            print("🏆 DEPLOY AUTOMÁTICO CONCLUÍDO!")
            print("=" * 60)
            return True
        else:
            print("   ❌ Arquivo não encontrado após upload.")
            ftp.quit()
            return False

    except Exception as e:
        print(f"❌ Erro de conexão/upload FTP: {e}")
        return False

if __name__ == "__main__":
    success = deploy_pesca_bot()
    sys.exit(0 if success else 1)
