import time
import random
import sys
import shutil
import os
import json
from datetime import datetime
from social.core.image_generator import ImageGenerator
from social.core.instagram_client import InstagramClient
from social.core.copywriter import Copywriter
from social.core.uploader import ResilientUploader
from infra.upload_logic import upload_to_hostinger
from dotenv import load_dotenv

load_dotenv()

class SocialBot:
    """
    Orquestrador do Robô Titanium para Redes Sociais.
    """
    def __init__(self, data_path="site/data.json", assets_path="site/images"):
        self.data_path = data_path
        self.gen = ImageGenerator(assets_path)
        self.copywriter = Copywriter()
        
        # Modo de Segurança (Staging)
        self.env_mode = os.getenv('ENV_MODE', 'STAGING').upper()
        if self.env_mode == "STAGING":
            print("🧪 AMBIENTE DE STAGING ATIVADO: Postagens reais bloqueadas.")

        # Configurações de FTP
        self.ftp_config = {
            "host": os.getenv("FTP_HOST"),
            "user": os.getenv("FTP_USER"),
            "pass": os.getenv("FTP_PASS")
        }
        
        # Inicializa Orquestrador de Upload
        self.uploader = ResilientUploader(
            ftp_config=self.ftp_config,
            imgbb_api_key=os.getenv("IMGBB_API_KEY")
        )
        self.instagram = None
        self.max_carousel_size = 10 # Limite da Meta API

    def load_offers(self):
        with open(self.data_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def select_best_offers(self, count=3):
        offers = self.load_offers()
        # Requisito de Compliance: Filtrar apenas ofertas com imagem válida
        valid_offers = [o for o in offers if o.get('image') and str(o.get('image')).startswith('http')]
        
        # Prioriza ofertas com maior desconto
        sorted_offers = sorted(valid_offers, key=lambda x: x.get('discount', 0), reverse=True)
        return sorted_offers[:count]

    def get_scheduled_store(self):
        """
        Define a loja baseada na política 100% Shopee Exclusive.
        """
        return "shopee"

    def run_daily_cycle(self, ig_token=None, ig_business_id=None, force_store=None):
        """
        Orquestra a postagem PRIORIZANDO a fila de curadoria.
        Agora suporta CARROSSEL AUTOMÁTICO de até 10 itens.
        """
        print("\n" + "="*60)
        print("🤖 INICIANDO TITANIUM SOCIAL BOT - MODO POST ÚNICO (v2.1.0)")
        print("="*60)
        
        from social.utils.video_utils import image_to_video

        # Configuração do Cliente Instagram
        if self.env_mode == "STAGING":
            print("🧪 MODO STAGING: Simulação de postagem ativa.")
            self.instagram = None
        elif ig_token and ig_business_id:
            self.instagram = InstagramClient(ig_token, ig_business_id)
        else:
            print("⚠️ Sem credenciais! Operando em modo de visualização local.")
            self.instagram = None

        fila_dir = "social/fila"
        postados_dir = "social/postados"
        formatos_validos = ('.png', '.jpg', '.jpeg', '.mp4', '.mov')
        arquivos_fila = sorted([f for f in os.listdir(fila_dir) if f.lower().endswith(formatos_validos)])
        
        if not arquivos_fila:
            # Fallback para Banner (mantem logica atual simplificada)
            print("📭 Fila vazia. Iniciando modo fallback (Banners de Categoria)...")
            self._run_fallback_cycle(force_store)
            return

        # --- NOVA LÓGICA DE AGRUPAMENTO (CARROSSEL) ---
        # Pegamos o primeiro item para definir o contexto (loja/categoria)
        # e então tentamos agrupar itens similares que estejam na fila.
        target_files = arquivos_fila[:1]  # Modo Post Único: processa 1 por ciclo
        print(f"📂 Encontrado(s) {len(arquivos_fila)} arquivo(s). Selecionando 1 para postagem...")
        
        media_to_upload = []
        combined_captions = []
        full_paths = []
        
        store = "shopee" # Default
        category = "ofertas"

        for i, filename in enumerate(target_files):
            local_path = os.path.join(fila_dir, filename)
            full_paths.append(local_path)
            is_video = filename.lower().endswith(('.mp4', '.mov'))
            
            # Identificação básica
            parts = filename.lower().split('_')
            store = parts[0] if len(parts) > 0 else "shopee"
            
            # Lendo Metadata JSON se existir
            json_path = local_path.replace(os.path.splitext(local_path)[1], '.json')
            if os.path.exists(json_path):
                try:
                    with open(json_path, 'r', encoding='utf-8') as mj:
                        meta = json.load(mj)
                    combined_captions.append(f"{i+1}️⃣ {meta['title']} ➔ R$ {meta['price']}")
                except: pass

            media_to_upload.append({"local": local_path, "type": "VIDEO" if is_video else "IMAGE"})

        # Construir Legenda Premium do Carrossel
        header = f"✨ SELEÇÃO EXCLUSIVA: {store.upper()} ✨\n\n"
        body = "\n".join(combined_captions) if combined_captions else f"Novidades incríveis em {category.upper()} para você! 🚀"
        footer = f"\n\n💬 Comente **'QUERO'** que o nosso robô Titanium manda todos os links no seu direct! 🦾🤖\n\n#TitaniumBot #ShopeeBrasil #Achadinhos #Moda #Curadoria"
        final_caption = header + body + footer

        # --- EXECUÇÃO DO UPLOAD ---
        public_urls = []
        for item in media_to_upload:
            ext = ".mp4" if item["type"] == "VIDEO" else ".jpg"
            remote_name = f"titanium_cluster_{int(time.time())}_{os.path.basename(item['local'])}"
            url = self.uploader.upload(item["local"], remote_name)
            if url:
                public_urls.append({"url": url, "type": item["type"]})
            else:
                print(f"❌ Falha crítica no upload de {item['local']}. Abortando ciclo.")
                sys.exit(1)

        # --- POSTAGEM ---
        success = False
        if self.instagram and public_urls:
            if len(public_urls) > 1:
                print(f"📢 Publicando CARROSSEL com {len(public_urls)} itens...")
                success = self.instagram.post_carousel(public_urls, final_caption)
            else:
                # Se só sobrou 1 (ou a fila só tinha 1), posta como Reel
                item = public_urls[0]
                if item["type"] == "IMAGE":
                    video_temp = "social/temp_reel.mp4"
                    image_to_video(media_to_upload[0]["local"], video_temp)
                    url = self.uploader.upload(video_temp, f"reel_{int(time.time())}.mp4")
                    success = self.instagram.post_reels(url, final_caption)
                else:
                    success = self.instagram.post_reels(item["url"], final_caption)
        else:
            print("🧪 [SIMULAÇÃO] Postagem de Carrossel Simulada com Sucesso.")
            success = True

        # --- FINALIZAÇÃO ---
        if success:
            print("🎉 CICLO CONCLUÍDO COM SUCESSO!")
            os.makedirs(postados_dir, exist_ok=True)
            for path in full_paths:
                # Move imagem/vídeo
                shutil.move(path, os.path.join(postados_dir, os.path.basename(path)))
                # Move JSON
                jp = path.replace(os.path.splitext(path)[1], '.json')
                if os.path.exists(jp):
                    shutil.move(jp, os.path.join(postados_dir, os.path.basename(jp)))
            sys.exit(0)
        else:
            print("❌ Falha crítica no ciclo de postagem.")
            sys.exit(1)

    def _run_fallback_cycle(self, force_store):
        """Lógica de banners de categoria se a fila estiver vazia (simplificada para manter histórico)"""
        # (Aqui iria a lógica antiga de banners, mantida como fallback)
        print("⚠️ Pulando fallback por enquanto: Prioridade total na CURADORIA.")
        sys.exit(0) # Sem falha, apenas sem trabalho.


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    bot = SocialBot()
    # Teste local lendo segredos reais
    bot.run_daily_cycle(
        ig_token=os.getenv("IG_ACCESS_TOKEN"),
        ig_business_id=os.getenv("IG_BUSINESS_ID")
    )
