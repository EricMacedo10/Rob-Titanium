import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class TitaniumEditorial:
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.api_url = "https://api.deepseek.com/chat/completions"
        
    def generate_article(self, topic, keywords):
        """Usa DeepSeek-V3.2 para criar um artigo de alta autoridade para o AdSense"""
        print(f"[Info] Solicitando artigo sobre: {topic}...")
        
        prompt = f"""
        Você é uma Editora de Moda Sênior da revista Vogue e especialista em tendências da Shopee.
        Escreva um artigo de blog luxuoso, informativo e otimizado para SEO sobre: '{topic}'.
        
        REGRAS CRÍTICAS:
        1. Público-alvo: Mulheres que buscam elegância com economia (Moda Shopee Luxo).
        2. Tamanho: Mínimo de 1000 palavras.
        3. Estrutura: Use <h1> para o título, <h2> e <h3> para seções, e parágrafos detalhados.
        4. E-E-A-T: Use um tom de especialista que testou os produtos e conhece a qualidade dos tecidos.
        5. Palavras-chave: {keywords}.
        6. Formato: Retorne APENAS o código HTML (dentro de uma <div>) para ser inserido direto no site.
        7. Não use placeholders. Escreva o conteúdo completo.
        8. Adicione uma seção final de 'Dicas de Lavagem e Cuidados' para aumentar a utilidade.
        9. Ao final do artigo, assine sempre como: 'IA Titanium, Curadoria Inteligente & Especialista em Tendências Shopee'.
        """
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "Você é uma especialista em redação SEO de Moda e Beleza."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except Exception as e:
            print(f"[Erro] Falha ao gerar artigo: {e}")
            return None

    def save_article(self, slug, content):
        """Salva o artigo em HTML no diretório do blog"""
        out_dir = 'site/blog'
        os.makedirs(out_dir, exist_ok=True)
        filename = f"{out_dir}/{slug}.html"
        
        # Template simples para o artigo
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[Sucesso] Artigo salvo com sucesso: {filename}")

if __name__ == "__main__":
    hub = TitaniumEditorial()
    
    artigos_para_gerar = [
        {
            "slug": "guia-alfaiataria-luxo",
            "topico": "Guia Definitivo: Alfaiataria Feminina Luxo na Shopee",
            "palavras": "alfaiataria feminino, moda shopee, conjunto luxo barato, como usar blazer"
        },
        {
            "slug": "segredos-skincare-coreano",
            "topico": "Os 5 Segredos do Skincare Coreano disponíveis na Shopee",
            "palavras": "skincare coreano, produtos beleza shopee, rotina facial, k-beauty brasil"
        },
        {
            "slug": "tendencia-inverno-jaqueta-couro",
            "topico": "Tendências Inverno 2026: A Ascensão da Jaqueta de Couro Ecológico",
            "palavras": "jaqueta couro ecologico, tendencias inverno 2026, moda feminina shopee, looks inverno"
        }
    ]
    
    for info in artigos_para_gerar:
        artigo_html = hub.generate_article(info['topico'], info['palavras'])
        if artigo_html:
            hub.save_article(info['slug'], artigo_html)
