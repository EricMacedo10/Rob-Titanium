# 📅 CRONOGRAMA ZERO CUSTO - Árbitro de Preços + Robô Interativo
## Aproveitando 100% da Infraestrutura Existente

---

## 🎯 **ANÁLISE DO QUE JÁ TEMOS**

### ✅ **INFRAESTRUTURA COMPLETA (100% Pronta)**

| Componente | Status | Arquivo | Observação |
|------------|--------|---------|------------|
| **Mercado Livre API** | ✅ 100% | `scraper/ml_affiliate.py` | 436 linhas, Selenium + OAuth |
| **Shopee API** | ✅ 100% | `scraper/shopee_affiliate.py` | SHA256 signature correto |
| **Amazon Scraper** | ✅ 100% | `scraper/amazon.py` | Selenium com anti-bot |
| **Site Frontend** | ✅ 100% | `site/index.html` | HTML/CSS/JS pronto |
| **Deploy Automático** | ✅ 100% | `deploy_site.py` + GitHub Actions | FTP para Hostinger |
| **Hosting** | ✅ GRÁTIS | Hostinger (já pago) | Sem custo adicional |

### ⚠️ **O QUE FALTA (Desenvolvimento Necessário)**

| Componente | Status | Estimativa | Custo |
|------------|--------|------------|-------|
| **Classe ArbitroDePreco** | ✅ 100% | ~~2 dias~~ **1h30** | $0 |
| **Integração com LLM** | ✅ 100% | ~~1 dia~~ **30min** | **$0/mês (Groq GRÁTIS!)** |
| **API REST (Flask)** | ✅ 100% | ~~1 dia~~ **45min** | $0 |
| **Assistente Família (Widget)** | ✅ 100% | ~~4 horas~~ **OK** | $0 |
| **Frontend Integration** | ✅ 100% | **OK** | $0 |
| **Testes E2E** | ❌ 0% | 1 dia | $0 |

---

## 💰 **ORÇAMENTO REAL (MÍNIMO ABSOLUTO)**

### Custos Mensais
| Item | Custo Original | **Custo ZERO** | Como? |
|------|----------------|----------------|-------|
| Servidor | $30/mês | **$0** | ✅ Usar Hostinger existente |
| Redis Cache | $15/mês | **$0** | ✅ Usar cache em arquivo JSON |
| PostgreSQL | $20/mês | **$0** | ✅ Usar SQLite local |
| CDN | $10/mês | **$0** | ✅ Hostinger já tem CDN |
| Monitoramento | $15/mês | **$0** | ✅ Logs em arquivo + Sentry Free |
| **LLM (Única despesa)** | $20/mês | **$5-10/mês** | ✅ Usar Groq (Llama3 grátis até 30k req/dia!) |

### **TOTAL MENSAL: $0-10** (vs $90 original)

---

## 🚀 **CRONOGRAMA OTIMIZADO (ZERO CUSTO)**

### **SEMANA 1: Core do Árbitro (5 dias)**

#### **Dia 1: Classe ArbitroDePreco Base** ✅ CONCLUÍDO
- [x] Criar `scraper/arbitro_preco.py`
- [x] Implementar busca assíncrona (asyncio)
- [x] Integrar com `ml_affiliate.py`, `shopee_affiliate.py`, `amazon.py`
- [x] Cache em JSON (sem Redis)

**Código Base**:
```python
import asyncio
import json
from scraper.ml_affiliate import generate_affiliate_link
from scraper.shopee_affiliate import get_shopee_affiliate_link
from scraper.amazon import search_amazon

class ArbitroDePreco:
    def __init__(self):
        self.cache_file = "arbitro_cache.json"
        
    async def buscar_ml(self, termo):
        # Já temos isso pronto!
        return generate_affiliate_link(termo, driver, first_time=True)
    
    async def buscar_shopee(self, termo):
        # Já temos isso pronto!
        return get_shopee_affiliate_link(termo)
    
    async def buscar_amazon(self, termo):
        # Já temos isso pronto!
        return search_amazon(termo)
```

#### **Dia 2: Integração LLM (Groq GRÁTIS)** ✅ CONCLUÍDO
- [x] Criar conta Groq: https://console.groq.com
- [x] Obter API Key (GRÁTIS: 30k req/dia)
- [x] Implementar `curadoria_ia.py`

