import json
from social.bot import SocialBot

def run_multi_brand_test():
    bot = SocialBot()
    offers = bot.load_offers()
    
    # Selecionar um de cada marca para o teste
    test_offers = []
    brands = ["amazon", "shopee", "mercado livre"]
    
    for brand in brands:
        for offer in offers:
            if offer['store'].lower() == brand:
                test_offers.append(offer)
                break
    
    print(f"🚀 Iniciando Teste Multi-Marca com {len(test_offers)} produtos.")
    
    for i, offer in enumerate(test_offers):
        print(f"\n🎬 [{offer['store']}] Processando: {offer['title']}")
        
        output_name = f"social/test_triade_{brand_to_filename(offer['store'])}.jpg"
        
        # Gerar Legenda
        caption = bot.copywriter.generate_caption(
            offer['title'], 
            str(offer['price']), 
            offer['store'],
            offer.get('discount', 0),
            offer.get('category', 'default')
        )
        
        # Gerar Arte
        try:
            bot.gen.generate_post(
                offer['title'],
                str(offer['price']),
                offer['image'],
                offer['store'].lower().replace(" ", ""),
                output_name,
                format="post"
            )
            print(f"✅ Arte gerada: {output_name}")
            print(f"📝 Legenda:\n{caption[:100]}...")
        except Exception as e:
            print(f"❌ Erro: {e}")

def brand_to_filename(brand):
    return brand.lower().replace(" ", "")

if __name__ == "__main__":
    run_multi_brand_test()
