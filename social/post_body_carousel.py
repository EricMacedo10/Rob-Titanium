import os
import time
import json
import requests
from dotenv import load_dotenv
from social.core.instagram_client import InstagramClient
from social.core.uploader import ResilientUploader
from infra.upload_logic import upload_to_hostinger

def post_body_carousel():
    load_dotenv()
    
    # 0. CONFIGURAÇÕES E CREDENCIAIS
    os.environ["ENV_MODE"] = "PRODUCTION" # Forçar produção para links limpos
    
    ig_token = os.getenv("IG_ACCESS_TOKEN")
    ig_business_id = os.getenv("IG_BUSINESS_ID")
    page_id = os.getenv("PAGE_ID")
    
    ftp_config = {
        "host": os.getenv("FTP_HOST"),
        "user": os.getenv("FTP_USER"),
        "pass": os.getenv("FTP_PASS")
    }
    
    fila_dir = r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium\social\fila"
    state_dir = r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium\state"
    os.makedirs(state_dir, exist_ok=True)
    
    # 1. ATUALIZAR OFERTAS.JSON NO SERVIDOR
    print("--- Sincronizando ofertas.json com o servidor Hostinger...")
    local_ofertas = r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium\social\ofertas.json"
    upload_to_hostinger(
        local_ofertas,
        ftp_config["host"],
        ftp_config["user"],
        ftp_config["pass"],
        "ofertas.json" # Sobe para a raiz
    )
    
    # 2. PREPARAR MÍDIAS (Slide 1:01, 2:vid, 3:02, 4:03, 5:04, 6:05)
    uploader = ResilientUploader(ftp_config=ftp_config)
    media_files = [
        {"file": "imagem_01.jpeg", "type": "IMAGE"},
        {"file": "video_01.mp4", "type": "VIDEO"},
        {"file": "imagem_02.jpeg", "type": "IMAGE"},
        {"file": "imagem_03.jpeg", "type": "IMAGE"},
        {"file": "imagem_04.jpeg", "type": "IMAGE"},
        {"file": "imagem_05.jpeg", "type": "IMAGE"}
    ]
    
    public_items = []
    ts = int(time.time())
    
    print(f"Iniciando upload de {len(media_files)} itens para o carrossel...")
    
    for item in media_files:
        filename = item["file"]
        local_path = os.path.join(fila_dir, filename)
        
        if not os.path.exists(local_path):
            print(f"❌ Erro: Arquivo {filename} não encontrado em {fila_dir}")
            return
            
        print(f"--- Processando {filename} ({item['type']})...")
        remote_name = f"body_post_{ts}_{filename}"
        
        # O robô prefere FTP para vídeos obrigatoriamente
        url = uploader.upload(local_path, remote_name)
        
        if url:
            public_items.append({"url": url, "type": item["type"]})
        else:
            print(f"❌ Falha crítica no upload de {filename}. Abortando.")
            return

    # 3. LEGENDA E HASHTAG
    caption = """✨ ELEGÂNCIA E CONFORTO: O Body que valoriza sua silhueta! 👗💎

Procurando a peça perfeita para o verão? Conheça o nosso Body com decote quadrado nas costas! Design moderno, tecido macio (viscose com elastano) e um caimento impecável. 

🔥 Por apenas **R$ 20,10** na Shopee! 🎁

✅ Versátil: Combina com jeans, saias ou shorts.
✅ Fresquinho: Ideal para os dias quentes.
✅ Estiloso: Detalhe costas nuas traz sofisticação premium.

💬 **Comente "QUERO"** que o nosso robô Titanium envia o link agora no seu direct! 🚀🦾

#ModaFeminina #ShopeeBrasil #Achadinhos #BodyFeminino #LookDoDia #LookShopee #body_costas_nuas"""

    # 4. POSTAGEM
    print("\nEnviando Carrossel Misto para o Instagram...")
    client = InstagramClient(ig_token, ig_business_id, page_id=page_id)
    post_data = client.post_carousel_with_id(public_items, caption)
    
    if post_data and "id" in post_data:
        post_id = post_data["id"]
        print(f"\n[SUCESSO] Carrossel publicado. ID: {post_id}")
        
        # 5. SALVAR ESTADO PARA O BOT DE COMENTÁRIOS
        # O link do produto está na hashtag #body_costas_nuas facilitada pelo bot PHP,
        # mas o robô Python também precisa saber para o DM direto.
        product_url = "https://shopee.com.br/product/1496791246/58252918685?exp_group=rollout&gads_t_sig=gqRjZGVrxHCFomtpsTE0MjUxOnRzc19zZGtfa2V5omt20QABpGFsZ2_SAAAAZKNkZWvAomN0xEAAAAAMRvS3L9OTXdZ5FJNxILig8p7lQ7pNpXYtdZAbsM8MQrkGmzJ0eOQRwaQfuYgAF9FAqYvxRTQ9oVrOjPOJqmNpcGhlcnRleHTEmQAAAAzwzTIaOjjbtYS9UN6vB6mst0qCZgB3PCzVLKBPk4XL39kg_qoDVaVUE7cHop-gRmISuDGscUnUeTRrCRk_V-J5RiKVgFMU2_nUeY1TNDCF0V1VEVZXpx472P5E6Ide6bStNjS-OYhKE-9I2MN7e_7jd_COBm2pqAgzsvPb6lloa57swSSRTz3Q1gU8Bv4S7--QXyzAMQ&mmp_pid=an_18318830863&uls_trackid=55ctfmgu00pn&utm_campaign=id_83V3N84q0f&utm_content=----&utm_medium=affiliates&utm_source=an_18318830863&utm_term=eqq7r1mgbgoq"
        
        state = {
            "post_id": post_id,
            "product_url": product_url,
            "hashtag": "#body_costas_nuas",
            "keyword": "QUERO"
        }
        
        state_path = os.path.join(state_dir, "body_active_post.json")
        with open(state_path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
        
        print(f"--- Estado salvo em {state_path}")
        print("--- Robô de DM pronto para ativação.")
        
    else:
        print("\n❌ Falha na postagem do carrossel.")

if __name__ == "__main__":
    post_body_carousel()
