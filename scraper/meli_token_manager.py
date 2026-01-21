import requests
import json
import time
import os

# --- ARQUIVO DE TOKENS ---
TOKEN_FILE = os.path.join(os.path.dirname(__file__), "meli_tokens.json")

# --- CREDENCIAIS ---
CLIENT_ID = "2181313931486448"
CLIENT_SECRET = "9Zx4P9wmJtIzHuryQxVL8e5HArKdZxlH"
REDIRECT_URI = "https://www.guiadodesconto.com.br"

def exchange_code_for_token(code):
    """
    Troca o Authorization Code pelo Access Token + Refresh Token
    """
    url = "https://api.mercadolibre.com/oauth/token"
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
    
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        tokens = response.json()
        # Adiciona timestamp para controle
        tokens['updated_at'] = time.time()
        save_tokens(tokens)
        return tokens
    else:
        raise Exception(f"Erro ao trocar token: {response.text}")

def refresh_access_token():
    """
    Usa o Refresh Token para pegar um novo Access Token
    """
    tokens = load_tokens()
    if not tokens or 'refresh_token' not in tokens:
        raise Exception("Nenhum refresh_token encontrado. Faça a autenticação inicial.")

    url = "https://api.mercadolibre.com/oauth/token"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": tokens['refresh_token']
    }
    
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        new_tokens = response.json()
        
        # O ML as vezes retorna um novo refresh_token, as vezes não.
        # Devemos atualizar o que vier.
        tokens.update(new_tokens)
        tokens['updated_at'] = time.time()
        
        save_tokens(tokens)
        print("Token renovado com sucesso!")
        return tokens['access_token']
    else:
        raise Exception(f"Erro ao renovar token: {response.text}")

def get_valid_token():
    """
    Retorna um token válido, renovando se necessário.
    """
    tokens = load_tokens()
    if not tokens:
        return None
        
    now = time.time()
    updated_at = tokens.get('updated_at', 0)
    expires_in = tokens.get('expires_in', 21600) # 6 horas padrão
    
    # Se passou mais de 5 horas, renova (margem de segurança)
    if (now - updated_at) > (expires_in - 3600):
        try:
            return refresh_access_token()
        except Exception as e:
            print(f"Erro na renovação automática: {e}")
            return None
            
    return tokens.get('access_token')

def save_tokens(tokens):
    with open(TOKEN_FILE, "w") as f:
        json.dump(tokens, f, indent=4)

def load_tokens():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return json.load(f)
    return None

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        # Modo manual: python meli_token_manager.py CODIGO
        code = sys.argv[1]
        try:
            tokens = exchange_code_for_token(code)
            print("Autenticação realizada com sucesso!")
            print(f"Access Token: {tokens['access_token'][:10]}...")
            print(f"Refresh Token: {tokens['refresh_token'][:10]}...")
        except Exception as e:
            print(f"FALHA: {e}")
    else:
        # Modo teste de renovação
        try:
            token = get_valid_token()
            if token:
                print(f"Token válido atual: {token[:10]}...")
            else:
                print("Nenhum token válido. Necessário autenticar.")
        except Exception as e:
            print(e)
