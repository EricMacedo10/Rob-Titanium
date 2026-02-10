import os
import requests
import socket
import ftplib
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_internet(host="8.8.8.8", port=53, timeout=3):
    """Checks if there's a basic internet connection via Google DNS."""
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False

def check_imgbb(api_key):
    """Checks if ImgBB API is reachable and key is valid."""
    url = "https://api.imgbb.com/1/upload"
    if not api_key:
        return False, "API Key missing in .env"
    
    # Simple GET or invalid POST to test reachability/auth
    try:
        # ImgBB returns 400 for missing 'image' but validates 'key' first
        response = requests.post(url, data={"key": api_key}, timeout=10)
        data = response.json()
        if "error" in data and data["error"]["message"] in ["No image data or invalid format.", "Empty upload source."]:
            return True, "API reachable and Key valid"
        elif "error" in data:
            return False, f"API Error: {data['error']['message']}"
        return True, "API reachable"
    except Exception as e:
        return False, str(e)

def check_ftp(host, user, password):
    """Checks FTP connection to Hostinger."""
    if not all([host, user, password]):
        return False, "FTP credentials incomplete in .env"
    try:
        ftp = ftplib.FTP(host)
        ftp.login(user, password)
        ftp.quit()
        return True, "FTP Connection Success"
    except Exception as e:
        return False, f"FTP error: {e}"

def run_verify():
    print(f"\n{'='*20} SENIOR INFRA DIAGNOSTIC {'='*20}")
    
    # 1. Internet
    status_internet = check_internet()
    print(f"[INTERNET]  {'✅ ONLINE' if status_internet else '❌ OFFLINE'}")
    
    # 2. ImgBB
    imgbb_key = os.getenv("IMGBB_API_KEY")
    success, msg = check_imgbb(imgbb_key)
    print(f"[IMGBB]     {'✅' if success else '❌'} {msg}")
    
    # 3. FTP
    ftp_host = os.getenv("FTP_HOST")
    ftp_user = os.getenv("FTP_USER")
    ftp_pass = os.getenv("FTP_PASS")
    success, msg = check_ftp(ftp_host, ftp_user, ftp_pass)
    print(f"[FTP]       {'✅' if success else '❌'} {msg}")
    
    # 4. APIs reachability
    print(f"\n{'='*20} API ENDPOINTS {'='*20}")
    endpoints = {
        "Shopee API": "https://open.shopee.com.br",
        "Mercado Livre API": "https://api.mercadolibre.com",
    }
    for name, url in endpoints.items():
        try:
            res = requests.head(url, timeout=5)
            print(f"[{name:15}] ✅ HTTP {res.status_code}")
        except Exception as e:
            print(f"[{name:15}] ❌ FAIL: {e}")

if __name__ == "__main__":
    run_verify()
