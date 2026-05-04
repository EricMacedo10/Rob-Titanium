import os
import random
from core.editorial_engine import TitaniumEditorial

def _get_real_products_for_article():
    """Busca 5 produtos reais do Datafeed para enriquecer o artigo."""
    try:
        from scraper.datafeed_shopee import get_datafeed_products
        products = get_datafeed_products(max_items=30)
        selected = random.sample(products, min(5, len(products)))
        lines = []
        for p in selected:
            lines.append(f"- {p['titulo']} | R$ {p['preco']:.2f} | Loja: {p.get('shop_name', 'Shopee')}")
        return "\n".join(lines)
    except Exception as e:
        print(f"[Info] Datafeed indisponível para Editorial: {e}")
        return ""

def auto_generate_weekly_article():
    """Escolhe um tema de tendência e gera um artigo completo com produtos reais"""
    temas = [
        "Looks de Trabalho: Como unir Conforto e Elegância com Alfaiataria Shopee",
        "Tendências de Maquiagem 2026: O que não pode faltar na sua necessaire",
        "Moda Fitness Shopee: Os melhores tecidos e conjuntos para treinar com estilo",
        "Guia de Calçados: Do Tênis Casual ao Salto Luxo por preços imbatíveis",
        "Acessórios que Transformam: Como usar Semijoias e Bolsas Shopee para elevar o look",
        "Skincare Noturno: A rotina completa com achados de beleza internacionais",
        "Moda Praia 2026: Os biquínis e saídas de praia que são febre no verão",
        "Vestidos de Festa: Opções deslumbrantes para casamentos e eventos sociais"
    ]
    
    # Escolhe um tema aleatório
    tema_escolhido = random.choice(temas)
    print(f"[Automação] Tema da Semana: {tema_escolhido}")
    
    # Busca produtos reais para enriquecer o conteúdo
    produtos_reais = _get_real_products_for_article()
    if produtos_reais:
        print(f"[Automação] Injetando 5 produtos reais do Datafeed no artigo.")
    
    engine = TitaniumEditorial()
    
    # Extrai palavras-chave simplificadas do tema para SEO
    keywords = ", ".join([w for w in tema_escolhido.split() if len(w) > 3])
    
    # Injeta produtos reais no tema se disponíveis
    tema_com_produtos = tema_escolhido
    if produtos_reais:
        tema_com_produtos += f"\n\nProdutos reais para citar no artigo (com preços atuais da Shopee):\n{produtos_reais}"
    
    artigo_html = engine.generate_article(tema_com_produtos, keywords)
    
    if artigo_html:
        # Gera slug amigável
        slug = tema_escolhido.lower().split(':')[0].replace(' ', '-').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ã', 'a').replace('õ', 'o')
        slug = "".join([c for c in slug if c.isalnum() or c == '-'])
        
        # Salva o arquivo HTML
        engine.save_article(slug, artigo_html)
        
        # Atualiza o index.html com o novo card (Rotação)
        update_index_editorial(slug, tema_escolhido, artigo_html)

def update_index_editorial(slug, title, html_content):
    """Rotaciona os cards de editorial no index.html"""
    import re
    from bs4 import BeautifulSoup
    
    index_path = 'site/index.html'
    if not os.path.exists(index_path):
        print(f"[Erro] {index_path} não encontrado.")
        return

    # Extrai um resumo curto (primeiro parágrafo ou frase significativa)
    soup = BeautifulSoup(html_content, 'html.parser')
    p_text = soup.get_text().strip().split('\n')[0]
    resumo = (p_text[:120] + '...') if len(p_text) > 120 else p_text
    
    # Imagem padrão baseada no tema (ou fallback)
    img_map = {
        "vestidos": "images/fashion_post_01.jpg",
        "maquiagem": "images/beauty-hero.png",
        "skincare": "images/beauty-hero.png",
        "trabalho": "images/fashion_post_01.jpg",
        "inverno": "images/fashion_post_02.jpg",
        "praia": "images/fashion-hero.png",
        "fitness": "images/fashion_post_01.jpg",
        "acessorios": "images/fashion_post_02.jpg"
    }
    
    selected_img = "images/fashion-hero.png"
    for key, img in img_map.items():
        if key in title.lower():
            selected_img = img
            break

    category = "Tendências"
    if "maquiagem" in title.lower() or "skincare" in title.lower() or "beleza" in title.lower():
        category = "Beleza & Skincare"
    elif "trabalho" in title.lower() or "alfaiataria" in title.lower():
        category = "Moda & Estilo"

    new_card = f"""<!-- EDITORIAL_LATEST -->
                <a href="blog.html?slug={slug}" class="article-card">
                    <div class="article-image" style="background-image: url('{selected_img}');"></div>
                    <div class="article-content">
                        <span style="color: #FF4500; font-weight: 700; font-size: 0.8rem; text-transform: uppercase;">{category}</span>
                        <h3>{title.split(':')[0]}</h3>
                        <p>{resumo}</p>
                    </div>
                </a>"""

    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Rotação: 
    # 1. Pega o conteúdo de LATEST e joga para MID
    # 2. Pega o conteúdo de MID e joga para OLD
    # 3. Insere o NEW em LATEST
    
    try:
        # Extrai os cards atuais
        latest_match = re.search(r'<!-- EDITORIAL_LATEST -->(.*?)<!-- EDITORIAL_MID -->', content, re.DOTALL)
        mid_match = re.search(r'<!-- EDITORIAL_MID -->(.*?)<!-- EDITORIAL_OLD -->', content, re.DOTALL)
        
        if latest_match and mid_match:
            current_latest = latest_match.group(1).strip()
            current_mid = mid_match.group(1).strip()
            
            # Novo MID é o antigo LATEST
            new_mid = f"<!-- EDITORIAL_MID -->\n                {current_latest}"
            # Novo OLD é o antigo MID
            new_old = f"<!-- EDITORIAL_OLD -->\n                {current_mid}"
            
            # Aplica as substituições
            # Primeiro o OLD para não perder a referência do MID
            content = re.sub(r'<!-- EDITORIAL_OLD -->.*?</a>', new_old, content, flags=re.DOTALL)
            # Depois o MID para não perder a referência do LATEST
            content = re.sub(r'<!-- EDITORIAL_MID -->.*?<!-- EDITORIAL_OLD -->', new_mid + "\n                <!-- EDITORIAL_OLD -->", content, flags=re.DOTALL)
            # Por fim o LATEST
            content = re.sub(r'<!-- EDITORIAL_LATEST -->.*?<!-- EDITORIAL_MID -->', new_card + "\n                <!-- EDITORIAL_MID -->", content, flags=re.DOTALL)
            
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[Sucesso] index.html atualizado com rotação de editorial: {slug}")
        else:
            print("[Erro] Marcadores de editorial não encontrados no index.html")
    except Exception as e:
        print(f"[Erro] Falha ao rotacionar editorial: {e}")

if __name__ == "__main__":
    auto_generate_weekly_article()

