"""
API REST - Árbitro de Preços
Production-ready API com Flask seguindo best practices

Arquitetura:
- RESTful endpoints
- CORS configurado
- Rate limiting
- Error handling robusto
- Logging estruturado
- Health checks
- Validação de input
- Segurança (OWASP Top 10)
"""

import os
import sys
import logging
from datetime import datetime
from functools import wraps
from typing import Dict, Any

from flask import Flask, request, jsonify, g
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

# Adicionar path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scraper.arbitro_preco import ArbitroDePreco

# ============================================================================
# CONFIGURAÇÃO
# ============================================================================

app = Flask(__name__)

# CORS: Permitir apenas domínios específicos em produção
ALLOWED_ORIGINS = [
    "https://guiadodesconto.com.br",
    "http://localhost:3000",  # Dev frontend
    "http://127.0.0.1:5000"   # Dev local
]

CORS(app, resources={
    r"/api/*": {
        "origins": ALLOWED_ORIGINS,
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "max_age": 3600
    }
})

# Configuração de segurança
app.config['JSON_SORT_KEYS'] = False
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1MB max request size

# ============================================================================
# LOGGING ESTRUTURADO
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler('api_arbitro.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# ============================================================================
# RATE LIMITING (Simples, sem Redis)
# ============================================================================

from collections import defaultdict
from time import time

# Armazenamento em memória (para produção, usar Redis)
request_counts = defaultdict(list)

def rate_limit(max_requests: int = 10, window: int = 60):
    """
    Rate limiting decorator
    
    Args:
        max_requests: Máximo de requisições permitidas
        window: Janela de tempo em segundos
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # Identificar cliente (IP ou API key)
            client_id = request.headers.get('X-API-Key') or request.remote_addr
            
            now = time()
            
            # Limpar requisições antigas
            request_counts[client_id] = [
                req_time for req_time in request_counts[client_id]
                if now - req_time < window
            ]
            
            # Verificar limite
            if len(request_counts[client_id]) >= max_requests:
                logger.warning(f"Rate limit exceeded for {client_id}")
                return jsonify({
                    "erro": "Muitas requisições. Tente novamente em 1 minuto.",
                    "retry_after": window
                }), 429
            
            # Registrar requisição
            request_counts[client_id].append(now)
            
            return f(*args, **kwargs)
        return wrapped
    return decorator

# ============================================================================
# MIDDLEWARE & ERROR HANDLERS
# ============================================================================

@app.before_request
def before_request():
    """Log de todas as requisições"""
    g.start_time = time()
    logger.info(f"{request.method} {request.path} from {request.remote_addr}")

@app.after_request
def after_request(response):
    """Log de tempo de resposta"""
    if hasattr(g, 'start_time'):
        elapsed = time() - g.start_time
        logger.info(f"Response: {response.status_code} in {elapsed:.3f}s")
    
    # Security headers (OWASP)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    
    return response

@app.errorhandler(Exception)
def handle_exception(e):
    """Handler global de exceções"""
    
    # HTTP exceptions
    if isinstance(e, HTTPException):
        return jsonify({
            "erro": e.description,
            "codigo": e.code
        }), e.code
    
    # Outras exceções
    logger.error(f"Unhandled exception: {e}", exc_info=True)
    
    return jsonify({
        "erro": "Erro interno do servidor",
        "mensagem": "Por favor, tente novamente mais tarde"
    }), 500

# ============================================================================
# VALIDAÇÃO DE INPUT
# ============================================================================

def validate_search_term(termo: str) -> tuple[bool, str]:
    """
    Valida termo de busca
    
    Returns:
        (is_valid, error_message)
    """
    if not termo:
        return False, "Termo de busca não pode ser vazio"
    
    if len(termo) < 3:
        return False, "Termo de busca deve ter pelo menos 3 caracteres"
    
    if len(termo) > 100:
        return False, "Termo de busca muito longo (máximo 100 caracteres)"
    
    # Sanitização básica (prevenir injection)
    forbidden_chars = ['<', '>', '{', '}', '\\', ';']
    if any(char in termo for char in forbidden_chars):
        return False, "Termo contém caracteres inválidos"
    
    return True, ""

# ============================================================================
# INSTÂNCIA DO ÁRBITRO (Singleton)
# ============================================================================

arbitro = ArbitroDePreco()

# ============================================================================
# ENDPOINTS
# ============================================================================

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint para monitoramento
    """
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }), 200

