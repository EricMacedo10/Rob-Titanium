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

# CATEGORIAS COMPLETAS - TESTE COMPLETO
TARGETS = [
    # 🎒 VOLTA ÀS AULAS (Janeiro-Fevereiro)
    {
        "term": "mochila escolar",
        "store": "amazon",
        "max_price": 1000.00,
        "category": "volta-aulas"
    },
    {
        "term": "caderno universitário",
        "store": "amazon",
        "max_price": 1000.00,
        "category": "volta-aulas"
    },
    {
        "term": "estojo escolar",
        "store": "amazon",
        "max_price": 1000.00,
        "category": "volta-aulas"
    },
    
    # 💻 TECNOLOGIA (Sempre relevante)
    {
        "term": "fone bluetooth",
        "store": "amazon",
        "max_price": 1000.00,
        "category": "tecnologia"
    },
    {
        "term": "mouse gamer",
        "store": "amazon",
        "max_price": 1000.00,
        "category": "tecnologia"
    },
    {
        "term": "teclado gamer",
        "store": "amazon",
        "max_price": 1000.00,
        "category": "tecnologia"
    },
    
    # 🏠 CASA E COZINHA
    {
        "term": "air fryer",
        "store": "amazon",
        "max_price": 1000.00,
        "category": "casa"
    },
    {
        "term": "liquidificador",
        "store": "amazon",
        "max_price": 1000.00,
        "category": "casa"
    },
    {
        "term": "panela elétrica",
        "store": "amazon",
        "max_price": 1000.00,
        "category": "casa"
    },
    
    # 💪 FITNESS E ESPORTES
    {
        "term": "halteres",
        "store": "amazon",
        "max_price": 1000.00,
        "category": "esportes"
    },
    {
        "term": "tapete yoga",
        "store": "amazon",
        "max_price": 1000.00,
        "category": "esportes"
    },
    
    # 💄 BELEZA E CUIDADOS
    {
        "term": "kit maquiagem",
        "store": "amazon",
        "max_price": 1000.00,
        "category": "beleza"
    },
    {
        "term": "secador cabelo",
        "store": "amazon",
        "max_price": 1000.00,
        "category": "beleza"
    },
    
    # 🟡 MERCADO LIVRE - Produtos com link de afiliado automático!
    {
        "term": "fone bluetooth",
        "store": "mercadolivre",
        "max_price": 300.00,
        "category": "tecnologia"
    },
    {
        "term": "smartwatch",
        "store": "mercadolivre",
        "max_price": 500.00,
        "category": "tecnologia"
    },
    {
        "term": "cafeteira expresso",
        "store": "mercadolivre",
        "max_price": 800.00,
        "category": "casa"
    },
    
    # 🟠 SHOPEE - Ofertas via API Oficial
    {
        "term": "fone bluetooth",
        "store": "shopee",
        "max_price": 300.00,
        "category": "tecnologia"
    },
    {
        "term": "kit cozinha",
        "store": "shopee",
        "max_price": 500.00,
        "category": "casa"
    },
    {
        "term": "maquiagem kit",
        "store": "shopee",
        "max_price": 200.00,
        "category": "beleza"
    }
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
