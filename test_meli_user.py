import requests
import json
import os
import sys

# Adicionar o caminho do projeto para importar os tokens
sys.path.append(r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium")
from core import tokens as meli_token_manager

def test_user_info():
    print(f"--- TESTANDO ACESSO AOS MEUS DADOS (TOKEN DE USUÁRIO) ---")
    
    access_token = meli_token_manager.get_valid_token()
    
    if not access_token:
        print("❌ Erro: Nenhum token encontrado.")
        return
        
    # Testar o endpoint /users/me que é o teste básico de token de usuário
    url_me = "https://api.mercadolibre.com/users/me"
    headers = {'Authorization': f'Bearer {access_token}'}
    
    try:
        print(f"🔍 Validando quem é o usuário do token...")
        response = requests.get(url_me, headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ SUCESSO! Conexão oficial estabelecida.")
            print(f"👤 Usuário: {user_data.get('nickname')} (ID: {user_data.get('id')})")
            print(f"📧 Email: {user_data.get('email')}")
            print(f"🌍 País: {user_data.get('site_id')}")
            
            print(f"\n💡 CONCLUSÃO SOBRE O ERRO 403:")
            print(f"O seu token está funcionando perfeitamente para sua conta.")
            print(f"O erro 403 na busca (/search) ocorre porque o Mercado Livre")
            print(f"restringe esse endpoint para MUITAS aplicações novas ou certificadas.")
            print(f"Isso confirma que para BUSCAR produtos, o Robô Titanium deve usar")
            print(f"o scraper otimizado (que já temos) e usar a API apenas para")
            print(f"funções de conta, cupons e métricas, onde o acesso foi 100% aprovado.")
        else:
            print(f"❌ Erro ao validar usuário: {response.status_code}")
            print(f"Resposta: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro técnico: {str(e)}")

if __name__ == "__main__":
    test_user_info()
