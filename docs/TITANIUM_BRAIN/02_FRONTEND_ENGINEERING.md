# 🌐 Titanium Brain: Frontend Engineering (v2026.1)

This document details the mechanics of the "Guia do Desconto" frontend, focusing on the link intelligence and the dynamic rendering system.

## 🏛️ Design Philosophy: "The Elite Hub" (v2026-v3)

A evolução do design do Guia do Desconto prioriza a **autoridade técnica** em vez de truques visuais agressivos.

### 1. Header: Autoridade & Confiança
O projeto estabilizou em um **Header Estático e Premium** com variações por vertical:
- **Boutique Titanium**: Estética Clean, Shopee Orange & Deep Purple.
- **Boutique Íntima**: Estética Luxo, Deep Mauve & Soft Gold com Glassmorphism avançado.

### 2. A Vitrine Aberta & Especializada
O sistema agora gerencia múltiplas vitrines simultâneas:
- **index.html**: Foco em Moda e Beleza (Titanium).
- **sensual.html**: Foco em Bem-Estar e SexTech (Boutique Íntima).
Ambos compartilham o motor de auditoria de links, mas possuem lógica de renderização (`app.js` vs `app_sensual.js`) e pools de dados independentes.

## 🚀 The Redirection Engine ("Links Inteligentes")

### Core Logic: `window.titaniumRedirect(categoria, lojaPreferida)`
Implemented in [app.js](file:///c:/Users/ericm/OneDrive/Área de Trabalho/PESSOAL/Robô Titanium/site/js/app.js) and [app_sensual.js](file:///c:/Users/ericm/OneDrive/Área de Trabalho/PESSOAL/Robô Titanium/site/js/app_sensual.js).

1.  **Normalization**: The store name is normalized to match `TITANIUM_CONFIG.TAGS`.
2.  **Shopee Exclusive**: Fallbacks para Amazon/ML foram desativados para maximizar a conversão no ecossistema Shopee.
3.  **Titanium Link Auditor (v3.8.1)**: Todos os cliques são interceptados para garantir a injeção da tag `an_18318830863`.

### 3. Boutique Shopee Design (v2.1)

#### **A. Estrutura dos Cards (Edição Íntima)**
- **Background**: Glassmorphism (`rgba(255, 255, 255, 0.03)` + `blur(15px)`).
- **Bordas**: Soft Gold (`#D4AF37`) reativo ao hover.
- **Micro-Animações**: Efeito de flutuação e brilho metálico nos itens de elite.

#### **C. Boutique Íntima v3.9 (High-Presence Visuals)**
1.  **Hero Background**: 
    *   Utiliza pseudo-elemento `::before` com imagem de silhueta artística.
    *   **Opacidade Mandatória**: 85% para garantir que a marca seja "viva" e não apenas um fundo claro.
2.  **Robô Titanium (Assistant)**:
    *   **Ícone**: `fas fa-robot`.
    *   **Estilo**: Fundo Azul Shopee (`#2563eb`), Borda Branca (`2px solid white`) e Sombra de Destaque.
    *   **Comportamento Íntima (v3.8.3)**: Atua como um "Mestre de Cerimônias" exibindo 40 frases curtas de empoderamento, autoestima e autocuidado. A lista é embaralhada randomicamente (`Math.random() - 0.5`) a cada load.
    *   **CSS Fade-in/out Logic**: Utiliza a classe `.active` combinada com `opacity` e `transform` no `style.css`/`titanium-security.css`. O JS controla os gatilhos: espera 3s para aparecer, fica visível por 8s, e rotaciona para uma nova frase a cada 25s.
3.  **Badges de Seção**:
    *   **Curadoria VIP**: Cor sólida `#FF4500` (Laranja Shopee) com sombra, garantindo leitura instantânea.

#### **D. Selos de Autoridade (Dynamic Badges)**
1.  **TITANIUM CHOICE (Gold)**: Selo injetado via JS para ofertas com desconto > 30% em itens de alto valor agregado.
2.  **Oferta Relâmpago (Laranja)**: Para descontos acima de 20%.
3.  **Link Seguro Verificado**: Selo de confiança injetado após auditoria em tempo real.

---

## 🏗️ DOM Structure & IDs

| ID | Purpose | Vertical |
| :--- | :--- | :--- |
| `search-input` | Primary search field. | Global |
| `radar-grid` | AI Trend Radar container (18 items). | Global |
| `platinum-grid`| Specialist Selection container (24 items). | Global |
| `deals-grid` | General Offers container (24 items). | Global |

## 📦 State Hydration

The frontend is "re-hydrated" every time the browser loads:
1.  **Moda**: Downloads `data.json`, `specialist.json`, `ai_reviews.json`.
2.  **Sensual**: Downloads `data_sensual.json`, `specialist_sensual.json`, `ai_reviews_sensual.json`.

---

## 🎨 Design System & Styling Rules

- **Glassmorphism**: Aplicado intensamente na vertical Íntima para transmitir luxo e discrição.
- **Symmetry Compliance**: Grades fixas de 18 e 24 itens para garantir harmonia visual no desktop e mobile.

### 🛡️ Styling Protection Protocols (Senior Rules)

1.  **CSS Class Isolation (Prefixing)**: Sempre use prefixos específicos (ex: `.sensual-card`) para evitar colisões com o `style.css` global.
2.  **The "Relative Parent" Rule**: Obrigatório para posicionamento de Badges e Selos de Qualidade.
3.  **Nuclear Shield Gate**: Nenhum link Shopee pode ser renderizado sem passar pelo interceptor global de auditoria.

---
*Atualizado em: 06/05/2026 - Versão: 3.8.3-Nuclear (Frontend Modular Active - Assistant Empowered)*

> [!TIP]
> To update the affiliate tags globally, modify the `TITANIUM_CONFIG.TAGS` object at the top of `app.js`.
