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
    
    engine.generate_article(tema_com_produtos, keywords)

if __name__ == "__main__":
    auto_generate_weekly_article()