@app.route('/api/status', methods=['GET'])
def api_status():
    """
    Status da API e estatísticas
    """
    return jsonify({
        "status": "online",
        "endpoints": {
            "/health": "Health check",
            "/api/status": "API status",
            "/api/arbitrar": "Comparar preços (POST)"
        },
        "rate_limit": {
            "max_requests": 10,
            "window_seconds": 60
        },
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route('/api/arbitrar', methods=['POST'])
@rate_limit(max_requests=10, window=60)  # 10 req/min por IP
def arbitrar_preco():
    """
    Endpoint principal: compara preços nas 3 lojas
    
    Request Body:
    {
        "termo": "iPhone 15"
    }
    
    Response:
    {
        "termo_busca": "iPhone 15",
        "melhor_produto": {
            "titulo": "...",
            "preco": 4200.00,
            "loja": "Amazon",
            "link": "https://..."
        },
        "todos_produtos": [...],
        "timestamp": "2026-01-22T19:00:00"
    }
    """
    
    try:
        # 1. Validar Content-Type
        if not request.is_json:
            return jsonify({
                "erro": "Content-Type deve ser application/json"
            }), 400
        
        # 2. Extrair e validar termo
        data = request.get_json()
        termo = data.get('termo', '').strip()
        
        is_valid, error_msg = validate_search_term(termo)
        if not is_valid:
            return jsonify({
                "erro": error_msg
            }), 400
        
        logger.info(f"Processando busca: '{termo}'")
        
        # 3. Processar com o árbitro
        resultado = arbitro.processar_pedido(termo)
        
        # 4. Verificar se houve erro
        if "erro" in resultado:
            logger.warning(f"Erro na busca: {resultado['erro']}")
            return jsonify(resultado), 404
        
        # 5. Retornar resultado
        logger.info(f"Busca concluída: {resultado['melhor_produto']['loja']} - R$ {resultado['melhor_produto']['preco']:.2f}")
        
        return jsonify(resultado), 200
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return jsonify({
            "erro": "Dados inválidos",
            "detalhes": str(e)
        }), 400
        
    except Exception as e:
        logger.error(f"Error processing request: {e}", exc_info=True)
        return jsonify({
            "erro": "Erro ao processar requisição",
            "mensagem": "Por favor, tente novamente"
        }), 500

@app.route('/api/limpar-cache', methods=['POST'])
def limpar_cache():
    """
    Endpoint administrativo para limpar cache
    Requer API Key
    """
    
    # Verificar API Key (segurança básica)
    api_key = request.headers.get('X-API-Key')
    
    if api_key != os.getenv('ADMIN_API_KEY', 'dev-key-change-me'):
        return jsonify({
            "erro": "Não autorizado"
        }), 401
    
    try:
        # Limpar cache do árbitro
        arbitro.cache = {}
        arbitro._save_cache()
        
        logger.info("Cache limpo via API")
        
        return jsonify({
            "mensagem": "Cache limpo com sucesso"
        }), 200
        
    except Exception as e:
        logger.error(f"Error clearing cache: {e}")
        return jsonify({
            "erro": "Erro ao limpar cache"
        }), 500

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    # Configuração para desenvolvimento
    DEBUG = os.getenv('FLASK_ENV') == 'development'
    PORT = int(os.getenv('PORT', 5000))
    HOST = os.getenv('HOST', '0.0.0.0')
    
    logger.info(f"Starting API server on {HOST}:{PORT} (debug={DEBUG})")
    
    app.run(
        host=HOST,
        port=PORT,
        debug=DEBUG,
        threaded=True  # Suporte a múltiplas requisições simultâneas
    )
