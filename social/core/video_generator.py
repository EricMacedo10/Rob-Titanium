import os
import random
import requests
import math
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip, AudioFileClip

class VideoGenerator:
    """
    Gera vídeos Reels e Stories combinando um B-Roll cinemático de fundo
    com um overlay em Glassmorphism contendo a oferta do Titanium.
    """
    def __init__(self, broll_dir="assets/broll"):
        self.width = 1080
        self.height = 1920
        self.broll_dir = os.path.join(os.path.dirname(__file__), "..", broll_dir)
        self.audio_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "audio")
        self.temp_dir = os.path.join(os.path.dirname(__file__), "..", "temp_videos")
        os.makedirs(self.temp_dir, exist_ok=True)
        os.makedirs(self.audio_dir, exist_ok=True)

    def _parse_price(self, price_val):
        try:
            p = str(price_val).replace('R$', '').replace(' ', '').strip()
            if ',' in p and '.' in p:
                p = p.replace('.', '').replace(',', '.')
            elif ',' in p:
                p = p.replace(',', '.')
            elif '.' in p:
                parts = p.split('.')
                if len(parts[-1]) > 2:
                    p = p.replace('.', '')
            return float(p)
        except Exception:
            return 0.0

    def _remove_white_background(self, img, threshold=230):
        img = img.convert("RGBA")
        data = img.getdata()
        newData = []
        for item in data:
            if item[0] > threshold and item[1] > threshold and item[2] > threshold:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        img.putdata(newData)
        return img

    def _get_random_broll(self):
        if not os.path.exists(self.broll_dir):
            raise Exception(f"Pasta de B-roll não existe: {self.broll_dir}")
        files = [f for f in os.listdir(self.broll_dir) if f.endswith('.mp4') or f.endswith('.mov')]
        if not files:
            raise Exception("Nenhum vídeo B-roll encontrado na pasta.")
        return os.path.join(self.broll_dir, random.choice(files))

    def _prepare_product_image(self, product_url):
        """Baixa, remove o fundo e salva a imagem do produto."""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
            "Referer": "https://www.google.com/"
        }
        try:
            resp = requests.get(product_url, headers=headers, timeout=15)
            if resp.status_code == 200:
                product_img = Image.open(BytesIO(resp.content)).convert("RGBA")
                product_img = self._remove_white_background(product_img)
                
                max_size = 900
                img_w, img_h = product_img.size
                ratio = min(max_size / img_w, max_size / img_h)
                new_w, new_h = int(img_w * ratio), int(img_h * ratio)
                product_img = product_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                
                prod_path = os.path.join(self.temp_dir, "temp_product.png")
                product_img.save(prod_path, "PNG")
                return prod_path
        except Exception as e:
            print(f"Erro ao baixar produto: {e}")
        return None

    def _create_glassmorphism_card(self, price, video_type="reel"):
        """Cria apenas o card de preço com fundo transparente."""
        canvas = Image.new('RGBA', (self.width, 500), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)
        
        try:
            font_path = "C:\\Windows\\Fonts\\arialbd.ttf"
            if not os.path.exists(font_path): font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            font_price = ImageFont.truetype(font_path, 110)
            font_title = ImageFont.truetype(font_path, 45)
            font_cta = ImageFont.truetype(font_path, 35)
        except Exception:
            font_price = font_title = font_cta = ImageFont.load_default()

        val = self._parse_price(price)
        price_str = f"R$ {val:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        
        tw = font_price.getlength(price_str) if hasattr(font_price, 'getlength') else 300
        
        # Dinâmico baseado no tipo de vídeo
        if video_type.lower() == "story":
            cta_str = "Responda EU QUERO para o link"
        else:
            cta_str = "Comente QUERO para o link"
            
        cta_w = font_cta.getlength(cta_str) if hasattr(font_cta, 'getlength') else 200
        title_str = "SELEÇÃO TITANIUM"
        title_w = font_title.getlength(title_str) if hasattr(font_title, 'getlength') else 200

        # Ajuste dinâmico da largura do card para não cortar a frase
        bw = max(int(tw + 120), int(cta_w + 120), int(title_w + 120))
        bh = 300
        bx, by = (self.width - bw) // 2, 50
        
        # Fundo branco sólido com borda preta fina
        draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=50, fill=(255, 255, 255, 255), outline=(50, 50, 50, 255), width=3)
        
        draw.text((bx + (bw - title_w)//2, by + 30), title_str, font=font_title, fill=(100, 100, 100, 255))
        
        draw.text((bx + (bw - tw)//2, by + 90), price_str, font=font_price, fill=(238, 77, 45, 255))
        
        draw.text((bx + (bw - cta_w)//2, by + 220), cta_str, font=font_cta, fill=(50, 50, 50, 255))

        card_path = os.path.join(self.temp_dir, "temp_card.png")
        canvas.save(card_path, "PNG")
        return card_path

    def generate_video(self, product_url, price, store_type="shopee", output_filename="reel.mp4", video_type="reel"):
        print(f"--- Preparando assets para formato {video_type.upper()}...")
        prod_path = self._prepare_product_image(product_url)
        card_path = self._create_glassmorphism_card(price, video_type=video_type)
        
        # Fundo claro sólido (Cinza bem clarinho)
        from moviepy import ColorClip
        video = ColorClip(size=(self.width, self.height), color=(245, 245, 245)).with_duration(5)
        output_path = os.path.join(self.temp_dir, output_filename)
            
        clips = [video]
        
        if prod_path:
            prod_clip = ImageClip(prod_path).with_duration(video.duration)
            # ANIMAÇÃO: Efeito de Flutuação Suave (Levitation)
            def fl_position(t):
                # Flutua 20 pixels para cima e para baixo
                y_pos = 300 + 20 * math.sin(t * 3)
                return ('center', y_pos)
            animated_prod = prod_clip.with_position(fl_position)
            clips.append(animated_prod)
            
        card_clip = ImageClip(card_path).with_duration(video.duration).with_position(('center', 1300))
        clips.append(card_clip)
        
        final = CompositeVideoClip(clips)
        
        print("--- Renderizando Reel com Animação (Sem áudio, Fundo Claro)...")
        final.write_videofile(output_path, codec="libx264", audio=False, fps=24, logger=None)
        
        if prod_path and os.path.exists(prod_path): os.remove(prod_path)
        if card_path and os.path.exists(card_path): os.remove(card_path)
            
        print(f"--- Reel Premium gerado em: {output_path}")
        return output_path
