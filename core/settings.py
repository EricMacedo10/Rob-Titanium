# Configurações do Robô Titanium
# IMPORTANTE: Preencha com seus IDs de Afiliado abaixo

import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# 1. Configurações de Afiliado
AFFILIATE_TAGS = {
    "amazon": os.getenv("AMAZON_AFFILIATE_TAG", "guiadodesco00-20"),
    "shopee": "shopee_affiliate",  # Gerenciado via API
}

# Shopee API Configuration
SHOPEE_APP_ID = os.getenv("SHOPEE_APP_ID", "")
SHOPEE_SECRET = os.getenv("SHOPEE_SECRET", "")
SHOPEE_API_URL = "https://partner.shopeemobile.com/graphql"

# Lomadee API Configuration
LOMADEE_APP_TOKEN = os.getenv("LOMADEE_APP_TOKEN", "")
LOMADEE_SOURCE_ID = os.getenv("LOMADEE_SOURCE_ID", "")
LOMADEE_API_URL = f"https://api.lomadee.com/v3/{LOMADEE_APP_TOKEN}/offer/_search"


# 2. Configurações de Segurança (Anti-Ban)
# Tempo de espera entre cada busca (em segundos). 
MIN_DELAY = 8
MAX_DELAY = 20

# 3. Lista de Produtos para Monitorar (REBALANCEADA 50/50 - AMAZON/SHOPEE)
TARGETS = [
    # 📱 TECNOLOGIA
    {"term": "iphone 15 plus", "store": "amazon", "max_price": 6000.00, "category": "tecnologia"},
    {"term": "samsung galaxy s24", "store": "amazon", "max_price": 5000.00, "category": "tecnologia"},
    {"term": "notebook dell inspiron", "store": "amazon", "max_price": 4000.00, "category": "tecnologia"},
    {"term": "fone jbl bluetooth", "store": "shopee", "max_price": 400.00, "category": "tecnologia"},
    {"term": "monitor gamer curvo", "store": "amazon", "max_price": 1500.00, "category": "tecnologia"},
    
    # 👗 MODA
    {"term": "conjunto alfaiataria feminino", "store": "shopee", "max_price": 300.00, "category": "moda"},
    {"term": "calca pantalona feminina", "store": "shopee", "max_price": 200.00, "category": "moda"},
    {"term": "blazer feminino alongado", "store": "shopee", "max_price": 250.00, "category": "moda"},
    {"term": "bolsa schutz leather", "store": "amazon", "max_price": 1000.00, "category": "moda"},
    {"term": "tenis casual feminino", "store": "shopee", "max_price": 300.00, "category": "moda"},
    
    # 🏠 CASA & DECOR
    {"term": "sofa retratil cinza", "store": "shopee", "max_price": 2500.00, "category": "casa"},
    {"term": "luminaria mesa retro", "store": "shopee", "max_price": 150.00, "category": "casa"},
    {"term": "jogo de panelas ceramic", "store": "amazon", "max_price": 800.00, "category": "casa"},
    {"term": "kit toalha banho luxo", "store": "amazon", "max_price": 250.00, "category": "casa"},
    
    # 💄 BELEZA
    {"term": "perfume carolina herrera", "store": "amazon", "max_price": 600.00, "category": "beleza"},
    {"term": "maquiagem batom mac", "store": "amazon", "max_price": 150.00, "category": "beleza"},
    {"term": "kit skincare cerave", "store": "amazon", "max_price": 300.00, "category": "beleza"},

    # 🍳 ELETRODOMÉSTICOS / ELETRO
    {"term": "geladeira duplex frost free", "store": "amazon", "max_price": 4000.00, "category": "eletro"},
    {"term": "air fryer mundial", "store": "shopee", "max_price": 400.00, "category": "eletro"},

    # 🚗 AUTOMOTIVO
    {"term": "pneu aro 15", "store": "shopee", "max_price": 500.00, "category": "automotivo"},
    {"term": "central multimidia", "store": "shopee", "max_price": 800.00, "category": "automotivo"}
]

# 📅 CATEGORIAS SAZONAIS
SEASONAL_TARGETS = {
    "natal": [
        {"term": "presente natal", "max_price": 500.00},
        {"term": "decoração natal", "max_price": 200.00}
    ],
    "dia_das_maes": [
        {"term": "perfume feminino", "max_price": 400.00},
        {"term": "joia prata", "max_price": 300.00}
    ]
}
