import os
import sys
import time
import json
from dotenv import load_dotenv

project_root = r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium"
if project_root not in sys.path:
    sys.path.append(project_root)

from social.core.instagram_client import InstagramClient
from social.core.uploader import ResilientUploader

def post_pantalona():
    load_dotenv(os.path.join(project_root, ".env"))
    
    # Configurações do Post
    PRODUCT_URL = "https://s.shopee.com.br/7podwPkdvl?utm_source=ericmacedo" # Link #pantalona com tag afiliado
    KEYWORD = "QUERO"
    
    # Credenciais
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
    
    fila_dir = os.path.join(project_root, "social", "fila")
    
    image_files = [
        "imagem1.png",
        "imagem2.png",
        "imagem3.png",
        "imagem4.png",
        "imagem5.png"
    ]
    
    public_urls = []
    
    print(f"🚀 Iniciando upload de {len(image_files)} imagens para o carrossel da Pantalona...")
    
    for filename in image_files:
        local_path = os.path.join(fila_dir, filename)
        if not os.path.exists(local_path):
            print(f"❌ Arquivo não encontrado: {local_path}")
            continue
            
        print(f"--- Processando {filename}...")
        remote_name = f"pantalona_{int(time.time())}_{filename}"
        url = uploader.upload(local_path, remote_name)
        
        if url:
            public_urls.append(url)
        else:
            print(f"❌ Falha no upload de {filename}.")

    if not public_urls:
        print("❌ Erro: Nenhuma imagem foi carregada corretamente.")
        return

    caption = """✨ CONFORTO E ESTILO: A Calça Pantalona de Moletom que você não vai querer tirar! ☁️👗\n\nSabe aquela peça que une o toque aveludado do moletom com a elegância do corte pantalona? É ESSA! Ideal para quem busca um look casual sem abrir mão da sofisticação. Totalmente adaptável do tênis ao salto! 👠👟\n\n🔥 POR QUE VOCÊ VAI AMAR:\n✅ Cintura Alta: valoriza a silhueta e garante segurança.\n✅ 100% Algodão Flanelado: macia e "quentinha" por dentro (toque aveludado).\n✅ Corte Pantalona: Elegância que flui no corpo.\n✅ Versátil: Perfeita para o home office, passeio ou um look formal moderno.\n\n📏 Tamanhos: P (36), M (38/40), G (42), GG.\n\n💬 Quer o link com DESCONTO na Shopee?\nComente "QUERO" que o nosso Robô Titanium envia o link direto no seu direct agora mesmo! 🤖🚀\n\n⚠️ *Imagens meramente ilustrativas geradas por Inteligência Artificial para demonstração de uso.*\n\n#RoboTitanium #ModaFeminina #CalcaPantalona #LookMoletom #ConfortoEEstilo #AchadinhosShopee #ModaCasual #LookDoDia #PromoçãoShopee"""

    print(f"\n📢 Enviando carrossel de {len(public_urls)} imagens para o Instagram...")
    success = client.post_carousel(public_urls, caption)
    
    if success:
        print("\n🏆 SUCESSO! O carrossel da Pantalona está no ar.")
        
        print("\n🔍 Buscando o ID da postagem para o Bot de Comentários...")
        time.sleep(10)  # Aguardar alguns segundos para a API refletir a criação
        latest_media = client.get_latest_media(limit=1)
        if latest_media and len(latest_media) > 0:
            post_id = latest_media[0].get("id")
            print(f"✅ ID da postagem encontrado: {post_id}")
            
            # Salvar no state para o bot de comentário
            state_dir = os.path.join(project_root, "state")
            os.makedirs(state_dir, exist_ok=True)
            state_file = os.path.join(state_dir, "pantalona_active_post.json")
            
            state_data = {
                "post_id": post_id,
                "product_url": PRODUCT_URL,
                "keyword": KEYWORD,
                "timestamp": time.time()
            }
            
            with open(state_file, "w", encoding="utf-8") as f:
                json.dump(state_data, f, indent=4)
                
            print(f"✅ Arquivo de state salvo em: {state_file}")
            print(f"🤖 Lembre-se de iniciar o bot de monitoramento: python social/bot_comentario_pantalona.py")
        else:
            print("⚠️ Não foi possível obter o ID da postagem mais recente para configurar o Bot automaticamente.")
    else:
        print("\n❌ Falha na postagem do carrossel.")

if __name__ == "__main__":
    post_pantalona()
