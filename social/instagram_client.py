import requests
import time
import os

class InstagramClient:
    """
    Cliente para interação com a Instagram Graph API.
    """
    def __init__(self, access_token, business_id):
        self.access_token = access_token
        self.business_id = business_id
        self.base_url = f"https://graph.facebook.com/v21.0/{self.business_id}"

    def post_image(self, image_url, caption):
        """
        Realiza o fluxo completo de postagem:
        1. Cria o container de mídia.
        2. Aguarda o processamento (se necessário).
        3. Publica o container.
        """
        print(f"🚀 Iniciando postagem no Instagram...")
        
        # Passo 1: Criar Media Container
        container_url = f"{self.base_url}/media"
        payload = {
            "image_url": image_url,
            "caption": caption,
            "access_token": self.access_token
        }
        
        try:
            response = requests.post(container_url, data=payload)
            response_data = response.json()
            
            if "id" not in response_data:
                print(f"❌ Erro ao criar container: {response_data}")
                return False
            
            creation_id = response_data["id"]
            print(f"✅ Container criado (ID: {creation_id}). Aguardando processamento...")
            
            # Passo 2: Aguardar (Meta geralmente leva alguns segundos)
            time.sleep(10)
            
            # Passo 3: Publicar Container
            publish_url = f"{self.base_url}/media_publish"
            publish_payload = {
                "creation_id": creation_id,
                "access_token": self.access_token
            }
            
            publish_response = requests.post(publish_url, data=publish_payload)
            publish_data = publish_response.json()
            
            if "id" in publish_data:
                print(f"🏆 POSTAGEM REALIZADA COM SUCESSO! (ID: {publish_data['id']})")
                return True
            else:
                print(f"❌ Erro ao publicar: {publish_data}")
                return False
                
        except Exception as e:
            print(f"💥 Falha crítica no cliente Instagram: {e}")
            return False

    def post_reels(self, video_url, caption):
        """
        Similar ao post_image, mas para Reels (vídeos).
        """
        # Implementação futura conforme necessário
        pass
