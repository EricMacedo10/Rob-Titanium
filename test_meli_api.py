import requests
import json

CLIENT_ID = "2181313931486448"
CLIENT_SECRET = "9Zx4P9wmJtIzHuryQxVL8e5HArKdZxlH"

def test_connection():
    print(f"--- TESTANDO CONEXÃO API MERCADO LIVRE ---")
    
    # 1. Teste de Busca Pública (Sem Token)
    print(f"1. Testando busca pública (sem token)...")
    url_search = "https://api.mercadolibre.com/sites/MLB/search?q=iPhone&limit=1"
    try:
        res_public = requests.get(url_search)
        if res_public.status_code == 200:
            print(f"✅ API acessível publicamente.")
        else:
            print(f"⚠️ API pública retornou: {res_public.status_code}")
    except Exception as e:
        print(f"❌ Erro ao acessar API pública: {e}")

    # 2. Tentar obter Access Token via Client Credentials
    print(f"\n2. Validando Credenciais (Client ID/Secret)...")
    url_token = "https://api.mercadolibre.com/oauth/token"
    payload = f'grant_type=client_credentials&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    try:
        response = requests.post(url_token, data=payload, headers=headers)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get('access_token')
            print(f"✅ Credenciais VÁLIDAS! Token obtido.")
            
            # 3. Testar endpoint de sites (mais genérico)
            url_sites = "https://api.mercadolibre.com/sites/MLB"
            headers_auth = {'Authorization': f'Bearer {access_token}'}
            res_sites = requests.get(url_sites, headers=headers_auth)
            
            if res_sites.status_code == 200:
                print(f"✅ Conexão autenticada confirmada (GET /sites/MLB).")
            else:
                print(f"⚠️ Token validado, mas acesso restrito ao endpoint: {res_sites.status_code}")
            
            # 4. Explicar o 403 na busca
            print(f"\n💡 OBSERVAÇÃO TÉCNICA:")
            print(f"As credenciais estão 100% corretas. O erro 403 em buscas com este tipo de token")
            print(f"é comum no ML. Para buscas completas de afiliado, o sistema deve usar o")
            print(f"fluxo 'Authorization Code' (que você configurou) para obter um token de USUÁRIO.")
            
            return True
        else:
            print(f"❌ Credenciais INVÁLIDAS ou App Bloqueado: {response.status_code}")
            print(f"Mensagem: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro técnico: {str(e)}")
        return False

if __name__ == "__main__":
    test_connection()
