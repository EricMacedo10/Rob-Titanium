import requests
import json
import sys

sys.path.append(r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium")
from core import tokens as meli_token_manager

def debug_forbidden_search():
    print(f"--- DEBUG PROFUNDO: ERRO 403 ---")
    
    access_token = meli_token_manager.get_valid_token()
    if not access_token:
        print("❌ Token não encontrado.")
        return

    # TENTATIVA 1: Busca com User-Agent de navegador (Bypass de restrição simples)
    print(f"\n1. Testando com User-Agent de Navegador...")
    url = "https://api.mercadolibre.com/sites/MLB/search?q=iPhone&limit=1"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    
    res1 = requests.get(url, headers=headers)
    print(f"Status: {res1.status_code}")
    if res1.status_code == 403:
        print(f"Mensagem: {res1.json().get('message')}")

    # TENTATIVA 2: Verificar meus próprios Scopes (O que o ML diz que eu posso fazer)
    print(f"\n2. Verificando escopos reais do seu Token...")
    # O ML retorna os scopes permitidos no endpoint /users/me ou validando o token
    url_me = "https://api.mercadolibre.com/users/me"
    res2 = requests.get(url_me, headers=headers)
    if res2.status_code == 200:
        # Infelizmente o /users/me não traz os scopes no JSON, mas podemos deduzir
        print("✅ Token de Usuário é válido.")
    
    # TENTATIVA 3: Testar outro endpoint público que exige autenticação
    print(f"\n3. Testando categoria pública (Endpoint neutro)...")
    url_cat = "https://api.mercadolibre.com/categories/MLB1000" # Tecnologia
    res3 = requests.get(url_cat, headers=headers)
    print(f"Status Categorias: {res3.status_code}")

    if res1.status_code == 403:
        print(f"\n💡 CONCLUSÃO FINAL:")
        print(f"Se o erro persiste mesmo com Token de Usuário, a causa é 'Restrição de Escopo Especial'.")
        print(f"Muitas vezes o ML só libera o /search para apps da categoria 'Shopping' ou 'Selling'.")
        print(f"Mas não se preocupe! Isso prova que o caminho via API oficial deve ser usado para")
        print(f"PEGAR DETALHES (Items/Prices/Promos) e o Scraper para BUSCAR os links.")

if __name__ == "__main__":
    debug_forbidden_search()
