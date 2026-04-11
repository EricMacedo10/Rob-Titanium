import json
import random
import os

def generate_dynamic_phrases(products):
    """
    Gera frases dinâmicas baseadas nos produtos encontrados na Shopee.
    Simula o Robô Titanium monitorando a API em tempo real.
    """
    base_phrases = [
        "🔥 ALERTA: Detectei novas quedas de preço na Shopee AGORA!",
        "🎫 DICA: Lembre de ativar seus Cupons de Frete Grátis no App.",
        "🛡️ SEGURANÇA: Todas as ofertas de hoje são de Vendedores Oficiais.",
        "📱 APP FIRST: Links otimizados para abrir direto no seu App Shopee.",
        "🤖 MONITOR: Robô Titanium sincronizado com a Shopee API v2."
    ]
    
    # Extrair destaques reais da curadoria
    if products:
        try:
            # Pegar o maior desconto do catálogo
            top_deal = max(products, key=lambda x: x.get('discount', 0))
            if top_deal and top_deal.get('discount', 0) > 15:
                base_phrases.append(f"✨ ACHADO: {top_deal['title'][:25]}... está com {top_deal['discount']}% OFF!")
        except:
            pass
            
        # Frase baseada no volume de ofertas
        if len(products) > 20:
            base_phrases.append(f"🛍️ Temos {len(products)} peças auditadas na vitrine de hoje!")

    # Sortear 5 frases para não repetir sempre
    selected_phrases = random.sample(base_phrases, min(len(base_phrases), 5))

    notification_data = {
        "notifications": [
            {
                "id": i + 1,
                "text": p,
                "time": "Agora",
                "icon": "fa-fire" if "🔥" in p else ("fa-ticket-alt" if "🎫" in p else "fa-robot")
            } for i, p in enumerate(selected_phrases)
        ]
    }
    
    output_path = os.path.join("site", "notifications.json")
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(notification_data, f, indent=4, ensure_ascii=False)
        print(f"✅ Maestro: Frases Shopee atualizadas em {output_path}")
    except Exception as e:
        print(f"❌ Erro ao salvar frases: {e}")

if __name__ == "__main__":
    # Teste de Boutique Fashion
    mock_products = [
        {"title": "Vestido Midi Elegante", "discount": 45, "category": "moda"},
        {"title": "Bolsa Luxo Couro", "discount": 30, "category": "acessorios"}
    ]
    generate_dynamic_phrases(mock_products)
