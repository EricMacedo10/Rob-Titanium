import os
from infra.upload_logic import upload_to_hostinger
from dotenv import load_dotenv

load_dotenv()

ftp_host = os.getenv('FTP_HOST')
ftp_user = os.getenv('FTP_USER')
ftp_pass = os.getenv('FTP_PASS')

print("Uploading data.json para STAGING...")
upload_to_hostinger('site/data.json', ftp_host, ftp_user, ftp_pass, remote_path='data.json')

print("Uploading notifications.json para STAGING...")
upload_to_hostinger('site/notifications.json', ftp_host, ftp_user, ftp_pass, remote_path='notifications.json')

print("Upload rápido concluído.")
