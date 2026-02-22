import socket
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def diagnostic_lomadee():
    print("🔍 DIAGNÓSTICO DE CONEXÃO LOMADEE")
    print("-" * 40)
    
    hosts_to_test = [
        "api-beta.lomadee.com.br",
        "api.lomadee.com.br"
    ]
    
    token = os.getenv("LOMADEE_APP_TOKEN")
    
    for host in hosts_to_test:
        print(f"\n--- Testando Host: {host} ---")
        try:
            ip = socket.gethostbyname(host)
            print(f"   ✅ DNS Resolvido: {ip}")
            
            # Novo endpoint: /affiliate/products
            url = f"https://{host}/affiliate/products"
            headers = {"x-api-key": token}
            # Adding sourceId to see if it generates tracked links
            source_id = os.getenv("LOMADEE_SOURCE_ID")
            params = {
                "search": "mouse gamer", 
                "limit": 10,
                "sourceId": source_id
            }
            
            print(f"   Tentando GET {url} com x-api-key...")
            response = requests.get(url, params=params, headers=headers, timeout=10)
            print(f"   Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print("   🎉 SUCESSO! Dados recebidos:")
                import json
                try:
                    data = response.json()
                    products = data.get("products", [])
                    if products:
                        print("SCHEMA ANALYSIS (First Product):")
                        print(json.dumps(products[0], indent=2))
                    else:
                        print("   ⚠️ Nenhum produto retornado. Raw Data:")
                        print(json.dumps(data, indent=2))
                except Exception as parse_err:
                    print(f"   Erro parse JSON: {parse_err}")
                    print(response.text[:500])
            else:
                print(f"   Resposta: {response.text[:500]}")
                
            # TEST 2: Deeplink Generation Endpoint?
            test_url = f"https://www.webfones.com.br/mouse-gamer-viper-pro-naja-7200-dpi-s-rgb-usb-preto/p"
            deeplink_url = f"https://{host}/affiliate/deeplink"
            dl_params = {
                "sourceId": source_id,
                "url": test_url
            }
            print(f"\n   Tentando GET {deeplink_url}...")
            dl_response = requests.get(deeplink_url, params=dl_params, headers=headers, timeout=10)
            print(f"   Status Code: {dl_response.status_code}")
            if dl_response.status_code == 200:
                print("   🎉 DEEPLINK ENDPOINT FOUND!")
                print(json.dumps(dl_response.json(), indent=2))
            else:
                print(f"   Resposta: {dl_response.text[:200]}")

        except Exception as e:
            print(f"   ❌ FALHA: {e}")

if __name__ == "__main__":
    diagnostic_lomadee()
