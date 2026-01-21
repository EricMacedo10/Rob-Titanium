import requests
import json
from urllib.parse import urlencode

# --- CONFIGURAÇÕES DO MERCADO LIVRE ---
CLIENT_ID = "2181313931486448"
CLIENT_SECRET = "9Zx4P9wmJtIzHuryQxVL8e5HArKdZxlH"
REDIRECT_URI = "https://www.guiadodesconto.com.br" 

# --- ENDPOINTS ---
AUTH_URL = "https://auth.mercadolivre.com.br/authorization"
TOKEN_URL = "https://api.mercadolibre.com/oauth/token"

def step_1_get_auth_url():
    """
    Gera a URL de autorização.
    """
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI
    }
    return f"{AUTH_URL}?{urlencode(params)}"

def step_2_get_tokens(code):
    """
    Troca o código de autorização pelos tokens.
    """
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI
    }
    
    print(f"Solicitando token para code: {code}...")
    response = requests.post(TOKEN_URL, headers=headers, data=data)
    
    if response.status_code == 200:
        tokens = response.json()
        with open("meli_tokens.json", "w") as f:
            json.dump(tokens, f, indent=4)
        print("✅ TOKENS SALVOS COM SUCESSO em 'meli_tokens.json'!")
        return tokens
    else:
        print(f"❌ ERRO: {response.status_code}")
        print(response.text)
        return None

if __name__ == "__main__":
    url = step_1_get_auth_url()
    print("\n" + "="*50)
    print("      AUTENTICAÇÃO MERCADO LIVRE")
    print("="*50 + "\n")
    print("1. Abra este link no navegador e autorize:")
    print(f"\n{url}\n")
    print("-" * 50)
    print("2. Você será redirecionado para o guiadodesconto.com.br.")
    print("3. Na URL final, copie o código que aparece depois de '?code='")
    print("   Ex: ...com.br/?code=TG-67890...")
    print("-" * 50)
    
    code = input(">> Cole o CÓDIGO (code) aqui: ").strip()
    
    if code:
        step_2_get_tokens(code)
