"""
Shopee Datafeed Integration (100K Products)
Baixa, parseia e filtra os CSVs massivos do Feed de Produto da Shopee.
Foco exclusivo: Moda & Beleza.

Uso:
    from scraper.datafeed_shopee import get_datafeed_products
    products = get_datafeed_products(max_items=500)
"""

import os
import csv
import json
import time
import requests
import random
import io
from dotenv import load_dotenv

load_dotenv()

# Cache local para evitar downloads repetidos na mesma execução
CACHE_FILE = "site/datafeed_cache.json"
CACHE_MAX_AGE_HOURS = 12  # Redownload se cache tiver mais de 12h

# Filtro de categorias: Moda & Beleza APENAS
MODA_KEYWORDS = [
    "vestido", "blusa", "calça", "conjunto", "saia", "body", "macaquinho",
    "macacão", "cropped", "blazer", "cardigan", "pijama", "lingerie",
    "sutiã", "calcinha", "legging", "jaqueta", "casaco", "shorts", "short",
    "regata", "camiseta", "tricot", "moletom", "kimono", "pantalona",
    "alfaiataria", "fitness", "academia", "camisola", "sobretudo",
    "parka", "poncho", "meia", "cinta", "modeladora", "baby doll",
    "camisa", "bermuda", "calção", "collant", "top", "mula manca",
    "wide leg", "cargo", "flare", "skinny", "mom", "jeans", "denim",
]

BELEZA_KEYWORDS = [
    "maquiagem", "batom", "base", "sombra", "rímel", "máscara", "sérum",
    "skincare", "perfume", "hidratante", "protetor", "shampoo", "condicionador",
    "secador", "chapinha", "babyliss", "pincel", "paleta", "delineador",
    "corretivo", "pó", "blush", "gloss", "esmalte", "creme", "óleo",
    "tratamento capilar", "tônico", "agua micelar",
]

ALL_KEYWORDS = MODA_KEYWORDS + BELEZA_KEYWORDS

# Bloqueio Temporário: Estimuladores e SexTech Explícito
# Conforme solicitado pelo USER (Bloqueio nos links de 100K)
BLOCKLIST_KEYWORDS = [
    "vibrador", "sugador", "clitoris", "clitóris", "estimulador", 
    "masturbador", "plug anal", "sex toy", "brinquedo erótico",
    "massageador íntimo", "bullet", "wand", "ovo masturbador",
    "lingerie aberta", "fio dental aberto", "cápsula discreto",
    "pompoarismo", "ponto g", "consolador", "algema", "chicote",
    "vibratório", "vibratoria", "prazer íntimo", "prazer intimo"
]


def _is_moda_beleza(product_name: str) -> bool:
    """Verifica se o produto pertence ao nicho Moda & Beleza e NÃO está na blocklist."""
    name_lower = product_name.lower()
    
    # 1. Bloqueio Mandatório
    if any(bw in name_lower for bw in BLOCKLIST_KEYWORDS):
        return False
        
    # 2. Pertencimento ao Nicho
    return any(kw in name_lower for kw in ALL_KEYWORDS)


def _parse_price(price_str: str) -> float:
    """Converte string de preço BR para float."""
    try:
        clean = price_str.replace('"', '').replace('R$', '').strip()
        # Formato BR: 1.299,99 -> 1299.99
        if ',' in clean and '.' in clean:
            clean = clean.replace('.', '').replace(',', '.')
        elif ',' in clean:
            clean = clean.replace(',', '.')
        return float(clean)
    except (ValueError, AttributeError):
        return 0.0


def _parse_commission_rate(rate_str: str) -> float:
    """Converte string de comissão para float percentual."""
    try:
        clean = rate_str.replace('"', '').replace('%', '').replace(',', '.').strip()
        return float(clean)
    except (ValueError, AttributeError):
        return 0.0


