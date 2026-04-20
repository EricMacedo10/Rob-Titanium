import os
import json
import random
import requests
from dotenv import load_dotenv

load_dotenv()

class TitaniumRadar:
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.api_url = "https://api.deepseek.com/chat/completions"
        self.data_file = 'site/data.json'
        self.output_file = 'site/ai_reviews.json'

    def generate_reviews(self):
        """Sorteia 3 produtos do pool combinado (site + datafeed) e gera reviews de elite com IA"""
        # Fonte 1: Produtos já no site
        site_products = []
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                site_products = json.load(f)

        # Fonte 2: Produtos frescos do Datafeed (Moda & Beleza)
        datafeed_products = []
        try:
            from scraper.datafeed_shopee import get_datafeed_products
            raw_feed = get_datafeed_products(max_items=50)
            # Normaliza para o formato do data.json
            for p in raw_feed:
                datafeed_products.append({
                    "title": p.get("titulo", "Produto Shopee"),
                    "price": p.get("preco", 0),
                    "category": "moda",
                    "link": p.get("link_afiliado", ""),
                    "store": "Shopee",
                    "source": "datafeed_100k"
                })
        except Exception as e:
            print(f"[Info] Datafeed indisponível para Radar: {e}")

        # Pool combinado (prioriza datafeed para novidade)
        all_products = datafeed_products + site_products
        
        if len(all_products) < 3:
            print("[Erro] Poucos produtos para o radar.")
            return

        # Sorteia 16 produtos aleatórios
        selected = random.sample(all_products, min(16, len(all_products)))
        print(f"[Info] Selecionados para o Radar: {[p['title'][:30] for p in selected]}")

        reviews = []
        for product in selected:
            review_text = self._ask_deepseek(product)
            if review_text:
                product['ai_review'] = review_text
                reviews.append(product)

        if reviews:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(reviews, f, ensure_ascii=False, indent=4)
            print(f"[Sucesso] Radar de Tendências atualizado: {self.output_file}")

    def _ask_deepseek(self, product):
        """Solicita um mini-review de luxo usando DeepSeek-V3.2"""
        prompt = f"""
        Você é a Consultora de Estilo da Boutique Titanium. 
        Escreva um parágrafo curto, sofisticado e persuasivo (máximo 60 palavras) explicando por que este produto é uma tendência imperdível agora.
        Produto: {product['title']}
        Categoria: {product['category']}
        Preço: R$ {product['price']}
        
        Tom: Luxuoso, direto e convincente. Use termos como 'essencial', 'sofisticação', 'tendência' ou 'curadoria'.
        Assine no final apenas como '- IA Titanium'.
        """
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "Você é uma Consultora de Moda de luxo."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 150
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content'].strip()
        except Exception as e:
            print(f"[Erro] Falha ao gerar review para {product['title']}: {e}")
            return None

if __name__ == "__main__":
    radar = TitaniumRadar()
    radar.generate_reviews()
