import os
import time
import requests
import base64
from infra.upload_logic import upload_to_hostinger

# User-Agent que o Meta/Facebook usa para baixar mídias
META_USER_AGENT = "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)"

class ResilientUploader:
    """
    Orquestrador de upload com lógica de redundância (FTP + Cloud Fallback).
    Blindagem v2: Verificação Meta-realista + auto-fallback para ImgBB.
    """
    def __init__(self, ftp_config=None, imgbb_api_key=None):
        self.ftp_config = ftp_config
        self.imgbb_api_key = imgbb_api_key or os.getenv("IMGBB_API_KEY")
        self.provider_used = None  # Rastreia qual provedor foi usado (para logs)

    def upload(self, local_path, remote_name, force_cloud=False):
        """
        Tenta upload via FTP e, em caso de falha, usa ImgBB como fallback.
        BLINDAGEM: Após FTP, simula o crawler do Meta para detectar bloqueios do WAF.
        Retorna a URL pública final ou None.
        """
        # 0. Forced Cloud Check
        if force_cloud and self.imgbb_api_key:
            print(f"--- Forçando upload via Cloud (ImgBB) para garantir acessibilidade...")
            url = self._upload_to_imgbb(local_path)
            if url:
                self.provider_used = "ImgBB (forçado)"
            return url

        # 1. Tentativa via FTP (Hostinger)
        if self.ftp_config and self.ftp_config.get("user"):
            print(f"--- Tentando upload via FTP (Hostinger): {remote_name}")
            try:
                success = upload_to_hostinger(
                    local_path,
                    self.ftp_config["host"],
                    self.ftp_config["user"],
                    self.ftp_config["pass"],
                    f"social/{remote_name}"
                )
                if success:
                    env_mode = os.getenv('ENV_MODE', 'STAGING').upper()
                    base_url = "https://guiadodesconto.com.br"
                    if env_mode == "STAGING":
                        url = f"{base_url}/teste/social/{remote_name}"
                    else:
                        url = f"{base_url}/social/{remote_name}"
                    
                    if self._verify_link(url):
                        # BLINDAGEM: Verificação extra simulando o crawler do Meta
                        print("--- Verificacao Meta-realista (simulando crawler do Facebook)...")
                        if self._verify_link_for_meta(url):
                            self.provider_used = "Hostinger (FTP)"
                            return url
                        else:
                            print("--- Aviso: Hostinger bloqueado para crawlers do Meta!")
                            print("--- Ativando fallback automático para ImgBB...")
            except Exception as e:
                print(f"--- Erro no FTP: {e}")

        # 2. Fallback via ImgBB (Cloud)
        if self.imgbb_api_key:
            print(f"--- Fallback: Tentando upload via ImgBB API...")
            url = self._upload_to_imgbb(local_path)
            if url and self._verify_link(url):
                print("--- Verificacao Meta-realista para ImgBB...")
                if self._verify_link_for_meta(url):
                    self.provider_used = "ImgBB (fallback)"
                    return url
                else:
                    print("--- ❌ ERRO: ImgBB tambem falhou na verificacao Meta!")
            else:
                print("--- ❌ ERRO: ImgBB falhou no upload ou primeiro check.")

        print("--- Todas as tentativas de upload falharam.")
        return None

    def _upload_to_imgbb(self, local_path):
        """Upload para tmpfiles (substituindo ImgBB que bloqueia o Meta)"""
        url = "https://tmpfiles.org/api/v1/upload"
        try:
            with open(local_path, "rb") as file:
                files = {"file": file}
                response = requests.post(url, files=files, timeout=30)
                data = response.json()
                if data.get("status") == "success":
                    raw_url = data["data"]["url"]
                    # Força HTTPS e converte para link direto (dl/)
                    if raw_url.startswith("http://"):
                        raw_url = raw_url.replace("http://", "https://", 1)
                    
                    direct_url = raw_url.replace("tmpfiles.org/", "tmpfiles.org/dl/", 1)
                    print(f"--- [OK] Tmpfiles upload OK: {direct_url}")
                    return direct_url
                else:
                    print(f"--- Erro Tmpfiles: {data}")
        except Exception as e:
            print(f"--- Falha critica no Tmpfiles: {e}")
        return None

    def _verify_link(self, url):
        """Health Check: Garante que a URL é acessível e retorna Status 200."""
        print(f"--- Validando link: {url}")
        try:
            response = requests.head(url, timeout=10, allow_redirects=True)
            if response.status_code == 200:
                print("--- Link validado e publico!")
                return True
            else:
                print(f"--- Link retornou status {response.status_code}")
                return False
        except Exception as e:
            print(f"--- Erro ao validar link: {e}")
            return False

    def _verify_link_for_meta(self, url):
        """
        Verificação avançada: Simula EXATAMENTE o que o crawler do Meta/Facebook faz.
        - GET completo (não HEAD) com User-Agent do Facebook
        - Valida Content-Type (deve ser image/* ou video/*)
        - Valida tamanho mínimo (>10KB = não é página de erro)
        - Aguarda 2s e refaz para verificar estabilidade (WAF rate-limit)
        """
        headers = {"User-Agent": META_USER_AGENT}
        try:
            # Primeira verificação
            r = requests.get(url, headers=headers, timeout=15, stream=True)
            content_type = r.headers.get("Content-Type", "")
            content_length = int(r.headers.get("Content-Length", 0))
            r.close()

            if r.status_code != 200:
                print(f"--- [ERRO] Meta-check: Status {r.status_code} (esperado 200)")
                return False

            if not content_type.startswith(("image/", "video/")):
                print(f"--- [ERRO] Meta-check: Content-Type '{content_type}' (esperado image/* ou video/*)")
                # Se for HTML, verificamos se é um erro conhecido do WAF
                if "text/html" in content_type:
                    body_sample = r.content[:1024].decode('utf-8', errors='ignore').lower()
                    if "browser challenge" in body_sample or "blocked" in body_sample:
                        print(f"--- [ERRO] Meta-check: Detectado desafio de browser ou bloqueio (WAF).")
                return False

            if content_length < 10240:  # Menos de 10KB = provavelmente uma página de erro
                print(f"--- [AVISO] Meta-check: Content-Length {content_length} bytes (muito pequeno para mídia)")
                return False

            # Segunda verificação (estabilidade — WAF pode bloquear após N requests)
            time.sleep(2)
            r2 = requests.get(url, headers=headers, timeout=15, stream=True)
            ct2 = r2.headers.get("Content-Type", "")
            r2.close()

            if r2.status_code != 200 or not ct2.startswith(("image/", "video/")):
                print(f"--- [AVISO] Meta-check (2ª tentativa): Instável — Status {r2.status_code}, CT: {ct2}")
                return False

            print(f"--- [OK] Meta-check: OK (Content-Type: {content_type}, Size: {content_length} bytes)")
            return True

        except Exception as e:
            print(f"--- ❌ Meta-check falhou: {e}")
            return False

if __name__ == "__main__":
    # Teste isolado
    import os
    up = ResilientUploader(imgbb_api_key=os.getenv("IMGBB_API_KEY", "YOUR_IMGBB_API_KEY"))
    # print(up.upload("social/temp_post_0.jpg", "test_resilience.jpg"))
