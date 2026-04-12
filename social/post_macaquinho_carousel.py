import os
import time
from dotenv import load_dotenv
from social.core.instagram_client import InstagramClient
from social.core.uploader import ResilientUploader

def post_macaquinho_carousel():
    load_dotenv()
    os.environ["ENV_MODE"] = "PRODUCTION"
    
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
    files = [f"macaquinho_post_{i:02d}.jpg" for i in range(6)]
    
    public_urls = []
    
    print("--- Iniciando upload do carrossel do Macaquinho Modelador (6 slides) ---")
    
    for filename in files:
        local_path = os.path.join(fila_dir, filename)
        if not os.path.exists(local_path):
            print(f"Erro: Arquivo não encontrado: {local_path}")
            return
            
        remote_name = f"macaquinho_carousel_{int(time.time())}_{filename}"
        url = uploader.upload(local_path, remote_name)
        
        if url:
            public_urls.append(url)
        else:
            print(f"Erro: Falha no upload de {filename}.")
            return

    if len(public_urls) < 6:
        return

    # Legenda Persuasiva
    caption = """A SILHUETA QUE VOCÊ SEMPRE QUIS! 💎✨

Diga adeus às marcações na roupa e olá para a confiança total! Nosso Macaquinho Modelador de Alta Compressão é o segredo das melhores produções.

✅ Por que este é o MODELADOR DEFINITIVO?
* Alta Compressão: Define a silhueta e reduz medidas na hora.
* Invisível: Perfeito para usar com vestidos, não marca nada!
* Conforto Premium: Tecido cetinete anatômico e forro 100% algodão.
* Postura: Auxilia na sustentação lombar e corrige a postura.
* Ajustável: Alças que garantem a sustentação que você precisa.

💰 Investimento em você: **R$ 104,50**

🚨 COMO COMPRAR?
Comente **"QUERO"** que eu te envio o link oficial agora mesmo no seu Direct! 🚀🦾

#Modelador #CintaModeladora #SilhuetaPerfeita #ModaFeminina #AchadinhosShopee #CorpoReal #Postura #look_titanium #macaquinho_modelador"""

    print("\n--- Enviando carrossel para o Instagram ---")
    result = client.post_carousel_with_id(public_urls, caption)
    
    if result and "id" in result:
        post_id = result["id"]
        print(f"\nSUCESSO! O carrossel do Macaquinho está no ar. ID: {post_id}")
        
        # Salvar estado para o bot de DMs
        state_path = r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium\state\macaquinho_active_post.json"
        product_url = "https://s.shopee.com.br/1gEZjABR6e"
        with open(state_path, "w") as f:
            import json
            json.dump({
                "post_id": post_id, 
                "hashtag": "#macaquinho_modelador",
                "product_url": product_url
            }, f)
            
        print(f"Estado do post salvo em {state_path}")
    else:
        print("\nFalha na postagem do carrossel.")

if __name__ == "__main__":
    post_macaquinho_carousel()
