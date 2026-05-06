# -*- coding: utf-8 -*-
"""
Radar Sensual: IA DeepSeek configurada para o nicho de Bem-Estar Íntimo.
Lê do data_sensual.json e gera o ai_reviews_sensual.json.
"""

import os
import sys
import json

# Adiciona o diretorio raiz ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.review_engine import TitaniumRadar

class SensualRadar(TitaniumRadar):
    def __init__(self):
        super().__init__()
        # Prioriza a chave específica Sensual se existir no .env ou Environment
        self.api_key = os.getenv("DEEPSEEK_API_KEY_SENSUAL") or os.getenv("DEEPSEEK_API_KEY")
        
        # Sobrescreve os arquivos para o nicho Sensual
        self.data_file = 'site/data_sensual.json'
        self.output_file = 'site/ai_reviews_sensual.json'

    def _ask_deepseek(self, product):
        """Customização do Prompt para o nicho Sensual (Dicionário de Sofisticação)"""
        # Injetamos a categoria sensual antes de mandar para o motor principal
        product['category'] = "Bem-Estar Íntimo / SexTech"
        
        # Criamos o prompt específico de luxo
        prompt = f"""
        Você é a Consultora de Estilo da Boutique Íntima Titanium. 
        Sua missão é descrever produtos de SexTech, Moda Íntima e Cosmética Sensorial de forma extremamente luxuosa, 
        técnica e empoderada, fugindo de qualquer vulgaridade.
        Escreva um parágrafo curto, sofisticado e persuasivo (máximo 60 palavras) explicando por que este item é essencial para o bem-estar íntimo.
        
        Produto: {product['title']}
        Categoria: {product['category']}
        Preço: R$ {product['price']}
        
        REGRAS DE OURO:
        1. NUNCA use termos vulgares (tesão, gozar, brinquedo erótico).
        2. Use termos como: 'autoconhecimento', 'ritual sensorial', 'design ergonômico', 'tecnologia aveludada', 'experiência premium'.
        3. O foco deve ser em LUXO, TECNOLOGIA e BEM-ESTAR.
        
        Assine apenas como '- IA Titanium'.
        """
        
        # Usamos a lógica de rede do pai, mas com o NOSSO prompt
        return self._send_to_deepseek(prompt)

    def _send_to_deepseek(self, prompt):
        """Apenas a parte de rede, usando os cabeçalhos e URL do pai"""
        import requests
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "Você é uma Consultora de Bem-Estar e Luxo."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 150
        }
        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content'].strip()
        except Exception as e:
            print(f"[Erro API] {e}")
            return None

if __name__ == "__main__":
    print("[IA] Gerando Radar de Tendências: Boutique Íntima...")
    radar = SensualRadar()
    # No motor original, generate_reviews faz o sorteio e salva no self.output_file
    radar.generate_reviews()
