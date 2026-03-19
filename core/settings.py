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
    "mercadolivre": "ericmacedo"
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
# Quanto maior, mais seguro. AUMENTADO para máxima proteção.
MIN_DELAY = 8  # Aumentado de 5 para 8 segundos
MAX_DELAY = 20 # Aumentado de 15 para 20 segundos

# 3. Lista de Produtos para Monitorar
# TESTE COMPLETO: Todas as 13 categorias
# Foco em produtos até R$ 1000 (parte inteira)

# TESTE RÁPIDO (Comentado - usando teste completo agora)
"""
TARGETS = [
    {
        "term": "mouse gamer",
        "store": "amazon",
        "max_price": 1000.00,
        "category": "tecnologia"
    },
    {
        "term": "fone bluetooth",
        "store": "amazon",
        "max_price": 1000.00,
        "category": "tecnologia"
    },
    {
        "term": "teclado gamer",
        "store": "amazon",
        "max_price": 1000.00,
        "category": "tecnologia"
    }
]
"""

# CATEGORIAS COMPLETAS E EXTENDIDAS - BOUTIQUE DE MODA (MÊS DAS MÃES)
TARGETS = [
    # 👗 MODA FEMININA - ALFAIATARIA & CASUAL
    {"term": "conjunto alfaiataria feminino colete calca", "store": "mercadolivre", "max_price": 300.00, "category": "moda"},
    {"term": "calca pantalona alfaiataria feminina", "store": "mercadolivre", "max_price": 200.00, "category": "moda"},
    {"term": "blazer feminino max alongado", "store": "shopee", "max_price": 250.00, "category": "moda"},
    {"term": "saia midi alfaiataria fenda", "store": "shopee", "max_price": 150.00, "category": "moda"},
    {"term": "vestido midi canelado fenda", "store": "shopee", "max_price": 150.00, "category": "moda"},
    {"term": "vestido longo fluido elegante", "store": "mercadolivre", "max_price": 300.00, "category": "moda"},
    {"term": "calca jeans wide leg cintura alta", "store": "shopee", "max_price": 180.00, "category": "moda"},
    {"term": "camisa social feminina manga longa", "store": "shopee", "max_price": 150.00, "category": "moda"},
    {"term": "blusa tricot feminino modal", "store": "shopee", "max_price": 120.00, "category": "moda"},
    {"term": "jaqueta couro ecologico feminina", "store": "mercadolivre", "max_price": 250.00, "category": "moda"},
    
    # 👜 ACESSÓRIOS & PERFUMARIA PREMIUM (AMAZON)
    {"term": "bolsa feminina couro legitimo", "store": "amazon", "max_price": 800.00, "category": "acessorios"},
    {"term": "bolsa schutz", "store": "amazon", "max_price": 1000.00, "category": "acessorios"},
    {"term": "perfume feminino importado", "store": "amazon", "max_price": 800.00, "category": "perfumaria"},
    {"term": "perfume carolina herrera", "store": "amazon", "max_price": 900.00, "category": "perfumaria"},
    {"term": "relogio feminino tommy", "store": "amazon", "max_price": 1000.00, "category": "acessorios"},
    {"term": "colar prata 925 ponto luz", "store": "amazon", "max_price": 300.00, "category": "joias"},
    {"term": "kit maquiagem profissional", "store": "amazon", "max_price": 500.00, "category": "beleza"},
    {"term": "batom mac matte", "store": "amazon", "max_price": 200.00, "category": "beleza"},
]

# 📅 CATEGORIAS SAZONAIS (Ative conforme a época do ano)
# Descomente as categorias relevantes para a época:

SEASONAL_TARGETS = {
    "natal": [  # Novembro-Dezembro
        {"term": "presente natal", "max_price": 500.00},
        {"term": "decoração natal", "max_price": 200.00},
        {"term": "brinquedo infantil", "max_price": 300.00}
    ],
    "dia_das_maes": [  # Abril-Maio
        {"term": "perfume feminino", "max_price": 400.00},
        {"term": "joia prata", "max_price": 300.00},
        {"term": "kit spa", "max_price": 200.00}
    ],
    "dia_dos_pais": [  # Julho-Agosto
        {"term": "kit churrasco", "max_price": 300.00},
        {"term": "relógio masculino", "max_price": 500.00},
        {"term": "perfume masculino", "max_price": 400.00}
    ],
    "black_friday": [  # Novembro
        {"term": "smart tv", "max_price": 1000.00},
        {"term": "notebook", "max_price": 1000.00},
        {"term": "smartphone", "max_price": 1000.00}
    ]
}

# Para ativar categorias sazonais, descomente a linha abaixo e escolha a categoria:
# TARGETS.extend([{**item, "store": "amazon", "category": "sazonal"} for item in SEASONAL_TARGETS["natal"]])
