
import os
import socket
import requests
import ftplib
from dotenv import load_dotenv

load_dotenv()

def test_internet():
    print("--- Testando Conexão com a Internet ---")
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        print("[OK] Internet: Conectado")
        return True
    except OSError:
        print("[ERRO] Internet: Sem conexão")
        return False

def test_api_reachability(name, url):
    print(f"--- Testando Alcance da API: {name} ---")
    try:
        response = requests.get(url, timeout=5)
        print(f"[OK] {name}: Acessível (Status: {response.status_code})")
        return True
    except Exception as e:
        print(f"[ERRO] {name}: Inacessível ({e})")
        return False

def test_ftp():
    print("--- Testando Conexão FTP ---")
    host = os.getenv("FTP_HOST")
    user = os.getenv("FTP_USER")
    password = os.getenv("FTP_PASS")
    
    if not all([host, user, password]):
        print("[AVISO] FTP: Credenciais incompletas no .env")
        return False
        
    try:
        ftp = ftplib.FTP(host, timeout=10)
        ftp.login(user, password)
        ftp.quit()
        print(f"[OK] FTP: Conectado com sucesso em {host}")
        return True
    except Exception as e:
        print(f"[ERRO] FTP: Falha na conexão ({e})")
        return False

if __name__ == "__main__":
    test_internet()
    test_api_reachability("Shopee API (Home)", "https://shopee.com.br")
    test_api_reachability("DeepSeek-V3.2 API", "https://api.deepseek.com")
    test_ftp()
