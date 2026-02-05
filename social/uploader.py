import os
import requests
import base64
from scraper.upload import upload_to_hostinger

class ResilientUploader:
    """
    Orquestrador de upload com lógica de redundância (FTP + Cloud Fallback).
    """
    def __init__(self, ftp_config=None, imgbb_api_key=None):
        self.ftp_config = ftp_config
        self.imgbb_api_key = imgbb_api_key or os.getenv("IMGBB_API_KEY")

    def upload(self, local_path, remote_name):
        """
        Tenta upload via FTP e, em caso de falha, usa ImgBB como fallback.
        Retorna a URL pública final ou None.
        """
        # 1. Tentativa via FTP (Hostinger)
        if self.ftp_config and self.ftp_config.get("user"):
            print(f"📡 Tentando upload via FTP (Hostinger): {remote_name}")
            try:
                success = upload_to_hostinger(
                    local_path,
                    self.ftp_config["host"],
                    self.ftp_config["user"],
                    self.ftp_config["pass"],
                    f"social/{remote_name}"
                )
                if success:
                    url = f"https://guiadodesconto.com.br/social/{remote_name}"
                    if self._verify_link(url):
                        return url
            except Exception as e:
                print(f"⚠️ Erro no FTP: {e}")

        # 2. Fallback via ImgBB (Cloud)
        if self.imgbb_api_key:
            print(f"☁️ Fallback: Tentando upload via ImgBB API...")
            url = self._upload_to_imgbb(local_path)
            if url and self._verify_link(url):
                return url

        print("❌ Todas as tentativas de upload falharam.")
        return None

    def _upload_to_imgbb(self, local_path):
        """Upload simples para ImgBB API."""
        url = "https://api.imgbb.com/1/upload"
        try:
            with open(local_path, "rb") as file:
                payload = {
                    "key": self.imgbb_api_key,
                    "image": base64.b64encode(file.read()),
                }
                response = requests.post(url, payload, timeout=30)
                data = response.json()
                if data.get("success"):
                    return data["data"]["url"]
                else:
                    print(f"❌ Erro ImgBB: {data.get('error', {}).get('message')}")
        except Exception as e:
            print(f"💥 Falha crítica no ImgBB: {e}")
        return None

    def _verify_link(self, url):
        """Health Check: Garante que a URL é acessível e retorna Status 200."""
        print(f"🔍 Validando link: {url}")
        try:
            # Head request para ser rápido
            response = requests.head(url, timeout=10, allow_redirects=True)
            if response.status_code == 200:
                print("✅ Link validado e público!")
                return True
            else:
                print(f"⚠️ Link retornou status {response.status_code}")
                return False
        except Exception as e:
            print(f"⚠️ Erro ao validar link: {e}")
            return False

if __name__ == "__main__":
    # Teste isolado
    up = ResilientUploader(imgbb_api_key="TEST_KEY")
    # print(up.upload("social/temp_post_0.jpg", "test_resilience.jpg"))
