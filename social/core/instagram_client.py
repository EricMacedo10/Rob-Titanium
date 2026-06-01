import requests
import json
import time
import os
import sys
import functools

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def prevent_concurrent_posts(func):
    """Decorator para impedir que dois scripts publiquem na Meta API simultaneamente."""
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        lock_file = os.path.join(os.path.dirname(__file__), "..", "..", "state", "post.lock")
        lock_file = os.path.abspath(lock_file)
        
        if os.path.exists(lock_file):
            try:
                age = time.time() - os.path.getmtime(lock_file)
                if age > 600: # 10 minutos
                    print("--- [AVISO] Removendo lock de postagem obsoleto (>10 min)...")
                    os.remove(lock_file)
                else:
                    print(f"--- [ERRO] Já existe uma postagem em andamento! (Lock ativo há {age:.0f}s)")
                    print("--- Operacao cancelada automaticamente para impedir postagem duplicada na sua página.")
                    return False
            except Exception:
                pass
                
        # Lock adquirido
        os.makedirs(os.path.dirname(lock_file), exist_ok=True)
        with open(lock_file, "w") as f:
            f.write(str(time.time()))
            
        try:
            return func(self, *args, **kwargs)
        finally:
            # Libera o lock
            if os.path.exists(lock_file):
                try:
                    os.remove(lock_file)
                except Exception:
                    pass
    return wrapper

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
            print("[!] Aviso: Falha ao obter Page Access Token. As DMs podem falhar.")

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
        return self._create_and_publish(image_url, caption, media_type="IMAGE")

    @prevent_concurrent_posts
    def post_carousel(self, media_items, caption):
        """
        Realiza o fluxo completo de postagem para Carrossel (Album).
        
        Aceita dois formatos:
          - Lista de strings (URLs de imagens) → retrocompatível
          - Lista de dicts: [{"url": "...", "type": "IMAGE"}, {"url": "...", "type": "VIDEO"}]
        
        Tipos suportados: IMAGE, VIDEO
        Máximo de 10 itens. Mínimo de 2 itens.
        """
        print(f"--- Iniciando postagem de CARROSSEL MISTO no Instagram...")

        # Normaliza para lista de dicts
        normalized = []
        video_exts = ('.mp4', '.mov', '.avi', '.webm')
        for item in media_items:
            if isinstance(item, str):
                # Detecta tipo pela extensão da URL
                ext = item.split('?')[0].lower()
                item_type = "VIDEO" if any(ext.endswith(e) for e in video_exts) else "IMAGE"
                normalized.append({"url": item, "type": item_type})
            else:
                normalized.append(item)

        child_ids = []
        for i, item in enumerate(normalized):
            url = item["url"]
            item_type = item.get("type", "IMAGE").upper()
            is_video = (item_type == "VIDEO")
            
            print(f"--- [RELAX] Aguardando 10s antes do item {i+1} para evitar erro 2 da Meta...")
            time.sleep(10)

            print(f"--- Criando container [{item_type}] para item {i+1}/{len(normalized)}...")
            container_url = f"{self.base_url}/media"
            payload = {
                "is_carousel_item": "true",
                "access_token": self.access_token
            }
            if is_video:
                payload["video_url"] = url
                payload["media_type"] = "VIDEO"
            else:
                payload["image_url"] = url

            resp = requests.post(container_url, data=payload)
            data = resp.json()
            if "id" in data:
                child_id = data["id"]
                print(f"--- Aguardando processamento do item {i+1} [{item_type}]...")
                if self._wait_for_processing(child_id, is_video=is_video, is_carousel_item=True):
                    child_ids.append(child_id)
                else:
                    print(f"--- Falha ao aguardar processamento do item {i+1}")
                    return False
            else:
                print(f"--- Erro ao criar container filho: {data}")
                if "error" in data:
                    print(f"--- Meta Error Details: {json.dumps(data['error'], indent=2)}")
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
            
        # Passo 4: Publicar com retry (pois o processamento assíncrono interno pode demorar extra para vídeos)
        publish_url = f"{self.base_url}/media_publish"
        publish_payload = {
            "creation_id": creation_id,
            "access_token": self.access_token
        }
        
        max_pub_attempts = 5
        for attempt in range(max_pub_attempts):
            resp = requests.post(publish_url, data=publish_payload)
            publish_data = resp.json()
            
            if "id" in publish_data:
                print(f"--- [OK] CARROSSEL PUBLICADO COM SUCESSO! (ID: {publish_data['id']})")
                return True
            else:
                err_msg = publish_data.get('error', {}).get('message', '')
                if 'Media ID is not available' in err_msg or 'Please wait a moment' in err_msg:
                    print(f"--- [AVISO] Backend do Meta ocupado (Tentativa {attempt+1}/{max_pub_attempts}). Aguardando 15s...")
                    time.sleep(15)
                else:
                    print(f"--- [ERRO] Falha ao publicar carrossel: {publish_data}")
                    return False
        
        print(f"--- ❌ Falha ao publicar carrossel após {max_pub_attempts} tentativas.")
        return False

    @prevent_concurrent_posts
    def post_carousel_with_id(self, media_items, caption):
        """
        Similar ao post_carousel, mas retorna o dict da resposta da publicação (incluindo o ID)
        em vez de apenas um booleano. Útil para bots de comentário.
        """
        print(f"--- Iniciando postagem de CARROSSEL COM ID no Instagram...")

        # Normaliza para lista de dicts
        normalized = []
        video_exts = ('.mp4', '.mov', '.avi', '.webm')
        for item in media_items:
            if isinstance(item, str):
                ext = item.split('?')[0].lower()
                item_type = "VIDEO" if any(ext.endswith(e) for e in video_exts) else "IMAGE"
                normalized.append({"url": item, "type": item_type})
            else:
                normalized.append(item)

        child_ids = []
        for i, item in enumerate(normalized):
            url = item["url"]
            item_type = item.get("type", "IMAGE").upper()
            is_video = (item_type == "VIDEO")
            
            print(f"--- Aguardando 10s antes do item {i+1}...")
            time.sleep(10)

            container_url = f"{self.base_url}/media"
            payload = {
                "is_carousel_item": "true",
                "access_token": self.access_token
            }
            if is_video:
                payload["video_url"] = url
                payload["media_type"] = "VIDEO"
            else:
                payload["image_url"] = url

            resp = requests.post(container_url, data=payload)
            data = resp.json()
            if "id" in data:
                child_id = data["id"]
                if self._wait_for_processing(child_id, is_video=is_video, is_carousel_item=True):
                    child_ids.append(child_id)
                else:
                    return False
            else:
                return False
        
        carousel_url = f"{self.base_url}/media"
        carousel_payload = {
            "media_type": "CAROUSEL",
            "children": ",".join(child_ids),
            "caption": caption,
            "access_token": self.access_token
        }
        
        resp = requests.post(carousel_url, data=carousel_payload)
        data = resp.json()
        if "id" not in data:
            return False
            
        creation_id = data["id"]
        if not self._wait_for_processing(creation_id):
            return False
            
        publish_url = f"{self.base_url}/media_publish"
        publish_payload = {
            "creation_id": creation_id,
            "access_token": self.access_token
        }
        
        max_pub_attempts = 5
        for attempt in range(max_pub_attempts):
            resp = requests.post(publish_url, data=publish_payload)
            publish_data = resp.json()
            
            if "id" in publish_data:
                print(f"--- [OK] CARROSSEL PUBLICADO COM SUCESSO! (ID: {publish_data['id']})")
                return publish_data
            else:
                err_msg = publish_data.get('error', {}).get('message', '')
                if 'Media ID is not available' in err_msg or 'Please wait a moment' in err_msg:
                    time.sleep(15)
                else:
                    return False
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

    @prevent_concurrent_posts
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
                print(f"--- [OK] POSTAGEM REALIZADA COM SUCESSO! (ID: {publish_data['id']})")
                return True
            else:
                print(f"--- [ERRO] Erro ao publicar: {publish_data}")
                return False
                
        except Exception as e:
            print(f"--- Falha critica no cliente Instagram: {e}")
            return False

    def _wait_for_processing(self, creation_id, is_video=False, is_carousel_item=False):
        """
        Verifica o status do container até que esteja pronto ou expire.
        
        Nota: Para vídeos em itens de carrossel, a API do Instagram frequentemente
        retorna status_code=null mesmo quando o vídeo está sendo processado corretamente.
        Nesses casos, após max_none tentativas sem status, assumimos FINISHED e prosseguimos.
        """
        status_url = f"https://graph.facebook.com/v21.0/{creation_id}"
        params = {
            "fields": "status_code,status",
            "access_token": self.access_token
        }
        
        # Para Reels (vídeo standalone), timeout mais longo
        # Para itens de carrossel (video + image), comportamento mais tolerante ao null
        max_attempts = 60 if (is_video and not is_carousel_item) else 30
        none_count = 0
        # Número de tentativas null antes de assumir que está OK
        # Carrossel: tolera mais nulos (API menos confiável para status de vídeo em carrossel)
        max_none = 20 if (is_video and is_carousel_item) else (30 if is_video else 5)
        
        for attempt in range(max_attempts):
            try:
                response = requests.get(status_url, params=params)
                data = response.json()
                status = data.get("status_code")
                
                if status == "FINISHED":
                    print(f"--- [OK] Midia processada e pronta para publicacao.")
                    return True
                elif status == "IN_PROGRESS":
                    none_count = 0
                    print(f"--- [..] Processando midia no Instagram Cloud... (Tentativa {attempt+1}/{max_attempts})")
                    time.sleep(10)
                elif status == "ERROR":
                    failure = data.get("failure_reason", "desconhecido")
                    print(f"--- [ERRO] Erro no processamento da midia: {failure} | {data}")
                    return False
                else:
                    none_count += 1
                    # Status null = API ainda não registrou — comum em imagens e vídeos de carrossel
                    if none_count >= max_none:
                        print(f"--- [AVISO] Status nulo por {none_count} tentativas consecutivas.")
                        if is_video and not is_carousel_item:
                            print("--- Timeout aguardando inicio de processamento do video Reel.")
                            return False
                        else:
                            print("--- Assumindo midia pronta (comportamento esperado da API para carrossel).")
                            return True
                    
                    print(f"--- Aguardando inicio do processamento... ({status or 'Pendente'}) [{none_count}/{max_none}]")
                    time.sleep(5)
            except Exception as e:
                print(f"--- Erro ao checar status: {e}")
                time.sleep(5)
                
        print("--- [!] Timeout total aguardando processamento da midia.")
        return False
