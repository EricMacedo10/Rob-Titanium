# -*- coding: utf-8 -*-
"""
Minerador de Acessórios Premium Amazon - Dia das Mães
Injeta 20 acessórios de alto padrão no arquivo principal de produção (data.json)
para compor o "Look Completo" com os vestidos e pantalonas. 👜⌚✨
"""

import os
import sys
import json
import time
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from engines.amazon import search_amazon

def run_amazon_injector():
    print("👜 INICIANDO INJEÇÃO DE ACESSÓRIOS AMAZON NO BANCO MESTRE...")
    
    # 20 Queries específicas de Alta Conversão de Presentes na Amazon Brasil
    targets = [
        {"q": "bolsa moleca feminina lancamento", "tag": "#bolsa"},
        {"q": "bolsa colcci feminina", "tag": "#bolsa"},
        {"q": "bolsa santa lolla feminina", "tag": "#bolsa"},
        {"q": "bolsa transversal modare bege", "tag": "#bolsa"},
        {"q": "relogio champion feminino dourado", "tag": "#relogio"},
        {"q": "relogio mondaine feminino prata", "tag": "#relogio"},
        {"q": "relogio casio vintage feminino", "tag": "#relogio"},
        {"q": "relogio condor feminino rose gold", "tag": "#relogio"},
        {"q": "perfume carolina herrera good girl feminino", "tag": "#perfume"},
        {"q": "perfume lancome la vie est belle", "tag": "#perfume"},
        {"q": "perfume calvin klein euphoria feminino", "tag": "#perfume"},
        {"q": "perfume boticario lily tradicional", "tag": "#perfume"},
        {"q": "kit pincel maquiagem macrilan profissional", "tag": "#make"},
        {"q": "paleta de sombras ruby rose classica", "tag": "#make"},
        {"q": "base liquida bruna tavares alta", "tag": "#make"},
        {"q": "mascara de cilios maybelline sky", "tag": "#make"},
        {"q": "carteira feminina santa lolla matelasse", "tag": "#carteira"},
        {"q": "carteira feminina slim couro legitimo", "tag": "#carteira"},
        {"q": "colar prata 925 feminino coracao ponto", "tag": "#joia"},
        {"q": "brinco argola feminina romantica premium", "tag": "#joia"}
    ]

    # Carrega a base atual (Os 80 a 100 vestuários recém minerados)
    data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../site/data.json'))
    
    if os.path.exists(data_path):
        with open(data_path, 'r', encoding='utf-8') as f:
            production_db = json.load(f)
    else:
        production_db = []
        
    print(f"📦 Base atual possui: {len(production_db)} roupas da ML e Shopee")
    print(f"🔮 Injetando {len(targets)} Alvos Avançados da Amazon...")

    new_items = 0
    
    try:
        for idx, target in enumerate(targets):
            print(f"\n[{idx+1}/{len(targets)}] 🔎 Buscando Amazon: {target['q']}")
            
            res = search_amazon(target['q'])
            if res:
                # Customizar o item para padrão de Jóias/Acessórios
                res['category'] = "acessorios_amazon"
                res['added_date'] = "2026-03-20"
                res['tags'] = [target['tag']]
                
                production_db.append(res)
                new_items += 1
                print(f"💎 Amazon Entregou: {res['title'][:50]}... R$ {res['price']}")
            else:
                print(f"⚠️ Alvo cego: {target['q']}")
            
            # Pausa humana de 10s entre buscas na Amazon para evitar CAPTCHAs pesados
            time.sleep(random.uniform(5, 8))

        # Embaralhar a lista de PRODUÇÃO no final!
        # Isso garante que no site fique 1 vestuário ML, 1 Shopee, 1 Perfume Amazon, de forma misturada!
        random.shuffle(production_db)

        # Salva o arquivo Mestre com os acessórios injetados
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(production_db, f, indent=4, ensure_ascii=False)
            
        print(f"\n✨ SUCESSO ABSOLUTO! O Banco Mestre de Dia das Mães agora possui {len(production_db)} itens Premium.")
        print(f"👜 Total de Acessórios Amazon importados na rodada: {new_items}")

    except Exception as e:
        print(f"❌ Erro na mineração Amazon: {e}")

if __name__ == "__main__":
    run_amazon_injector()
