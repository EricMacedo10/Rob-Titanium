import hashlib
import time
import json
import requests

# AppID confirmado
APP_ID = "18318830863"
ENDPOINT = "https://open-api.affiliate.shopee.com.br/v2/api/graphql"

# Variações possíveis da Senha (Baseado na leitura visual do print)
# Pos 9: Pode ser K ou X
# Pos 21: Pode ser 0 ou O
secrets_to_test = [
    "04546A3D5KC664BG6SDHB0EMNTUMSX07", # Guess 1 (K e 0)
    "04546A3D5KC664BG6SDHBOEMNTUMSX07", # Guess 2 (K e O)
    "04546A3D5XC664BG6SDHB0EMNTUMSX07", # Guess 3 (X e 0)
    "04546A3D5XC664BG6SDHBOEMNTUMSX07"  # Guess 4 (X e O)
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
