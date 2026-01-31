import os
import ftplib
from dotenv import load_dotenv

load_dotenv()

def sync_site():
    ftp_host = os.getenv("FTP_HOST")
    ftp_user = os.getenv("FTP_USER")
    ftp_pass = os.getenv("FTP_PASS")

    if not all([ftp_host, ftp_user, ftp_pass]):
        print("Erro: Credenciais de FTP não encontradas no .env")
        return

    # 1. Renomear arquivos localmente
    image_dir = "site/images"
    for filename in os.listdir(image_dir):
        if filename.startswith("banner_") and "_" in filename:
            # Ex: banner_tecnologia_amazon_1769812563304.png -> banner_tecnologia_amazon.png
            parts = filename.split("_")
            if len(parts) > 3: # banner + desc + desc + timestamp.png
                new_name = "_".join(parts[:-1]) + ".png"
                old_path = os.path.join(image_dir, filename)
                new_path = os.path.join(image_dir, new_name)
                
                # Se o novo nome já existe e é diferente, remove o antigo
                if os.path.exists(new_path) and old_path != new_path:
                    os.remove(new_path)
                
                print(f"Renomeando: {filename} -> {new_name}")
                os.rename(old_path, new_path)

    # 2. Upload para Hostinger
    files_to_upload = [
        ("site/index.html", "index.html"),
        ("site/js/app.js", "js/app.js"),
        ("site/css/style.css", "css/style.css"),
    ]
    
    # Adiciona todos os banners renomeados
    for filename in os.listdir(image_dir):
        if filename.startswith("banner_") and not any(char.isdigit() for char in filename.split(".")[0].split("_")[-1]):
             files_to_upload.append((os.path.join(image_dir, filename), f"images/{filename}"))

    print(f"🚀 Iniciando Sincronização v3.0 para {ftp_host}...")
    
    try:
        session = ftplib.FTP(ftp_host, ftp_user, ftp_pass, timeout=60)
        
        # Entrar na public_html ou usar a raiz como fallback
        base_dir = "/"
        paths_to_try = ["public_html", "domains/guiadodesconto.com.br/public_html", "www"]
        for p in paths_to_try:
            try:
                session.cwd(p)
                base_dir = session.pwd()
                print(f"✅ Diretório base definido: {base_dir}")
                break
            except:
                continue
        
        if base_dir == "/":
            session.cwd("/")
            print("✅ Usando a raiz (/) como diretório base.")

        for local_path, remote_path in files_to_upload:
            session.cwd(base_dir) # Sempre volta para a base
            print(f"📤 Subindo: {local_path} -> {remote_path}")
            
            # Garantir pasta remota
            if "/" in remote_path:
                folder = remote_path.split("/")[0]
                try:
                    session.cwd(folder)
                except:
                    print(f"📁 Criando pasta: {folder}")
                    session.mkd(folder)
                    session.cwd(folder)
                remote_file = remote_path.split("/")[-1]
            else:
                remote_file = remote_path

            with open(local_path, "rb") as f:
                result = session.storbinary(f"STOR {remote_file}", f)
                print(f"   📨 {result}")

        session.quit()
        print("✅ Sincronização v3.0 concluída com sucesso!")
    except Exception as e:
        print(f"❌ Erro na sincronização: {e}")

if __name__ == "__main__":
    sync_site()
