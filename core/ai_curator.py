"""
Curadoria Inteligente de Produtos usando DeepSeek-V3.2 (Speciale / Agentic)
O "Cérebro" do Robô Titanium para tomada de decisões de alta precisão.
"""

import os
import json
import requests
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = "https://api.deepseek.com/chat/completions"

def decidir_melhor_oferta(termo_busca: str, produtos: list) -> int:
    """
    Usa DeepSeek para escolher o melhor produto baseado no termo de busca
    """
    if not DEEPSEEK_API_KEY:
        print("[!] Erro: DEEPSEEK_API_KEY não configurada.")
        raise Exception("DEEPSEEK_API_KEY ausente")

    # Preparar dados para a IA (sem mostrar links para economizar tokens)
    catalogo_limpo = []
    for i, p in enumerate(produtos):
        catalogo_limpo.append({
            "id_interno": i,
            "titulo": p.get('title', p.get('titulo', '')),
            "preco": p.get('price', p.get('preco', 0)),
            "loja": p.get('store', p.get('loja', ''))
        })
    
    # Prompt otimizado para DeepSeek
    prompt = f"""Você é o cérebro da Boutique Titanium, especialista em moda e beleza.
ANALISE A BUSCA: "{termo_busca}"

PRODUTOS ENCONTRADOS NO NOSSO CATÁLOGO:
{json.dumps(catalogo_limpo, indent=2, ensure_ascii=False)}

REGRAS DE OURO:
1. FOCO TOTAL: Escolha o produto que melhor atende o desejo do usuário.
2. QUALIDADE: Priorize produtos novos e descrições completas.
3. ECONOMIA: Havendo empate técnico em relevância, escolha o de menor preço.
4. FILTRO: Ignore acessórios se o usuário busca o item principal.

TAREFA:
Responda APENAS o número do "id_interno" do vencedor. Sem explicações.

RESPOSTA:"""

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Você é um assistente de curadoria de elite que responde apenas IDs numéricos."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1,
        "max_tokens": 10
    }

    try:
        print(f"[IA Titanium] Consultando DeepSeek-V3.2 para curadoria de '{termo_busca}'...")
        response = requests.post(DEEPSEEK_BASE_URL, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        
        resultado = response.json()
        resposta = resultado['choices'][0]['message']['content'].strip()
        print(f"[IA Titanium] Decisão DeepSeek: ID {resposta}")
        
        # Tentar converter para inteiro
        import re
        numeros = re.findall(r'\d+', resposta)
        if numeros:
            id_vencedor = int(numeros[0])
            if 0 <= id_vencedor < len(produtos):
                return id_vencedor
        
        raise ValueError(f"IA retornou ID inválido: {resposta}")

    except Exception as e:
        print(f"[IA Titanium] [ERROR] Erro na API DeepSeek: {e}")
        raise

def decidir_com_fallback(termo_busca: str, produtos: list) -> int:
    try:
        return decidir_melhor_oferta(termo_busca, produtos)
    except Exception as e:
        print(f"[IA] Fallback: Escolhendo menor preço devido a erro na DeepSeek.")
        id_vencedor = min(
            enumerate(produtos),
            key=lambda x: x[1].get('price', x[1].get('preco', float('inf')))
        )[0]
        return id_vencedor

if __name__ == "__main__":
    # Teste rápido
    produtos_teste = [
        {"id_interno": 0, "titulo": "Capa Celular", "preco": 10.00, "store": "Shopee"},
        {"id_interno": 1, "titulo": "iPhone 15 Pro", "preco": 7000.00, "store": "Shopee"}
    ]
    print(decidir_com_fallback("iPhone 15", produtos_teste))
