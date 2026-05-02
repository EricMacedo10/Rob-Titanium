"""
🛡️ Titanium Social Deploy v1.0
================================
Envia o bot_instagram.php E ofertas.json para o servidor Hostinger.
Garante que a correção Smart Link Priority v2.0 entre em produção.

Uso:
  python -m social.deploy_bot
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import ftplib
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Arquivos a serem sincronizados com o servidor
DEPLOY_FILES = [
    {
        "local": "social/bot_instagram.php",
        "remote": "bot_instagram.php",
        "desc": "Bot de Comentários (Smart Link v2.0)"
    },
    {
        "local": "social/ofertas.json",
        "remote": "ofertas.json",
        "desc": "Dicionário de Links Hashtag→Produto"
    },
]


def deploy_bot():
    print("=" * 60)
    print("🚀 TITANIUM SOCIAL DEPLOY v1.0")
    print("=" * 60)

    ftp_host = os.getenv('FTP_HOST')
    ftp_user = os.getenv('FTP_USER')
    ftp_pass = os.getenv('FTP_PASS')

    if not all([ftp_host, ftp_user, ftp_pass]):
        print("❌ FTP credentials missing! Verifique o .env")
        return False

    # Validar que todos os arquivos locais existem
    for item in DEPLOY_FILES:
        local_path = Path(item["local"])
        if not local_path.exists():
            print(f"❌ Arquivo local não encontrado: {item['local']}")
            return False
        print(f"✅ {item['desc']}: {item['local']} ({local_path.stat().st_size} bytes)")

    print(f"\n📡 Conectando ao servidor {ftp_host}...")

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

        # Upload de cada arquivo
        success_count = 0
        for item in DEPLOY_FILES:
            local_path = Path(item["local"])
            remote_name = item["remote"]

            print(f"\n📤 Enviando {item['desc']}...")
            print(f"   Local:  {local_path}")
            print(f"   Remoto: {base_path}/{remote_name}")

            try:
                with open(local_path, 'rb') as f:
                    ftp.storbinary(f'STOR {remote_name}', f)
                print(f"   ✅ Upload concluído!")
                success_count += 1
            except Exception as e:
                print(f"   ❌ Falha no upload: {e}")

        # Verificação: listar arquivos no servidor
        print(f"\n🔍 Verificando arquivos no servidor...")
        files = []
        ftp.retrlines('LIST', files.append)

        for item in DEPLOY_FILES:
            found = any(item["remote"] in f for f in files)
            status = "✅" if found else "❌"
            print(f"   {status} {item['remote']}: {'encontrado' if found else 'NÃO encontrado'}")

        ftp.quit()

        print(f"\n{'=' * 60}")
        if success_count == len(DEPLOY_FILES):
            print(f"🏆 DEPLOY COMPLETO! {success_count}/{len(DEPLOY_FILES)} arquivos sincronizados.")
            print(f"   O Smart Link Priority v2.0 está ATIVO em produção.")
        else:
            print(f"⚠️  Deploy parcial: {success_count}/{len(DEPLOY_FILES)} arquivos enviados.")
        print("=" * 60)

        return success_count == len(DEPLOY_FILES)

    except Exception as e:
        print(f"❌ Erro de conexão FTP: {e}")
        return False


if __name__ == "__main__":
    success = deploy_bot()
    sys.exit(0 if success else 1)
