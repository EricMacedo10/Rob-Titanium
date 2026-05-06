import json
import os
import random

def auto_curate_sensual_platinum():
    """
    🦾 Motor de Curadoria Inteligente para Boutique Sensual.
    Seleciona automaticamente os melhores produtos do feed geral
    baseado em critérios de 'Luxo' e 'Performance'.
    """
    data_source = 'site/data_sensual.json'
    output_file = 'site/specialist_sensual.json'
    
    if not os.path.exists(data_source):
        print(f"[Erro] Fonte de dados {data_source} não encontrada.")
        return

    try:
        with open(data_source, 'r', encoding='utf-8') as f:
            products = json.load(f)
        
        if not products:
            print("[Aviso] Nenhum produto encontrado no feed sensual.")
            return

        # --- LÓGICA DE SELEÇÃO SMART LUXO ---
        # 1. Filtra apenas itens com imagem e título
        valid_items = [p for p in products if p.get('image') and p.get('title')]
        
        # 2. Score de Qualidade: Prioriza itens com maior preço (Luxo) e maior desconto
        # Peso: Preço (70%) + Desconto (30%)
        for p in valid_items:
            price = float(p.get('price', 0))
            discount = float(p.get('discount', 0))
            p['quality_score'] = (price * 0.7) + (discount * 2.0) # Desconto tem multiplicador para ser atrativo

        # 3. Ordena pelo Score e pega os Top 60 para sorteio
        top_candidates = sorted(valid_items, key=lambda x: x['quality_score'], reverse=True)[:60]
        
        # 4. Sorteia 24 para a vitrine (Freshness)
        selected_platinum = random.sample(top_candidates, min(24, len(top_candidates)))

        # 5. Salva o resultado
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(selected_platinum, f, ensure_ascii=False, indent=4)
            
        print(f"[Sucesso] Seleção da Especialista Sensual gerada com {len(selected_platinum)} itens de elite.")

    except Exception as e:
        print(f"[Erro] Falha na curadoria automática: {e}")

if __name__ == "__main__":
    auto_curate_sensual_platinum()
