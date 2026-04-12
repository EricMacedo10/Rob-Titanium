import os
import random
from editorial_engine import TitaniumEditorial

def auto_generate_weekly_article():
    """Escolhe um tema de tendência e gera um artigo completo"""
    temas = [
        "Looks de Trabalho: Como unir Conforto e Elegância com Alfaiataria Shopee",
        "Tendências de Maquiagem 2026: O que não pode faltar na sua necessaire",
        "Moda Fitness Shopee: Os melhores tecidos e conjuntos para treinar com estilo",
        "Guia de Calçados: Do Tênis Casual ao Salto Luxo por preços imbatíveis",
        "Acessórios que Transformam: Como usar Semijoias e Bolsas Shopee para elevar o look",
        "Skincare Noturno: A rotina completa com achados de beleza internacionais",
        "Moda Praia 2026: Os biquínis e saídas de praia que são febre no verão",
        "Vestidos de Festa: Opções deslumbrantes para casamentos e eventos sociais"
    ]
    
    # Escolhe um tema aleatório
    tema_escolhido = random.choice(temas)
    print(f"[Automação] Tema da Semana: {tema_escolhido}")
    
    engine = TitaniumEditorial()
    engine.generate_article(tema_escolhido)

if __name__ == "__main__":
    auto_generate_weekly_article()
