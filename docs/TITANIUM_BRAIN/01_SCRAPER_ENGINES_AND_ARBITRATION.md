# 🔍 Titanium Brain: Scraper Engines & Arbitration

This document explains how Titanium ingests data from e-commerce platforms and decides which offer is the "Best Deal".

## 🏎️ Parallel Engine Orchestration
Implemented in [arbitrator.py](file:///c:/Users/ericm/OneDrive/Área de Trabalho/PESSOAL/Robô Titanium/core/arbitrator.py).

Titanium uses `asyncio` to search multiple stores simultaneously. This minimizes wait time and ensures the comparison is fresh.

### 1. Amazon Engine (`scraper/engines/amazon.py`)
- **Method**: Headless Selenium (Chrome).
- **Anti-Bot**: Intelligent delays and customized User-Agents.
- **Link Builder**: Injects `tag=guiadodesco00-20` and sorts by `price-asc-rank` (Lower Price).
- **Diversity Engine**: Avoids static vitrine by having `core.orchestrator` shuffle and pick a new subset (`random.sample`) of search terms at every scheduled run.

### 2. Mercado Livre Engine (⚠️ DEPRECATED IN v1.4)
- **Status**: Desativado permanentemente em 2026-03-31 a pedido do usuário.
- **Motivo**: Instabilidade crônica da API (erros 403), frequentes bloqueios de IP (Soft Blocks) que retornavam imagens SVG falsas e falhas de rastreio de afiliação na versão mobile.
- **Ação**: Todo o fluxo de busca destinado ao Mercado Livre (`store_target == 'mercadolivre'`) foi removido do `core/orchestrator.py` e focado 100% em Amazon e Shopee. Documentação legada mantida abaixo apenas para fins de arquivamento:
  - *Legado:* Método Híbrido (API + Scraper Selenium).
  - *Legado:* SVG Soft-Block trapping (exigia filtragem severa).
  - *Legado:* Obrigatoriedade de `forceInApp=true` e `matt_tool`.

### 3. Shopee Engine (`scraper/shopee_api_test_v2.py` & Integração GraphQL)
- **Method**: GraphQL Open API v2 (Oficial).
- **Authentication**: Protocolo **SHA256 Direct** (`hashlib.sha256(AppID + Timestamp + Payload + Secret)`).
- **Endpoint BR**: `https://open-api.affiliate.shopee.com.br/graphql`.
- **Performance**: Suporte a 8.000 chamadas/hora e uso de `scrollId` para paginação de alta escala (catálogos de 500+ itens por requisição).
- **Deep Link Strategy**: Geração automática de links curtos oficiais (`s.shopee.com.br`) via API, garantindo abertura direta no App e maior taxa de conversão.
- **Product Feed (Update 2026-03-05)**: Implementação de motores DELTA para sincronização diária apenas de mudanças de preço e estoque, otimizando largura de banda.

## 🤖 The AI Arbitration & Titanium Balancer (v1.4)
The system goes beyond simplistic price picking by enforcing logical curations and, crucially, a visual balance in the UI.

### 1. The `decidir_com_fallback` Curation Logic:
1.  **AI Analysis**: The engine sends the search term and the top 3 results to **Groq (Llama 3.3 70B)**.
2.  **Scoring**: The AI evaluates title relevance, brand quality, and price competitiveness.
3.  **The Veto**: If the AI detects a "mismatch" (e.g., search for "iPhone" returns a "Case"), it discards the result.
4.  **Fail-Safe**: If the AI is slow or fails, the system defaults to the **Lowest Price** among verified/available products.

### 2. The Titanium Balancer (Introduced 2026-03-31):
After all products (`trends_only` + `unique_fixed`) have been curated, standardized, and sanitized, they pass through the `TITANIUM_BALANCER` inside `orchestrator.py`:
- **Forced Parity**: The algorithm aggregates the sanitized products and splits them strictly by `.lower() == 'shopee'` and `.lower() == 'amazon'`.
- **Interleaving Algorithm**: It determines a `target_per_store` (currently set at 27). It slices each list up to the target amount.
- **Alternating Output**: It then iterates and interleaves the final list (`shopee[0]`, `amazon[0]`, `shopee[1]`, `amazon[1]`), guaranteeing the end-user perceives exactly a 50/50 exposure when browsing the grid.
- **Fail-Safe Fallback**: If one store fails (e.g. Amazon blocks due to Selenium rate limiting), the balancer absorbs the available items from the other store to maintain UI consistency up to the target length (`len(final_list) > 0`).

## 💾 Cache Management
Results are cached in `state/arbitro_cache.json` for **5 minutes (300 seconds)**.
- **Hit**: Returns immediate result to frontend/orchestrator.
- **Miss**: Triggers a new parallel search cycle.

---

## 🧹 Database Sanitation Protocol (`scraper/clean_db.py`)

A dedicated script `scraper/clean_db.py` must be run after any bulk scraping session before deploying to production. It enforces:

1. **SVG Filter**: Removes any item whose `image` contains `.svg` or `logos-api-admin` (ML soft-block placeholders).
2. **Link Validity**: Removes any item whose `link` does not start with `https://`.
3. **Placeholder Detection**: Removes any `data:image` base64 items.

> Always run `clean_db.py` → `upload_data.py` (Production) → verify on site.

## 🛍️ Fashion Boutique Batch Scripts (Created 2026-03-19)

| Script | Purpose |
| :--- | :--- |
| `scraper/production_fashion_miner.py` | Mines 100+ women's clothing items from ML + Shopee. |
| `scraper/amazon_accessories_injector.py` | Mines 20 accessories (bags, perfumes) from Amazon and merges into `data.json`. |
| `scraper/fix_ml_production.py` | Emergency script to recover ML items with valid images after a soft-block purge. |
| `scraper/clean_db.py` | Quality assurance: removes broken images and invalid links from `data.json`. |

---
> [!IMPORTANT]
> The `state/` directory is excluded from Git to protect the cache and refresh tokens. Never delete this folder in production unless a full re-authentication is required.
