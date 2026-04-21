"""
📅 Post Scheduled Feed - Sistema de Postagens Agendadas
Lê o manifesto schedule.json e posta a imagem do dia no Feed do Instagram.
Blindagem: texto gerado com base nos metadados (loja, categoria, tema).
Anti-duplicata: verifica social/postados/ antes de publicar.
"""
import os
import sys
import json
import time
import shutil
import requests
from PIL import Image
import io
from datetime import datetime
from dotenv import load_dotenv

# Mapeamento de lojas para emojis e nomes de exibição
STORE_CONFIG = {
    "shopee": {
        "nome": "Shopee",
        "emoji": "🟠",
        "icon": "🛒",
        "cor": "laranja",
        "hashtags": ["#Shopee", "#ShopeeOfertas", "#ShopeeCarnaval", "#CupomShopee", "#FreteGrátis"]
    },
    "amazon": {
        "nome": "Amazon",
        "emoji": "📦",
        "icon": "🔥",
        "cor": "laranja",
        "hashtags": ["#Amazon", "#AmazonBrasil", "#AmazonOfertas", "#PrimeDay", "#AmazonCarnaval"]
    },
    "mercadolivre": {
        "nome": "Mercado Livre",
        "emoji": "🟡",
        "icon": "🤝",
        "cor": "amarelo",
        "hashtags": ["#MercadoLivre", "#MeLi", "#MercadoLivreOfertas", "#FreteGrátisMeLi", "#MLCarnaval"]
    }
}

CATEGORY_CONFIG = {
    "tecnologia": {
        "emoji": "💻",
        "hashtags": ["#Tecnologia", "#Tech", "#Gadgets", "#Eletrônicos"]
    },
    "beleza": {
        "emoji": "💄",
        "hashtags": ["#Beleza", "#CuidadosPessoais", "#Maquiagem", "#SkinCare"]
    },
    "casa": {
        "emoji": "🏠",
        "hashtags": ["#Casa", "#CasaECozinha", "#Decoração", "#Utilidades"]
    },
    "moda": {
        "emoji": "👗",
        "hashtags": ["#Moda", "#Fashion", "#Acessórios", "#Estilo"]
    },
    "esportes": {
        "emoji": "💪",
        "hashtags": ["#Esportes", "#Fitness", "#Treino", "#VidaSaudável"]
    },
    "volta-aulas": {
        "emoji": "🎒",
        "hashtags": ["#VoltaÀsAulas", "#Escolar", "#Material", "#Estudos"]
    },
    "automotivo": {
        "emoji": "🚗",
        "hashtags": ["#Automotivo", "#Carro", "#Acessórios", "#Auto"]
    },
    "games": {
        "emoji": "🎮",
        "hashtags": ["#Games", "#Gamer", "#Jogos", "#Setup"]
    }
}

def gerar_legenda(entry):
    """
    Gera legenda com emojis e hashtags baseada nos metadados do manifesto.
    BLINDAGEM: Nunca adivinha — usa apenas o que está no schedule.json.
    """
    loja = entry["loja"].lower()
    categoria = entry["categoria"].lower()
    tema = entry["tema"]
    
    store = STORE_CONFIG.get(loja, STORE_CONFIG["amazon"])
    cat = CATEGORY_CONFIG.get(categoria, {"emoji": "🔥", "hashtags": ["#Ofertas"]})
    
    # Legenda dinâmica baseada nos metadados
    caption = (
        f"🎭🔥 {tema.upper()} 🔥🎭\n\n"
        f"{store['emoji']} Ofertas imperdíveis na {store['nome']}! {cat['emoji']}\n\n"
        f"Não perca essa oportunidade de economizar com segurança! "
        f"Produtos selecionados com os melhores preços do mercado. 💎\n\n"
        f"⏰ Corre que é por tempo limitado!\n"
        f"👉 Acesse o link na bio e garanta sua oferta! 🎯\n\n"
    )
    
    # Hashtags: gerais + loja + categoria (sem duplicatas)
    hashtags_gerais = [
        "#Carnaval", "#Carnaval2026", "#Ofertas", "#Desconto",
        "#Economia", "#GuiaDoDesconto", "#OfertaCerta",
        "#ComprasOnline", "#MelhorPreço", "#Promoção"
    ]
    
    all_hashtags = hashtags_gerais + store["hashtags"] + cat["hashtags"]
    # Remover duplicatas mantendo ordem
    seen = set()
    unique_hashtags = []
    for h in all_hashtags:
        if h.lower() not in seen:
            seen.add(h.lower())
            unique_hashtags.append(h)
    
    caption += " ".join(unique_hashtags[:25])  # Limite de 30, usando 25 para segurança
    
    return caption


