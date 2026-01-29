import json
import random
import os

def generate_dynamic_phrases(products):
    """
    Gera frases dinâmicas baseadas nos produtos encontrados.
    Simula uma 'IA' selecionando o destaque do momento.
    """
    phrases = [
        "Aproveite as ofertas do dia! Os estoques podem acabar a qualquer momento.",
        "Nossa família selecionou o que há de melhor para você economizar.",
        "Se virem o ícone de 🔥, é porque a oferta está muito quente!"
    ]
    
    # Extrair categorias e produtos de destaque
    if products:
        # Tentar pegar o produto com maior desconto
        try:
            top_deal = max(products, key=lambda x: x.get('discount', 0))
            if top_deal and top_deal.get('discount', 0) > 20:
                phrases.append(f"Destaque: {top_deal['title'][:30]}... com {top_deal['discount']}% OFF!")
        except:
            pass
            
        # Frase baseada na categoria mais frequente
        try:
            categories = [p.get('category') for p in products if p.get('category')]
            if categories:
                top_category = max(set(categories), key=categories.count)
                phrases.append(f"Hoje é dia de {top_category}! Confira as melhores opções.")
        except:
            pass

    # Garantir formato JSON correto para o site
    notification_data = {
        "notifications": [
            {
                "id": 1,
                "text": p,
                "time": "Agora",
                "icon": "fa-fire" if "quente" in p or "OFF" in p else "fa-comment"
            } for i, p in enumerate(phrases[:5]) # Limitar a 5 frases
        ]
    }
    
    # Salvar no arquivo que o site lê
    output_path = os.path.join("site", "notifications.json")
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(notification_data, f, indent=4, ensure_ascii=False)
        print(f"✅ Frases dinâmicas atualizadas em {output_path}")
    except Exception as e:
        print(f"❌ Erro ao salvar frases: {e}")

if __name__ == "__main__":
    # Teste isolado
    mock_products = [
        {"title": "Notebook Gamer", "discount": 35, "category": "tecnologia"},
        {"title": "Geladeira", "discount": 10, "category": "casa"}
    ]
    generate_dynamic_phrases(mock_products)