def _download_and_parse_csv(url: str) -> list:
    """Baixa um CSV do Datafeed e retorna lista de produtos parseados."""
    print(f"[Datafeed] Baixando CSV: {url[:80]}...")
    
    try:
        resp = requests.get(url, timeout=120, stream=True)
        resp.raise_for_status()
        
        # Decodifica o conteúdo
        content = resp.content.decode('utf-8-sig')
        # 🛡️ IDENTIFICAÇÃO DINÂMICA DE SEPARADOR & CABEÇALHO
        # Shopee às vezes muda entre , e ;
        delimiter = ';' if ';' in content[:1000] else ','
        reader = csv.reader(io.StringIO(content), delimiter=delimiter)
        
        header = next(reader, None)
        if not header:
            print("[Datafeed] CSV vazio ou sem cabeçalho.")
            return []
        
        col_map = {}
        header_lower = [h.strip().lower().replace('"', '') for h in header]
        
        for i, col in enumerate(header_lower):
            # Mapeamento Flexível (Aceita variações de nome de coluna PT/EN)
            if any(k in col for k in ['item id', 'id do item', 'id_item']):
                col_map['id'] = i
            elif any(k in col for k in ['item name', 'nome do item', 'titulo', 'title']):
                col_map['name'] = i
            elif any(k in col for k in ['price', 'preco', 'preço']):
                col_map['price'] = i
            elif 'sales' in col or 'vendas' in col:
                col_map['sales'] = i
            elif any(k in col for k in ['shop name', 'shop', 'nome da loja', 'loja']):
                col_map['shop'] = i
            elif any(k in col for k in ['commission rate', 'taxa de comissão', 'taxa_comissao']):
                col_map['commission_rate'] = i
            elif 'commission' in col and 'rate' not in col:
                col_map['commission'] = i
            elif any(k in col for k in ['product link', 'link do produto', 'url']):
                col_map['product_link'] = i
            elif any(k in col for k in ['offer link', 'link de oferta', 'link_afiliado']):
                col_map['offer_link'] = i
        
        print(f"[Datafeed] Colunas detectadas: {list(col_map.keys())}")
        
        products = []
        for row in reader:
            try:
                if len(row) < 8:
                    continue
                
                name = row[col_map.get('name', 1)].strip()
                if not name:
                    continue
                
                # Filtro de Moda & Beleza
                if not _is_moda_beleza(name):
                    continue
                
                price = _parse_price(row[col_map.get('price', 2)])
                if price <= 0 or price > 2000:
                    continue  # Filtro de preço razoável
                
                commission_rate = _parse_commission_rate(
                    row[col_map.get('commission_rate', 5)]
                )
                
                offer_link = row[col_map.get('offer_link', -1)].strip()
                product_link = row[col_map.get('product_link', -2)].strip()
                shop_name = row[col_map.get('shop', 4)].strip()
                
                products.append({
                    "id_interno": row[col_map.get('id', 0)].strip(),
                    "titulo": name,
                    "preco": price,
                    "loja": "Shopee",
                    "shop_name": shop_name,
                    "link_afiliado": offer_link if offer_link else product_link,
                    "url_produto": product_link,
                    "commission_rate": commission_rate,
                    "disponivel": True,
                    "source": "datafeed"
                })
                
            except (IndexError, KeyError):
                continue
        
        print(f"[Datafeed] {len(products)} produtos de Moda & Beleza filtrados.")
        return products
        
    except requests.RequestException as e:
        print(f"[Datafeed] Erro ao baixar CSV: {e}")
        return []
    except Exception as e:
        print(f"[Datafeed] Erro inesperado no parse: {e}")
        return []


def _load_cache() -> list:
    """Carrega o cache local se ainda for válido."""
    if not os.path.exists(CACHE_FILE):
        return []
    
    try:
        age_hours = (time.time() - os.path.getmtime(CACHE_FILE)) / 3600
        if age_hours > CACHE_MAX_AGE_HOURS:
            print(f"[Datafeed] Cache expirado ({age_hours:.1f}h). Redownloading...")
            return []
        
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"[Datafeed] Cache válido carregado: {len(data)} produtos (idade: {age_hours:.1f}h)")
        return data
    except (json.JSONDecodeError, OSError):
        return []


def _save_cache(products: list):
    """Salva o cache local."""
    try:
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False)
        print(f"[Datafeed] Cache salvo: {len(products)} produtos.")
    except Exception as e:
        print(f"[Datafeed] Aviso: Falha ao salvar cache: {e}")


def get_datafeed_urls() -> list:
    """
    Retorna as URLs do Datafeed.
    Prioridade: variável de ambiente > fallback para BatchProductLinks.csv
    """
    urls_env = os.getenv("SHOPEE_DATAFEED_URLS", "")
    if urls_env:
        return [u.strip() for u in urls_env.split("|") if u.strip()]
    return []


