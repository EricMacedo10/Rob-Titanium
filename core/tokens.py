import requests
import json
import time
import os

# --- ARQUIVO DE TOKENS ---
STATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "state")
TOKEN_FILE = os.path.join(STATE_DIR, "meli_tokens.json")

# --- CREDENCIAIS ---
CLIENT_ID = os.getenv("MELI_CLIENT_ID", "YOUR_MELI_CLIENT_ID")
CLIENT_SECRET = os.getenv("MELI_CLIENT_SECRET", "YOUR_MELI_CLIENT_SECRET")
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
    refresh_token = tokens.get('refresh_token') if tokens else None
    
    # Fallback: Environment Variable (GitHub Actions)
    if not refresh_token:
        refresh_token = os.environ.get("MELI_REFRESH_TOKEN")
        
    if not refresh_token:
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
        "refresh_token": refresh_token
    }
    
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        new_tokens = response.json()
        
        # Se carregou do arquivo, atualiza o arquivo
        if tokens:
            tokens.update(new_tokens)
            tokens['updated_at'] = time.time()
            save_tokens(tokens)
        else:
            # Se veio de Env Var, não salvamos em arquivo (readonly environment), mas retornamos
            pass
            
        return new_tokens['access_token']
    else:
        raise Exception(f"Erro ao renovar token: {response.text}")

def get_valid_token():
    """
    Retorna um token válido, renovando se necessário.
    """
    tokens = load_tokens()
    
    # Se tem arquivo local, valida expiração
    if tokens:
        now = time.time()
        updated_at = tokens.get('updated_at', 0)
        expires_in = tokens.get('expires_in', 21600) 
        
        if (now - updated_at) > (expires_in - 3600):
            try:
                return refresh_access_token()
            except Exception as e:
                print(f"Erro na renovação automática: {e}")
                return None
        return tokens.get('access_token')
    
    # Se não tem arquivo, tenta renovar direto usando Env Var (stateless mode)
    if os.environ.get("MELI_REFRESH_TOKEN"):
         try:
             return refresh_access_token()
         except Exception as e:
             print(f"Erro na renovação via Env Var: {e}")
             return None
             
    return None

def save_tokens(tokens):
    try:
        with open(TOKEN_FILE, "w") as f:
            json.dump(tokens, f, indent=4)
    except:
        pass # Pode falhar em ambientes readonly

def load_tokens():
    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, "r") as f:
                return json.load(f)
        except:
            return None
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
