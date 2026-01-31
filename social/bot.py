import json
import os
import random
from social.image_generator import ImageGenerator
from social.instagram_client import InstagramClient
from social.copywriter import Copywriter
from scraper.upload import upload_to_hostinger
from dotenv import load_dotenv

load_dotenv()

class SocialBot:
    """
    Orquestrador do Robô Titanium para Redes Sociais.
    """
    def __init__(self, data_path="site/data.json", assets_path="site/images"):
        self.data_path = data_path
        self.gen = ImageGenerator(assets_path=assets_path)
        self.copywriter = Copywriter()
        self.instagram = None 
        # Configurações de FTP para "Ponte de Imagem"
        self.ftp_config = {
            "host": os.getenv("FTP_HOST"),
            "user": os.getenv("FTP_USER"),
            "pass": os.getenv("FTP_PASS")
        }
        
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

    def run_daily_cycle(self, ig_token=None, ig_business_id=None):
        """
        Executa um ciclo de postagens.
        """
        print("🤖 Iniciando ciclo do Social Bot Titanium...")
        
        offers = self.select_best_offers(count=3)
        if not offers:
            print("⚠️ Nenhuma oferta encontrada para postar.")
            return

        # Inicializa cliente se tiver os dados
        if ig_token and ig_business_id:
            self.instagram = InstagramClient(ig_token, ig_business_id)

        for i, offer in enumerate(offers):
            print(f"🎬 Processando oferta {i+1}: {offer['title']}")
            
            output_name = f"social/temp_post_{i}.jpg"
            
            # Gerar Legenda Dinâmica (Copywriting)
            caption = self.copywriter.generate_caption(
                offer['title'], 
                str(offer['price']), 
                offer['store'],
                offer.get('discount', 0),
                offer.get('category', 'default')
            )
            
            # Gerar Arte com Tratamento de Erro (Compliance de Imagem)
            try:
                self.gen.generate_post(
                    offer['title'],
                    str(offer['price']),
                    offer['image'],
                    offer['store'].lower().replace(" ", ""),
                    output_name,
                    format="post" if random.random() > 0.3 else "reels"
                )
                print(f"✅ Arte gerada: {output_name}")
                # Se tivermos o cliente e a ponte FTP, postamos de verdade
                if self.instagram and self.ftp_config["user"]:
                    # 1. Enviar para o Servidor (Ponte)
                    remote_name = f"social/insta_post_{i}.jpg"
                    public_url = f"https://guiadodesconto.com.br/{remote_name}"
                    
                    print(f"📤 Enviando arte para a ponte: {public_url}")
                    success = upload_to_hostinger(
                        output_name, 
                        self.ftp_config["host"], 
                        self.ftp_config["user"], 
                        self.ftp_config["pass"], 
                        remote_name
                    )
                    
                    if success:
                        # 2. Postar no Instagram
                        print(f"📢 Postando no Instagram via API...")
                        self.instagram.post_image(public_url, caption)
                    else:
                        print("❌ Falha na ponte FTP. Postagem abortada.")
                else:
                    print("📢 Modo Simulação: Postagem não enviada (faltam credenciais ou FTP).")
            except Exception as e:
                print(f"❌ Pulando oferta devido a erro na imagem: {e}")
                continue
            

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    bot = SocialBot()
    # Teste local lendo segredos reais
    bot.run_daily_cycle(
        ig_token=os.getenv("IG_ACCESS_TOKEN"),
        ig_business_id=os.getenv("IG_BUSINESS_ID")
    )
