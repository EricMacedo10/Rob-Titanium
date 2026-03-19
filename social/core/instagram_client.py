import requests
import json
import time
import os

class InstagramClient:
    """
    Cliente para interação com a Instagram Graph API.
    """
    def __init__(self, access_token, business_id, page_id=None):
        self.user_access_token = access_token
        self.access_token = access_token # Default fallback para requests publicos
        self.business_id = business_id
        self.page_id = page_id
        self.base_url = f"https://graph.facebook.com/v21.0/{self.business_id}"
        self.page_access_token = None
        self._init_page_token()

    def _init_page_token(self):
        """Converte o User Token para um Page Token (obrigatório para endpoints de DM)."""
        url = f"https://graph.facebook.com/v21.0/me/accounts"
        resp = requests.get(url, params={"access_token": self.user_access_token})
        data = resp.json()
        if "data" in data and len(data["data"]) > 0:
            for page in data["data"]:
                if str(page["id"]) == str(self.page_id):
                    self.page_access_token = page["access_token"]
                    return
            # Caso o page_id não corresponda (ou não especificado), pega a primeira página atrelada
            self.page_id = data["data"][0]["id"]
            self.page_access_token = data["data"][0]["access_token"]
        else:
            print("⚠️ Aviso: Falha ao obter Page Access Token. As DMs podem falhar.")

    def get_latest_media(self, limit=10):
        """
        Retorna a lista de IDs das postagens mais recentes.
        """
        url = f"{self.base_url}/media"
        params = {
            "fields": "id,caption,media_type,timestamp,permalink",
            "limit": limit,
            "access_token": self.access_token
        }
        resp = requests.get(url, params=params)
        data = resp.json()
        return data.get("data", [])

    def get_comments(self, media_id):
        """
        Retorna a lista de comentários de uma postagem específica.
        """
        url = f"https://graph.facebook.com/v21.0/{media_id}/comments"
        params = {
            "fields": "id,text,from,timestamp,username",
            "access_token": self.access_token
        }
        resp = requests.get(url, params=params)
        data = resp.json()
        return data.get("data", [])

    def post_private_reply(self, comment_id, message):
        """
        Envia uma resposta privada (DM) para o autor de um comentário via Inbox do IG.
        """
        url = f"https://graph.facebook.com/v21.0/{self.page_id}/messages"
        payload = {
            "recipient": {"comment_id": comment_id},
            "message": {"text": message}
        }
        token_to_use = self.page_access_token if self.page_access_token else self.user_access_token
        resp = requests.post(url, json=payload, params={"access_token": token_to_use})
        return resp.json()

    def post_public_reply(self, comment_id, message):
        """
        Responde publicamente a um comentário na sua postagem.
        """
        url = f"https://graph.facebook.com/v21.0/{comment_id}/replies"
        payload = {
            "message": message,
            "access_token": self.access_token
        }
        resp = requests.post(url, data=payload)
        return resp.json()


    def get_conversations(self):
        """
        Retorna as conversas da caixa de entrada do Instagram (requer Page ID).
        """
        if not self.page_id:
            return {"error": "Page ID não configurado no cliente."}
            
        url = f"https://graph.facebook.com/v21.0/{self.page_id}/conversations"
        params = {
            "platform": "instagram",
            "fields": "id,messages.limit(1){id,message,from,timestamp}",
            "access_token": self.access_token # Pode precisar de Page Token em alguns casos
        }
        resp = requests.get(url, params=params)
        return resp.json()

    def send_direct_message(self, recipient_id, message):
        """
        Envia uma mensagem direta (DM) para um IGSID específico (requer Page ID).
        """
        if not self.page_id:
            return {"error": "Page ID não configurado no cliente."}

        url = f"https://graph.facebook.com/v21.0/{self.page_id}/messages"
        payload = {
            "recipient": json.dumps({"id": recipient_id}),
            "message": json.dumps({"text": message}),
            "access_token": self.access_token
        }
        resp = requests.post(url, data=payload)
        return resp.json()

    def post_image(self, image_url, caption):
        """
        Realiza o fluxo completo de postagem para Feed (Imagem).
        """
        return self._create_and_publish(image_url, caption, media_type=None)

    def post_carousel(self, image_urls, caption):
        """
        Realiza o fluxo completo de postagem para Carrossel (Album).
        """
        print(f"--- Iniciando postagem de CARROSSEL no Instagram...")
        
        child_ids = []
        for i, url in enumerate(image_urls):
            print(f"--- Criando container para imagem {i+1}/{len(image_urls)}...")
            container_url = f"{self.base_url}/media"
            payload = {
                "image_url": url,
                "is_carousel_item": "true",
                "access_token": self.access_token
            }
            resp = requests.post(container_url, data=payload)
            data = resp.json()
            if "id" in data:
                child_id = data["id"]
                # BLINDAGEM: Aguardar o item do carrossel ser processado antes de continuar
                print(f"--- Aguardando processamento do item {i+1}...")
                if self._wait_for_processing(child_id):
                    child_ids.append(child_id)
                else:
                    print(f"--- Falha ao aguardar processamento do item {i+1}")
                    return False
            else:
                print(f"--- Erro ao criar container filho: {data}")
                return False
        
        # Passo 2: Criar Carousel Container
        print(f"--- Agrupando {len(child_ids)} imagens no carrossel...")
        carousel_url = f"{self.base_url}/media"
        carousel_payload = {
            "media_type": "CAROUSEL",
            "children": json.dumps(child_ids) if isinstance(child_ids, list) else child_ids,
            "caption": caption,
            "access_token": self.access_token
        }
        
        # Nota: Algumas versoes da API preferem uma string separada por virgula em vez de JSON array para 'children'
        if isinstance(child_ids, list):
            carousel_payload["children"] = ",".join(child_ids)

        resp = requests.post(carousel_url, data=carousel_payload)
        data = resp.json()
        if "id" not in data:
            print(f"--- Erro ao criar container de carrossel: {data}")
            return False
            
        creation_id = data["id"]
        
        # Passo 3: Aguardar processamento
        if not self._wait_for_processing(creation_id):
            return False
            
        # Passo 4: Publicar
        publish_url = f"{self.base_url}/media_publish"
        publish_payload = {
            "creation_id": creation_id,
            "access_token": self.access_token
        }
        resp = requests.post(publish_url, data=publish_payload)
        publish_data = resp.json()
        
        if "id" in publish_data:
            print(f"--- CARROSSEL PUBLICADO COM SUCESSO! (ID: {publish_data['id']})")
            return True
        else:
            print(f"--- Erro ao publicar carrossel: {publish_data}")
            return False

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
