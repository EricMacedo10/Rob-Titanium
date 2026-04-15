# Configurações do Robô Titanium
# IMPORTANTE: Preencha com seus IDs de Afiliado abaixo

import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# 1. Configurações de Afiliado
AFFILIATE_TAGS = {
    "shopee": "shopee_affiliate",  # Gerenciado via API Dinâmica
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

# 3. Lista de Produtos para Monitorar (BOUTIQUE EXCLUSIVE - 100% SHOPEE)
TARGETS = [
    # 👗 MODA FEMININA (Categoria #1 Shopee)
    {"term": "conjunto alfaiataria feminino luxo", "store": "shopee", "max_price": 400.00, "category": "moda"},
    {"term": "vestido midi canelado elegante", "store": "shopee", "max_price": 200.00, "category": "moda"},
    {"term": "calca pantalona linho premium", "store": "shopee", "max_price": 250.00, "category": "moda"},
    {"term": "blazer feminino alongado forrado", "store": "shopee", "max_price": 300.00, "category": "moda"},
    {"term": "body poliamida decote quadrado", "store": "shopee", "max_price": 100.00, "category": "moda"},
    {"term": "saia midi alfaiataria fenda", "store": "shopee", "max_price": 200.00, "category": "moda"},
    {"term": "macaquinho feminino transpassado", "store": "shopee", "max_price": 250.00, "category": "moda"},
    {"term": "tshirt algodão pima feminina", "store": "shopee", "max_price": 120.00, "category": "moda"},
    {"term": "vestido longo festa fluido", "store": "shopee", "max_price": 500.00, "category": "moda"},
    {"term": "jaqueta couro ecologico feminina", "store": "shopee", "max_price": 350.00, "category": "moda"},
    
    # 💄 BELEZA & SKINCARE (Categoria #2 Shopee)
    {"term": "kit pinceis maquiagem profissional", "store": "shopee", "max_price": 300.00, "category": "beleza"},
    {"term": "serum vitamina c skin care", "store": "shopee", "max_price": 150.00, "category": "beleza"},
    {"term": "paleta de sombras matte nude", "store": "shopee", "max_price": 200.00, "category": "beleza"},
    {"term": "base maquiagem alta cobertura", "store": "shopee", "max_price": 150.00, "category": "beleza"},
    {"term": "mascara cilios volume shopee", "store": "shopee", "max_price": 100.00, "category": "beleza"},
    {"term": "kit limpeza facial profunda", "store": "shopee", "max_price": 300.00, "category": "beleza"},
    {"term": "batom matte longa duracao", "store": "shopee", "max_price": 80.00, "category": "beleza"},
    {"term": "secador de cabelo profissional", "store": "shopee", "max_price": 500.00, "category": "beleza"},
    {"term": "chapinha nano titanium original", "store": "shopee", "max_price": 400.00, "category": "beleza"},
    {"term": "babyliss modelador cachos", "store": "shopee", "max_price": 250.00, "category": "beleza"}
]

# 📅 CAMPANHAS SAZONAIS (Foco em Presentes Shopee)
SEASONAL_TARGETS = {
    "dia_dos_namorados": [
        {"term": "lingerie luxo renda", "max_price": 200.00},
        {"term": "perfume feminino importado", "max_price": 500.00}
    ],
    "dia_das_maes": [
        {"term": "bolsa feminina luxo couro", "max_price": 400.00},
        {"term": "kit semi joias banhadas", "max_price": 300.00}
    ]
}