def get_datafeed_products(max_items: int = 500, force_refresh: bool = False) -> list:
    """
    Função principal: Retorna produtos do Datafeed filtrados para Moda & Beleza.
    
    Args:
        max_items: Número máximo de produtos a retornar
        force_refresh: Se True, ignora o cache
    
    Returns:
        Lista de dicts no formato padrão do Titanium
    """
    # 1. Tentar cache
    if not force_refresh:
        cached = _load_cache()
        if cached:
            # Embaralha para variar a seleção a cada execução
            random.shuffle(cached)
            return cached[:max_items]
    
    # 2. Baixar dos Datafeeds
    urls = get_datafeed_urls()
    if not urls:
        print("[Datafeed] Nenhuma URL de Datafeed configurada. Use SHOPEE_DATAFEED_URLS.")
        print("[Datafeed] Fallback: usando BatchProductLinks.csv local.")
        return _fallback_local_csv(max_items)
    
    all_products = []
    for url in urls:
        products = _download_and_parse_csv(url)
        all_products.extend(products)
        time.sleep(1)  # Pausa entre downloads
    
    if not all_products:
        print("[Datafeed] Datafeed vazio. Usando fallback local.")
        return _fallback_local_csv(max_items)
    
    # 3. Deduplicação por ID
    seen = set()
    unique = []
    for p in all_products:
        pid = p.get('id_interno', '')
        if pid not in seen:
            seen.add(pid)
            unique.append(p)
    
    print(f"[Datafeed] Total único Moda & Beleza: {len(unique)} produtos.")
    
    # 4. Salvar cache
    _save_cache(unique)
    
    # 5. Embaralhar e retornar
    random.shuffle(unique)
    return unique[:max_items]


def get_top_commission_products(count: int = 20) -> list:
    """Retorna os produtos com maior taxa de comissão (para maximizar ganhos)."""
    products = get_datafeed_products(max_items=5000)
    sorted_products = sorted(products, key=lambda x: x.get('commission_rate', 0), reverse=True)
    return sorted_products[:count]


def get_best_deals(count: int = 20, max_price: float = 200.0) -> list:
    """Retorna os melhores achados: alta comissão + preço acessível."""
    products = get_datafeed_products(max_items=5000)
    # Filtro de preço máximo + ordenação por comissão
    filtered = [p for p in products if p['preco'] <= max_price and p.get('commission_rate', 0) >= 10]
    sorted_products = sorted(filtered, key=lambda x: x.get('commission_rate', 0), reverse=True)
    return sorted_products[:count]


def _fallback_local_csv(max_items: int) -> list:
    """Fallback: lê o BatchProductLinks.csv local (seus 400 produtos curados)."""
    csv_file = "BatchProductLinks.csv"
    if not os.path.exists(csv_file):
        print(f"[Datafeed] Arquivo local {csv_file} não encontrado.")
        return []
    
    products = []
    try:
        with open(csv_file, mode='r', encoding='utf-8-sig') as f:
            lines = f.readlines()[1:]  # Pula cabeçalho
            for line in lines:
                clean_line = line.strip()
                if not clean_line:
                    continue
                if clean_line.startswith('"') and clean_line.endswith('"'):
                    clean_line = clean_line[1:-1]
                clean_line = clean_line.replace('""', '"')
                
                parts = next(csv.reader([clean_line]))
                
                if len(parts) >= 8:
                    price = _parse_price(parts[2])
                    products.append({
                        "id_interno": parts[0].strip(),
                        "titulo": parts[1].strip(),
                        "preco": price if price > 0 else 49.99,
                        "loja": "Shopee",
                        "shop_name": parts[4].strip() if len(parts) > 4 else "",
                        "link_afiliado": parts[-1].strip(),
                        "url_produto": parts[-2].strip(),
                        "commission_rate": _parse_commission_rate(parts[5]) if len(parts) > 5 else 10,
                        "disponivel": True,
                        "source": "local_csv"
                    })
    except Exception as e:
        print(f"[Datafeed] Erro ao ler CSV local: {e}")
    
    random.shuffle(products)
    return products[:max_items]


if __name__ == "__main__":
    print("🧪 Testando Datafeed Shopee...")
    products = get_datafeed_products(max_items=10)
    print(f"\nResultado: {len(products)} produtos")
    for p in products[:5]:
        print(f"  - {p['titulo'][:50]}... | R$ {p['preco']:.2f} | Comissão: {p.get('commission_rate', 0)}%")
