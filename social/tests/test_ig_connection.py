import os
import requests
from dotenv import load_dotenv

def test_instagram_connection():
    load_dotenv()
    
    token = os.getenv("IG_ACCESS_TOKEN")
    business_id = os.getenv("IG_BUSINESS_ID")
    
    print("=" * 50)
    print("🔍 DIAGNÓSTICO DE CONEXÃO INSTAGRAM")
    print("=" * 50)
    
    if not token or not business_id:
        print("❌ ERRO: IG_ACCESS_TOKEN ou IG_BUSINESS_ID não encontrados no .env")
        return

    # Endpoint para checar o próprio token
    debug_url = f"https://graph.facebook.com/debug_token"
    params = {
        "input_token": token,
        "access_token": token # Para debug_token, precisamos de um token (pode ser o mesmo se tiver permissões)
    }
    
    # Alternativa mais simples: tentar pegar os dados do perfil business
    profile_url = f"https://graph.facebook.com/v21.0/{business_id}"
    profile_params = {
        "fields": "name,username",
        "access_token": token
    }
    
    print(f"📡 Testando Business ID: {business_id}...")
    
    try:
        response = requests.get(profile_url, params=profile_params)
        data = response.json()
        
        if "id" in data:
            print(f"✅ CONEXÃO ESTABELECIDA!")
            print(f"👤 Nome: {data.get('name')}")
            print(f"📸 Username: {data.get('username')}")
            print("\n💡 O token local está VÁLIDO. O problema pode estar apenas nos Secrets do GitHub.")
        else:
            error = data.get("error", {})
            print(f"❌ FALHA NA AUTENTICAÇÃO")
            print(f"🛑 Erro Meta: {error.get('message')}")
            print(f"🔢 Código: {error.get('code')}")
            print(f"ℹ️ Tipo: {error.get('type')}")
            
            if error.get('code') == 190:
                print("\n⚠️ O Token expirou ou é inválido. Você precisa gerar um novo no Portal de Desenvolvedores da Meta.")
            elif error.get('code') == 100:
                print("\n⚠️ O Business ID pode estar incorreto.")
                
    except Exception as e:
        print(f"💥 Erro inesperado: {e}")

if __name__ == "__main__":
    test_instagram_connection()
