"""
Pesca Titanium — Gerador de Vídeo (Identidade Visual de Pesca)
==============================================================
Usa os templates oficiais (bg_feed.png e bg_story.png) gerados a partir
dos mockups perfeitos (fibra de carbono + neon verde).
"""

import os
import math
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

class PescaVideoGenerator:
    def __init__(self):
        self.width  = 1080
        self.height = 1920
        self.temp_dir = os.path.join(os.path.dirname(__file__), "temp_videos")
        os.makedirs(self.temp_dir, exist_ok=True)

    def _get_font(self, size: int, bold: bool = True):
        font_paths = [
            "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        ]
        for path in font_paths:
            if os.path.exists(path):
                try:
                    return ImageFont.truetype(path, size)
                except Exception:
                    continue
        return ImageFont.load_default()

    def _parse_price(self, price_val) -> float:
        try:
            p = str(price_val).replace('R$', '').replace(' ', '').strip()
            if ',' in p and '.' in p:
                p = p.replace('.', '').replace(',', '.')
            elif ',' in p:
                p = p.replace(',', '.')
            return float(p)
        except Exception:
            return 0.0

    def _prepare_product_image(self, image_url: str):
        if not image_url:
            return None
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "image/*,*/*;q=0.8",
        }
        try:
            resp = requests.get(image_url, headers=headers, timeout=15)
            if resp.status_code == 200:
                img = Image.open(BytesIO(resp.content)).convert("RGBA")
                
                # Inteligência Artificial para remover QUALQUER fundo (bege, cinza, branco, etc)
                try:
                    from rembg import remove
                    img = remove(img)
                except ImportError:
                    print("⚠️ rembg não instalado, caindo para remoção básica (quadrados beges podem aparecer).")
                    data = img.getdata()
                    new_data = []
                    for item in data:
                        if item[0] > 230 and item[1] > 230 and item[2] > 230:
                            new_data.append((255, 255, 255, 0))
                        else:
                            new_data.append(item)
                    img.putdata(new_data)

                # Resize to fit perfectly inside the neon frame without touching logo/price
                max_size = 500
                w, h = img.size
                ratio = min(max_size / w, max_size / h)
                img = img.resize((int(w * ratio), int(h * ratio)), Image.Resampling.LANCZOS)

                prod_path = os.path.join(self.temp_dir, "pesca_temp_product.png")
                img.save(prod_path, "PNG")
                return prod_path
        except Exception as e:
            print(f"⚠️  Erro ao baixar imagem do produto: {e}")
        return None

    def _create_template_background(self, price: str, video_type: str) -> str:
        assets_dir = os.path.join(os.path.dirname(__file__), "assets")
        bg_file = "bg_story.png" if video_type == "story" else "bg_feed.png"
        bg_path = os.path.join(assets_dir, bg_file)
            
        if not os.path.exists(bg_path):
            canvas = Image.new('RGB', (self.width, self.height), (15, 15, 15))
            y_offset = (self.height - 1080) // 2
        else:
            img = Image.open(bg_path).convert("RGBA")
            w, h = img.size
            ratio = self.width / w
            new_w, new_h = int(w * ratio), int(h * ratio)
            img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
            
            canvas = Image.new('RGB', (self.width, self.height), (10, 10, 10))
            
            try:
                from PIL import ImageFilter
                bg_blur = img.resize((self.width, self.height)).filter(ImageFilter.GaussianBlur(50))
                canvas.paste(bg_blur, (0, 0))
            except Exception:
                pass
            
            y_offset = (self.height - new_h) // 2
            canvas.paste(img, (0, y_offset), img)

        draw = ImageDraw.Draw(canvas)
        font_price = self._get_font(60, bold=True)
        val = self._parse_price(price)
        price_str = f"R$ {val:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

        def txt_w(font, text):
            return font.getlength(text) if hasattr(font, 'getlength') else 200

        pw = txt_w(font_price, price_str)
        
        if video_type == "story":
            text_x = (self.width - pw) // 2
            text_y = y_offset + int(1080 * 0.81)
        else:
            text_x = int(1080 * 0.74) - (pw // 2)
            text_y = y_offset + int(1080 * 0.755)

        draw.text((text_x + 3, text_y + 3), price_str, font=font_price, fill=(0, 0, 0, 150))
        draw.text((text_x, text_y), price_str, font=font_price, fill=(255, 255, 255, 255))

        # --- ADICIONANDO A "ESCRITA" (CTA) APENAS NO STORY ---
        if video_type == "story":
            cta_str = "Responda EU QUERO para receber o link 🎣"
            font_cta = self._get_font(42, bold=True)
            cw = txt_w(font_cta, cta_str)
            cta_x = (self.width - cw) // 2
            # Posiciona abaixo do card do preço (na área borrada inferior)
            cta_y = text_y + 180 
            
            # Fundo escuro arredondado com borda neon para a escrita
            pad_x, pad_y = 40, 20
            draw.rounded_rectangle(
                [cta_x - pad_x, cta_y - pad_y, cta_x + cw + pad_x, cta_y + 42 + pad_y],
                radius=35, fill=(15, 15, 15, 230), outline=self.COR_CTA, width=3
            )
            draw.text((cta_x, cta_y), cta_str, font=font_cta, fill=(255, 255, 255, 255))

        tmp_path = os.path.join(self.temp_dir, f"pesca_temp_bg_{video_type}.png")
        canvas.save(tmp_path, "PNG")
        return tmp_path

    def generate_video(
        self,
        product_url: str,
        price,
        product_title: str = "",
        output_filename: str = "pesca_reel.mp4",
        video_type: str = "reel"
    ) -> str:
        from moviepy import ImageClip, CompositeVideoClip

        print(f"   🎬 Gerando vídeo PESCA [{video_type.upper()}]...")

        prod_path = self._prepare_product_image(product_url)
        bg_path = self._create_template_background(price, video_type)

        duration = 7

        bg_clip = ImageClip(bg_path).with_duration(duration)
        clips = [bg_clip]

        if prod_path and os.path.exists(prod_path):
            prod_clip = ImageClip(prod_path).with_duration(duration)
            
            def fl_position(t):
                y_offset = 15 * math.sin(t * 2.5)
                # Centraliza a imagem do produto dentro da area do template (y_offset do template)
                # O centro do template é exatament self.height // 2 = 960
                return ('center', int(960 - (prod_clip.h // 2) + y_offset))

            animated_prod = prod_clip.with_position(fl_position)
            clips.append(animated_prod)

        output_path = os.path.join(self.temp_dir, output_filename)
        final = CompositeVideoClip(clips, size=(self.width, self.height))
        final.write_videofile(
            output_path,
            codec="libx264",
            audio=False,
            fps=24,
            logger=None
        )

        for tmp in [prod_path, bg_path]:
            if tmp and os.path.exists(tmp):
                try:
                    os.remove(tmp)
                except Exception:
                    pass

        print(f"   ✅ Vídeo Pesca gerado: {output_path}")
        return output_path
