"""
Pesca Titanium — Datafeed Shopee (Nicho de Pesca)
==================================================
Baixa, parseia e filtra o feed de produtos da Shopee.
Foco exclusivo: Pesca Esportiva e Acessórios.

Usa a variável de ambiente PESCA_SHOPEE_DATAFEED_URLS (separada do bot de moda).

Uso:
    from pesca.datafeed_pesca import get_pesca_products
    products = get_pesca_products(max_items=500)
"""

import os
import csv
import json
import time
import requests
import random
import sys
import io
from dotenv import load_dotenv

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

# ─────────────────────────────────────────────────────────
# KEYWORDS EXCLUSIVOS DE PESCA
# ─────────────────────────────────────────────────────────
PESCA_KEYWORDS = [
    "pesca", "pescaria", "pescador", "carretilha", "molinete",
    "isca artificial", "isca de pesca", "iscas", "anzol", "anzóis",
    "linha de pesca", "multifilamento", "monofilamento", "fluorocarbon",
    "caixa de pesca", "estojo de pesca", "bolsa de pesca",
    "alicate de pesca", "chumbada", "boia cevadeira", "boia de pesca",
    "sonar de pesca", "tucunaré", "tilápia", "camisa uv pesca",
    "chapéu de pesca", "luva de pesca", "passaguá", "samburá",
    "suporte de vara", "girador", "snap", "boga grip",
    "vara telescópica", "vara de pesca", "vara de carretilha",
    "vara de molinete", "maleta de pesca", "camisa de pesca",
    "kit pesca", "anzol jig", "plug de pesca", "lure", "jig",
    "atum pesca", "tainha", "robalo", "dourado pesca",
    "kit anzol", "rede de pesca", "puçá", "caniço",
    "flutuador", "chumbadeira", "tira-anzol", "desenganchador",
    "colete salva vidas pesca", "óculos polarizado pesca",
]

# Blocklist para garantir que produtos irrelevantes não passem
BLOCKLIST_KEYWORDS = [
    "vibrador", "sugador", "clitoris", "clitóris", "estimulador",
    "masturbador", "plug anal", "sex toy", "brinquedo erótico",
    "massageador íntimo", "bullet", "wand", "ovo masturbador",
    "lingerie aberta", "fio dental aberto", "cápsula discreto",
    "pompoarismo", "ponto g", "consolador", "algema", "chicote",
    "vibratório", "vibratoria", "prazer íntimo", "prazer intimo",
    # Itens de moda que não são pesca
    "vestido", "saia", "blusa", "maquiagem", "batom",
]


def _is_pesca(product_name: str) -> bool:
    """Verifica se o produto é de pesca e não está na blocklist."""
    name_lower = product_name.lower()
    if any(bw in name_lower for bw in BLOCKLIST_KEYWORDS):
        return False
    return any(kw in name_lower for kw in PESCA_KEYWORDS)


def _parse_price(price_str: str) -> float:
    """Converte string de preço BR para float."""
    try:
        clean = price_str.replace('"', '').replace('R$', '').strip()
        if ',' in clean and '.' in clean:
            clean = clean.replace('.', '').replace(',', '.')
        elif ',' in clean:
            clean = clean.replace(',', '.')
        return float(clean)
    except (ValueError, AttributeError):
        return 0.0


def _download_and_parse_csv(url: str, max_rows: int = 5000) -> list:
    """Baixa e parseia um CSV do feed da Shopee, retornando produtos de pesca."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/csv,text/plain,*/*"
    }
    products = []
    try:
        print(f"   ⬇️  Baixando datafeed de pesca: {url[:80]}...")
        resp = requests.get(url, headers=headers, timeout=120, stream=True)
        resp.raise_for_status()

        # Detecta encoding do CSV
        content = resp.content.decode('utf-8-sig', errors='replace')
        reader = csv.DictReader(io.StringIO(content), delimiter=',')

        count = 0
        for row in reader:
            if count >= max_rows:
                break

            # Mapeia colunas mais comuns do datafeed Shopee
            name = (
                row.get('product_name') or
                row.get('title') or
                row.get('name') or
                row.get('item_name') or
                ''
            ).strip()

            if not name or not _is_pesca(name):
                continue

            price_raw = (
                row.get('sale_price') or
                row.get('price') or
                row.get('min_price') or
                '0'
            ).strip()
            price = _parse_price(price_raw)
            if price <= 0:
                continue

            product_url = (
                row.get('product_link') or
                row.get('affiliate_link') or
                row.get('link') or
                row.get('url') or
                ''
            ).strip()
            if not product_url:
                continue

            image_url = (
                row.get('image_link') or
                row.get('image') or
                row.get('thumbnail') or
                ''
            ).strip()

            products.append({
                'id_interno': row.get('item_id', '') or row.get('id', f'pesca_{count}'),
                'titulo': name,
                'preco': price,
                'url_produto': product_url,
                'link_afiliado': product_url,
                'imagem_url': image_url,
                'fonte': 'shopee_datafeed_pesca'
            })
            count += 1

        print(f"   ✅ {len(products)} produtos de pesca encontrados neste feed.")
    except Exception as e:
        print(f"   ❌ Erro ao processar datafeed: {e}")

    return products


def get_pesca_products(max_items: int = 2000) -> list:
    """
    Ponto de entrada principal.
    Lê PESCA_SHOPEE_DATAFEED_URLS (separado do bot de moda) e retorna
    uma lista embaralhada de produtos de pesca, limitada a max_items.
    """
    # Usa variável exclusiva do bot de pesca — sem tocar nas vars do bot de moda
    raw_urls = os.getenv("PESCA_SHOPEE_DATAFEED_URLS", "")

    if not raw_urls:
        # Fallback: usa as mesmas URLs do bot de moda mas filtra só pesca
        raw_urls = os.getenv("SHOPEE_DATAFEED_URLS", "")
        if raw_urls:
            print("⚠️  PESCA_SHOPEE_DATAFEED_URLS não definido — usando SHOPEE_DATAFEED_URLS como fallback.")
        else:
            print("❌ ERRO: Nenhuma URL de datafeed encontrada (PESCA_SHOPEE_DATAFEED_URLS).")
            return []

    # Suporta múltiplas URLs separadas por "|" ou quebra de linha
    separators = ["|", "\n", ";"]
    urls = [raw_urls]
    for sep in separators:
        if sep in raw_urls:
            urls = [u.strip() for u in raw_urls.split(sep) if u.strip()]
            break

    all_products = []
    for url in urls:
        batch = _download_and_parse_csv(url, max_rows=max_items)
        all_products.extend(batch)

    # Remove duplicatas por título
    seen = set()
    unique = []
    for p in all_products:
        key = p['titulo'].lower().strip()
        if key not in seen:
            seen.add(key)
            unique.append(p)

    random.shuffle(unique)
    result = unique[:max_items]
    print(f"📦 Total de produtos únicos de pesca disponíveis: {len(result)}")
    return result
