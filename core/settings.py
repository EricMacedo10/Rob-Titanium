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

# CATEGORIAS COMPLETAS E EXTENDIDAS - PARA SORTEIO DIÁRIO
TARGETS = [
    # 🎒 VOLTA ÀS AULAS
    {"term": "mochila escolar", "store": "amazon", "max_price": 1000.00, "category": "volta-aulas"},
    {"term": "caderno universitário", "store": "amazon", "max_price": 1000.00, "category": "volta-aulas"},
    {"term": "estojo escolar", "store": "amazon", "max_price": 1000.00, "category": "volta-aulas"},
    {"term": "caneta esferográfica kit", "store": "amazon", "max_price": 1000.00, "category": "volta-aulas"},
    {"term": "fichário escolar", "store": "amazon", "max_price": 1000.00, "category": "volta-aulas"},
    {"term": "lápis de cor 24 cores", "store": "amazon", "max_price": 1000.00, "category": "volta-aulas"},
    
    # 💻 TECNOLOGIA & GADGETS
    {"term": "fone bluetooth", "store": "amazon", "max_price": 1000.00, "category": "tecnologia"},
    {"term": "mouse gamer rg", "store": "amazon", "max_price": 1000.00, "category": "tecnologia"},
    {"term": "teclado mecânico", "store": "amazon", "max_price": 1000.00, "category": "tecnologia"},
    {"term": "suporte celular mesa", "store": "amazon", "max_price": 1000.00, "category": "tecnologia"},
    {"term": "caixa de som led", "store": "amazon", "max_price": 1000.00, "category": "tecnologia"},
    {"term": "projetor portátil h300", "store": "amazon", "max_price": 1000.00, "category": "tecnologia"},
    {"term": "smartband m8", "store": "amazon", "max_price": 1000.00, "category": "tecnologia"},
    
    # 🏠 CASA & UTILIDADES CRIATIVAS
    {"term": "dispenser detergente pia", "store": "amazon", "max_price": 1000.00, "category": "casa"},
    {"term": "umidificador de ar chama", "store": "amazon", "max_price": 1000.00, "category": "casa"},
    {"term": "luminária pôr do sol", "store": "amazon", "max_price": 1000.00, "category": "casa"},
    {"term": "mini processador alimentos", "store": "amazon", "max_price": 1000.00, "category": "casa"},
    {"term": "fita led rgb 5m", "store": "amazon", "max_price": 1000.00, "category": "casa"},
    {"term": "garrafa de água motivacional", "store": "amazon", "max_price": 1000.00, "category": "casa"},
    {"term": "kit organizador geladeira", "store": "amazon", "max_price": 1000.00, "category": "casa"},

    # 💄 BELEZA & CUIDADOS
    {"term": "massageador facial elétrico", "store": "amazon", "max_price": 1000.00, "category": "beleza"},
    {"term": "kit pincel maquiagem", "store": "amazon", "max_price": 1000.00, "category": "beleza"},
    {"term": "espelho led maquiagem", "store": "amazon", "max_price": 1000.00, "category": "beleza"},
    
    # 🟡 MERCADO LIVRE - "O QUE TODO MUNDO QUER"
    {"term": "fone lenovo lp40", "store": "mercadolivre", "max_price": 150.00, "category": "tecnologia"},
    {"term": "tv box 4k", "store": "mercadolivre", "max_price": 400.00, "category": "tecnologia"},
    {"term": "aspirador portatil carro", "store": "mercadolivre", "max_price": 200.00, "category": "casa"},
    {"term": "maquina de cortar cabelo", "store": "mercadolivre", "max_price": 150.00, "category": "beleza"},
    
    # 🟠 SHOPEE - "ACHADINHOS"
    {"term": "mini ventilador portatil", "store": "shopee", "max_price": 100.00, "category": "casa"},
    {"term": "carregador iphone cabo", "store": "shopee", "max_price": 100.00, "category": "tecnologia"},
    {"term": "organizador de fios", "store": "shopee", "max_price": 50.00, "category": "tecnologia"},
    {"term": "ring light mesa", "store": "shopee", "max_price": 100.00, "category": "tecnologia"},
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
