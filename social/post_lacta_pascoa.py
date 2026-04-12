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
from infra.upload_logic import upload_to_hostinger

def sync_ofertas(ftp_config):
    # Forçar modo PRODUCTION para que os arquivos subam para a raiz (ofertas.json)
    # e os links gerados não tenham o prefixo /teste/
    os.environ["ENV_MODE"] = "PRODUCTION"
    
    print("🔄 Sincronizando ofertas.json com o servidor Hostinger (MODO PRODUÇÃO)...")
    local_path = os.path.join(project_root, "social", "ofertas.json")
    # Forçar upload para a raiz (production) se quisermos que o robô de DM (bot_instagram.php) funcione,
    # caso contrário ele vai para /teste/ dependendo do ENV_MODE.
    # Mas como o post será real, o robô de DM também deve ser atualizado na raiz.
    
    # Temporariamente forçando PRODUCTION para esse upload específico se o usuário permitir, 
    # ou apenas seguindo o ENV_MODE.
    success = upload_to_hostinger(
        local_path,
        ftp_config["host"],
        ftp_config["user"],
        ftp_config["pass"],
        "ofertas.json"
    )
    if success:
        print("✅ ofertas.json sincronizado com sucesso!")
    else:
        print("❌ Falha ao sincronizar ofertas.json.")

def post_lacta():
    load_dotenv(os.path.join(project_root, ".env"))
    
    # Configurações do Post
    PRODUCT_URL = "https://www.amazon.com.br/stores/page/38FC855B-27C6-4079-BC5F-15B939EC3EC7?_encoding=UTF8&channel=patroc%C3%ADnioabril&tag=guiadodesco00-20"
    KEYWORD = "QUERO"
    HASHTAG_DM = "#pascoa_lacta"
    
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
    
    # Sincronizar ofertas.json ANTES da postagem
    sync_ofertas(ftp_config)
    
    fila_dir = os.path.join(project_root, "social", "fila")
    image_filename = "loja_lacta.jpeg"
    local_path = os.path.join(fila_dir, image_filename)
    
    if not os.path.exists(local_path):
        print(f"❌ Arquivo não encontrado: {local_path}")
        return

    print(f"🚀 Iniciando postagem da Lacta...")
    
    # Upload da imagem
    remote_name = f"lacta_{int(time.time())}.jpg"
    print(f"--- Fazendo upload de {image_filename}...")
    public_url = uploader.upload(local_path, remote_name)
    
    if not public_url:
        print("❌ Erro: Falha no upload da imagem.")
        return

    caption = f"""🐰✨ PÁSCOA ANTECIPADA: Garanta o presente perfeito com a @lacta no precinho! 🍫🎁\n\nA Páscoa está chegando e você não precisa esperar a última hora para garantir os seus chocolates favoritos. De caixas de bombons a ovos clássicos, a Lacta tem tudo para deixar seu feriado mais doce! ☁️💙\n\n🔥 DESTAQUES:\n✅ Caixa de Bombom Especial: Perfeita para presentear e agradecer.\n✅ Clássicos Irresistíveis: Ouro Branco, Sonho de Valsa, Laka e Diamante Negro!\n✅ Praticidade Amazon: Entrega rápida e segura no conforto da sua casa.\n\n🎁 Uma doce lembrança para quem você ama (ou para você mesmo, afinal, você merece!)\n\n💬 Quer o link direto da Loja Lacta na Amazon?\nComente "{KEYWORD}" que o nosso Robô Titanium envia o link agora mesmo no seu direct! 🤖🚀\n\n#RoboTitanium #Pascoa2024 #Lacta #Chocolates #OuroBranco #SonhoDeValsa #OfertasPascoa #AmazonBrasil #AchadinhosAmazon #PascoaLacta {HASHTAG_DM}"""

    print(f"\n📢 Enviando postagem para o Instagram...")
    success = client.post_image(public_url, caption)
    
    if success:
        print("\n🏆 SUCESSO! A postagem da Lacta está no air.")
        
        print("\n🔍 Buscando o ID da postagem para o Bot de Comentários...")
        time.sleep(10)  # Aguardar alguns segundos para a API refletir a criação
        latest_media = client.get_latest_media(limit=1)
        if latest_media and len(latest_media) > 0:
            post_id = latest_media[0].get("id")
            print(f"✅ ID da postagem encontrado: {post_id}")
            
            # Salvar no state para o bot de comentário
            state_dir = os.path.join(project_root, "state")
            os.makedirs(state_dir, exist_ok=True)
            state_file = os.path.join(state_dir, "lacta_active_post.json")
            
            state_data = {
                "post_id": post_id,
                "product_url": PRODUCT_URL,
                "keyword": KEYWORD,
                "timestamp": time.time()
            }
            
            with open(state_file, "w", encoding="utf-8") as f:
                json.dump(state_data, f, indent=4)
                
            print(f"✅ Arquivo de state salvo em: {state_file}")
            
            # Criar script de bot de comentário específico para este post
            create_comment_bot(post_id, PRODUCT_URL, KEYWORD)
            
            print(f"🤖 Inicie o bot de monitoramento: python social/bot_comentario_lacta.py")
        else:
            print("⚠️ Não foi possível obter o ID da postagem mais recente para configurar o Bot automaticamente.")
    else:
        print("\n❌ Falha na postagem.")

def create_comment_bot(post_id, product_url, keyword):
    bot_template_path = os.path.join(project_root, "social", "bot_comentario_pantalona.py")
    if not os.path.exists(bot_template_path):
        return
        
    with open(bot_template_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Substituições básicas para criar um bot dedicado
    new_content = content.replace("pantalona_active_post.json", "lacta_active_post.json")
    new_content = new_content.replace("pantalona_replied_users.json", "lacta_replied_users.json")
    
    bot_script_path = os.path.join(project_root, "social", "bot_comentario_lacta.py")
    with open(bot_script_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print(f"✅ Bot de comentário criado em: {bot_script_path}")

if __name__ == "__main__":
    post_lacta()
