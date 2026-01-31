from scraper.upload import upload_to_hostinger

# Credentials provided by user
ftp_host = "ftp.guiadodesconto.com.br"
ftp_user = "u534624268.guiadodesconto"
ftp_pass = "IsaManu@14"

print("🔥 Iniciando upload manual de emergência...")

# Upload data.json (Generated locally, verified to have images)
success_data = upload_to_hostinger('site/data.json', ftp_host, ftp_user, ftp_pass, 'data.json')

# Upload notifications.json
success_notif = upload_to_hostinger('site/notifications.json', ftp_host, ftp_user, ftp_pass, 'notifications.json')

if success_data:
    print("✅ Site RECUPERADO com sucesso!")
else:
    print("❌ Falha no upload manual.")
