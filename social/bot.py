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
        Orquestra um ciclo completo de postagem para a loja agendada do horário.
        """
        print("🤖 Iniciando ciclo do Social Bot Titanium (Modo Senior)...")
        
        from social.video_utils import image_to_video
        from datetime import datetime

        # Forçar simulação se estiver em staging
        if self.env_mode == "STAGING":
            ig_token = None
            ig_business_id = None
            
        if not ig_token or not ig_business_id:
            print("📢 Modo Simulação: Operando sem credenciais do Instagram.")
            self.instagram = None
        else:
            self.instagram = InstagramClient(ig_token, ig_business_id)

        # 1. Escolher a Loja (Agendamento)
        store = force_store or self.get_scheduled_store()
        print(f"🕒 Horário: {datetime.now().strftime('%H:%M')} | Loja Alvo: {store.upper()}")

        # 2. Selecionar Melhor Categoria ou Produto
        offers = self.load_offers()
        store_offers = [o for o in offers if o.get('store', '').lower().replace(" ", "") == store.lower()]
        
        if not store_offers:
            print(f"⚠️ Nenhuma oferta da {store} encontrada. Abortando.")
            return

        # Prioriza a melhor oferta da loja específica
        best_offer = sorted(store_offers, key=lambda x: x.get('discount', 0), reverse=True)[0]
        category = best_offer.get('category', 'tecnologia').lower()

        # 3. Verificar se temos Banner de Categoria
        banner_extensions = ['.png', '.jpg', '.jpeg']
        banner_path = None
        for ext in banner_extensions:
            path = f"social/banners/banner_{store}_{category}{ext}"
            if os.path.exists(path):
                banner_path = path
                break
        
        # 4. Orquestração do Post
        if banner_path:
            print(f"💎 Banner Premium encontrado: {banner_path}")
            caption = self.copywriter.generate_category_caption(store, category)
            local_image = banner_path
            use_category_layout = True
        else:
            print(f"📦 Usando layout de Produto Individual (Banner não encontrado para {category}).")
            caption = self.copywriter.generate_caption(
                best_offer['title'], 
                str(best_offer['price']), 
                best_offer['store'],
                best_offer.get('discount', 0),
                category
            )
            local_image = f"social/temp_category_post.jpg"
            self.gen.generate_post(
                best_offer['title'],
                str(best_offer['price']),
                best_offer['image'],
                store,
                local_image,
                format="reels" # Posts de horário sempre em formato vertical (Story/Reels)
            )
            use_category_layout = False

        # 5. Decisão de Formato (Story ou Reels para maior impacto)
        post_format = "reels" if random.random() > 0.5 else "story"
        print(f"📌 Formato: {post_format.upper()}")

        local_video = f"social/temp_video_cycle.mp4"
        success = False

        # 6. Fluxo de Ativos e Postagem
        if post_format == "reels":
            if image_to_video(local_image, local_video):
                if self.instagram:
                    public_url = self.uploader.upload(local_video, f"cycle_reels_{store}.mp4")
                    if public_url:
                        success = self.instagram.post_reels(public_url, caption)
            
            if not success:
                print("⚠️ Falha no Reels. Tentando Fallback para Story...")
                post_format = "story"

        if post_format == "story":
            if self.instagram:
                public_url = self.uploader.upload(local_image, f"cycle_story_{store}.jpg")
                if public_url:
                    success = self.instagram.post_story(public_url, is_video=False)
            else:
                print(f"📢 Modo Simulação: [{post_format}] {store} categoria {category}")

        if success:
            print(f"🏆 Ciclo concluído com sucesso!")
        else:
            print(f"❌ Falha no ciclo de postagem.")
            

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    bot = SocialBot()
    # Teste local lendo segredos reais
    bot.run_daily_cycle(
        ig_token=os.getenv("IG_ACCESS_TOKEN"),
        ig_business_id=os.getenv("IG_BUSINESS_ID")
    )
