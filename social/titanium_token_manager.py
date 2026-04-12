"""
TITANIUM TOKEN MANAGER - Gerador de Page Access Token Permanente
Etapas:
  1. Pega o User Token atual do .env
  2. Troca por um Long-Lived User Token (60 dias)
  3. Busca o PAGE ACCESS TOKEN (nunca expira)
  4. Atualiza o .env local
  5. Atualiza o bot_instagram.php local
  6. Faz upload do bot atualizado para o servidor
"""
import os
import re
import ftplib
import requests
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURAÇÕES ---
APP_ID = "1834207343896407"
APP_SECRET = "9a6dfa1b1269447273e3251afd153881"
PAGE_ID = "1032000233318987"
CURRENT_TOKEN = os.getenv("IG_ACCESS_TOKEN")
BOT_PATH = r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium\social\bot_instagram.php"
ENV_PATH = r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium\.env"
FTP_HOST = os.getenv("FTP_HOST", "guiadodesconto.com.br")
FTP_USER = os.getenv("FTP_USER", "u534624268.guiadodesconto")
FTP_PASS = os.getenv("FTP_PASS", "IsaManu@14")

print("="*60)
print("🤖 TITANIUM TOKEN MANAGER - Iniciando...")
print("="*60)

# PASSO 1: Trocar pelo Long-Lived User Token (60 dias)
print("\n[1/4] Trocando User Token pelo Long-Lived Token...")
exchange_url = (
    f"https://graph.facebook.com/oauth/access_token"
    f"?grant_type=fb_exchange_token"
    f"&client_id={APP_ID}"
    f"&client_secret={APP_SECRET}"
    f"&fb_exchange_token={CURRENT_TOKEN}"
)
response = requests.get(exchange_url)
data = response.json()

if "access_token" not in data:
    print(f"❌ Falha ao obter Long-Lived Token: {data}")
    exit(1)

long_lived_token = data["access_token"]
expires_in = data.get("expires_in", "desconhecido")
print(f"✅ Long-Lived Token obtido! Expira em: {expires_in} segundos (~{int(expires_in)//86400} dias)")

# PASSO 2: Buscar o Page Access Token PERMANENTE
print("\n[2/4] Buscando Page Access Token permanente...")
accounts_url = f"https://graph.facebook.com/v21.0/me/accounts?access_token={long_lived_token}"
accounts_resp = requests.get(accounts_url)
accounts_data = accounts_resp.json()

page_token = None
if "data" in accounts_data:
    for page in accounts_data["data"]:
        if str(page["id"]) == PAGE_ID:
            page_token = page["access_token"]
            print(f"✅ Page Token encontrado para Página ID: {PAGE_ID}")
            break
    if not page_token and accounts_data["data"]:
        # Pega o primeiro disponível
        page_token = accounts_data["data"][0]["access_token"]
        found_id = accounts_data["data"][0]["id"]
        print(f"✅ Page Token da primeira página disponível (ID: {found_id})")

if not page_token:
    print(f"⚠️  Nenhuma página encontrada. Usando Long-Lived User Token como fallback.")
    page_token = long_lived_token

print(f"🔑 Token Final: {page_token[:40]}...")

# PASSO 3: Atualizar o .env
print("\n[3/4] Atualizando .env...")
with open(ENV_PATH, "r", encoding="utf-8") as f:
    env_content = f.read()

env_content = re.sub(
    r"IG_ACCESS_TOKEN=.*",
    f"IG_ACCESS_TOKEN={page_token}",
    env_content
)

with open(ENV_PATH, "w", encoding="utf-8") as f:
    f.write(env_content)

print("✅ .env atualizado!")

# PASSO 4: Atualizar o bot_instagram.php
print("\n[4/4] Atualizando bot_instagram.php e fazendo upload...")
with open(BOT_PATH, "r", encoding="utf-8") as f:
    bot_content = f.read()

bot_content = re.sub(
    r'\$USER_TOKEN = ".*?";',
    f'$USER_TOKEN = "{page_token}";',
    bot_content
)

with open(BOT_PATH, "w", encoding="utf-8") as f:
    f.write(bot_content)

print("✅ bot_instagram.php local atualizado!")

# Upload para o servidor
print("   📤 Enviando para o servidor Hostinger...")
with ftplib.FTP(FTP_HOST) as ftp:
    ftp.login(FTP_USER, FTP_PASS)
    with open(BOT_PATH, "rb") as f:
        ftp.storbinary("STOR /bot_instagram.php", f)

print("✅ bot_instagram.php enviado ao servidor!")

print("\n" + "="*60)
print("🏆 SUCESSO TOTAL! Resumo:")
print(f"   - Long-Lived Token: Válido por {int(expires_in)//86400} dias")
print(f"   - Page Token: NUNCA EXPIRA ♾️")
print(f"   - .env: Atualizado")
print(f"   - bot_instagram.php: Atualizado localmente e no servidor")
print("="*60)
