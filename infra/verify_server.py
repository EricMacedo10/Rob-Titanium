"""
verify_server.py — Verifica se os assets do subdomínio staging estão atualizados.
Staging URL: https://teste.guiadodesconto.com.br/
"""
import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

STAGING_USER = os.getenv('STAGING_USER', 'deiamanuisa')
STAGING_PASS = os.getenv('STAGING_PASS', 'IsaManu@14')
BASE_URL = "https://teste.guiadodesconto.com.br"

checks = [
    {
        "url": f"{BASE_URL}/index_staging.html",
        "label": "index_staging.html",
        "checks": [
            ("20260220_v4", "✅ Versão v4 confirmada"),
            ("app.js", "⚠️ app.js mencionado mas versão v4 não encontrada"),
        ]
    },
    {
        "url": f"{BASE_URL}/js/app.js",
        "label": "js/app.js",
        "checks": [
            ("toLocaleString('pt-BR'", "✅ Formatação BRL (toLocaleString) confirmada"),
        ]
    },
    {
        "url": f"{BASE_URL}/data.json",
        "label": "data.json",
        "checks": [
            ('"store": "Shopee"', "✅ Shopee presente no data.json"),
            ('"store": "Mercado Livre"', "✅ Mercado Livre presente no data.json"),
            ('"store": "Amazon"', "✅ Amazon presente no data.json"),
        ]
    },
]

print("=" * 60)
print(f"🔍 VERIFICANDO STAGING: {BASE_URL}")
print("=" * 60)

all_ok = True
for check in checks:
    url = f"{check['url']}?t={int(time.time())}"
    print(f"\n📄 {check['label']}")
    try:
        r = requests.get(url, auth=(STAGING_USER, STAGING_PASS), timeout=10)
        print(f"   Status: {r.status_code} | Size: {len(r.content)} bytes")
        if r.status_code == 200:
            for pattern, msg in check["checks"]:
                if pattern in r.text:
                    print(f"   {msg}")
                else:
                    print(f"   ❌ NÃO encontrado: {pattern}")
                    all_ok = False
        else:
            print(f"   ❌ HTTP {r.status_code}")
            all_ok = False
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        all_ok = False

print("\n" + "=" * 60)
if all_ok:
    print("✅ STAGING 100% ATUALIZADO E OPERACIONAL")
else:
    print("❌ STAGING COM FALHAS — verificar uploads acima")
print("=" * 60)
