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
    
    # 💻 TECNOLOGIA
    {"term": "fone bluetooth", "store": "amazon", "max_price": 1000.00, "category": "tecnologia"},
    {"term": "mouse gamer", "store": "amazon", "max_price": 1000.00, "category": "tecnologia"},
    {"term": "teclado gamer", "store": "amazon", "max_price": 1000.00, "category": "tecnologia"},
    {"term": "monitor pc pc", "store": "amazon", "max_price": 1000.00, "category": "tecnologia"},
    {"term": "caixa de som bluetooth", "store": "amazon", "max_price": 1000.00, "category": "tecnologia"},
    {"term": "ssd 1tb", "store": "amazon", "max_price": 1000.00, "category": "tecnologia"},
    {"term": "pendrive 64gb", "store": "amazon", "max_price": 1000.00, "category": "tecnologia"},
    {"term": "carregador portátil powerbank", "store": "amazon", "max_price": 1000.00, "category": "tecnologia"},
    {"term": "webcam full hd", "store": "amazon", "max_price": 1000.00, "category": "tecnologia"},
    
    # 🏠 CASA E COZINHA
    {"term": "air fryer", "store": "amazon", "max_price": 1000.00, "category": "casa"},
    {"term": "liquidificador", "store": "amazon", "max_price": 1000.00, "category": "casa"},
    {"term": "panela elétrica", "store": "amazon", "max_price": 1000.00, "category": "casa"},
    {"term": "aspirador de pó robô", "store": "amazon", "max_price": 1000.00, "category": "casa"},
    {"term": "jogo de panelas antiaderente", "store": "amazon", "max_price": 1000.00, "category": "casa"},
    {"term": "pipoqueira elétrica", "store": "amazon", "max_price": 1000.00, "category": "casa"},
    {"term": "mixer de mão", "store": "amazon", "max_price": 1000.00, "category": "casa"},
    {"term": "cafeteira", "store": "amazon", "max_price": 1000.00, "category": "casa"},
    {"term": "ferro de passar", "store": "amazon", "max_price": 1000.00, "category": "casa"},
    
    # 💪 FITNESS E ESPORTES
    {"term": "halteres", "store": "amazon", "max_price": 1000.00, "category": "esportes"},
    {"term": "tapete yoga", "store": "amazon", "max_price": 1000.00, "category": "esportes"},
    {"term": "corda de pular", "store": "amazon", "max_price": 1000.00, "category": "esportes"},
    {"term": "whey protein", "store": "amazon", "max_price": 1000.00, "category": "esportes"},
    {"term": "garrafa térmica", "store": "amazon", "max_price": 1000.00, "category": "esportes"},
    {"term": "kit elástico extensor", "store": "amazon", "max_price": 1000.00, "category": "esportes"},
    
    # 💄 BELEZA E CUIDADOS
    {"term": "kit maquiagem", "store": "amazon", "max_price": 1000.00, "category": "beleza"},
    {"term": "secador cabelo", "store": "amazon", "max_price": 1000.00, "category": "beleza"},
    {"term": "escova secadora", "store": "amazon", "max_price": 1000.00, "category": "beleza"},
    {"term": "chapinha de cabelo", "store": "amazon", "max_price": 1000.00, "category": "beleza"},
    {"term": "protetor solar facial", "store": "amazon", "max_price": 1000.00, "category": "beleza"},
    {"term": "kit skincare", "store": "amazon", "max_price": 1000.00, "category": "beleza"},
    
    # 🟡 MERCADO LIVRE - Produtos com link de afiliado automático!
    {"term": "fone bluetooth", "store": "mercadolivre", "max_price": 300.00, "category": "tecnologia"},
    {"term": "smartwatch", "store": "mercadolivre", "max_price": 500.00, "category": "tecnologia"},
    {"term": "cafeteira expresso", "store": "mercadolivre", "max_price": 800.00, "category": "casa"},
    {"term": "ventilador de mesa", "store": "mercadolivre", "max_price": 300.00, "category": "casa"},
    {"term": "cadeira de escritório", "store": "mercadolivre", "max_price": 1000.00, "category": "casa"},
    {"term": "mochila notebook", "store": "mercadolivre", "max_price": 400.00, "category": "tecnologia"},
    
    # 🟠 SHOPEE - Ofertas via API Oficial
    {"term": "fone bluetooth", "store": "shopee", "max_price": 300.00, "category": "tecnologia"},
    {"term": "kit cozinha", "store": "shopee", "max_price": 500.00, "category": "casa"},
    {"term": "maquiagem kit", "store": "shopee", "max_price": 200.00, "category": "beleza"},
    {"term": "capinha celular", "store": "shopee", "max_price": 100.00, "category": "tecnologia"},
    {"term": "organizador de gavetas", "store": "shopee", "max_price": 100.00, "category": "casa"},
    {"term": "luminária de mesa", "store": "shopee", "max_price": 150.00, "category": "casa"},
    
    # 🔵 LOMADEE (Estrutura ativa para testes no STAGING)
    # (Comentado ou removido, conforme original mantido mas expandido acima)
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
