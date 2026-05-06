# ⚙️ Expansão: Boutique Íntima (v1.1)
## Documento 02: Arquitetura Técnica e Integração (Status: 100% OPERACIONAL)

> [!TIP]
> **Diferencial Técnico**: Implementado o selo dinâmico `TITANIUM CHOICE` no arquivo `app_sensual.js` para destacar ofertas com desconto superior a 30% via CSS Glassmorphism.

Este documento detalha como a nova vertical se integra ao sistema **Titanium v3.8** existente.

---

### 1. 📂 Estrutura de Arquivos [CONCLUÍDO ✅]
A expansão utiliza a infraestrutura "Stateless" atual:
*   [x] `site/sensual.html`: Template exclusivo com paleta de cores e scripts específicos.
*   [x] `site/data_sensual.json`: Pool de produtos minerados.
*   [x] `site/ai_reviews_sensual.json`: Reviews sensoriais gerados por IA.
*   [x] `site/specialist_sensual.json`: Vitrine de elite gerada automaticamente.
*   [x] `site/js/app_sensual.js`: Motor de renderização adaptado.

### 2. 🛰️ Motor de Mineração & IA [CONCLUÍDO ✅]
1. [x] **Minerador**: `scraper/production_sensual_miner.py` operacional.
2. [x] **Radar IA**: `core/production_sensual_radar.py` integrado com DeepSeek.
3. [x] **Curador de Elite**: `core/curator_sensual_auto.py` (100% Automático).
4. [x] **Automação (Data)**: `.github/workflows/sensual_auto_update.yml` (Staging).
5. [x] **Automação (Specialist)**: `.github/workflows/sensual_specialist_auto.yml` (Independent).

### 3. 🛡️ Integração com o Nuclear Shield (v3.8) [CONCLUÍDO ✅]
A nova vertical herda automaticamente todas as proteções:
*   [x] **Global Click Interceptor**: Auditoria de links injetando tag `an_18318830863`.
*   [x] **MutationObserver**: Correção de links dinâmicos em tempo real.
*   [x] **Atomic Sync**: Deploy isolado via Actions.

### 4. 📈 Tracking e Analytics
Novas metas de eventos no GA4:
*   `sensual_view`: Visualização de itens da vertical.
*   `sensual_click`: Clique em produtos sensuais.
*   `category_switch_sensual`: Troca entre categorias dentro da boutique.

---
**Regra de Ouro**: O arquivo `sensual.html` deve manter o mesmo cabeçalho (`<header>`) da Titanium para permitir a transição fluida do usuário entre os dois "mundos".
