"""
Pesca Titanium — Gerador de Vídeo (Identidade Visual de Pesca)
==============================================================
Versão independente do VideoGenerator do bot de moda.
Identidade visual: azul-marinho profundo + dourado (tema pesca esportiva).

Gera Reels (vertical 1080x1920) com:
- Fundo: gradiente azul-água escuro
- Card: branco com borda dourada e logo "PESCA TITANIUM"
- Produto: imagem centralizada com efeito de flutuação suave
- CTA: "Comente QUERO o link" ou "Responda EU QUERO" (stories)
"""

import os
import math
import random
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


class PescaVideoGenerator:
    """
    Gera vídeos Reels e Stories para a conta @pescatitanium.
    Identidade visual completamente separada do bot de moda Titanium.
    """

    # Paleta de cores da Pesca Titanium (Estilo Cyber/Neon Green)
    COR_FUNDO_TOPO = (15, 15, 15)         # Cinza muito escuro (quase preto)
    COR_FUNDO_BASE = (5, 5, 5)            # Preto
    COR_CARD_FUNDO = (20, 20, 20, 245)    # Fundo do card metálico/escuro
    COR_CARD_BORDA = (57, 255, 20, 255)   # Verde Neon (glowing green)
    COR_PRECO      = (255, 255, 255, 255) # Branco (preço)
    COR_TITULO     = (200, 200, 200, 255) # Cinza claro (nome do produto)
    COR_CTA        = (57, 255, 20, 255)   # Verde Neon (CTA)
    COR_ACENTO     = (57, 255, 20, 255)   # Verde Neon (detalhes)

    def __init__(self):
        self.width  = 1080
        self.height = 1920
        # Diretório de saída dentro de pesca/
        self.temp_dir = os.path.join(os.path.dirname(__file__), "temp_videos")
        os.makedirs(self.temp_dir, exist_ok=True)

    def _get_font(self, size: int, bold: bool = True):
        """Tenta carregar fonte Arial Bold; cai para DejaVu (Linux/Actions)."""
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

    def _create_gradient_background(self) -> Image.Image:
        """Cria fundo com gradiente vertical azul-marinho → azul-petróleo."""
        bg = Image.new('RGB', (self.width, self.height))
        draw = ImageDraw.Draw(bg)

        top_r, top_g, top_b = self.COR_FUNDO_TOPO
        bot_r, bot_g, bot_b = self.COR_FUNDO_BASE

        for y in range(self.height):
            ratio = y / self.height
            r = int(top_r + (bot_r - top_r) * ratio)
            g = int(top_g + (bot_g - top_g) * ratio)
            b = int(top_b + (bot_b - top_b) * ratio)
            draw.line([(0, y), (self.width, y)], fill=(r, g, b))

        # Reflexo sutil de luz na parte superior (efeito profundidade)
        overlay = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        ov_draw = ImageDraw.Draw(overlay)
        for i in range(200):
            alpha = int(30 * (1 - i / 200))
            ov_draw.line([(0, i), (self.width, i)], fill=(255, 255, 255, alpha))
        bg = Image.alpha_composite(bg.convert('RGBA'), overlay).convert('RGB')

        return bg

    def _prepare_product_image(self, image_url: str):
        """Baixa a imagem do produto e remove fundo branco."""
        if not image_url:
            return None
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
            "Referer": "https://www.google.com/"
        }
        try:
            resp = requests.get(image_url, headers=headers, timeout=15)
            if resp.status_code == 200:
                img = Image.open(BytesIO(resp.content)).convert("RGBA")

                # Remove fundo branco
                data = img.getdata()
                new_data = []
                for item in data:
                    if item[0] > 230 and item[1] > 230 and item[2] > 230:
                        new_data.append((255, 255, 255, 0))
                    else:
                        new_data.append(item)
                img.putdata(new_data)

                # Redimensiona para caber no frame
                max_size = 850
                w, h = img.size
                ratio = min(max_size / w, max_size / h)
                img = img.resize((int(w * ratio), int(h * ratio)), Image.Resampling.LANCZOS)

                prod_path = os.path.join(self.temp_dir, "pesca_temp_product.png")
                img.save(prod_path, "PNG")
                return prod_path
        except Exception as e:
            print(f"⚠️  Erro ao baixar imagem do produto: {e}")
        return None

    def _create_price_card(self, price, title: str, video_type: str = "reel") -> str:
        """
        Cria o card de oferta com identidade visual da Pesca Titanium.
        Fundo branco, borda dourada, preço em azul royal.
        """
        card_w, card_h = 960, 340
        canvas = Image.new('RGBA', (self.width, card_h + 60), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)

        # Fontes
        font_label  = self._get_font(38, bold=False)
        font_price  = self._get_font(108, bold=True)
        font_name   = self._get_font(32, bold=False)
        font_cta    = self._get_font(34, bold=True)

        val = self._parse_price(price)
        price_str = f"R$ {val:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

        # Trunca título do produto se muito longo
        product_title = (title[:55] + "...") if len(title) > 58 else title

        cta_str = "Responda EU QUERO para o link 🎣" if video_type == "story" else "Comente QUERO para receber o link 🎣"

        # Calcula largura máxima necessária
        def txt_w(font, text):
            return font.getlength(text) if hasattr(font, 'getlength') else 300

        bw = max(
            int(txt_w(font_price, price_str) + 100),
            int(txt_w(font_cta, cta_str) + 80),
            int(txt_w(font_name, product_title) + 80),
            700
        )
        bw = min(bw, self.width - 60)
        bh = card_h
        bx = (self.width - bw) // 2
        by = 30

        # Sombra do card
        shadow = Image.new('RGBA', (self.width, card_h + 60), (0, 0, 0, 0))
        sh_draw = ImageDraw.Draw(shadow)
        sh_draw.rounded_rectangle(
            [bx + 8, by + 8, bx + bw + 8, by + bh + 8],
            radius=30, fill=(0, 0, 0, 60)
        )
        canvas = Image.alpha_composite(canvas, shadow)
        draw = ImageDraw.Draw(canvas)

        # Fundo do card
        draw.rounded_rectangle(
            [bx, by, bx + bw, by + bh],
            radius=30,
            fill=self.COR_CARD_FUNDO,
            outline=self.COR_CARD_BORDA,
            width=4
        )

        # Barra superior dourada (detalhe premium)
        draw.rounded_rectangle([bx, by, bx + bw, by + 14], radius=30, fill=self.COR_ACENTO)

        # Label "PESCA TITANIUM"
        label = "🎣 PESCA TITANIUM"
        lw = txt_w(font_label, label)
        draw.text(
            (bx + (bw - lw) // 2, by + 28),
            label, font=font_label, fill=self.COR_TITULO
        )

        # Preço em destaque
        pw = txt_w(font_price, price_str)
        draw.text(
            (bx + (bw - pw) // 2, by + 80),
            price_str, font=font_price, fill=self.COR_PRECO
        )

        # Título do produto (abreviado)
        nw = txt_w(font_name, product_title)
        draw.text(
            (bx + (bw - nw) // 2, by + 210),
            product_title, font=font_name, fill=(80, 80, 80, 255)
        )

        # CTA
        cw = txt_w(font_cta, cta_str)
        draw.text(
            (bx + (bw - cw) // 2, by + 260),
            cta_str, font=font_cta, fill=self.COR_CTA
        )

        card_path = os.path.join(self.temp_dir, "pesca_temp_card.png")
        canvas.save(card_path, "PNG")
        return card_path

    def generate_video(
        self,
        product_url: str,
        price,
        product_title: str = "",
        output_filename: str = "pesca_reel.mp4",
        video_type: str = "reel"
    ) -> str:
        """
        Gera o vídeo completo para Reels ou Stories.
        Retorna o caminho do arquivo gerado.
        """
        from moviepy import ImageClip, CompositeVideoClip

        print(f"   🎬 Gerando vídeo PESCA [{video_type.upper()}]...")

        # Assets
        prod_path = self._prepare_product_image(product_url)
        card_path = self._create_price_card(price, product_title, video_type=video_type)

        # Frame de fundo (imagem estática → clip)
        bg_img = self._create_gradient_background()
        bg_path = os.path.join(self.temp_dir, "pesca_temp_bg.png")
        bg_img.save(bg_path, "PNG")

        duration = 7  # segundos

        bg_clip   = ImageClip(bg_path).with_duration(duration)
        card_clip = ImageClip(card_path).with_duration(duration).with_position(('center', 1460))

        clips = [bg_clip]

        if prod_path and os.path.exists(prod_path):
            prod_clip = ImageClip(prod_path).with_duration(duration)

            # Animação: flutuação suave (efeito levitation)
            def fl_position(t):
                y_offset = 18 * math.sin(t * 2.5)
                return ('center', int(280 + y_offset))

            animated_prod = prod_clip.with_position(fl_position)
            clips.append(animated_prod)

        clips.append(card_clip)

        output_path = os.path.join(self.temp_dir, output_filename)
        final = CompositeVideoClip(clips, size=(self.width, self.height))
        final.write_videofile(
            output_path,
            codec="libx264",
            audio=False,
            fps=24,
            logger=None
        )

        # Limpeza dos assets temporários
        for tmp in [prod_path, card_path, bg_path]:
            if tmp and os.path.exists(tmp):
                try:
                    os.remove(tmp)
                except Exception:
                    pass

        print(f"   ✅ Vídeo Pesca gerado: {output_path}")
        return output_path
