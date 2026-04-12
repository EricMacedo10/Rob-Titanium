import os
import time
import json
from dotenv import load_dotenv
from social.core.instagram_client import InstagramClient
from social.core.uploader import ResilientUploader

def post_conjunto_carousel():
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
    
    # Arquivos na fila (5 imagens)
    fila_dir = r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium\social\fila"
    files = [f"conjunto_post_{i:02d}.jpg" for i in range(5)]
    
    public_urls = []
    
    print(f"🚀 Iniciando upload das {len(files)} imagens do carrossel do Conjunto Alfaiataria...")
    print(f"Modo: {os.environ.get('ENV_MODE')}")
    
    for i, filename in enumerate(files):
        local_path = os.path.join(fila_dir, filename)
        if not os.path.exists(local_path):
            print(f"❌ Arquivo não encontrado: {local_path}")
            return
            
        print(f"--- [{i+1}/{len(files)}] Fazendo upload de {filename}...")
        remote_name = f"conjunto_carousel_{int(time.time())}_{filename}"
        # Força ImgBB para evitar erro 9004 do Hostinger detectado anteriormente
        url = uploader.upload(local_path, remote_name, force_cloud=True)
        
        if url:
            public_urls.append(url)
        else:
            print(f"❌ Falha crítica no upload de {filename}. Abortando.")
            return

    # Legenda agradável e focada em conversão
    caption = (
        "✨ DELICADEZA E SOFISTICAÇÃO: O CONJUNTO DOS SEUS SONHOS! 🔸👗\n\n"
        "Meninas, se existe um look que abraça o corpo e eleva a autoestima, é este! "
        "Nosso novo Conjunto Alfaiataria com modelagem de ombro único é a definição de elegância sem esforço. \n\n"
        "Seja para um almoço especial, um passeio ao pôr do sol ou aquele jantar chic, ele garante um caimento "
        "impecável e muito conforto para você brilhar. A faixa na cintura valoriza cada detalhe, trazendo aquele "
        "toque feminino que amamos! ✨\n\n"
        "💎 Por que você vai se apaixonar:\n"
        "• Design assimétrico super moderno\n"
        "• Tecido premium de toque suave\n"
        "• Short com corte alfaiataria (comprimento perfeito!)\n"
        "• Versatilidade para usar com salto ou rasteirinha\n\n"
        "🔥 OFERTA ESPECIAL SHOPEE: Apenas R$ 59,99! \n"
        "(Um preço incrível para uma peça de alta qualidade)\n\n"
        "💬 QUER O LINK PARA GARANTIR O SEU?\n"
        "Basta comentar \"QUERO\" abaixo e o Robô Titanium enviará o link oficial agora mesmo no seu Direct "
        "com total segurança! 🔗📲\n\n"
        "#TitaniumModa #ConjuntoAlfaiataria #LookCasualChic #AchadinhosShopee #ModaFeminina #LookDoDia #ShopeeBrasil #MulherElegante #look_titanium #conjunto_casual"
    )

    print("\n📢 Enviando carrossel para o Instagram...")
    # Usar post_carousel_with_id para capturar o ID necessário para o bot de comentários
    result = client.post_carousel_with_id(public_urls, caption)
    
    if result and isinstance(result, dict) and "id" in result:
        post_id = result["id"]
        print(f"\n🏆 SUCESSO! O carrossel do Conjunto está no ar. ID: {post_id}")
        
        # Salvar estado para o bot de comentários
        state_path = r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium\state\conjunto_active_post.json"
        product_url = "https://shopee.com.br/product/1293226072/23698847324?mmp_pid=an_18318830863&utm_source=an_18318830863"
        with open(state_path, "w", encoding="utf-8") as f:
            json.dump({
                "post_id": post_id, 
                "hashtag": "#conjunto_casual",
                "product_url": product_url
            }, f, indent=4, ensure_ascii=False)
            
        print(f"✅ Estado do post salvo em {state_path}")
    else:
        print("\n❌ Falha na postagem do carrossel.")

if __name__ == "__main__":
    post_conjunto_carousel()
