# 🌐 Titanium Brain: Frontend Engineering

This document details the mechanics of the "Guia do Desconto" frontend, focusing on the link intelligence and the dynamic rendering system.

## 🚀 The Redirection Engine ("Links Inteligentes")

The frontend implements a resilient redirection system to ensure that affiliate tracking is always present, even for searches not in the local cache.

### Core Logic: `window.titaniumRedirect(categoria, lojaPreferida)`
Implemented in [app.js](file:///c:/Users/ericm/OneDrive/Área de Trabalho/PESSOAL/Robô Titanium/site/js/app.js).

1.  **Normalization**: The store name is normalized (lowercase, no spaces) to ensure it matches the `TITANIUM_CONFIG.TAGS` keys.
2.  **Fallback Priority**: If no store is specified or the preferred store is inactive, the system follows `PRIORIDADE: ['amazon', 'mercadolivre', 'shopee']`.
3.  **Store-Specific Builders**:
    - **Amazon**: Direct URL with `&tag=guiadodesco00-20&s=price-asc-rank`.
    - **Mercado Livre**: Calls `buildMLAffiliateUrl`. It uses the **Matt-Tool System** with `matt_tool=188269638` and a dynamic `tracking_id`.
    - **Shopee**: Calls `buildShopeeAffiliateUrl`. It uses a **Hybrid System**:
        - Checks a hardcoded map for "Official Verified Links" (Priority 1).
        - Falls back to a search URL with `utm_source=ericmacedo` (Priority 2).

### Dashboard Hubs (Interativos)
O sistema conta com Hubs de Categoria Inteligentes (ex: `tech-hub-card`, `home-hub-card`):
- **Brand Tabs**: Permite ao usuário alternar entre Amazon, Mercado Livre e Shopee sem sair do card.
- **Sync Visual**: A troca de aba sincroniza instantaneamente o banner, a imagem de destaque e o termo de busca do redirecionamento.
- **Auto-Rotation**: Implementa rodízio automático de marcas a cada 30 minutos para equilibrar o tráfego de afiliados.

### Security Layer (Blindagem)
- **Whitelist**: Todo redirecionamento é validado contra domínios permitidos (`amazon.com.br`, `mercadolivre.com.br`, `shopee.com.br`).
- **Exclusion Logic**: Banners interativos e cards sazonais (.seasonal e .interactive-card) são ignorados pelo motor de renderização dinâmico para evitar estados de "Nenhuma oferta encontrada" ao retornar ao site.
- **Cache Busting**: Uso mandatório de tags de versão (ex: `app.js?v=2026v5`) para garantir a entrega imediata de correções críticas.
- **Content Security Policy (CSP)**: Implementa regras de "Zero Trust" mas permite especificamente a comunicação com domínios de rastreamento do Google (`www.googletagmanager.com`, `*.google-analytics.com`) para garantir métricas precisas.

## 🏗️ DOM Structure & IDs

The site uses specific IDs to facilitate interaction and future automated testing/scraping.

| ID | Purpose |
| :--- | :--- |
| `search-input` | The primary search field. |
| `search-suggestions` | Container for the search autocomplete dropdown. |
| `deals-grid` | The container where `data.json` products are rendered. |
| `tech-hub-card` | Specialized card for "Tecnologia" category. |
| `titanium-bot-trap` | Anti-bot honeypot for security. |

## 📦 State Hydration (`data.json`)

The frontend is "re-hydrated" every time the browser loads:
1.  Downloads `data.json` (the source of truth).
2.  Filters by current active category or search query.
3.  **Fail-Safe Image Handling**: If a product image fails to load or matches a known "Blocked Image" pattern, `window.handleImageError` replaces it with a branded placeholder card to maintain site aesthetics.

## 🎨 Design System
- **Family Widget**: Specialized CSS for a premium, mobile-first look.
- **Micro-Animations**: Confetti triggers on seasonal cards to enhance UX.
- **Glassmorphism**: Applied to headers and card overlays for a premium feel.

---
> [!TIP]
> To update the affiliate tags globally, modify the `TITANIUM_CONFIG.TAGS` object at the top of `app.js`.
