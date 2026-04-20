from scraper.upload import upload_to_hostinger

import os

# Credentials provided by user or env
ftp_host = os.getenv("FTP_HOST", "ftp.guiadodesconto.com.br")
ftp_user = os.getenv("FTP_USER")
ftp_pass = os.getenv("FTP_PASS")

print("🔥 Iniciando upload manual de emergência...")

# Upload data.json (Generated locally, verified to have images)
success_data = upload_to_hostinger('site/data.json', ftp_host, ftp_user, ftp_pass, 'data.json')

# Upload notifications.json
success_notif = upload_to_hostinger('site/notifications.json', ftp_host, ftp_user, ftp_pass, 'notifications.json')

if success_data:
    print("✅ Site RECUPERADO com sucesso!")
else:
    print("❌ Falha no upload manual.")
