import os
import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO

class ImageGenerator:
    """
    Classe responsável por gerar artes para Instagram (Feed) no estilo 'Oferta Certa'.
    """
    def __init__(self, assets_path="site/images"):
        self.width = 1080
        self.height = 1080
        self.assets_path = assets_path
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        })
        
        # Paletas de Cores das Marcas (Premium Gradients)
        self.brand_colors = {
            "amazon": {"bg": (255, 153, 0), "text": (255, 255, 255)},
            "mercadolivre": {"bg": (255, 230, 0), "text": (51, 51, 51)},
            "shopee": {"bg": (238, 77, 45), "text": (255, 255, 255)},
            "default": {"bg": (12, 12, 12), "text": (255, 255, 255)}
        }
        self.color_accent = (0, 230, 118)  # Fallback accent
        
    def _parse_price(self, price_val):
        """Converte strings de preço (R$ 1.299,00 ou 49.0) em float de forma segura."""
        try:
            p = str(price_val).replace('R$', '').replace(' ', '').strip()
            # Se tem vírgula e ponto, a vírgula é o decimal (padrão BR)
            if ',' in p and '.' in p:
                p = p.replace('.', '').replace(',', '.')
            # Se tem apenas vírgula, trocamos por ponto
            elif ',' in p:
                p = p.replace(',', '.')
            # Se tem apenas um ponto e ele está nas últimas 2 ou 3 casas, é decimal
            # Caso contrário, se for algo como 1.299 (sem decimais), tratamos como milhar
            elif '.' in p:
                parts = p.split('.')
                if len(parts[-1]) > 2: # Ex: 1.299 -> 1299
                    p = p.replace('.', '')
            
            return float(p)
        except Exception as e:
            print(f"⚠️ Erro ao parsear preço '{price_val}': {e}")
            return 0.0

    def _create_brand_background(self, store_type):
        """Cria um fundo vibrante baseado na marca e campanha."""
        brand = self.brand_colors.get(store_type.lower(), self.brand_colors["default"])
        color = brand["bg"]
        
        base = Image.new('RGB', (self.width, self.height), color)
        draw = ImageDraw.Draw(base)
        
        # Adicionar Degradê Esférico/Radial para profundidade
        for i in range(self.height // 2, 0, -2):
            alpha = int(100 * (1 - i / (self.height // 2)))
            inner_color = (
                min(255, color[0] + 40),
                min(255, color[1] + 40),
                min(255, color[2] + 40)
            )
            draw.ellipse(
                [self.width//2 - i*2, self.height//2 - i*2, self.width//2 + i*2, self.height//2 + i*2],
                outline=inner_color, width=2
            )
            
        return base

    def generate_post(self, product_title, price, image_url, store_type, output_path, format="post"):
        """
        Cria a imagem final do post.
        format: 'post' (1080x1080) ou 'reels' (1080x1920)
        """
        if format == "reels":
            self.height = 1920
        else:
            self.height = 1080
            
        # 1. Criar Fundo Vibrante
        canvas = self._create_brand_background(store_type)
        draw = ImageDraw.Draw(canvas)
        
        # 2. Carregar Imagem do Produto com Headers Defensivos
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Referer": "https://www.google.com/"
        }
        try:
            response = requests.get(image_url, headers=headers, timeout=15)
            # print(f"HTTP Status: {response.status_code} | Content-Type: {response.headers.get('Content-Type')}")
            
            if response.status_code == 200:
                img_data = BytesIO(response.content)
                product_img = Image.open(img_data).convert("RGBA")
                
                # Garantir Uniformidade (Mesmo Tamanho Exato e Aconchegante Independente da Origem)
                max_size = 850 if format == "post" else 950
                
                # 1. Força a amplificação se a imagem for pequena, ou redução se mto grande
                img_w, img_h = product_img.size
                ratio = min(max_size / img_w, max_size / img_h)
                new_w, new_h = int(img_w * ratio), int(img_h * ratio)
                
                product_img = product_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                
                # 2. Insere num "Box Invisível" do mesmo tamanho pra criar padronização e peso igual
                box = Image.new('RGBA', (max_size, max_size), (0, 0, 0, 0))
                box.paste(product_img, ((max_size - new_w) // 2, (max_size - new_h) // 2))
                product_img = box
                
                # Centralizar o Box Uniforme no Canvas
                img_x = (self.width - max_size) // 2
                img_y = (self.height - max_size) // 2 - (50 if format == "post" else 150)
                
                # Sombra Projetada Uniforme
                shadow = Image.new("RGBA", product_img.size, (0, 0, 0, 30))
                canvas.paste(shadow, (img_x + 20, img_y + 20), shadow)
                canvas.paste(product_img, (img_x, img_y), product_img)
            else:
                raise Exception(f"HTTP {response.status_code}")
            
        except Exception as e:
            # Requisito de Compliance: Não postar sem imagem real
            raise Exception(f"Falha Crítica: Imagem do produto indisponível ({e}). Abortando postagem.")

        # 3. Adicionar Logo da Loja
        logo_filename = f"logo-{store_type}.png"
        logo_path = os.path.join(self.assets_path, logo_filename)
        if os.path.exists(logo_path):
            store_logo = Image.open(logo_path).convert("RGBA")
            store_logo.thumbnail((250, 100), Image.Resampling.LANCZOS)
            canvas.paste(store_logo, (50, 50), store_logo)

        # 4. Fontes Minimalistas (Compatibilidade Windows/Linux)
        try:
            # Lista de caminhos possíveis para Arial Bold ou similar
            font_candidates = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux (Ubuntu)
                "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", # Linux (Alternative)
                "C:\\Windows\\Fonts\\arialbd.ttf" # Windows
            ]
            font_price = None
            for p in font_candidates:
                if os.path.exists(p):
                    font_price = ImageFont.truetype(p, 90) # REDUZIDO EM 50% (MINIMALISTA)
                    break
            
            if not font_price:
                font_price = ImageFont.load_default() # Fallback final
        except Exception:
            font_price = ImageFont.load_default()

        # 5. Adicionar Preço (Badge Premium Clean)
        try:
            val = self._parse_price(price)
            price_formatted = f"R$ {val:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        except Exception as e:
            print(f"Erro na formatação de preço ({price}): {e}")
            price_formatted = f"R$ {price}"
        
        # Cálculo Dinâmico da Moldura do Preço (SLIM)
        text_width = font_price.getlength(price_formatted) if hasattr(font_price, 'getlength') else 200
        badge_w, badge_h = int(text_width + 60), 100 # Reduzido proporcionalmente
        badge_x = (self.width - badge_w) // 2
        badge_y = self.height - 190  # Posição otimizada para evitar crop de busca e botões de UI
        
        # Cor do badge clean e contrastante (Fundo Branco, Fonte Laranja Shopee)
        badge_fill = (255, 255, 255)
        text_fill = (238, 77, 45) if store_type.lower() == 'shopee' else (51, 51, 51)
        
        # Sombreamento ultra-suave para dar profundidade Elite Glassmorphism
        shadow_overlay = Image.new('RGBA', canvas.size, (0,0,0,0))
        shadow_draw = ImageDraw.Draw(shadow_overlay)
        shadow_draw.rounded_rectangle([badge_x + 8, badge_y + 8, badge_x + badge_w + 8, badge_y + badge_h + 8], radius=35, fill=(0, 0, 0, 40))
        canvas.paste(shadow_overlay, (0,0), shadow_overlay)

        # Desenhar base do Preço
        draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=35, fill=badge_fill)
        draw.text((badge_x + (badge_w - text_width)//2, badge_y + 0), 
                  price_formatted, font=font_price, fill=text_fill)

        # 6. Salvar e Retornar
        canvas.convert("RGB").save(output_path, "JPEG", quality=95)
        return output_path

    def generate_premium_reel_frame(self, product_title, price, image_url, store_type, output_path):
        """
        Cria o 'Frame Mestre' de alta fidelidade para o Reel Premium.
        Focado em Harmonização, Credibilidade e Design de Revista.
        """
        self.width = 1080
        self.height = 1920 # Proporção Reel
        
        # 1. Fundo Minimalista Profissional (Degradê Suave / Neutral)
        bg_color = (245, 245, 245) # Off-white premium
        canvas = Image.new('RGB', (self.width, self.height), bg_color)
        draw = ImageDraw.Draw(canvas)
        
        # Adicionar uma textura sutil ou degradê de profundidade
        for i in range(self.height):
            # Degradê quase imperceptível de cima para baixo
            r = int(245 - (i / self.height) * 10)
            g = int(245 - (i / self.height) * 10)
            b = int(245 - (i / self.height) * 10)
            draw.line([(0, i), (self.width, i)], fill=(r, g, b))

        # 2. Carregar e Processar Imagem do Produto
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            response = requests.get(image_url, headers=headers, timeout=15)
            if response.status_code == 200:
                img_data = BytesIO(response.content)
                product_img = Image.open(img_data).convert("RGBA")
                
                # Redimensionamento Inteligente (Ocupando o centro com "respiro")
                max_size = 900
                img_w, img_h = product_img.size
                ratio = min(max_size / img_w, max_size / img_h)
                new_w, new_h = int(img_w * ratio), int(img_h * ratio)
                product_img = product_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                
                # Centralização
                img_x = (self.width - new_w) // 2
                img_y = (self.height - new_h) // 2
                
                # Sombra Projetada Suave (Efeito Flutuante)
                shadow_offset = 25
                shadow = Image.new("RGBA", product_img.size, (0, 0, 0, 15)) # Ultra-suave
                canvas.paste(shadow, (img_x + shadow_offset, img_y + shadow_offset), shadow)
                canvas.paste(product_img, (img_x, img_y), product_img)
            else:
                raise Exception(f"HTTP {response.status_code}")
        except Exception as e:
            print(f"Erro ao carregar imagem para Premium: {e}")
            # Fallback seguro: Fundo colorido se falhar imagem
            draw.rectangle([100, 400, 980, 1400], fill=(220, 220, 220))

        # 3. Cabeçalho Minimalista "SELEÇÃO TITANIUM"
        try:
            font_path = "C:\\Windows\\Fonts\\arial.ttf" # Simples e elegante
            if not os.path.exists(font_path):
                font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
            
            font_header = ImageFont.truetype(font_path, 45) if os.path.exists(font_path) else ImageFont.load_default()
            header_text = "SELEÇÃO TITANIUM"
            
            # Espaçamento entre letras (Manual para efeito premium)
            header_x = 100
            header_y = 150
            for char in header_text:
                draw.text((header_x, header_y), char, font=font_header, fill=(100, 100, 100))
                header_x += 40 # Letter spacing
                
            # Linha de detalhe sutil
            draw.line([(100, 210), (250, 210)], fill=(238, 77, 45), width=3) # Accent color Shopee
        except: pass

        # 4. Badge de Preço Elite (Otimizado)
        try:
            font_price_path = "C:\\Windows\\Fonts\\arialbd.ttf"
            if not os.path.exists(font_price_path):
                font_price_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            
            font_price = ImageFont.truetype(font_price_path, 110) if os.path.exists(font_price_path) else ImageFont.load_default()
            
            # Formatação
            val = self._parse_price(price)
            price_str = f"R$ {val:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            
            # Caixa do Badge
            tw = font_price.getlength(price_str) if hasattr(font_price, 'getlength') else 300
            bw, bh = int(tw + 100), 160
            bx, by = (self.width - bw) // 2, self.height - 520 # Elevado para visibilidade em Search Grid (Safe Zone)
            
            # Glassmorphism/Flat-Premium Shadow
            draw.rounded_rectangle([bx + 10, by + 10, bx + bw + 10, by + bh + 10], radius=80, fill=(0,0,0,20))
            draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=80, fill=(255, 255, 255))
            
            # Texto do Preço
            draw.text((bx + (bw - tw)//2, by + 15), price_str, font=font_price, fill=(238, 77, 45))
        except: pass

        # 5. Logo Shopee (Pequeno e Discreto no Canto)
        logo_path = os.path.join(self.assets_path, "logo-shopee.png")
        if os.path.exists(logo_path):
            logo = Image.open(logo_path).convert("RGBA")
            logo.thumbnail((150, 150))
            canvas.paste(logo, (self.width - 200, 100), logo)

        # 6. Salvar Resultado (Qualidade Máxima)
        canvas.save(output_path, "JPEG", quality=98)
        return output_path

if __name__ == "__main__":
    # Teste rápido se executado diretamente
    gen = ImageGenerator(assets_path="../site/images")
    test_img = "https://m.media-amazon.com/images/I/71ovN4v2YFL._AC_SL1500_.jpg"
    gen.generate_premium_reel_frame(
        "Monitor Gamer Premium", 
        "1.299,00", 
        test_img, 
        "shopee", 
        "test_premium.jpg"
    )
    print("Post Premium gerado em test_premium.jpg")
