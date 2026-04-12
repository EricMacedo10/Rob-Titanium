import os
import time
from dotenv import load_dotenv
from social.core.instagram_client import InstagramClient
from social.core.uploader import ResilientUploader

def post_top_tricot_carousel():
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
    
    # Nossas 5 imagens geradas
    image_files = [
        "post_1_loira.png",
        "post_2_morena.png",
        "post_3_negra.png",
        "post_4_plusize.png",
        "post_5_madura.png"
    ]
    
    public_urls = []
    
    print(f"🚀 Iniciando upload de {len(image_files)} imagens para o carrossel do Top Cropped...")
    
    for filename in image_files:
        local_path = os.path.join(fila_dir, filename)
        if not os.path.exists(local_path):
            print(f"❌ Arquivo não encontrado: {local_path}")
            continue
            
        print(f"--- Processando {filename}...")
        # Adiciona timestamp para evitar cache no servidor FTP
        remote_name = f"top_tricot_{int(time.time())}_{filename}"
        url = uploader.upload(local_path, remote_name)
        
        if url:
            public_urls.append(url)
        else:
            print(f"❌ Falha no upload de {filename}.")

    if not public_urls:
        print("❌ Erro: Nenhuma imagem foi carregada corretamente.")
        return

    # Legenda Magnética e Chamativa
    caption = """✨ O LOOK QUE VOCÊ NÃO SABIA QUE PRECISAVA! 🧶💎

Conheça o nosso novo **Top Cropped Strapless em Tricot Modal**. A peça coringa que combina conforto absoluto com um caimento impecável. 

✅ Tecido Premium (não amassa!)
✅ Toque macio e leve para o verão
✅ Ajuste perfeito: do casual ao arraso na festa
✅ Estilo Strapless (Tomara que caia) chic

🔥 **COMO COMPRAR?**
💬 Comente **'QUERO'** que o nosso robô Titanium envia o link direto com o menor preço da Shopee agora no seu Direct! 🚀🦾

⚠️ *Imagens geradas por IA para ilustração de estilo e caimento do produto.*

#GuiaDoDesconto #ModaFeminina #TopCropped #TricotModal #LookVerão #AchadinhosShopee #ShopeeBrasil #LookDoDia"""

    print(f"\n📢 Enviando carrossel de {len(public_urls)} imagens para o Instagram...")
    success = client.post_carousel(public_urls, caption)
    
    if success:
        print("\n🏆 SUCESSO! O carrossel do Top Cropped está no ar.")
    else:
        print("\n❌ Falha na postagem do carrossel.")

if __name__ == "__main__":
    post_top_tricot_carousel()
