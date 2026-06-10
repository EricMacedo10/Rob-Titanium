import os
import ftplib
import sys
from dotenv import load_dotenv

# Adiciona diretorio infra ao path para usar a logica de blindagem
sys.path.append(os.path.join(os.path.dirname(__file__), 'infra'))
from upload_logic import upload_to_hostinger

load_dotenv()

def sync_titanium_production():
    """
    DEPLOY FINAL + AI RADAR: Sincroniza a Boutique Titanium 
    com o sistema de Radar de Tendencias Inteligente.
    """
    print("============================================================")
    print("TITANIUM PRODUCTION DEPLOY v12.8 - RADAR READY")
    print("============================================================")

    ftp_host = os.getenv("FTP_HOST")
    ftp_user = os.getenv("FTP_USER")
    ftp_pass = os.getenv("FTP_PASS")

    if not all([ftp_host, ftp_user, ftp_pass]):
        print("[!] Erro: Credenciais FTP nao encontradas no .env")
        return

    # === TITANIUM NUCLEAR SHIELD (MANDATORY GATE) ===
    try:
        from infra.shield import apply_nuclear_shield
        if not apply_nuclear_shield():
            print("[!] Falha critica na blindagem dos dados. Abortando deploy.")
            return
    except Exception as e:
        print(f"[!] Erro ao carregar motor de blindagem: {e}")
        return

    # MODO FORCADO: PRODUCTION
    os.environ['ENV_MODE'] = 'PRODUCTION'

    # Lista de arquivos Core
    files_to_sync = [
        ("site/ads.txt", "ads.txt"),
        ("site/index.html", "index.html"),
        ("site/clear_cache_titanium.php", "clear_cache_titanium.php"),
        ("site/blog.html", "blog.html"),
        ("site/sobre.html", "sobre.html"),
        ("site/privacidade.html", "privacidade.html"),
        ("site/termos.html", "termos.html"),
        ("site/ai_reviews.json", "ai_reviews.json"),  # Radar de Tendencias
        ("site/track_clicks.php", "track_clicks.php"),
        ("site/js/app.js", "js/app.js"),
        ("site/css/style.css", "css/style.css"),
        ("site/favicon.ico", "favicon.ico"),
        ("site/specialist.json", "specialist.json"),  # Seleção da Especialista
        ("site/data.json", "data.json"),               # Feed de ofertas
        ("site/go.php", "go.php"),                     # Bridge Page (Segurança de Link)
        # === INSTAGRAM LINK PAGE (Vitrine para Bio do Instagram) ===
        ("site/instagram.html", "instagram.html"),         # NOVO: Página de links do Instagram
        ("site/instagram_posts.json", "instagram_posts.json"),  # NOVO: Feed de posts publicados
        # === BOUTIQUE ÍNTIMA (Vertical Sensual) ===
        ("site/sensual.html", "sensual.html"),
        ("site/js/app_sensual.js", "js/app_sensual.js"),
        ("site/data_sensual.json", "data_sensual.json"),
        ("site/specialist_sensual.json", "specialist_sensual.json"),
        ("site/ai_reviews_sensual.json", "ai_reviews_sensual.json"),
    ]


    # Adicionar dinamicamente todos os artigos da pasta blog
    blog_dir = 'site/blog'
    if os.path.exists(blog_dir):
        for article in os.listdir(blog_dir):
            if article.endswith('.html') or article.endswith('.json'):
                files_to_sync.append((f"site/blog/{article}", f"blog/{article}"))

    print(f"[Info] Iniciando Sincronizacao de {len(files_to_sync)} arquivos...")

    success_count = 0
    for local, remote in files_to_sync:
        if os.path.exists(local):
            print(f"\n>>> Sincronizando: {remote}")
            if upload_to_hostinger(local, ftp_host, ftp_user, ftp_pass, remote_path=remote):
                success_count += 1
        else:
            print(f"\n[!] Arquivo nao encontrado: {local}")

    print("\n" + "============================================================")
    print(f"RESULTADO: {success_count}/{len(files_to_sync)} arquivos em producao!")
    print(f"RADAR DE TENDENCIAS ATIVO: https://guiadodesconto.com.br")
    print("============================================================")

if __name__ == "__main__":
    sync_titanium_production()
