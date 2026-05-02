# -*- coding: utf-8 -*-
"""
Produção: Boutique Sensual Íntima - Minerador de Elite
Focado em SexTech, Moda Íntima e Cosmética Sensorial.
"""

import os
import sys
import json
import time
import random

# Adiciona o diretorio raiz ao path para importar modulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from engines.shopee_affiliate import search_shopee
except ImportError:
    from scraper.engines.shopee_affiliate import search_shopee

def refine_sensual_title(title):
    """
    Aplica o dicionário de sofisticação da IA Titanium (Documento 01)
    para evitar termos vulgares e manter o posicionamento Premium.
    """
    replacements = {
        "vibrador": "Estimulador de Precisão",
        "sugador de clitoris": "Tecnologia de Pulsação Air-Touch",
        "sugador": "Massageador de Pulsação",
        "sex toy": "Gadget de Bem-Estar",
        "brinquedo erótico": "Estimulador Sensorial",
        "lubrificante": "Sérum de Conforto Íntimo",
        "oleo de massagem": "Elixir Corporal Sensorial",
        "vela erotica": "Vela de Aromaterapia Sensorial",
        "lingerie": "Coleção Íntima de Luxo",
        "fantasia": "Traje Sensorial Temático"
    }
    
    refined = title
    for old, new in replacements.items():
        if old in refined.lower():
            # Tenta manter o case original se possível, ou apenas substitui
            import re
            refined = re.sub(re.escape(old), new, refined, flags=re.IGNORECASE)
    
    return refined

def run_sensual_miner():
    print("="*60)
    print("[Titanium] MINERADOR BOUTIQUE SENSUAL - FASE 1 (TESTE)")
    print("="*60)
    
    # Matriz de Busca baseada no Documento 01
    targets = [
        # SexTech (Prioridade 1 & 2)
        {"q": "sugador de clitoris air touch", "tag": "#sextech", "cat": "Tecnologia Íntima"},
        {"q": "vibrador bullet silencioso", "tag": "#precisao", "cat": "Tecnologia Íntima"},
        {"q": "vibrador com app bluetooth", "tag": "#connected", "cat": "Tecnologia Íntima"},
        {"q": "massageador varinha wand potente", "tag": "#power", "cat": "Tecnologia Íntima"},
        
        # Moda & Luxo (Prioridade 3)
        {"q": "lingerie de renda luxo preta", "tag": "#lingerie", "cat": "Moda & Luxo"},
        {"q": "camisola cetim com renda luxo", "tag": "#sleepwear", "cat": "Moda & Luxo"},
        {"q": "body renda sensual luxo", "tag": "#fashion", "cat": "Moda & Luxo"},
        {"q": "hobby cetim luxo", "tag": "#boutique", "cat": "Moda & Luxo"},
        
        # Cosmética Sensorial (Prioridade 4 & 6)
        {"q": "lubrificante intimo base agua premium", "tag": "#conforto", "cat": "Cosmética Sensorial"},
        {"q": "oleo de massagem corporal perfumado", "tag": "#elixir", "cat": "Cosmética Sensorial"},
        {"q": "vela de massagem aromaterapia", "tag": "#zen", "cat": "Cosmética Sensorial"},
        {"q": "spray hidratante intimo", "tag": "#care", "cat": "Cosmética Sensorial"}
    ]

    database = []
    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../site/data_sensual.json'))
    
    try:
        for idx, target in enumerate(targets):
            print(f"[{idx+1}/{len(targets)}] Minerando: {target['q']}")
            
            try:
                # Buscamos 8 itens por termo para compor a vitrine
                res_shp_list = search_shopee(target['q'], limit=8)
                
                for res_shp in res_shp_list:
                    # Filtro de qualidade: Apenas itens com imagem
                    if not res_shp.get('imagem'):
                        continue
                        
                    prod_shp = {
                        "id": f"sens_{int(time.time())}_{random.randint(100,999)}",
                        "title": refine_sensual_title(res_shp['titulo']),
                        "price": float(res_shp['preco']),
                        "old_price": round(float(res_shp['preco']) * 1.35, 2),
                        "discount": 35,
                        "store": "Shopee",
                        "category": target['cat'],
                        "image": res_shp['imagem'],
                        "link": res_shp['link_afiliado'],
                        "tags": [target['tag']],
                        "reason": "Titanium Choice: Bem-Estar Íntimo",
                        "added_date": time.strftime("%Y-%m-%d")
                    }
                    database.append(prod_shp)
                    print(f"   [OK] {prod_shp['title'][:40]}...")
            except Exception as e:
                print(f"   [!] Erro na busca: {e}")
                
            time.sleep(2) # Protecao de taxa API

        # Salva o banco de dados da Boutique Sensual
        if database:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(database, f, indent=4, ensure_ascii=False)
            print(f"\n[SUCESSO] {len(database)} produtos Sensuais carregados!")
            print(f"Arquivo data_sensual.json gerado em: {output_path}")
        else:
            print("\n[AVISO] Nenhum produto encontrado. Verifique as APIs.")

    except Exception as grand_error:
        print(f"ERRO FATAL: {grand_error}")

if __name__ == "__main__":
    run_sensual_miner()
