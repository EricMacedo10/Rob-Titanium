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
                
                # Redimensionar (MUITO MAIOR para destaque premium)
                max_size = 900 if format == "post" else 1000
                product_img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                
                # Centralizar imagem com sombra
                img_x = (self.width - product_img.width) // 2
                img_y = (self.height - product_img.height) // 2 - (50 if format == "post" else 150)
                
                # Sombra Projetada (Simples)
                shadow = Image.new("RGBA", product_img.size, (0, 0, 0, 60))
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

        # 4. Fontes
        try:
            font_path = "C:\\Windows\\Fonts\\arialbd.ttf"
            font_price = ImageFont.truetype(font_path, 130)  # Maior
            font_campaign = ImageFont.truetype(font_path, 110) # Volta às Aulas
            font_title = ImageFont.truetype(font_path, 50)
            font_cta = ImageFont.truetype(font_path, 40)
        except:
            font_price = font_campaign = font_title = ImageFont.load_default()

        # 5. Campanha "Volta às Aulas" (Padrão das Referências)
        brand_info = self.brand_colors.get(store_type.lower(), self.brand_colors["default"])
        campaign_text = "Volta às Aulas"
        draw.text(((self.width - draw.textlength(campaign_text, font=font_campaign))//2, self.height - 250), 
                  campaign_text, font=font_campaign, fill=brand_info["text"])

        # 6. Adicionar Preço (Badge Vibrante e Grande)
        try:
            raw_val = str(price).replace('R$', '').replace(' ', '').replace(',', '.')
            if raw_val.count('.') > 1:
                parts = raw_val.split('.')
                raw_val = "".join(parts[:-1]) + "." + parts[-1]
            val = float(raw_val)
            price_formatted = f"R$ {val:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        except Exception as e:
            print(f"Erro na formatação de preço ({price}): {e}")
            price_formatted = f"R$ {price}"
        
        badge_w, badge_h = 550, 180
        badge_x = (self.width - badge_w) // 2
        badge_y = self.height - 450
        
        # Cor do badge contrastante
        badge_fill = (255, 255, 255) if store_type.lower() != 'mercadolivre' else (51, 51, 51)
        text_fill = (0, 0, 0) if store_type.lower() != 'mercadolivre' else (255, 255, 255)
        
        draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=40, fill=badge_fill)
        draw.text((badge_x + (badge_w - font_price.getlength(price_formatted))//2, badge_y + 20), 
                  price_formatted, font=font_price, fill=text_fill)

        # 7. Título do Produto (Acima do preço, com contorno se necessário)
        clean_title = (product_title[:45] + '...') if len(product_title) > 45 else product_title
        title_y = badge_y - 80
        title_w = draw.textlength(clean_title, font=font_title)
        draw.text(((self.width - title_w)//2, title_y), clean_title, font=font_title, fill=brand_info["text"])
        
        # 8. Call to Action (CTA)
        cta_text = "LINK NA BIO 🔗"
        draw.text(((self.width - draw.textlength(cta_text, font=font_cta))//2, self.height - 80), 
                  cta_text, font=font_cta, fill=brand_info["text"])

        # 7. Salvar
        canvas.convert("RGB").save(output_path, "JPEG", quality=95)
        return output_path

if __name__ == "__main__":
    # Teste rápido se executado diretamente
    gen = ImageGenerator(assets_path="../site/images")
    test_img = "https://m.media-amazon.com/images/I/71ovN4v2YFL._AC_SL1500_.jpg" # Exemplo de monitor
    gen.generate_post(
        "Monitor Gamer LG UltraGear 27' Full HD 144Hz", 
        "1.299", 
        test_img, 
        "amazon", 
        "test_post.jpg"
    )
    print("Post de teste gerado em test_post.jpg")
