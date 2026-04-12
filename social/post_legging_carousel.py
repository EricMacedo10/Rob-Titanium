import os
import time
from dotenv import load_dotenv
from social.core.instagram_client import InstagramClient
from social.core.uploader import ResilientUploader

def sync_ofertas(uploader):
    """Sincroniza o ofertas.json local com o servidor Hostinger"""
    local_path = r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium\social\ofertas.json"
    if os.path.exists(local_path):
        print("🔄 Sincronizando ofertas.json com o servidor...")
        # Upload para a raiz do servidor (onde o bot PHP procura)
        uploader.upload(local_path, "ofertas.json")
    else:
        print("⚠️ ofertas.json não encontrado para sincronização.")

def post_legging_carousel():
    load_dotenv()
    
    # Forçar PRODUÇÃO para garantir que os links e a postagem sejam reais
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
    
    # Sincronizar links antes de postar
    sync_ofertas(uploader)
    
    # Arquivos na fila
    fila_dir = r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium\social\fila"
    files = [f"legging_post_{i:02d}.jpg" for i in range(6)]
    
    public_urls = []
    
    print("\n🚀 Iniciando upload das 6 imagens do carrossel de Leggings...")
    
    timestamp = int(time.time())
    for filename in files:
        local_path = os.path.join(fila_dir, filename)
        if not os.path.exists(local_path):
            print(f"❌ Arquivo não encontrado: {local_path}")
            return
            
        print(f"--- Processando {filename}...")
        remote_name = f"legging_carousel_{timestamp}_{filename}"
        url = uploader.upload(local_path, remote_name)
        
        if url:
            public_urls.append(url)
        else:
            print(f"❌ Falha crítica no upload de {filename}. Abortando postagem.")
            return

    if len(public_urls) < 6:
        print("❌ Erro: Nem todas as imagens foram carregadas corretamente.")
        return

    # Legenda estratégica
    caption = """🔥 CONFORTO & ESTILO: A Legging que você não vai querer tirar! 🧘‍♀️💎

Seja para o treino pesado, yoga ou para o dia a dia, essa legging com cintura alta e bolsos funcionais é a escolha perfeita. 

✅ Cintura Alta: Modelagem que valoriza a silhueta.
✅ Bolsos Funcionais: Praticidade total para seu celular.
✅ Tecido Premium: Elasticidade e zero transparência.
✅ Versátil: Combina com tudo!

Disponível nos tamanhos P ao GG. 

💬 **Comente "QUERO"** ou "LINK" que eu te envio o link direto no direct agora! 🚀🦾

#Fitness #ModaFitness #TreinoFeminino #LeggingComBolso #CinturaAlta #AchadinhosAmazon #SaudeEBemEstar #leggingbolso"""

    print("\n📢 Enviando carrossel de Leggings para o Instagram...")
    success = client.post_carousel(public_urls, caption)
    
    if success:
        print("\n🏆 SUCESSO! O carrossel de Leggings está no ar.")
        # Salvar estado para o bot de comentário (opcional mas recomendado)
        state_file = r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium\state\legging_active_post.json"
        with open(state_file, "w") as f:
            json.dump({"post_id": success, "timestamp": timestamp}, f)
    else:
        print("\n❌ Falha na postagem do carrossel.")

if __name__ == "__main__":
    import json # Import extra para o dump do state
    post_legging_carousel()
