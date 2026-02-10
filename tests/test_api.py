"""
Script de teste para API do Árbitro de Preços
"""

import requests
import json

API_URL = "http://localhost:5000"

def test_health():
    """Testa health check"""
    print("\n" + "="*70)
    print("TESTE 1: Health Check")
    print("="*70)
    
    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def test_status():
    """Testa status da API"""
    print("\n" + "="*70)
    print("TESTE 2: API Status")
    print("="*70)
    
    response = requests.get(f"{API_URL}/api/status")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def test_arbitrar(termo):
    """Testa endpoint de arbitragem"""
    print("\n" + "="*70)
    print(f"TESTE 3: Arbitrar Preço - '{termo}'")
    print("="*70)
    
    response = requests.get(
        f"{API_URL}/api/search",
        params={"q": termo}
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Melhor produto encontrado:")
        print(f"   Título: {data['best_price']['title']}")
        print(f"   Preço: R$ {data['best_price']['price']:.2f}")
        print(f"   Loja: {data['best_price']['store']}")
        print(f"   Link: {data['best_price']['link'][:60]}...")
    else:
        print(f"❌ Erro: {response.json()}")

def test_validation():
    """Testa validação de input"""
    print("\n" + "="*70)
    print("TESTE 4: Validação de Input")
    print("="*70)
    
    # Teste 1: Termo vazio
    response = requests.get(
        f"{API_URL}/api/search",
        params={"q": ""}
    )
    print(f"Termo vazio: {response.status_code} - {response.json()['erro']}")
    
    # Teste 2: Termo muito curto
    response = requests.get(
        f"{API_URL}/api/search",
        params={"q": "ab"}
    )
    print(f"Termo curto: {response.status_code} - {response.json()['erro']}")
    
    # Teste 3: Caracteres inválidos
    response = requests.get(
        f"{API_URL}/api/search",
        params={"q": "<script>alert('xss')</script>"}
    )
    print(f"XSS attempt: {response.status_code} - {response.json()['erro']}")

if __name__ == "__main__":
    print("\n🧪 TESTANDO API DO ÁRBITRO DE PREÇOS")
    print("="*70)
    
    try:
        test_health()
        test_status()
        test_validation()
        test_arbitrar("mouse gamer")  # Testando busca real
        
        print("\n" + "="*70)
        print("✅ TODOS OS TESTES CONCLUÍDOS")
        print("="*70)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERRO: API não está rodando!")
        print("Execute: python api_arbitro.py")
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
