import os
import time
from dotenv import load_dotenv
from social.core.instagram_client import InstagramClient
from social.core.uploader import ResilientUploader

def post_blazer_carousel():
    load_dotenv()
    
    # Forçar modo produção para garantir que links e postagem funcionem no ambiente real
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
    files = [f"blazer_post_{i:02d}.jpg" for i in range(6)]
    
    public_urls = []
    
    print("🚀 Iniciando upload das 6 imagens do carrossel do Blazer...")
    
    for filename in files:
        local_path = os.path.join(fila_dir, filename)
        if not os.path.exists(local_path):
            print(f"❌ Arquivo não encontrado: {local_path}")
            return
            
        print(f"--- Processando {filename}...")
        # Nome único para evitar cache no Meta
        remote_name = f"blazer_carousel_{int(time.time())}_{filename}"
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
    caption = """✨ O BLAZER QUE VOCÊ PRECISA: Elegância e Versatilidade! 🖤💎

Sabe aquela peça que transforma qualquer look básico em uma produção de luxo? Esse Blazer Alongado é exatamente isso! 

Nossa modelo testou em diferentes contextos e o resultado foi impecável. Seja no escritório, no rolê urbano ou em um evento sofisticado, ele entrega TUDO!

✅ Modelagem alongada que valoriza a silhueta
✅ Leve e sem forro: ideal para o dia a dia
✅ Qualidade premium com preço de achadinho Shopee

💰 **Apenas R$ 108,30**

💬 **Comente "QUERO"** que o nosso Robô Titanium envia o link oficial agora mesmo no seu direct! 🚀🦾

#TitaniumModa #BlazerFeminino #AchadinhosShopee #LookElegante #ModaFeminina #ShopeeBrasil #BlazerAlongado #look_titanium #blazer_premium"""

    print("\n📢 Enviando carrossel para o Instagram...")
    # Capturar o ID do post para o bot de comentários
    result = client.post_carousel_with_id(public_urls, caption)
    
    if result and "id" in result:
        post_id = result["id"]
        print(f"\n🏆 SUCESSO! O carrossel do Blazer está no ar. ID: {post_id}")
        
        # Salvar o ID do post ativo para o bot de comentários local
        state_path = r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium\state\blazer_active_post.json"
        product_url = "https://shopee.com.br/product/681681961/23493918147?mmp_pid=an_18318830863&utm_source=an_18318830863"
        with open(state_path, "w") as f:
            import json
            json.dump({
                "post_id": post_id, 
                "hashtag": "#blazer_premium",
                "product_url": product_url
            }, f)
            
        print(f"✅ Estado do post salvo em {state_path}")
    else:
        print("\n❌ Falha na postagem do carrossel.")

if __name__ == "__main__":
    # Nota: Precisamos garantir que InstagramClient tenha o método post_carousel_with_id
    # Se não tiver, o script acima pode falhar. Vamos verificar o InstagramClient.
    post_blazer_carousel()
