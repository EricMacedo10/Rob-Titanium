import ftplib
import os
from dotenv import load_dotenv

load_dotenv()

with open('probe_2026.txt', 'w') as f:
    f.write('PROBE SUCCESS')

ftp = ftplib.FTP(os.getenv('FTP_HOST'), os.getenv('FTP_USER'), os.getenv('FTP_PASS'))
with open('probe_2026.txt', 'rb') as f:
    ftp.storbinary('STOR probe_2026.txt', f)
ftp.quit()
print("Probe uploaded")
