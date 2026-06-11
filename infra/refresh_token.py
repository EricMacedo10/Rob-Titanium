import os, sys, requests, ftplib, io, re
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv('.env')

SHORT_TOKEN = os.getenv('SHORT_TOKEN', '')

APP_ID     = os.getenv('APP_ID')
APP_SECRET = os.getenv('APP_SECRET')

print("=" * 60)
print("TITANIUM TOKEN MANAGER — Long-Lived Token Generator")
print("=" * 60)

if not APP_ID or not APP_SECRET:
    print(f"APP_ID={APP_ID}")
    print(f"APP_SECRET={'***' if APP_SECRET else 'AUSENTE'}")
    print()
    print("ERRO: APP_ID ou APP_SECRET nao encontrados no .env")
    print("Verificando .env atual...")
    with open('.env', 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            if not line.strip().startswith('#') and line.strip():
                key = line.split('=')[0].strip()
                print(f"  Chave encontrada: {key}")
    sys.exit(1)

# PASSO 1: Converter em Long-Lived Token (60 dias)
print(f"\n[1] Convertendo Short-Lived -> Long-Lived Token...")
resp = requests.get(
    "https://graph.facebook.com/v21.0/oauth/access_token",
    params={
        "grant_type": "fb_exchange_token",
        "client_id": APP_ID,
        "client_secret": APP_SECRET,
        "fb_exchange_token": SHORT_TOKEN
    }
)
data = resp.json()

if 'access_token' not in data:
    print(f"ERRO ao converter token: {data}")
    sys.exit(1)

LONG_TOKEN = data['access_token']
expires_in = data.get('expires_in', 'N/A')
print(f"   Long-Lived Token obtido! Expira em: {expires_in} segundos (~{int(expires_in)//86400} dias)")
print(f"   Token (primeiros 30 chars): {LONG_TOKEN[:30]}...")

# PASSO 2: Verificar o token
print(f"\n[2] Verificando token com a API Meta...")
verify = requests.get(
    f"https://graph.facebook.com/v21.0/me",
    params={"access_token": LONG_TOKEN, "fields": "id,name"}
).json()
print(f"   Conta: {verify}")

# PASSO 3: Buscar Page Token para DMs
print(f"\n[3] Buscando Page Token...")
pages_resp = requests.get(
    f"https://graph.facebook.com/v21.0/me/accounts",
    params={"access_token": LONG_TOKEN}
).json()
print(f"   Paginas encontradas: {pages_resp}")

# PASSO 4: Salvar no .env para referencia futura
print(f"\n[4] Salvando novo token no .env...")
with open('.env', 'r', encoding='utf-8', errors='replace') as f:
    env_content = f.read()

# Atualiza IG_ACCESS_TOKEN no .env
if 'IG_ACCESS_TOKEN=' in env_content:
    env_content = re.sub(r'IG_ACCESS_TOKEN=.*', f'IG_ACCESS_TOKEN={LONG_TOKEN}', env_content)
else:
    env_content += f'\nIG_ACCESS_TOKEN={LONG_TOKEN}'

with open('.env', 'w', encoding='utf-8') as f:
    f.write(env_content)
print("   .env atualizado!")

# PASSO 5: Atualizar bot_instagram.php (Moda)
print(f"\n[5] Atualizando social/bot_instagram.php (Moda Titanium)...")
with open('social/bot_instagram.php', 'r', encoding='utf-8', errors='replace') as f:
    php_moda = f.read()
php_moda = re.sub(r'\$USER_TOKEN\s*=\s*"[^"]*"', f'$USER_TOKEN = "{LONG_TOKEN}"', php_moda)
with open('social/bot_instagram.php', 'w', encoding='utf-8') as f:
    f.write(php_moda)
print("   bot_instagram.php (Moda) atualizado!")

# PASSO 6: Atualizar bot_instagram_pesca.php (Pesca)
print(f"\n[6] Atualizando pesca/bot_instagram_pesca.php (Pesca Titanium)...")
with open('pesca/bot_instagram_pesca.php', 'r', encoding='utf-8', errors='replace') as f:
    php_pesca = f.read()
php_pesca = re.sub(r'\$USER_TOKEN\s*=\s*"[^"]*"', f'$USER_TOKEN = "{LONG_TOKEN}"', php_pesca)
with open('pesca/bot_instagram_pesca.php', 'w', encoding='utf-8') as f:
    f.write(php_pesca)
print("   bot_instagram_pesca.php (Pesca) atualizado!")

# PASSO 7: Deploy FTP
print(f"\n[7] Fazendo deploy FTP para o Hostinger...")
ftp = ftplib.FTP(os.getenv('FTP_HOST'), os.getenv('FTP_USER'), os.getenv('FTP_PASS'))
print("   Conectado ao FTP!")

with open('social/bot_instagram.php', 'rb') as f:
    ftp.storbinary('STOR bot_instagram.php', f)
print("   bot_instagram.php (Moda) -> Hostinger OK!")

with open('pesca/bot_instagram_pesca.php', 'rb') as f:
    ftp.storbinary('STOR bot_instagram_pesca.php', f)
print("   bot_instagram_pesca.php (Pesca) -> Hostinger OK!")

ftp.quit()

print()
print("=" * 60)
print("DEPLOY COMPLETO!")
print(f"Long-Lived Token ativo por ~60 dias")
print(f"Ambos os robos (Moda + Pesca) estao operacionais!")
print("=" * 60)
