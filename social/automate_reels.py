import os
import json
import time
import ftplib
import uuid
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from social.core.video_generator import VideoGenerator
from social.core.instagram_client import InstagramClient
from scraper.datafeed_shopee import get_datafeed_products

QUEUE_DIR = os.path.join(os.path.dirname(__file__), "fila")
POSTED_DIR = os.path.join(os.path.dirname(__file__), "postados")
os.makedirs(QUEUE_DIR, exist_ok=True)
os.makedirs(POSTED_DIR, exist_ok=True)

FASHION_BEAUTY_KEYWORDS = [
    "vestido", "saia", "blusa", "cropped", "body", "macacão", "macaquinho", 
    "calça pantalona", "lingerie", "maquiagem", "batom", "base", "sérum", 
    "skincare", "salto", "sandália", "bolsa", "brinco", "colar", "corset"
]

def get_posted_titles():
    titles = set()
    for directory in [POSTED_DIR, QUEUE_DIR]:
        if os.path.exists(directory):
            for f in os.listdir(directory):
                if f.endswith('.json'):
                    try:
                        with open(os.path.join(directory, f), 'r', encoding='utf-8') as j:
                            data = json.load(j)
                            if 'title' in data:
                                titles.add(data['title'].lower().strip())
                    except: continue
    return titles



def run_automation():
    print("="*60)
    print("🎬 TITANIUM SOCIAL: MÁQUINA DE REELS/STORIES (FASHION) 🎬")
    print("="*60)
    load_dotenv()
    
    posted_titles = get_posted_titles()
    
    print("[1] Buscando produtos na base 100K...")
    raw_products = get_datafeed_products(max_items=3000)
    
    chosen_product = None
    for p in raw_products:
        title_lower = p['titulo'].lower().strip()
        
        # Filtro estrito de Moda e Beleza
        is_fashion = any(kw in title_lower for kw in FASHION_BEAUTY_KEYWORDS)
        if not is_fashion:
            continue
            
        if title_lower not in posted_titles:
            chosen_product = p
            break
            
    if not chosen_product:
        print("❌ Nenhum produto de moda/beleza novo encontrado no momento.")
        sys.exit(1)
        
    print(f"✅ Produto selecionado: {chosen_product['titulo']} (R$ {chosen_product['preco']})")
    
    print("🔍 Buscando imagem em alta resolução na API da Shopee...")
    from core.shopee_api import get_shopee_image_api
    image_url = get_shopee_image_api(chosen_product['titulo'])
    if not image_url:
        print("❌ Não foi possível encontrar a imagem para este produto.")
        sys.exit(1)
    
    # Gerando Vídeos
    gen = VideoGenerator()
    
    safe_id = str(uuid.uuid4())[:8]
    print("\n[2] Gerando formato REEL...")
    reel_path = gen.generate_video(
        product_url=image_url,
        price=str(chosen_product['preco']),
        store_type="shopee",
        output_filename=f"reel_{safe_id}.mp4",
        video_type="reel"
    )
    
    print("\n[3] Gerando formato STORY...")
    story_path = gen.generate_video(
        product_url=image_url,
        price=str(chosen_product['preco']),
        store_type="shopee",
        output_filename=f"story_{safe_id}.mp4",
        video_type="story"
    )
    
    # Upload via Cloud (GitHub Actions bloqueia FTP — força CDN diretamente)
    print("\n[4] Enviando arquivos via Cloud CDN (GitHub Actions bloqueia FTP)...")
    from social.core.uploader import ResilientUploader
    uploader = ResilientUploader(
        ftp_config={
            "host": os.getenv("FTP_HOST"),
            "user": os.getenv("FTP_USER"),
            "pass": os.getenv("FTP_PASS")
        },
        imgbb_api_key=os.getenv("IMGBB_API_KEY")  # necessário para o fallback cloud
    )
    # force_cloud=True: pula FTP (bloqueado no Actions) e vai direto para CDN
    reel_url = uploader.upload(reel_path, f"reel_{safe_id}.mp4", force_cloud=True)
    story_url = uploader.upload(story_path, f"story_{safe_id}.mp4", force_cloud=True)
    
    if not reel_url or not story_url:
        print("❌ Falha crítica no upload das mídias para a CDN. Abortando.")
        sys.exit(1)
    
    print("\n⏳ Aguardando propagação CDN...")
    time.sleep(10)
    
    # Postagem
    print("\n[5] Conectando ao Instagram API...")
    client = InstagramClient(
        access_token=os.getenv("IG_ACCESS_TOKEN"),
        business_id=os.getenv("IG_BUSINESS_ID"),
        page_id=os.getenv("PAGE_ID")
    )
    
    price_formatted = f"{float(chosen_product['preco']):.2f}".replace('.', ',')
    affiliate_link = chosen_product['link_afiliado'] if chosen_product.get('link_afiliado') else chosen_product['url_produto']
    hashtag_id = f"#titanium_{safe_id}"
    
    caption = f"{chosen_product['titulo']} ✨\n\nPor apenas R$ {price_formatted}!\n\n🔗 Link do Produto: {affiliate_link}\n\nComente QUERO para receber o link VIP no seu direct! 🛍️\n\n#ModaFeminina #ShopeeBR #LookDoDia #TitaniumBoutique {hashtag_id}"
    
    # Atualiza o ofertas.json — o git-auto-commit ao final do workflow commita o arquivo
    # e o bot_instagram.php busca a versão mais recente direto do GitHub Raw (sem FTP).
    ofertas_path = os.path.join(os.path.dirname(__file__), "ofertas.json")
    try:
        if os.path.exists(ofertas_path):
            with open(ofertas_path, 'r', encoding='utf-8') as f:
                ofertas = json.load(f)
        else:
            ofertas = {}
            
        ofertas[hashtag_id] = affiliate_link
        # Salva também como #latest_story para o bot usar nas respostas de Stories
        ofertas["#latest_story"] = affiliate_link
        
        with open(ofertas_path, 'w', encoding='utf-8') as f:
            json.dump(ofertas, f, indent=4, ensure_ascii=False)
        
        print(f"✅ ofertas.json atualizado localmente com {hashtag_id}. Será commitado pelo workflow.")
    except Exception as e:
        print(f"⚠️ Aviso: Não foi possível atualizar ofertas.json: {e}")


    print("\n🎬 Disparando REEL...")
    client.post_reels(video_url=reel_url, caption=caption)
    
    print("\n🎬 Disparando STORY...")
    client.post_story(media_url=story_url, is_video=True)
    
    # Marca como postado
    post_data = {
        "id": chosen_product['id_interno'],
        "title": chosen_product['titulo'],
        "timestamp": time.time(),
        "type": "video_reel_story"
    }
    with open(os.path.join(POSTED_DIR, f"{safe_id}.json"), 'w', encoding='utf-8') as f:
        json.dump(post_data, f, indent=4)
        
    print("\n🏆 Automação concluída com sucesso! Produto marcado como postado.")

if __name__ == "__main__":
    run_automation()
