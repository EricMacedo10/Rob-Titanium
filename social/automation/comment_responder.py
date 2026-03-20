
import os
import sys
import json
import time
from datetime import datetime
from dotenv import load_dotenv

# Path setup
PROJECT_ROOT = r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium"
sys.path.insert(0, PROJECT_ROOT)

from social.core.instagram_client import InstagramClient

# Configuração de Gatilhos e Respostas
TRIGGERS = ["eu quero", "quero", "link", "valor", "preço", "eu quero o link"]

# Mapeamento de links (Pode ser automatizado no futuro)
OFFERT_DATA = {
    "pantalona": {
        "link": "https://produto.mercadolivre.com.br/MLB-5653965336-calca-pantalona-alfaiataria-feminina-cintura-alta-elastico-_JM?matt_tool=188269638&matt_source=guiadodesconto",
        "site": "https://guiadodesconto.com.br"
    },
    "default": {
        "link": "https://guiadodesconto.com.br",
        "site": "https://guiadodesconto.com.br"
    }
}

def run_comment_responder():
    load_dotenv(os.path.join(PROJECT_ROOT, ".env"))
    
    IG_TOKEN = os.getenv("IG_ACCESS_TOKEN")
    IG_BUSINESS_ID = os.getenv("IG_BUSINESS_ID")
    PAGE_ID = os.getenv("PAGE_ID", "1032000233318987")
    
    if not IG_TOKEN or not IG_BUSINESS_ID:
        print("❌ Erro: Credenciais do Instagram não configuradas.")
        return

    client = InstagramClient(IG_TOKEN, IG_BUSINESS_ID, page_id=PAGE_ID)
    
    # Arquivo de log para evitar respostas duplicadas
    log_dir = os.path.join(PROJECT_ROOT, "social", "postados")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "comment_responses.json")
    
    responded_comments = []
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            try:
                responded_comments = json.load(f)
            except:
                responded_comments = []

    print("\n" + "="*60)
    print("🤖 TITANIUM COMMENT RESPONDER - MONITORAMENTO ATIVO")
    print("="*60)

    # 1. Buscar posts recentes
    media_list = client.get_latest_media(limit=3)
    
    for media in media_list:
        media_id = media["id"]
        caption = media.get("caption", "").lower()
        print(f"\n🔍 Verificando post: {media_id} (Caption: {caption[:30]}...)")
        
        # Identificar qual produto é baseado na legenda
        product_key = "default"
        if "pantalona" in caption:
            product_key = "pantalona"
        elif "suporte" in caption:
            product_key = "suporte" # (Implementar link se necessário)

        # 2. Buscar comentários
        comments = client.get_comments(media_id)
        
        for comment in comments:
            comment_id = comment["id"]
            text = comment["text"].lower()
            user = comment.get("username", "usuário")
            
            # Pular se já responderam
            if comment_id in responded_comments:
                continue

            # 3. Verificar Gatilho
            triggered = any(trigger in text for trigger in TRIGGERS)
            
            if triggered:
                print(f"🎯 Gatilho detectado! Usuário: {user} | Comentário: '{text}'")
                
                # Preparar Mensagens
                offert = OFFERT_DATA.get(product_key, OFFERT_DATA["default"])
                
                # Resposta Pública no Comentário
                public_message = f"Olá, {user}! 🎁 Te enviei o link com todos os detalhes lá no seu Direct (Inbox)! Corre lá pra conferir. 🏃‍♀️💨"
                
                # Resposta Privada (DM)
                private_message = (
                    f"Olá, {user}! 🎁 Aqui está o link da oferta que você pediu:\n\n"
                    f"🔗 Produto: {offert['link']}\n\n"
                    "Espero que aproveite! Se quiser explorar outras opções incríveis "
                    f"com os melhores preços, visite nosso portal: {offert['site']} \n\n"
                    "Atenciosamente,\n"
                    "Equipe Robô Titanium 🛡️💎"
                )
                
                # 4. Enviar Resposta Pública
                print(f"💬 Respondendo publicamente para {user}...")
                resp_pub = client.post_public_reply(comment_id, public_message)
                if "id" in resp_pub or resp_pub.get("success"):
                     print(f"   L_ OK: Resposta Pública foi!")
                else:
                     print(f"   L_ ⚠️ Erro Pública: {resp_pub}")

                # 5. Enviar Resposta Privada (DM)
                print(f"📲 Enviando DM (Inbox) para {user}...")
                resp_priv = client.post_private_reply(comment_id, private_message)
                if "message_id" in resp_priv or "recipient_id" in resp_priv:
                     print(f"   L_ ✅ DM enviada com sucesso ao {user}!")
                else:
                     print(f"   L_ ❌ ERRO NA DM: {resp_priv}")
                
                # Independentemente de falha na primeira tentativa, marcamos
                # para não floodar os comentários do usuário caso rodem de novo
                responded_comments.append(comment_id)

            
    # Salvar log atualizado
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(responded_comments, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    run_comment_responder()
