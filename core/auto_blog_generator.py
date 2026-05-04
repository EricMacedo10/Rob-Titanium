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
    """Gera 3 novos artigos (um por categoria) para renovação total do Editorial"""
    temas_por_categoria = {
        "Moda & Estilo": [
            "Vestidos de Festa: Opções deslumbrantes para casamentos e eventos sociais",
            "Looks de Trabalho: Como unir Conforto e Elegância com Alfaiataria Shopee",
            "Moda Fitness Shopee: Os melhores tecidos e conjuntos para treinar com estilo",
            "Moda Praia 2026: Os biquínis e saídas de praia que são febre no verão"
        ],
        "Beleza & Skincare": [
            "Tendências de Maquiagem 2026: O que não pode faltar na sua necessaire",
            "Skincare Noturno: A rotina completa com achados de beleza internacionais",
            "Skincare Diário: Proteção e hidratação com os melhores produtos da Shopee",
            "Segredos do Skincare Coreano: Por que o K-Beauty conquistou o mundo"
        ],
        "Tendências": [
            "Guia de Calçados: Do Tênis Casual ao Salto Luxo por preços imbatíveis",
            "Acessórios que Transformam: Como usar Semijoias e Bolsas para elevar o look",
            "Gadgets de Beleza: Ferramentas tecnológicas que estão revolucionando o autocuidado",
            "Smart Shopping: Como identificar as melhores ofertas de luxo na Shopee"
        ]
    }
    
    engine = TitaniumEditorial()
    artigos_gerados = []

    for categoria, lista_temas in temas_por_categoria.items():
        tema_escolhido = random.choice(lista_temas)
        print(f"[Automação] Gerando para {categoria}: {tema_escolhido}")
        
        # Busca produtos reais para enriquecer o conteúdo
        produtos_reais = _get_real_products_for_article()
        
        # Extrai palavras-chave simplificadas
        keywords = ", ".join([w for w in tema_escolhido.split() if len(w) > 3])
        
        # Injeta produtos reais no tema
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
            
            # Prepara dados para o index
            artigos_gerados.append({
                "slug": slug,
                "title": tema_escolhido,
                "category": categoria,
                "content": artigo_html
            })

    if len(artigos_gerados) == 3:
        update_all_editorial_slots(artigos_gerados)

def update_all_editorial_slots(artigos):
    """Atualiza simultaneamente os 3 slots do editorial no index.html"""
    import re
    from bs4 import BeautifulSoup
    
    index_path = 'site/index.html'
    if not os.path.exists(index_path):
        print(f"[Erro] {index_path} não encontrado.")
        return

    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Mapeamento de imagens para cada slot
    img_map = {
        "Moda & Estilo": "images/fashion_post_01.jpg",
        "Beleza & Skincare": "images/beauty-hero.png",
        "Tendências": "images/fashion_post_02.jpg"
    }

    slots = ["LATEST", "MID", "OLD"]
    
    for i, article in enumerate(artigos):
        slot_name = slots[i]
        
        # Extrai resumo
        soup = BeautifulSoup(article['content'], 'html.parser')
        p_text = soup.get_text().strip().split('\n')[0]
        resumo = (p_text[:120] + '...') if len(p_text) > 120 else p_text
        
        selected_img = img_map.get(article['category'], "images/fashion-hero.png")
        
        new_card = f"""<!-- EDITORIAL_{slot_name} -->
                <a href="blog.html?slug={article['slug']}" class="article-card">
                    <div class="article-image" style="background-image: url('{selected_img}');"></div>
                    <div class="article-content">
                        <span style="color: #FF4500; font-weight: 700; font-size: 0.8rem; text-transform: uppercase;">{article['category']}</span>
                        <h3>{article['title'].split(':')[0]}</h3>
                        <p>{resumo}</p>
                    </div>
                </a>"""
        
        # Substituição específica do slot
        pattern = f"<!-- EDITORIAL_{slot_name} -->.*?</a>"
        content = re.sub(pattern, new_card, content, flags=re.DOTALL)

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("[Sucesso] Editorial Titanium renovado com 3 novas categorias!")

if __name__ == "__main__":
    auto_generate_weekly_article()

