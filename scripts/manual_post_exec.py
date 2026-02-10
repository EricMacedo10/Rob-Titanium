import os
from dotenv import load_dotenv
from social.instagram_client import InstagramClient
from scraper.upload import upload_to_hostinger

def perform_manual_post():
    load_dotenv()
    
    # Configurações
    ig_token = os.getenv("IG_ACCESS_TOKEN")
    ig_business_id = os.getenv("IG_BUSINESS_ID")
    ftp_host = os.getenv("FTP_HOST")
    ftp_user = os.getenv("FTP_USER")
    ftp_pass = os.getenv("FTP_PASS")
    
    local_image = r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium\site\images\promo-instagram-family.png"
    remote_name = "social/primeiro-post-titanium.png"
    public_url = f"https://guiadodesconto.com.br/{remote_name}"
    
    caption = """Cansado de navegar por horas e ainda ter a dúvida se encontrou o melhor preço? Conheça a Tecnologia Titanium! 💎🦾

Mais do que um site de ofertas, somos uma curadoria inteligente. Unimos nossa paixão por tecnologia ao poder de um robô de elite que monitora a internet 24h por dia para garantir a sua economia. 🕵️‍♂️✨

Por que o Guia do Desconto é o seu parceiro ideal? ✅ Varredura Especializada: Análise em tempo real da Amazon, Mercado Livre e Shopee. ✅ Inteligência em Cupons: Identificamos oportunidades de desconto exclusivas. 🎫🔥 ✅ Navegação Segura: Você acessa o preço real e finaliza sua compra direto na loja oficial. ✅ Selo de Qualidade: Cada item passa pelo olhar atento da Família Titanium.

A tecnologia trabalha para você: Nossa inteligência automatiza toda a busca para que você encontre, com total praticidade no seu smartphone, apenas as oportunidades mais valiosas e selecionadas do mercado. 📱💎

O conforto de saber que você está comprando com inteligência está a apenas um clique de distância.

🔗 VISITE O LINK NA BIO: 👉 guiadodesconto.com.br

Economize tempo. Maximize seu dinheiro. Experimente a Tecnologia Titanium. 🦾🔥

#GuiaDoDesconto #TecnologiaTitanium #InteligenciaEmCompras #ConsumoConsciente #OfertasPremium #AmazonBrasil #MercadoLivre #Shopee #E-commerceBrasil #EconomiaReal"""

    print("🚀 Iniciando postagem manual estratégica...")
    
    # 1. Upload para o servidor (Ponte)
    print(f"📤 Enviando imagem para o servidor: {public_url}")
    success_upload = upload_to_hostinger(
        local_image, 
        ftp_host, 
        ftp_user, 
        ftp_pass, 
        remote_name
    )
    
    if not success_upload:
        print("❌ Erro ao subir imagem para o FTP.")
        return

    # 2. Postar no Instagram
    print("📢 Comunicando com a API do Instagram...")
    ig_client = InstagramClient(ig_token, ig_business_id)
    success_post = ig_client.post_image(public_url, caption)
    
    if success_post:
        print("🏆 SUCESSO! O post está no ar.")
    else:
        print("❌ Falha na postagem oficial.")

if __name__ == "__main__":
    perform_manual_post()
