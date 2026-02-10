import json
import os
import random
from social.image_generator import ImageGenerator
from social.instagram_client import InstagramClient
from social.copywriter import Copywriter
from social.uploader import ResilientUploader
from scraper.upload import upload_to_hostinger
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
        Define a loja baseada na hora do dia:
        Manhã (5h-12h): Amazon
        Tarde (12h-18h): Shopee
        Noite (18h-24h): Mercado Livre
        """
        from datetime import datetime
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return "amazon"
        elif 12 <= hour < 18:
            return "shopee"
        else:
            return "mercadolivre"

    def run_daily_cycle(self, ig_token=None, ig_business_id=None, force_store=None):
        """
        Orquestra a postagem PRIORIZANDO a fila de curadoria (social/fila/).
        Se a fila estiver vazia, ele atua no modo semi-automático de banners de categoria.
        """
        print("\n" + "="*60)
        print("🤖 INICIANDO TITANIUM SOCIAL BOT - MODO CURADORIA (v1144)")
        print("="*60)
        
        from social.video_utils import image_to_video
        from datetime import datetime
        import shutil

        # Configuração do Cliente Instagram
        if self.env_mode == "STAGING":
            print("🧪 MODO STAGING: Simulação de postagem ativa.")
            self.instagram = None
        elif ig_token and ig_business_id:
            self.instagram = InstagramClient(ig_token, ig_business_id)
        else:
            print("⚠️ Sem credenciais! Operando em modo de visualização local.")
            self.instagram = None

        # --- FASE 1: VERIFICAR FILA DE CURADORIA ---
        fila_dir = "social/fila"
        postados_dir = "social/postados"
        # Agora aceita imagens E vídeos
        formatos_validos = ('.png', '.jpg', '.jpeg', '.mp4', '.mov')
        arquivos_fila = [f for f in os.listdir(fila_dir) if f.lower().endswith(formatos_validos)]
        
        if arquivos_fila:
            print(f"📂 Encontrado(s) {len(arquivos_fila)} arquivo(s) na fila de curadoria.")
            # Pega o primeiro da fila
            target_file = sorted(arquivos_fila)[0]
            local_path = os.path.join(fila_dir, target_file)
            print(f"🎯 Arquivo Selecionado: {target_file}")
            
            is_video = target_file.lower().endswith(('.mp4', '.mov'))
            
            # Tentar identificar loja/categoria
            parts = target_file.lower().split('_')
            store = parts[0] if len(parts) > 0 else "default"
            category = parts[1].split('.')[0] if len(parts) > 1 else "ofertas"
            
            caption = self.copywriter.generate_category_caption(store, category)
            
            local_image = local_path if not is_video else None
            local_video = local_path if is_video else f"social/temp_video_output.mp4"
            target_banner = target_file # Para o arquivamento posterior
        else:
            # --- FASE 2: FALLBACK PARA BANNERS DE CATEGORIA ---
            print("📭 Fila vazia. Iniciando modo fallback (Banners de Categoria)...")
            store = force_store or self.get_scheduled_store()
            offers = self.load_offers()
            store_offers = [o for o in offers if o.get('store', '').lower().replace(" ", "") == store.lower()]
            
            if not store_offers:
                print(f"⚠️ Nenhuma oferta da {store} para processar fallback.")
                return

            best_offer = sorted(store_offers, key=lambda x: x.get('discount', 0), reverse=True)[0]
            category = best_offer.get('category', 'tecnologia').lower()
            
            # Procura banner de categoria
            local_image = None
            for ext in ['.png', '.jpg', '.jpeg']:
                path = f"social/banners/banner_{store}_{category}{ext}"
                if os.path.exists(path):
                    local_image = path
                    break
            
            if not local_image:
                print(f"❌ Abortando: Nenhum banner (curadoria ou categoria) disponível para {store}/{category}.")
                return
                
            caption = self.copywriter.generate_category_caption(store, category)

        # --- FASE 3: DECISÃO DE FORMATO E PROCESSAMENTO ---
        # Reels tem mais entrega, então priorizamos Reels (Vídeo)
        post_format = "reels" 
        success = False
        
        print(f"📌 Preparando postagem: {post_format.upper()} | Loja: {store.upper()}")

        # Só processa se NÃO for vídeo já
        if arquivos_fila and target_file.lower().endswith(('.mp4', '.mov')):
            print("🎬 Arquivo já é um vídeo. Pulando conversão...")
            ready_to_upload = True
            video_to_use = local_path
        else:
            print("🎬 Gerando vídeo a partir de imagem...")
            video_to_use = f"social/temp_video_output.mp4"
            ready_to_upload = image_to_video(local_image, video_to_use)

        if ready_to_upload:
            if self.instagram:
                # Upload do vídeo
                public_url = self.uploader.upload(video_to_use, f"titanium_{post_format}_{int(time.time())}.mp4")
                if public_url:
                    success = self.instagram.post_reels(public_url, caption)
            else:
                print(f"📸 [SIMULAÇÃO] Postando Reels: {video_to_use}")
                success = True

        # --- FASE 4: FINALIZAÇÃO E ARQUIVAMENTO ---
        if success:
            print("🎉 CICLO CONCLUÍDO COM SUCESSO!")
            if arquivos_fila:
                # Move da fila para postados
                os.makedirs(postados_dir, exist_ok=True)
                target_path = os.path.join(postados_dir, target_banner)
                # Evita sobrescrever se já existir
                if os.path.exists(target_path):
                    filename, extension = os.path.splitext(target_banner)
                    target_path = os.path.join(postados_dir, f"{filename}_{int(time.time())}{extension}")
                
                # Se for o vídeo temporário, não movemos (apenas apagamos se necessário), 
                # mas aqui target_banner é o arquivo original da FILA.
                shutil.move(local_path, target_path)
                print(f"📦 Arquivo arquivado em: {os.path.basename(target_path)}")
                
                # Limpeza do temporário se gerado
                temp_v = "social/temp_video_output.mp4"
                if os.path.exists(temp_v) and temp_v != local_path:
                    os.remove(temp_v)
        else:
            print("❌ Falha crítica no ciclo de postagem.")
            

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    bot = SocialBot()
    # Teste local lendo segredos reais
    bot.run_daily_cycle(
        ig_token=os.getenv("IG_ACCESS_TOKEN"),
        ig_business_id=os.getenv("IG_BUSINESS_ID")
    )
