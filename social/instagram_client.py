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
        Realiza o fluxo completo de postagem para Feed (Imagem).
        """
        return self._create_and_publish(image_url, caption, media_type=None)

    def post_story(self, media_url, is_video=False):
        """
        Posta um Story (Imagem ou Vídeo).
        """
        print(f"📸 Postando Story...")
        return self._create_and_publish(media_url, caption=None, media_type="STORIES", is_video=is_video)

    def post_reels(self, video_url, caption):
        """
        Posta um Reel (Vídeo).
        """
        print(f"🎬 Postando Reels...")
        return self._create_and_publish(video_url, caption, media_type="REELS", is_video=True)

    def _create_and_publish(self, media_url, caption, media_type=None, is_video=False):
        """
        Abstração do fluxo de criação e publicação.
        """
        print(f"🚀 Iniciando postagem [{media_type or 'FEED'}] no Instagram...")
        
        # Passo 1: Criar Media Container
        container_url = f"{self.base_url}/media"
        payload = {
            "access_token": self.access_token
        }
        
        if is_video:
            payload["video_url"] = media_url
            payload["media_type"] = media_type or "VIDEO"
        else:
            payload["image_url"] = media_url
            if media_type:
                payload["media_type"] = media_type

        if caption:
            payload["caption"] = caption
        
        try:
            response = requests.post(container_url, data=payload)
            response_data = response.json()
            
            if "id" not in response_data:
                print(f"❌ Erro ao criar container ({media_type}): {response_data}")
                return False
            
            creation_id = response_data["id"]
            print(f"✅ Container criado (ID: {creation_id}).")
            
            # Passo 2: Aguardar processamento (Especialmente crítico para vídeos)
            if not self._wait_for_processing(creation_id):
                return False
            
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

    def _wait_for_processing(self, creation_id):
        """
        Verifica o status do container até que esteja pronto ou expire.
        """
        status_url = f"https://graph.facebook.com/v21.0/{creation_id}"
        params = {
            "fields": "status_code",
            "access_token": self.access_token
        }
        
        max_attempts = 15
        for attempt in range(max_attempts):
            try:
                response = requests.get(status_url, params=params)
                data = response.json()
                status = data.get("status_code")
                
                if status == "FINISHED":
                    print(f"✅ Mídia processada e pronta.")
                    return True
                elif status == "ERROR":
                    print(f"❌ Erro no processamento da mídia: {data}")
                    return False
                else:
                    print(f"⏳ Processando mídia... (Tentativa {attempt+1}/{max_attempts})")
                    time.sleep(10)
            except Exception as e:
                print(f"⚠️ Erro ao checar status: {e}")
                time.sleep(5)
                
        print("❌ Timeout aguardando processamento da mídia.")
        return False
