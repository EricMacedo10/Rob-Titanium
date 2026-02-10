"""
🛡️ Deploy Seguro: Metatag Lomadee (Senior Workflow)
Operação cirúrgica: backup do index.html atual, upload do atualizado.
Não mexe em nenhum outro arquivo do site.
"""
import ftplib
import os
import shutil
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# === CONFIGURAÇÃO ===
SITE_DIR = Path('site')
LOCAL_INDEX = SITE_DIR / 'index.html'
BACKUP_DIR = Path('backups')
TIMESTAMP = datetime.now().strftime('%Y%m%d_%H%M%S')

def main():
    print("=" * 60)
    print("🛡️  DEPLOY SEGURO: Metatag Lomadee")
    print("     Seguindo SKILL_SENIOR_WORKFLOW")
    print("=" * 60)

    # ──────────────────────────────────────────────
    # ETAPA 1: Validação Local
    # ──────────────────────────────────────────────
    print("\n📋 ETAPA 1: Validação Local")
    
    if not LOCAL_INDEX.exists():
        print("❌ ERRO: site/index.html não encontrado!")
        return False
    
    content = LOCAL_INDEX.read_text(encoding='utf-8')
    
    # Verificar se a metatag Lomadee está presente
    if '<meta name="lomadee" content="2324685" />' not in content:
        print("❌ ERRO: Metatag Lomadee NÃO encontrada no index.html local!")
        return False
    print("   ✅ Metatag Lomadee encontrada no arquivo local")
    
    # Verificar se o HTML está íntegro (tags essenciais)
    checks = [
        ('<html', 'Tag <html>'),
        ('</html>', 'Tag </html>'),
        ('<head>', 'Tag <head>'),
        ('</head>', 'Tag </head>'),
        ('<body>', 'Tag <body>'),
        ('</body>', 'Tag </body>'),
        ('id="search-input"', 'Campo de busca'),
        ('id="tech-hub-card"', 'Card Tecnologia'),
        ('id="home-hub-card"', 'Card Casa'),
        ('id="carnaval-hub-card"', 'Card Carnaval'),
        ('app.js', 'Script app.js'),
        ('style.css', 'Stylesheet style.css'),
        ('family-widget', 'Family Widget'),
        ('titanium-bot-trap', 'Honeypot Security'),
    ]
    
    all_ok = True
    for tag, label in checks:
        if tag not in content:
            print(f"   ❌ FALHA: {label} ausente!")
            all_ok = False
        else:
            print(f"   ✅ {label}")
    
    if not all_ok:
        print("\n🚫 DEPLOY ABORTADO: Integridade do HTML comprometida!")
        return False
    
    print(f"   ✅ Total de linhas: {len(content.splitlines())}")
    print("   ✅ Validação local APROVADA!")

    # ──────────────────────────────────────────────
    # ETAPA 2: Backup do arquivo atual do servidor
    # ──────────────────────────────────────────────
    print("\n📋 ETAPA 2: Backup do index.html atual (servidor)")
    
    ftp_host = os.getenv('FTP_HOST')
    ftp_user = os.getenv('FTP_USER')
    ftp_pass = os.getenv('FTP_PASS')
    
    if not all([ftp_host, ftp_user, ftp_pass]):
        print("❌ ERRO: Credenciais FTP ausentes no .env!")
        return False
    
    try:
        ftp = ftplib.FTP(ftp_host, ftp_user, ftp_pass, timeout=120)
        print(f"   ✅ Conectado ao FTP: {ftp_host}")
    except Exception as e:
        print(f"❌ ERRO ao conectar FTP: {e}")
        return False
    
    # Navegar para public_html
    base_path = "/"
    for p in ["public_html", "www"]:
        try:
            ftp.cwd(f"/{p}")
            base_path = f"/{p}"
            print(f"   ✅ Web root: {base_path}")
            break
        except:
            continue
    
    # Fazer backup do index.html atual
    BACKUP_DIR.mkdir(exist_ok=True)
    backup_file = BACKUP_DIR / f"index_backup_{TIMESTAMP}.html"
    
    try:
        with open(backup_file, 'wb') as f:
            ftp.retrbinary('RETR index.html', f.write)
        print(f"   ✅ Backup salvo em: {backup_file}")
        
        # Verificar tamanho do backup
        backup_size = backup_file.stat().st_size
        if backup_size < 100:
            print(f"   ⚠️ AVISO: Backup muito pequeno ({backup_size} bytes)")
        else:
            print(f"   ✅ Tamanho do backup: {backup_size} bytes")
    except Exception as e:
        print(f"   ⚠️ Backup falhou (arquivo pode não existir no servidor): {e}")
        print("   ℹ️ Continuando sem backup (primeiro deploy?)")

    # ──────────────────────────────────────────────
    # ETAPA 3: Upload do index.html atualizado
    # ──────────────────────────────────────────────
    print("\n📋 ETAPA 3: Upload do index.html atualizado")
    
    try:
        ftp.cwd(base_path)
        with open(LOCAL_INDEX, 'rb') as f:
            ftp.storbinary('STOR index.html', f)
        print("   ✅ Upload concluído com sucesso!")
    except Exception as e:
        print(f"❌ ERRO no upload: {e}")
        print("🔄 Tentando restaurar backup...")
        try:
            with open(backup_file, 'rb') as f:
                ftp.storbinary('STOR index.html', f)
            print("   ✅ Backup restaurado! Nenhuma alteração foi feita no site.")
        except:
            print("   ❌ Falha ao restaurar backup. Verifique manualmente!")
        ftp.quit()
        return False

    # ──────────────────────────────────────────────
    # ETAPA 4: Verificação Pós-Deploy
    # ──────────────────────────────────────────────
    print("\n📋 ETAPA 4: Verificação Pós-Deploy")
    
    try:
        # Verificar se index.html existe no servidor
        files_list = []
        ftp.retrlines('LIST', files_list.append)
        index_found = any('index.html' in l for l in files_list)
        
        if index_found:
            print("   ✅ index.html confirmado no servidor")
        else:
            print("   ❌ index.html NÃO encontrado no servidor!")
            ftp.quit()
            return False
        
        # Verificar outros arquivos críticos
        for crit_dir, crit_file in [('js', 'app.js'), ('css', 'style.css')]:
            try:
                ftp.cwd(f"{base_path}/{crit_dir}")
                dir_files = []
                ftp.retrlines('LIST', dir_files.append)
                if any(crit_file in l for l in dir_files):
                    print(f"   ✅ {crit_dir}/{crit_file} intacto")
                else:
                    print(f"   ⚠️ {crit_dir}/{crit_file} não encontrado")
            except:
                print(f"   ⚠️ Pasta {crit_dir}/ não encontrada")
        
    except Exception as e:
        print(f"   ⚠️ Erro na verificação: {e}")
    
    ftp.quit()
    
    # ──────────────────────────────────────────────
    # RESULTADO FINAL
    # ──────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("🎉 DEPLOY CONCLUÍDO COM SUCESSO!")
    print(f"   📁 Backup: {backup_file}")
    print(f"   🌐 Verificação: Acesse https://guiadodesconto.com.br")
    print(f"   🔍 Clique com botão direito -> 'Exibir código-fonte'")
    print(f"   🏷️  Procure por: lomadee")
    print("=" * 60)
    print("\n⏭️  Próximo passo: Volte na Lomadee e clique 'Validar metatag'")
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
