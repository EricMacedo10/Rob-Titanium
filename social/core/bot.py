import time
import random
import sys
import shutil
import os
import json
import re
from datetime import datetime
from social.core.image_generator import ImageGenerator
from social.core.instagram_client import InstagramClient
from social.core.copywriter import Copywriter
from social.core.uploader import ResilientUploader
from moviepy import ImageClip
from infra.upload_logic import upload_to_hostinger
from dotenv import load_dotenv

load_dotenv()

class SocialBot:
    """
    Orquestrador do Robô Titanium para Redes Sociais.
    """
    def __init__(self, data_path="site/data.json", assets_path="site/images"):
        self.data_path = data_path
        self.gen = ImageGenerator(assets_path)
        self.copywriter = Copywriter()
        
        # Modo de Segurança (Staging)
        self.env_mode = os.getenv('ENV_MODE', 'STAGING').upper()
        if self.env_mode == "STAGING":
            print("🧪 AMBIENTE DE STAGING ATIVADO: Postagens reais bloqueadas.")

        # Configurações de FTP
        self.ftp_config = {
            "host": os.getenv("FTP_HOST"),
            "user": os.getenv("FTP_USER"),
            "pass": os.getenv("FTP_PASS")
        }
        
        # Inicializa Orquestrador de Upload
        self.uploader = ResilientUploader(
            ftp_config=self.ftp_config,
            imgbb_api_key=os.getenv("IMGBB_API_KEY")
        )
        self.instagram = None
        self.max_carousel_size = 10 # Limite da Meta API

    def load_offers(self):
        with open(self.data_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def select_best_offers(self, count=3):
        offers = self.load_offers()
        # Requisito de Compliance: Filtrar apenas ofertas com imagem válida
        valid_offers = [o for o in offers if o.get('image') and str(o.get('image')).startswith('http')]
        
        # Prioriza ofertas com maior desconto
        sorted_offers = sorted(valid_offers, key=lambda x: x.get('discount', 0), reverse=True)
        return sorted_offers[:count]

    def get_scheduled_store(self):
        """
        Define a loja baseada na política 100% Shopee Exclusive.
        """
        return "shopee"

    def run_daily_cycle(self, ig_token=None, ig_business_id=None, force_store=None):
        """
        Orquestra a postagem PRIORIZANDO a fila de curadoria.
        Agora suporta CARROSSEL AUTOMÁTICO de até 10 itens.
        """
        print("\n" + "="*60)
        print("🤖 INICIANDO TITANIUM SOCIAL BOT - MODO POST ÚNICO (v2.2.0)")
        print("="*60)
        
        from social.utils.video_utils import image_to_video

        # Configuração do Cliente Instagram
        if self.env_mode == "STAGING":
            print("🧪 MODO STAGING: Simulação de postagem ativa.")
            self.instagram = None
        elif ig_token and ig_business_id:
            self.instagram = InstagramClient(ig_token, ig_business_id)
        else:
            print("⚠️ Sem credenciais! Operando em modo de visualização local.")
            self.instagram = None

        fila_dir = "social/fila"
        postados_dir = "social/postados"
        temp_dir = "social/temp_videos"
        formatos_validos = ('.png', '.jpg', '.jpeg', '.mp4', '.mov')
        arquivos_fila = sorted([f for f in os.listdir(fila_dir) if f.lower().endswith(formatos_validos)])
        
        if not arquivos_fila:
            # Fallback para Banner (mantem logica atual simplificada)
            print("📭 Fila vazia. Iniciando modo fallback (Banners de Categoria)...")
            self._run_fallback_cycle(force_store)
            return

        # --- NOVA LÓGICA DE AGRUPAMENTO (CARROSSEL) ---
        # Pegamos o primeiro item para definir o contexto (loja/categoria)
        # e então tentamos agrupar itens similares que estejam na fila.
        # Filtramos apenas arquivos que possuem o respectivo .json (Evita postagens sem link)
        arquivos_validos = []
        for f in arquivos_fila:
            base = os.path.splitext(f)[0]
            if os.path.exists(os.path.join(fila_dir, f"{base}.json")):
                arquivos_validos.append(f)
        
        if not arquivos_validos:
            print("⚠️ Fila contém arquivos, mas nenhum possui metadata (.json). Abortando para evitar erro de link.")
            return

        target_files = arquivos_validos[:1]  # Modo Post Único: processa 1 por ciclo
        print(f"📂 Encontrado(s) {len(arquivos_validos)} arquivo(s) válidos. Selecionando 1 para postagem...")
        
        media_to_upload = []
        combined_captions = []
        full_paths = []
        temp_video_paths = []  # Rastrear vídeos temporários para limpeza
        
        store = "shopee" # Default
        category = "ofertas"

        # Garantir diretório temporário para vídeos convertidos
        os.makedirs(temp_dir, exist_ok=True)

        product_hashtags = []
        for i, filename in enumerate(target_files):
            local_path = os.path.join(fila_dir, filename)
            full_paths.append(local_path)
            is_image = filename.lower().endswith(('.png', '.jpg', '.jpeg'))
            is_video = filename.lower().endswith(('.mp4', '.mov'))
            
            # Identificação básica
            parts = filename.lower().split('_')
            store = parts[0] if len(parts) > 0 else "shopee"
            
            # Lendo Metadata JSON se existir
            json_path = local_path.replace(os.path.splitext(local_path)[1], '.json')
            if os.path.exists(json_path):
                try:
                    with open(json_path, 'r', encoding='utf-8') as mj:
                        meta = json.load(mj)
                    
                    # 💡 Lógica de Hashtag Única Automática
                    # Gera uma hashtag baseada no ID ou Título
                    raw_id = str(meta.get('id', int(time.time())))
                    safe_id = re.sub(r'[^a-zA-Z0-9]', '', raw_id)[:10]
                    unique_tag = f"#titanium_{safe_id}"
                    
                    # 💡 Formatação de Preço (Padrão Brasileiro)
                    raw_price = str(meta.get('price', '0'))
                    try:
                        p = raw_price.replace('R$', '').replace(' ', '').strip()
                        if ',' in p and '.' in p:
                            p = p.replace('.', '').replace(',', '.')
                        elif ',' in p:
                            p = p.replace(',', '.')
                        elif '.' in p:
                            parts_p = p.split('.')
                            if len(parts_p[-1]) > 2:
                                p = p.replace('.', '')
                        price_display = f"{float(p):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                    except:
                        price_display = raw_price
                    
                    combined_captions.append(f"{i+1}️⃣ {meta['title']} ➔ R$ {price_display} {unique_tag}")
                    
                    # Armazena para atualizar o dicionário depois
                    product_hashtags.append({
                        "tag": unique_tag,
                        "link": meta['link']
                    })
                except Exception as e:
                    print(f"⚠️ Erro ao processar meta JSON: {e}")

            # MODO ELITE: Postagem direta como imagem de alta fidelidade
            # Nota: Reels (vídeo) desativado temporariamente — FTP bloqueado pelo GitHub Actions
            # e tmpfiles.org bloqueado pela Meta para vídeos. Imagens funcionam perfeitamente.
            if is_image:
                print(f"📸 Preparando imagem premium para postagem direta: {filename}")
                media_to_upload.append({"local": local_path, "type": "IMAGE", "fallback_local": None})
            else:
                media_to_upload.append({"local": local_path, "type": "VIDEO", "fallback_local": None})

        if not combined_captions:
            print("❌ ERRO CRÍTICO: Não foi possível gerar as legendas/hashtags para o post. Abortando para evitar post 'órfão'.")
            for tmp in temp_video_paths:
                if os.path.exists(tmp): os.remove(tmp)
            sys.exit(1)

        # Construir Legenda Premium
        header = f"✨ SELEÇÃO EXCLUSIVA: {store.upper()} ✨\n\n"
        body = "\n".join(combined_captions)
        footer = f"\n\n💬 Comente **'QUERO'** que o nosso robô Titanium manda todos os links no seu direct! 🦾🤖\n\n#TitaniumBot #ShopeeBrasil #Achadinhos #Moda #Curadoria"
        final_caption = header + body + footer

        # --- EXECUÇÃO DO UPLOAD ---
        public_urls = []
        for item in media_to_upload:
            remote_name = f"titanium_elite_{int(time.time())}_{os.path.basename(item['local'])}"
            
            # Cloud direto para imagens (tmpfiles funciona perfeitamente para imagens)
            url = self.uploader.upload(item["local"], remote_name, force_cloud=True)
            
            if url:
                public_urls.append({"url": url, "type": item["type"]})
            else:
                print(f"❌ Falha crítica no upload de {item['local']}. Abortando ciclo.")
                for tmp in temp_video_paths:
                    if os.path.exists(tmp): os.remove(tmp)
                sys.exit(1)

        # --- POSTAGEM ---
        success = False
        if self.instagram and public_urls:
            item = public_urls[0]
            print(f"📸 Postando IMAGEM Premium Elite no feed do Instagram...")
            success = self.instagram.post_image(item["url"], final_caption)
        else:
            print("🧪 [SIMULAÇÃO] Postagem Simulada com Sucesso.")
            success = True

        # --- FINALIZAÇÃO ---
        if success:
            print("🎉 CICLO CONCLUÍDO COM SUCESSO!")
            os.makedirs(postados_dir, exist_ok=True)
            for path in full_paths:
                # Move imagem/vídeo original
                shutil.move(path, os.path.join(postados_dir, os.path.basename(path)))
                # Move JSON de metadata
                jp = path.replace(os.path.splitext(path)[1], '.json')
                if os.path.exists(jp):
                    shutil.move(jp, os.path.join(postados_dir, os.path.basename(jp)))
            # --- SINCRONIZAÇÃO DE OFERTAS AUTOMÁTICA ---
            if product_hashtags:
                print("🔄 Sincronizando novas hashtags com ofertas.json...")
                ofertas_local = "social/ofertas.json"
                try:
                    with open(ofertas_local, 'r', encoding='utf-8') as f:
                        dicionario = json.load(f)
                    
                    for item in product_hashtags:
                        dicionario[item['tag']] = item['link']
                        print(f"   ➕ Adicionado: {item['tag']} -> {item['link'][:30]}...")
                    
                    with open(ofertas_local, 'w', encoding='utf-8') as f:
                        json.dump(dicionario, f, indent=4, ensure_ascii=False)
                    
                    # Upload imediato para o servidor
                    from social.upload_ofertas import sync_ofertas
                    if sync_ofertas():
                        print("✅ ofertas.json sincronizado com o servidor com sucesso!")
                    else:
                        print("⚠️ Falha ao sincronizar ofertas.json com o servidor.")
                except Exception as e:
                    print(f"❌ Erro ao atualizar ofertas.json: {e}")

            # Limpeza de vídeos temporários
            for tmp in temp_video_paths:
                if os.path.exists(tmp): os.remove(tmp)
            sys.exit(0)
        else:
            print("❌ Falha crítica no ciclo de postagem.")
            # Limpeza de temporários antes de sair
            for tmp in temp_video_paths:
                if os.path.exists(tmp): os.remove(tmp)
            sys.exit(1)

    def _run_fallback_cycle(self, force_store):
        """Lógica de banners de categoria se a fila estiver vazia (simplificada para manter histórico)"""
        # (Aqui iria a lógica antiga de banners, mantida como fallback)
        print("⚠️ Pulando fallback por enquanto: Prioridade total na CURADORIA.")
        sys.exit(0) # Sem falha, apenas sem trabalho.


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    bot = SocialBot()
    # Teste local lendo segredos reais
    bot.run_daily_cycle(
        ig_token=os.getenv("IG_ACCESS_TOKEN"),
        ig_business_id=os.getenv("IG_BUSINESS_ID")
    )
