import os, ftplib, io, sys
from dotenv import load_dotenv

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

load_dotenv('.env')
ftp = ftplib.FTP(os.getenv('FTP_HOST'), os.getenv('FTP_USER'), os.getenv('FTP_PASS'))

buf = io.BytesIO()
ftp.retrbinary('RETR bot_debug.log', buf.write)
content = buf.getvalue().decode('utf-8', errors='replace')
lines = content.strip().split('\n')

print(f'Total de linhas no log: {len(lines)}')
print()
print('=== ULTIMAS 100 LINHAS DO BOT_DEBUG.LOG ===')
for l in lines[-100:]:
    print(l)

# Procurar erros recentes
print()
print('=== LINHAS COM ERRO NAS ULTIMAS 500 ENTRADAS ===')
recent = lines[-500:]
for i, l in enumerate(recent):
    low = l.lower()
    if any(kw in low for kw in ['erro', 'error', 'fatal', 'falha', 'exception', 'failed', 'invalid', 'denied', 'token', 'expirou']):
        print(f'[{len(lines)-500+i}] {l}')

ftp.quit()