**Groq vs OpenAI**:
| Feature | OpenAI GPT-4o-mini | **Groq Llama3-70B** |
|---------|-------------------|---------------------|
| Custo | $0.15/1M tokens | **GRÁTIS** (30k req/dia) |
| Latência | ~1s | **~0.3s** (3x mais rápido!) |
| Qualidade | Excelente | Muito Boa |

```python
import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def decidir_melhor_oferta(termo_busca, produtos):
    prompt = f"""
    Usuário quer: "{termo_busca}"
    
    Produtos:
    {json.dumps(produtos, indent=2, ensure_ascii=False)}
    
    Retorne APENAS o número do id_interno do melhor produto.
    """
    
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=10
    )
    
    return int(response.choices[0].message.content.strip())
```

```python
from flask import Flask, request, jsonify
from flask_cors import CORS
from scraper.arbitro_preco import ArbitroDePreco

app = Flask(__name__)
CORS(app)

arbitro = ArbitroDePreco()

@app.route('/api/arbitrar', methods=['POST'])
def arbitrar():
    termo = request.json.get('termo')
    resultado = arbitro.processar_pedido(termo)
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```
#### **Dia 3: API REST com Flask** ✅ CONCLUÍDO
- [x] Criar `api_arbitro.py`
- [x] Endpoint `/api/arbitrar` (POST)
- [x] CORS configurado

#### **Dia 4: Testes Unitários** ✅ CONCLUÍDO
- [x] Testar com "iPhone 15"
- [x] Testar com "notebook gamer"
- [x] Validar links de afiliado (Fallbacks e Tags corretas)

#### **Dia 5: Deploy no Hostinger**
- [ ] Adicionar `api_arbitro.py` ao projeto
- [ ] Configurar porta 5000 no Hostinger
- [ ] Testar endpoint público

---

### **SEMANA 2: Robô Interativo (3 dias)**

### **SEMANA 2: Engajamento & Família (CONCLUÍDO)**

#### **Dia 6: Design dos Avatares** ✅ CONCLUÍDO
- [x] **GRÁTIS**: Gerar avatares 3D Pixar (Família)
- [x] Otimizar imagens (WebP/PNG)
- [x] Adicionar a `site/images/`

#### **Dia 7: Widget "Assistente Família"** ✅ CONCLUÍDO
- [x] Implementar `family-widget.js` e `family-widget.css`
- [x] Animação de slide-in suave
- [x] Notificações aleatórias com dicas reias
- [x] Substitui o antigo conceito de "Robô Caminhando" por algo mais humanizado e confiável.

#### **Dia 8: Ajustes Finais de UX** ✅ CONCLUÍDO
- [x] Adicionar em `site/js/app.js`
- [x] Click handler → abrir modal de busca
- [x] Integração Visual Completa

---

### **SEMANA 3: Integração & Testes (2 dias)**

#### **Dia 9: Frontend ↔ Backend**
- [ ] Formulário de busca chama API
- [ ] Exibir resultados comparados
- [ ] Highlight do melhor preço

#### **Dia 10: Testes Finais**
- [ ] Testar fluxo completo
- [ ] Validar links de afiliado
- [ ] Deploy final

---

## 🎁 **BÔNUS: Ferramentas GRATUITAS**

### LLM (Escolha 1)
1. **Groq** (RECOMENDADO)
   - ✅ 30k req/dia GRÁTIS
   - ✅ Llama3-70B (muito bom)
   - ✅ Latência <500ms
   - 🔗 https://console.groq.com

2. **Hugging Face Inference API**
   - ✅ GRÁTIS ilimitado (rate limited)
   - ✅ Vários modelos
   - 🔗 https://huggingface.co/inference-api

3. **Ollama (Local)**
   - ✅ 100% GRÁTIS
   - ✅ Roda no seu PC
   - ⚠️ Precisa de GPU

### Monitoramento
- **Sentry** (Free Tier): 5k erros/mês
- **UptimeRobot**: 50 monitores grátis
- **Google Analytics**: GRÁTIS

### Imagens
- **DALL-E 3 Free**: https://www.bing.com/create (Microsoft)
- **Leonardo.ai**: 150 créditos/dia GRÁTIS
- **Posso gerar para você!**

---

## ✅ **CHECKLIST SIMPLIFICADO**

