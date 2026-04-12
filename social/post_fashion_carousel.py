import os
import time
from dotenv import load_dotenv
from social.core.instagram_client import InstagramClient
from social.core.uploader import ResilientUploader

def post_fashion_carousel():
    load_dotenv()
    
    # Configurações
    ig_token = os.getenv("IG_ACCESS_TOKEN")
    ig_business_id = os.getenv("IG_BUSINESS_ID")
    page_id = os.getenv("PAGE_ID")
    
    ftp_config = {
        "host": os.getenv("FTP_HOST"),
        "user": os.getenv("FTP_USER"),
        "pass": os.getenv("FTP_PASS")
    }
    
    uploader = ResilientUploader(ftp_config=ftp_config)
    client = InstagramClient(ig_token, ig_business_id, page_id=page_id)
    
    # Arquivos na fila
    fila_dir = r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium\social\fila"
    files = [f"fashion_post_{i:02d}.jpg" for i in range(6)]
    
    public_urls = []
    
    print("🚀 Iniciando upload das 6 imagens do carrossel...")
    
    for filename in files:
        local_path = os.path.join(fila_dir, filename)
        if not os.path.exists(local_path):
            print(f"❌ Arquivo não encontrado: {local_path}")
            return
            
        print(f"--- Processando {filename}...")
        remote_name = f"fashion_carousel_{int(time.time())}_{filename}"
        url = uploader.upload(local_path, remote_name)
        
        if url:
            public_urls.append(url)
        else:
            print(f"❌ Falha crítica no upload de {filename}. Abortando postagem.")
            return

    if len(public_urls) < 6:
        print("❌ Erro: Nem todas as imagens foram carregadas corretamente.")
        return

    # Legenda estratégica para o robô de DM
    caption = """✨ TOP 5 TENDÊNCIAS: O Look Perfeito com Preço Shopee! 👗💎

Selecionamos os 5 conjuntos e peças que estão dominando as ruas e que você encontra com os menores preços na nossa curadoria. Qual seu favorito?

1️⃣ Conjunto Alfaiataria Super Luxo - R$ 65,99
2️⃣ Jaqueta de Couro Ecológico - R$ 63,92
3️⃣ Calça Pantalona Alfaiataria - R$ 124,90
4️⃣ Blazer Max Alongado - R$ 99,90
5️⃣ Vestido Midi Tricot Canelado - R$ 39,90

💬 **Comente "QUERO"** que o nosso robô Titanium envia todos os links agora no seu direct! 🚀🦾

#TecnologiaTitanium #ModaFeminina #ShopeeBrasil #Achadinhos #LookDoDia #Pantalona #LookShopee #look_shopee1"""

    print("\n📢 Enviando carrossel para o Instagram...")
    success = client.post_carousel(public_urls, caption)
    
    if success:
        print("\n🏆 SUCESSO! O carrossel de moda está no ar.")
        # Opcional: mover arquivos para 'postados'
    else:
        print("\n❌ Falha na postagem do carrossel.")

if __name__ == "__main__":
    post_fashion_carousel()
