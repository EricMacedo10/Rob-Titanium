# 📘 API do Árbitro de Preços - Documentação

## 🚀 **Visão Geral**

API REST production-ready para comparação inteligente de preços usando IA.

**Base URL**: `http://localhost:5000` (dev) | `https://guiadodesconto.com.br` (prod)

---

## 🔐 **Segurança**

### Headers de Segurança (OWASP)
- ✅ `X-Content-Type-Options: nosniff`
- ✅ `X-Frame-Options: DENY`
- ✅ `X-XSS-Protection: 1; mode=block`
- ✅ `Strict-Transport-Security: max-age=31536000`

### Rate Limiting
- **Limite**: 10 requisições por minuto por IP
- **Response**: `429 Too Many Requests` se exceder

### CORS
- **Permitido**: `guiadodesconto.com.br`, `localhost:3000`
- **Métodos**: `GET`, `POST`, `OPTIONS`

---

## 📍 **Endpoints**

### 1. Health Check
```http
GET /health
```

**Response** (200 OK):
```json
{
  "status": "healthy",
  "timestamp": "2026-01-22T19:00:00",
  "version": "1.0.0"
}
```

---

### 2. API Status
```http
GET /api/status
```

**Response** (200 OK):
```json
{
  "status": "online",
  "endpoints": {
    "/health": "Health check",
    "/api/status": "API status",
    "/api/arbitrar": "Comparar preços (POST)"
  },
  "rate_limit": {
    "max_requests": 10,
    "window_seconds": 60
  }
}
```

---

### 3. Arbitrar Preço (Principal)
```http
POST /api/arbitrar
Content-Type: application/json
```

**Request Body**:
```json
{
  "termo": "iPhone 15"
}
```

**Validações**:
- Termo não pode ser vazio
- Mínimo 3 caracteres
- Máximo 100 caracteres
- Sem caracteres especiais: `< > { } \ ;`

**Response** (200 OK):
```json
{
  "termo_busca": "iPhone 15",
  "melhor_produto": {
    "titulo": "iPhone 15 128GB Novo Lacrado",
    "preco": 4200.00,
    "loja": "Amazon",
    "link": "https://amazon.com.br/...",
    "imagem": "https://..."
  },
  "todos_produtos": [
    {
      "id_interno": 0,
      "titulo": "iPhone 15 - Shopee",
      "preco": 0,
      "loja": "Shopee",
      "disponivel": false
    },
    {
      "id_interno": 1,
      "titulo": "iPhone 15 128GB Novo Lacrado",
      "preco": 4200.00,
      "loja": "Amazon",
      "disponivel": true
    }
  ],
  "timestamp": "2026-01-22T19:00:00"
}
```

**Errors**:

- **400 Bad Request** - Input inválido
```json
{
  "erro": "Termo de busca deve ter pelo menos 3 caracteres"
}
```

- **404 Not Found** - Nenhum produto encontrado
```json
{
  "erro": "Nenhum produto disponível no momento",
  "termo": "produto inexistente"
}
```

- **429 Too Many Requests** - Rate limit excedido
```json
{
  "erro": "Muitas requisições. Tente novamente em 1 minuto.",
  "retry_after": 60
}
```

- **500 Internal Server Error**
```json
{
  "erro": "Erro interno do servidor",
  "mensagem": "Por favor, tente novamente mais tarde"
}
```

---

### 4. Limpar Cache (Admin)
```http
POST /api/limpar-cache
X-API-Key: <admin_key>
```

**Response** (200 OK):
```json
{
  "mensagem": "Cache limpo com sucesso"
}
```

---

## 🧪 **Exemplos de Uso**

### cURL
```bash
# Health check
curl http://localhost:5000/health

# Buscar produto
curl -X POST http://localhost:5000/api/arbitrar \
  -H "Content-Type: application/json" \
  -d '{"termo":"notebook gamer"}'
```

### JavaScript (Fetch)
```javascript
async function buscarProduto(termo) {
  const response = await fetch('http://localhost:5000/api/arbitrar', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ termo })
  });
  
  const data = await response.json();
  
  if (response.ok) {
    console.log('Melhor produto:', data.melhor_produto);
  } else {
    console.error('Erro:', data.erro);
  }
}

buscarProduto('iPhone 15');
```

### Python (requests)
```python
import requests

response = requests.post(
    'http://localhost:5000/api/arbitrar',
    json={'termo': 'notebook gamer'}
)

if response.status_code == 200:
    data = response.json()
    print(f"Melhor: {data['melhor_produto']['titulo']}")
    print(f"Preço: R$ {data['melhor_produto']['preco']:.2f}")
else:
    print(f"Erro: {response.json()['erro']}")
```

---

## 🚀 **Deploy**

### Desenvolvimento
```bash
python api_arbitro.py
```

### Produção (Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 api_arbitro:app
```

### Variáveis de Ambiente
```bash
# .env
FLASK_ENV=production
PORT=5000
HOST=0.0.0.0
ADMIN_API_KEY=sua_chave_secreta_aqui
```

---

## 📊 **Monitoramento**

### Logs
- **Arquivo**: `api_arbitro.log`
- **Formato**: `timestamp [LEVEL] logger: message`
- **Níveis**: INFO, WARNING, ERROR

### Métricas
- Tempo de resposta (logged)
- Taxa de erro
- Rate limit hits

---

## 🔧 **Troubleshooting**

### API não inicia
```bash
# Verificar porta em uso
netstat -ano | findstr :5000

# Matar processo
taskkill /PID <pid> /F
```

### CORS Error
- Adicionar domínio em `ALLOWED_ORIGINS`
- Verificar headers no frontend

### Rate Limit muito restritivo
- Ajustar `@rate_limit(max_requests=10, window=60)`
- Implementar whitelist de IPs

---

## 📝 **Changelog**

### v1.0.0 (22/01/2026)
- ✅ Endpoint `/api/arbitrar`
- ✅ Rate limiting
- ✅ CORS configurado
- ✅ Validação de input
- ✅ Security headers
- ✅ Structured logging
- ✅ Error handling robusto
- ✅ Health checks

---

**Desenvolvido com ❤️ usando Flask + Groq AI**
