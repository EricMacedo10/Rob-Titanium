import requests
import json
import os
import sys

# Adicionar o caminho do projeto para importar os tokens
sys.path.append(r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium")
from core import tokens as meli_token_manager

def test_authenticated_search():
    print(f"--- TESTANDO BUSCA AUTENTICADA (TOKEN DE USUÁRIO) ---")
    
    # 1. Obter o token que acabamos de salvar
    access_token = meli_token_manager.get_valid_token()
    
    if not access_token:
        print("❌ Erro: Nenhum token de usuário encontrado no sistema.")
        return False
        
    print(f"✅ Token de usuário recuperado com sucesso.")
    
    # 2. Testar busca de produto com o token de USUÁRIO
    # O endpoint /sites/MLB/search com token de usuário deve contornar o 403
    url_search = "https://api.mercadolibre.com/sites/MLB/search?q=iPhone&limit=3"
    headers = {'Authorization': f'Bearer {access_token}'}
    
    try:
        print(f"🔍 Realizando busca por 'iPhone'...")
        response = requests.get(url_search, headers=headers)
        
        if response.status_code == 200:
            print(f"✅ SUCESSO! Erro 403 Corrigido.")
            data = response.json()
            results = data.get('results', [])
            print(f"📊 Foram encontrados {len(results)} produtos reais.")
            
            for i, prod in enumerate(results):
                print(f"   [{i+1}] {prod.get('title')} - R$ {prod.get('price')}")
            
            return True
        else:
            print(f"❌ Erro na busca autenticada: {response.status_code}")
            print(f"Motivo: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro técnico: {str(e)}")
        return False

if __name__ == "__main__":
    test_authenticated_search()
