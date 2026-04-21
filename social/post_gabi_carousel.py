import os
import time
from dotenv import load_dotenv
import sys

# Adicionar o diretório raiz ao path para poder importar módulos do projeto
project_root = r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium"
if project_root not in sys.path:
    sys.path.append(project_root)

from social.core.instagram_client import InstagramClient
from social.core.uploader import ResilientUploader

def post_gabi_carousel():
    load_dotenv(os.path.join(project_root, ".env"))
    
    # Configurações do Instagram
    ig_token = os.getenv("IG_ACCESS_TOKEN")
    ig_business_id = os.getenv("IG_BUSINESS_ID")
    page_id = os.getenv("PAGE_ID")
    
    # Configurações FTP para o Uploader (necessário para a Graph API ter URLs públicas)
    ftp_config = {
        "host": os.getenv("FTP_HOST"),
        "user": os.getenv("FTP_USER"),
        "pass": os.getenv("FTP_PASS")
    }
    
    uploader = ResilientUploader(ftp_config=ftp_config)
    client = InstagramClient(ig_token, ig_business_id, page_id=page_id)
    
    # Arquivos na fila (específicos para o Conjunto Gabi)
    fila_dir = r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium\social\fila"
    files = [f"gabi_post_{i:02d}.jpg" for i in range(6)]
    
    public_urls = []
    
    print("[UP] Iniciando upload das 6 imagens do carrossel Gabi...")
    
    for filename in files:
        local_path = os.path.join(fila_dir, filename)
        if not os.path.exists(local_path):
            print(f"[!] Arquivo não encontrado: {local_path}")
            return
            
        print(f"--- Processando {filename}...")
        # Nome único no servidor FTP
        remote_name = f"gabi_carousel_{int(time.time())}_{filename}"
        url = uploader.upload(local_path, remote_name)
        
        if url:
            public_urls.append(url)
        else:
            print(f"[ERROR] Falha crítica no upload de {filename}. Abortando postagem.")
            return

    if len(public_urls) < 6:
        print("[ERROR] Erro: Nem todas as imagens foram carregadas corretamente.")
        return

    # Legenda estratégica
    caption = """✨ **CONJUNTO GABI: Elegância e Estilo em Alfaiataria!** 👗💎

O look perfeito para mulheres que amam unir sofisticação e conforto. Ideal para festas, trabalho ou aquele encontro especial! 🌟

🌸 **DETALHES QUE ENCANTAM:**
✅ Tecido Alfaiataria leve e confortável
✅ Modelagem moderna que valoriza a silhueta
✅ Conjunto versátil (Colete + Shorts)
✅ Perfeito para arrasar agora no final de ano!

💬 **Comente "QUERO"** que o nosso robô Titanium envia o link direto agora no seu direct! 🚀🦾

🛍️ Ou confira o link oficial Shopee: https://shopee.com.br/product/1553995251/23394445605

⚠️ *Imagens meramente ilustrativas geradas por Inteligência Artificial para demonstração de uso.*

#TecnologiaTitanium #ModaFeminina #ConjuntoGabi #AchadinhosShopee #LookDoDia #AlfaiatariaFeminina #EstiloTotal #LookShopee"""

    print("\n📢 Enviando carrossel Gabi para o Instagram...")
    success = client.post_carousel(public_urls, caption)
    
    if success:
        print("\n[OK] SUCESSO! O carrossel de moda Conjunto Gabi está no ar.")
        # Opcional: mover arquivos para 'postados' se desejar automação total
    else:
        print("\n[!] Falha na postagem do carrossel.")

if __name__ == "__main__":
    post_gabi_carousel()
