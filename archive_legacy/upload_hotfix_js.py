import os
from infra.upload_logic import upload_to_hostinger
from dotenv import load_dotenv

load_dotenv()

# FORÇAR MODO PRODUÇÃO PARA O HOTFIX
os.environ['ENV_MODE'] = 'PRODUCTION'

ftp_host = os.getenv('FTP_HOST')
ftp_user = os.getenv('FTP_USER')
ftp_pass = os.getenv('FTP_PASS')

print("🚀 TITANIUM PRODUCTION ROBUST UPDATE (v1.3) 🚀")
print("⚠️ FORÇANDO MODO: PRODUÇÃO (Web Root)")

# 1. Update Homepage Assets (Robustness for index.html)
print("\n[Home] Enviando app.js (Filtros + Menor Preço)...")
upload_to_hostinger('site/js/app.js', ftp_host, ftp_user, ftp_pass, remote_path='js/app.js')

print("[Home] Enviando style.css (Novo Design Premium)...")
upload_to_hostinger('site/css/style.css', ftp_host, ftp_user, ftp_pass, remote_path='css/style.css')

# 2. Update Category Assets (Showcase fix)
print("\n[Categoria] Sincronizando app_categoria.js...")
upload_to_hostinger('site/js/app_categoria.js', ftp_host, ftp_user, ftp_pass, remote_path='js/app_categoria.js')

print("[Categoria] Sincronizando categoria.html...")
upload_to_hostinger('site/categoria.html', ftp_host, ftp_user, ftp_pass, remote_path='categoria.html')

print("\n✨ Update em PRODUÇÃO Finalizado! ✨")