def run_scheduled_post():
    load_dotenv()
    
    IG_TOKEN = os.getenv("IG_ACCESS_TOKEN")
    IG_BUSINESS_ID = os.getenv("IG_BUSINESS_ID")
    ENV_MODE = os.getenv("ENV_MODE", "STAGING").upper()
    
    print("\n" + "=" * 60)
    print("[POSTAGEM] POSTAGEM AGENDADA - FEED DO INSTAGRAM")
    print("=" * 60)
    
    # 1. Obter data de hoje (BRT)
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"[DATA] Data atual: {today}")
    
    # 2. Ler manifesto
    base_proj = os.getcwd()
    fila_dir = os.path.join(base_proj, "social", "fila")
    postados_dir = os.path.join(base_proj, "social", "postados")
    schedule_path = os.path.join(fila_dir, "schedule.json")
    
    if not os.path.exists(schedule_path):
        print("[!] Erro: schedule.json não encontrado em social/fila/")
        sys.exit(1)
    
    with open(schedule_path, "r", encoding="utf-8") as f:
        schedule = json.load(f)
    
    print(f"[INFO] Manifesto carregado: {len(schedule)} entradas")
    
    # 3. Procurar entrada para hoje
    entry_hoje = None
    for entry in schedule:
        if entry["data"] == today:
            entry_hoje = entry
            break
    
    if not entry_hoje:
        print(f"[SKIP] Nenhuma postagem agendada para {today}. Saindo.")
        sys.exit(0)
    
    print(f"\n[TARGET] Postagem encontrada para hoje:")
    print(f"   Imagem:    {entry_hoje['imagem']}")
    print(f"   Loja:      {entry_hoje['loja']}")
    print(f"   Categoria: {entry_hoje['categoria']}")
    print(f"   Tema:      {entry_hoje['tema']}")
    
    # 4. Validação de campos obrigatórios (Fail-Safe)
    campos_obrigatorios = ["data", "imagem", "loja", "categoria", "tema"]
    for campo in campos_obrigatorios:
        if not entry_hoje.get(campo):
            print(f"[ERROR] ERRO CRÍTICO: Campo '{campo}' vazio no manifesto. Recusando postagem.")
            sys.exit(1)
    
    # 5. Verificar se a imagem existe (Blindagem contra erros de encoding/casing)
    arquivos_disponiveis = os.listdir(fila_dir)
    imagem_file = next((f for f in arquivos_disponiveis if f.lower() == entry_hoje["imagem"].lower()), None)
    
    if not imagem_file:
        print(f"[ERROR] Erro: Imagem '{entry_hoje['imagem']}' não encontrada em {fila_dir}/")
        print(f"📂 Arquivos disponíveis: {arquivos_disponiveis}")
        sys.exit(1)
    
    imagem_path = os.path.join(fila_dir, imagem_file)
    print(f"[OK] Imagem encontrada: {imagem_path}")
    
    # 6. Anti-duplicata: verificar se já postou hoje
    os.makedirs(postados_dir, exist_ok=True)
    postados_arquivos = os.listdir(postados_dir)
    for arquivo in postados_arquivos:
        if arquivo.startswith(today):
            print(f"[!] DUPLICATA DETECTADA: '{arquivo}' já existe em postados/")
            print("[SKIP] Cancelando postagem para evitar duplicata.")
            sys.exit(0)
    
    # 7. Gerar legenda
    caption = gerar_legenda(entry_hoje)
    print(f"\n📝 Legenda gerada ({len(caption)} caracteres):")
    print("-" * 40)
    print(caption)
    print("-" * 40)
    
    # 8. Verificar modo
    if ENV_MODE != "PRODUCTION":
        print(f"\n[TEST] MODO {ENV_MODE}: Simulação encerrada com sucesso.")
        print("Para postar, defina ENV_MODE=PRODUCTION no .env")
        return True
    
    # 9. Upload da imagem
    print("\n☁️ Enviando imagem para a nuvem...")
    
    from social.core.uploader import ResilientUploader
    uploader = ResilientUploader(
        ftp_config={
            "host": os.getenv("FTP_HOST"),
            "user": os.getenv("FTP_USER"),
            "pass": os.getenv("FTP_PASS")
        },
        imgbb_api_key=os.getenv("IMGBB_API_KEY")
    )
    
    # --- Garantir formato JPEG e Upload resiliente ---
    remote_name = f"scheduled_{today}_{int(time.time())}.jpg"
    temp_jpg_path = os.path.join(fila_dir, f"temp_upload_{int(time.time())}.jpg")
    
    try:
        # Converter para RGB/JPEG usando PIL (garante compatibilidade máxima)
        print(f"🔄 Preparando {entry_hoje['imagem']} para upload (JPEG Conversion)...")
        with Image.open(imagem_path) as img:
            rgb_img = img.convert('RGB')
            temp_buffer = io.BytesIO()
            rgb_img.save(temp_buffer, format="JPEG", quality=95)
            temp_buffer.seek(0)
            
            with open(temp_jpg_path, "wb") as f:
                f.write(temp_buffer.read())
            
            # Upload usando Hostinger/ImgBB (uploader agora faz verificação Meta automática)
            public_url = uploader.upload(temp_jpg_path, remote_name, force_cloud=False)
            print(f"🔗 URL Pública gerada: {public_url}")
            if uploader.provider_used:
                print(f"📡 Provedor utilizado: {uploader.provider_used}")
    except Exception as e:
        print(f"[ERROR] Erro no processamento da imagem: {e}")
        # Limpar temp antes de sair
        if os.path.exists(temp_jpg_path):
            os.remove(temp_jpg_path)
        sys.exit(1)
    
    if not public_url:
        print("[ERROR] Falha no upload da imagem. Abortando.")
        if os.path.exists(temp_jpg_path):
            os.remove(temp_jpg_path)
        sys.exit(1)
    
    # 10. Publicar no Feed com RETRY + FALLBACK automático
    print("📲 Publicando no Feed do Instagram...")
    
    base_url = f"https://graph.facebook.com/v21.0/{IG_BUSINESS_ID}"
    
    def _try_create_container(image_url):
        """Tenta criar container no Instagram. Retorna (data_dict, success_bool)."""
        resp = requests.post(f"{base_url}/media", data={
            "image_url": image_url,
            "caption": caption,
            "access_token": IG_TOKEN
        })
        data = resp.json()
        return data, "id" in data
    
    # Tentativa 1: URL principal (FTP ou ImgBB, dependendo do upload)
    container_data, success = _try_create_container(public_url)
    
    # BLINDAGEM: Se falhar com erro 9004 (Meta não conseguiu baixar), retry com ImgBB
    if not success:
        error_code = container_data.get("error", {}).get("code")
        if error_code == 9004 and uploader.provider_used and "ImgBB" not in uploader.provider_used:
            print(f"⚠️ Erro 9004 detectado com URL do Hostinger — ativando fallback ImgBB...")
            fallback_url = uploader.upload(temp_jpg_path, remote_name, force_cloud=True)
            if fallback_url:
                print(f"🔗 URL Fallback (ImgBB): {fallback_url}")
                container_data, success = _try_create_container(fallback_url)
                if success:
                    public_url = fallback_url
                    print(f"✅ Fallback ImgBB funcionou!")
    
    # Limpar arquivo temporário (seguro pois já fez upload)
    if os.path.exists(temp_jpg_path):
        os.remove(temp_jpg_path)
    
    if not success:
        print(f"❌ Erro ao criar container: {container_data}")
        sys.exit(1)
    
    creation_id = container_data["id"]
    print(f"✅ Container criado: {creation_id}")
    
    # Aguardar 5 segundos (imagens processam rápido, sem polling)
    print("⏳ Aguardando processamento...")
    time.sleep(5)
    
    # Publicar
    publish_resp = requests.post(f"{base_url}/media_publish", data={
        "creation_id": creation_id,
        "access_token": IG_TOKEN
    })
    publish_data = publish_resp.json()
    
    if "id" not in publish_data:
        print(f"[!] Erro na publicação: {publish_data}")
        sys.exit(1)
    
    post_id = publish_data["id"]
    print(f"\n[WIN] POST PUBLICADO COM SUCESSO! (Post ID: {post_id})")
    print(f"📡 Provedor final: {uploader.provider_used}")
    
    # 11. Arquivar imagem (Anti-duplicata e Blindagem)
    # Se o nome original já começar com a data (ex: 2026-02-13_...), não duplicar o prefixo
    if entry_hoje['imagem'].startswith(today):
        dest_name = entry_hoje['imagem']
    else:
        dest_name = f"{today}_{entry_hoje['imagem']}"
        
    dest_path = os.path.join(postados_dir, dest_name)
    
    print(f"[OK] Movendo arquivo para postados: {dest_name}")
    shutil.move(imagem_path, dest_path)
    print(f"[OK] Arquivamento concluído.")
    
    # 12. Log de sucesso
    log_entry = {
        "data": today,
        "post_id": post_id,
        "imagem": entry_hoje["imagem"],
        "loja": entry_hoje["loja"],
        "categoria": entry_hoje["categoria"],
        "tema": entry_hoje["tema"],
        "timestamp": datetime.now().isoformat()
    }
    
    log_path = os.path.join(postados_dir, "post_log.json")
    logs = []
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            logs = json.load(f)
    logs.append(log_entry)
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)
    
    print(f"[DONE] Log salvo em {log_path}")
    print("\n[OK] EXECUÇÃO CONCLUÍDA COM SUCESSO!")
    return True


if __name__ == "__main__":
    run_scheduled_post()
