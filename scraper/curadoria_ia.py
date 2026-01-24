"""
Curadoria Inteligente de Produtos usando Groq LLM
Usa Llama 3.3 70B para escolher o melhor produto baseado no termo de busca
"""

import os
import json
from groq import Groq
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar cliente Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def decidir_melhor_oferta(termo_busca: str, produtos: list) -> int:
    """
    Usa IA para escolher o melhor produto baseado no termo de busca
    
    Args:
        termo_busca: O que o usuário está procurando (ex: "iPhone 15")
        produtos: Lista de dicionários com id_interno, titulo, preco, loja
        
    Returns:
        Índice (id_interno) do melhor produto
        
    Raises:
        ValueError: Se a IA retornar ID inválido
        Exception: Se houver erro na API
    """
    
    # Preparar dados para a IA (sem mostrar links)
    catalogo_limpo = []
    for i, p in enumerate(produtos):
        catalogo_limpo.append({
            "id_interno": i,
            "titulo": p.get('title', p.get('titulo', '')),
            "preco": p.get('price', p.get('preco', 0)),
            "loja": p.get('store', p.get('loja', ''))
        })
    
    # Prompt otimizado
    prompt = f"""Você é um especialista em comparação de preços.

BUSCA DO USUÁRIO: "{termo_busca}"

PRODUTOS ENCONTRADOS:
{json.dumps(catalogo_limpo, indent=2, ensure_ascii=False)}

REGRAS:
1. Ignore acessórios (capas, películas, carregadores) a menos que o usuário peça explicitamente
2. Ignore produtos usados/recondicionados/vitrine a menos que o usuário peça
3. Priorize produtos novos e completos que atendem EXATAMENTE o que o usuário quer
4. Se houver empate, escolha o de menor preço
5. Se nenhum produto for relevante, escolha o mais próximo do que o usuário quer

TAREFA:
Retorne APENAS o número do "id_interno" do melhor produto.
Não explique, não adicione texto, apenas o número.

RESPOSTA:"""

    try:
        print(f"[IA] Consultando Groq Llama 3.3 70B...")
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Melhor modelo gratuito
            messages=[
                {
                    "role": "system",
                    "content": "Você é um assistente especializado em comparação de produtos. Responda APENAS com números."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1,  # Baixa temperatura = mais determinístico
            max_tokens=10,     # Só precisa de 1-2 tokens (o número)
            top_p=1,
            stream=False
        )
        
        # Extrair resposta
        resposta = response.choices[0].message.content.strip()
        print(f"[IA] Resposta bruta: '{resposta}'")
        
        # Tentar converter para inteiro
        try:
            id_vencedor = int(resposta)
        except ValueError:
            # Se a IA retornou texto, tentar extrair o número
            import re
            numeros = re.findall(r'\d+', resposta)
            if numeros:
                id_vencedor = int(numeros[0])
            else:
                raise ValueError(f"IA não retornou um número válido: {resposta}")
        
        # Validar se o ID está no range
        if not (0 <= id_vencedor < len(produtos)):
            raise ValueError(f"IA retornou ID inválido: {id_vencedor} (range: 0-{len(produtos)-1})")
        
        print(f"[IA] ✅ Produto escolhido: ID {id_vencedor}")
        print(f"[IA] → {catalogo_limpo[id_vencedor]['titulo'][:50]}...")
        print(f"[IA] → R$ {catalogo_limpo[id_vencedor]['preco']:.2f} na {catalogo_limpo[id_vencedor]['loja']}")
        
        return id_vencedor
        
    except Exception as e:
        print(f"[IA] ❌ Erro: {e}")
        raise


def decidir_com_fallback(termo_busca: str, produtos: list) -> int:
    """
    Versão com fallback: se a IA falhar, escolhe o menor preço
    
    Args:
        termo_busca: O que o usuário está procurando
        produtos: Lista de produtos
        
    Returns:
        Índice do melhor produto (sempre retorna algo)
    """
    try:
        # Tentar usar IA
        return decidir_melhor_oferta(termo_busca, produtos)
    except Exception as e:
        print(f"[IA] ⚠️ Fallback ativado: {e}")
        print(f"[IA] Escolhendo produto de menor preço...")
        
        # Fallback: escolher menor preço
        id_vencedor = min(
            enumerate(produtos),
            key=lambda x: x[1].get('price', x[1].get('preco', float('inf')))
        )[0]
        
        print(f"[IA] ✅ Fallback: Produto ID {id_vencedor} (menor preço)")
        return id_vencedor


# Teste rápido
if __name__ == "__main__":
    print("🧪 Testando Curadoria com IA...\n")
    
    # Produtos de exemplo
    produtos_teste = [
        {
            "id_interno": 0,
            "titulo": "Capa para iPhone 15 Transparente",
            "preco": 29.90,
            "loja": "Shopee"
        },
        {
            "id_interno": 1,
            "titulo": "iPhone 15 128GB Novo Lacrado",
            "preco": 4200.00,
            "loja": "Amazon"
        },
        {
            "id_interno": 2,
            "titulo": "iPhone 15 128GB Vitrine",
            "preco": 3800.00,
            "loja": "Mercado Livre"
        }
    ]
    
    termo = "iPhone 15"
    print(f"Buscando: '{termo}'\n")
    
    try:
        id_escolhido = decidir_com_fallback(termo, produtos_teste)
        print(f"\n✅ Melhor produto: {produtos_teste[id_escolhido]['titulo']}")
        print(f"   R$ {produtos_teste[id_escolhido]['preco']:.2f} na {produtos_teste[id_escolhido]['loja']}")
    except Exception as e:
        print(f"\n❌ Erro no teste: {e}")