### Fase 1: Backend (Semana 1)
- [x] ✅ `scraper/arbitro_preco.py` (Dia 1) - **CONCLUÍDO 22/01/2026**
- [x] ✅ `scraper/curadoria_ia.py` (Dia 2) - **CONCLUÍDO 22/01/2026**
- [ ] `api_arbitro.py` (Dia 3) - **PRÓXIMO**
- [ ] Testes (Dia 4-5)

### Fase 2: Frontend (Semana 2) ✅ CONCLUÍDO
- [x] Avatares Família 3D (Dia 6)
- [x] Widget CSS Glassmorphism (Dia 7) - *Visual Premium!*
- [x] JavaScript Lógica (Dia 8) - *Dicas aleatórias*

### Fase 3: Deploy (Semana 3)
- [x] Integração (Dia 9) ✅
- [ ] Testes finais (Dia 10)

---

## 🎯 **PRÓXIMOS PASSOS IMEDIATOS**

### ✅ Concluído (22/01/2026):
1. ✅ Criar conta Groq (5 min)
2. ✅ Obter API Key
3. ✅ Adicionar ao `.env`: `GROQ_API_KEY=gsk_...`
4. ✅ Criar `scraper/arbitro_preco.py`
5. ✅ Criar `scraper/curadoria_ia.py`
6. ✅ Testar busca paralela com IA
7. ✅ Validar curadoria inteligente (ignorou acessórios!)

### Próximo (Dia 3):
1. ⏳ Criar `api_arbitro.py` (API REST com Flask)
2. ⏳ Testar endpoint `/api/arbitrar`

---

## 💡 **DICAS PARA ECONOMIZAR**

### Cache Agressivo
```python
# Cache de 5 minutos (evita chamar API 2x)
import time

cache = {}

def buscar_com_cache(termo):
    if termo in cache:
        timestamp, resultado = cache[termo]
        if time.time() - timestamp < 300:  # 5 min
            return resultado
    
    resultado = buscar_produto(termo)
    cache[termo] = (time.time(), resultado)
    return resultado
```

### Fallback sem IA
```python
# Se Groq cair, escolher menor preço
try:
    id_vencedor = decidir_com_ia(produtos)
except:
    id_vencedor = min(enumerate(produtos), key=lambda x: x[1]['preco'])[0]
```

---

## 📊 **COMPARAÇÃO: Original vs ZERO CUSTO**

| Métrica | Cronograma Original | **ZERO CUSTO** |
|---------|---------------------|----------------|
| **Duração** | 8 semanas | **3 semanas** |
| **Custo Mensal** | $110/mês | **$0-10/mês** |
| **Custo Setup** | $62 | **$0** |
| **Infraestrutura** | AWS/GCP | **Hostinger (já pago)** |
| **LLM** | OpenAI ($20/mês) | **Groq (GRÁTIS)** |
| **Cache** | Redis ($15/mês) | **JSON (GRÁTIS)** |
| **Banco** | PostgreSQL ($20/mês) | **SQLite (GRÁTIS)** |

---

## 🎉 **RESUMO EXECUTIVO**

### O que JÁ TEMOS (Valor: ~$5000 se fosse contratar):
- ✅ Mercado Livre API completa (Selenium + OAuth)
- ✅ Shopee API com SHA256 correto
- ✅ Amazon scraper anti-bot
- ✅ Site frontend profissional
- ✅ Deploy automático (GitHub Actions)
- ✅ Hosting pago (Hostinger)

### O que FALTA (10 dias de trabalho):
- ✅ Classe `ArbitroDePreco` (2 dias)
- ✅ Integração Groq LLM (1 dia)
- ✅ API REST Flask (1 dia)
- ✅ Integração frontend (1 dia)
- ✅ Assistente Família (Widget) (1 dia) - *Substituiu Robô Animado*
- ❌ Testes Finais (1 dia)

### Custo Total:
- **Desenvolvimento**: $0 (você mesmo)
- **Infraestrutura**: $0 (Hostinger já pago)
- **LLM**: $0-10/mês (Groq grátis ou OpenAI barato)

---

**Quer que eu comece a implementar agora?** Posso criar:
1. `scraper/arbitro_preco.py` (Dia 1) ✅ FEITO
2. `scraper/curadoria_ia.py` com Groq (Dia 2) ✅ FEITO
3. Avatares Família Pixar (GRÁTIS) ✅ FEITO
