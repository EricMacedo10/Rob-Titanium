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

### 2. Mercado Livre Engine (`scraper/engines/mercadolivre.py` & `meli_api.py`)
- **Method**: Hybrid Model (Official API + Scraper).
- **Affiliate Link Builder**: Uses the official **OAuth 2.0** flow. The engine retrieves a valid `access_token` using a `refresh_token` stored in GitHub Secrets.
- **Matt-Tool System**: Mandatory use of `matt_tool=188269638` (User ID). This is the "Heart" of the ML attribution.
- **Mobile Fix**: Mandatory inclusion of `forceInApp=true` in search/list links to ensure valid tracking within the ML native app.
- **Nuclear Search (Fallback)**: Selenium-based scraper used only for real-time price validation if the API returns 403 (restricted endpoints).
- **⚠️ SVG Soft-Block (2026-03-19):** When the ML listing page is under high load or bot-pressure, it may serve its own logo `.svg` file as the product image instead of the real photo. **The scraper MUST explicitly filter out any image URL containing `.svg` or `logos-api-admin`**. The `search_mercadolivre()` function in `mercadolivre.py` now validates images directly from the `poly-card` element before scraping the product page, saving time and avoiding this trap.
- **⚠️ URL Key Bug:** The `format_ml_product_for_site()` in `meli_api.py` must use key `link` (not `url`) to retrieve the product URL from the scraper's return dict. This caused all ML items to have empty affiliate links until fixed on 2026-03-19.

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
