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

### 2. Mercado Livre Engine (`scraper/engines/mercadolivre_api.py`)
- **Method**: Official REST API + Advanced Selenium Fallback ("Nuclear Search").
- **Nuclear Search**: Bypasses anti-bot blocks by starting from the Mercado Livre home page.
- **Sorting**: Mandatory use of `_OrderId_PRICE_ASC`.
- **Tracking**: Uses the **Matt-Tool** system with dynamic `tracking_id`.
- **Mobile Fix**: Mandatory inclusion of `forceInApp=true` in category/search links to prevent 404s and preserve affiliate cookies in the native App.

### 3. Shopee Engine (`scraper/engines/shopee_affiliate.py`)
- **Method**: REST API v4.
- **Fallback**: Selenium-based search if the API rate limit is reached.
- **Deep Link Strategy**: For search-based results, use the `/list/` path instead of `/search` to avoid the "Shop failed to load" error in the mobile app.
- **ID Standard**: Use numeric `an_...` IDs in `utm_source` for maximum compatibility.

## 🤖 The AI Arbitration Layer
After gathering results, Titanium doesn't just pick the lowest price. It performs "Intelligent Curation".

### The `decidir_com_fallback` Logic:
1.  **AI Analysis**: The engine sends the search term and the top 3 results to **Groq (Llama 3.3 70B)**.
2.  **Scoring**: The AI evaluates title relevance, brand quality, and price competitiveness.
3.  **The Veto**: If the AI detects a "mismatch" (e.g., search for "iPhone" returns a "Case"), it discards the result.
4.  **Fail-Safe**: If the AI is slow or fails, the system defaults to the **Lowest Price** among verified/available products.

## 💾 Cache Management
Results are cached in `state/arbitro_cache.json` for **5 minutes (300 seconds)**.
- **Hit**: Returns immediate result to frontend/orchestrator.
- **Miss**: Triggers a new parallel search cycle.

---
> [!IMPORTANT]
> The `state/` directory is excluded from Git to protect the cache and refresh tokens. Never delete this folder in production unless a full re-authentication is required.
