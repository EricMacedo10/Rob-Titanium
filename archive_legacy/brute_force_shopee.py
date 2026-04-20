import hashlib
import time
import json
import requests

import os

# AppID confirmado
APP_ID = os.getenv("SHOPEE_APP_ID", "YOUR_APP_ID")
ENDPOINT = "https://open-api.affiliate.shopee.com.br/v2/api/graphql"

# Variações possíveis da Senha (Baseado na leitura visual do print)
# Pos 9: Pode ser K ou X
# Pos 21: Pode ser 0 ou O
secrets_to_test = [
    "YOUR_SECRET_GUESS_1", 
    "YOUR_SECRET_GUESS_2", 
    "YOUR_SECRET_GUESS_3", 
    "YOUR_SECRET_GUESS_4"  
]

def test_permutation(secret):
    timestamp = int(time.time())
    query = """query($limit:Int){productOfferV2List(page:1,limit:$limit,sortType:"sales_volume",sortOrder:"desc"){nodes{itemId,productName,price}}}"""
    variables = {"limit": 1}
    body = json.dumps({"query": query, "variables": variables}, separators=(',', ':'))
    
    # Ordem V2: AppID + Timestamp + Payload + Secret
    factor = f"{APP_ID}{timestamp}{body}{secret}"
    signature = hashlib.sha256(factor.encode("utf-8")).hexdigest()
    
    headers = {
        "Authorization": f"SHA256 Credential={APP_ID},Timestamp={timestamp},Signature={signature}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(ENDPOINT, headers=headers, data=body, timeout=5)
        res_json = response.json()
        if "errors" not in res_json:
            return True, secret
        else:
            return False, res_json["errors"][0]["message"]
    except:
        return False, "Erro de rede"

if __name__ == "__main__":
    print(f"Iniciando Brute-Force Titanium para destravar AppID {APP_ID}...")
    for s in secrets_to_test:
        print(f"Testando: {s[:12]}...{s[-4:]}", end=" -> ")
        success, msg = test_permutation(s)
        if success:
            print("SUCESSO! Chave encontrada.")
            print(f"\nCHAVE VALIDA: {s}")
            break
        else:
            print(f"Falhou ({msg})")
