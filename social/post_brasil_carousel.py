import os
import time
from dotenv import load_dotenv
from social.core.instagram_client import InstagramClient
from social.core.uploader import ResilientUploader

def post_brasil_carousel():
    load_dotenv()
    
    # Forçar modo produção
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
    files = [f"brasil_post_{i:02d}.jpg" for i in range(5)]
    
    public_urls = []
    
    print("--- Iniciando upload das 5 imagens do carrossel da Seleção Brasil ---")
    
    for filename in files:
        local_path = os.path.join(fila_dir, filename)
        if not os.path.exists(local_path):
            print(f"Erro: Arquivo não encontrado: {local_path}")
            return
            
        # Nome único para evitar cache no Meta
        remote_name = f"brasil_carousel_{int(time.time())}_{filename}"
        url = uploader.upload(local_path, remote_name)
        
        if url:
            public_urls.append(url)
        else:
            print(f"Erro: Falha no upload de {filename}.")
            return

    if len(public_urls) < 5:
        return

    # Legenda oficial configurada
    caption = """VISTA O MANTO DA NOSSA SELEÇÃO! 🇧🇷✨

Chegou a hora de renovar o seu manto com estilo e conforto! Nossa Camiseta Dry Brasil é perfeita para quem não abre mão de torcer com qualidade.

✅ Por que você vai amar:
* Tecido Dry Fit: Peso médio, fresco e confortável.
* Design Oficial: Brasão clássico com detalhes impecáveis.
* Unissex: Modelagem regular.

🔥 OFERTA EXCLUSIVA AMAZON: R$ 46,45 😱

🚨 COMO GARANTIR A SUA?
Basta comentar 'QUERO' abaixo que eu te envio o link diretamente no seu Direct! 🔗👇

#SelecaoBrasileira #Brasil #CamisaDoBrasil #FutebolBrasileiro #OfertasAmazon #ModaEsportiva #Trend #look_titanium #camisa_brasil"""

    print("\n--- Enviando carrossel para o Instagram ---")
    result = client.post_carousel_with_id(public_urls, caption)
    
    if result and "id" in result:
        post_id = result["id"]
        print(f"\nSUCESSO! O carrossel da Seleção está no ar. ID: {post_id}")
        
        # Salvar o ID do post ativo para o bot de comentários
        state_path = r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium\state\brasil_active_post.json"
        product_url = "https://www.amazon.com.br/Camiseta-Unissex-Redonda-Sele%C3%A7%C3%A3o-Brasileira/dp/B0GT9SZHDD?tag=guiadodesco00-20"
        with open(state_path, "w") as f:
            import json
            json.dump({
                "post_id": post_id, 
                "hashtag": "#camisa_brasil",
                "product_url": product_url
            }, f)
            
        print(f"Estado do post salvo em {state_path}")
    else:
        print("\nFalha na postagem do carrossel.")

if __name__ == "__main__":
    post_brasil_carousel()
