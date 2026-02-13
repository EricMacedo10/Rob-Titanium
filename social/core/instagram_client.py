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
        print(f"--- Postando Story...")
        return self._create_and_publish(media_url, caption=None, media_type="STORIES", is_video=is_video)

    def post_reels(self, video_url, caption, cover_url=None):
        """
        Posta um Reel (Vídeo).
        """
        print(f"--- Postando Reels...")
        return self._create_and_publish(video_url, caption, media_type="REELS", is_video=True, cover_url=cover_url)

    def _create_and_publish(self, media_url, caption, media_type=None, is_video=False, cover_url=None):
        """
        Abstração do fluxo de criação e publicação.
        """
        print(f"--- Iniciando postagem [{media_type or 'FEED'}] no Instagram...")
        
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

        # Cover URL agora suportado para VIDEO (Reels/Stories) e IMAGE
        if cover_url:
            payload["cover_url"] = cover_url

        if caption:
            payload["caption"] = caption
        
        try:
            response = requests.post(container_url, data=payload)
            response_data = response.json()
            
            if "id" not in response_data:
                print(f"--- Erro ao criar container ({media_type}): {response_data}")
                return False
            
            creation_id = response_data["id"]
            print(f"--- Container criado (ID: {creation_id}).")
            
            # Passo 2: Aguardar processamento (Especialmente crítico para vídeos)
            if not self._wait_for_processing(creation_id, is_video=is_video):
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
                print(f"--- POSTAGEM REALIZADA COM SUCESSO! (ID: {publish_data['id']})")
                return True
            else:
                print(f"--- Erro ao publicar: {publish_data}")
                return False
                
        except Exception as e:
            print(f"--- Falha critica no cliente Instagram: {e}")
            return False

    def _wait_for_processing(self, creation_id, is_video=False):
        """
        Verifica o status do container até que esteja pronto ou expire.
        """
        status_url = f"https://graph.facebook.com/v21.0/{creation_id}"
        params = {
            "fields": "status_code,failure_reason",
            "access_token": self.access_token
        }
        
        # Aumentamos o timeout para Reels (vídeos pesados demoram mais)
        max_attempts = 100 if is_video else 30
        none_count = 0
        max_none = 15 if is_video else 5
        
        for attempt in range(max_attempts):
            try:
                response = requests.get(status_url, params=params)
                data = response.json()
                status = data.get("status_code")
                
                if status == "FINISHED":
                    print(f"--- Midia processada e pronta para publicacao.")
                    return True
                elif status == "IN_PROGRESS":
                    none_count = 0
                    print(f"--- Processando midia no Instagram Cloud... (Tentativa {attempt+1}/{max_attempts})")
                    time.sleep(10)
                elif status == "ERROR":
                    print(f"--- Erro no processamento da midia: {data}")
                    return False
                else:
                    none_count += 1
                    # Para vídeos, esperamos MUITO mais o status aparecer
                    if not is_video and none_count >= max_none:
                        print(f"--- Status nulo por {max_none} tentativas — assumindo imagem pronta (Feed).")
                        return True
                    
                    if is_video and none_count >= max_attempts:
                        print("--- Timeout aguardando inicio de processamento do video.")
                        return False
                        
                    print(f"--- Aguardando inicio do processamento... ({status or 'Pendente'}) [{none_count}/{max_none if not is_video else max_attempts}]")
                    time.sleep(5)
            except Exception as e:
                print(f"--- Erro ao checar status: {e}")
                time.sleep(5)
                
        print("--- Timeout total aguardando processamento da midia.")
        return False
