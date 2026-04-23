# 🌐 Titanium Brain: Frontend Engineering

This document details the mechanics of the "Guia do Desconto" frontend, focusing on the link intelligence and the dynamic rendering system.

## 🏛️ Design Philosophy: "The Elite Hub" (v2026-v3)

A evolução do design do Guia do Desconto prioriza a **autoridade técnica** em vez de truques visuais agressivos.

### 1. Header: Autoridade & Confiança (The "Anti-Truck" Clause)
Após testes A/B com animações complexas (caminhões e scanners), o projeto estabilizou em um **Header Estático e Premium**:
- **Logo Area**: Foco na identidade visual Shopee (Laranja) Platinum.
- **Trust Badges**: Uso de "Pills" de status ("Robô Online", "Links Auditados") para converter através da segurança.
- **Tagline**: "Monitoramento Inteligente de Preços" reforça o valor utilitário.

### 2. A Vitrine Aberta
Diferente de versões anteriores onde os produtos ficavam ocultos ("Vitrine Fechada"), a versão v3 mantém as **Ofertas do Momento** (`.voted-deals`) visíveis e em destaque no carregamento inicial. Isso transforma o site de um simples menu de links em um destino real de compras ("Shopping Aberto").

## 🚀 The Redirection Engine ("Links Inteligentes")

The frontend implements a resilient redirection system to ensure that affiliate tracking is always present, even for searches not in the local cache.

### Core Logic: `window.titaniumRedirect(categoria, lojaPreferida)`
Implemented in [app.js](file:///c:/Users/ericm/OneDrive/Área de Trabalho/PESSOAL/Robô Titanium/site/js/app.js).

1.  **Normalization**: The store name is normalized (lowercase, no spaces) to ensure it matches the `TITANIUM_CONFIG.TAGS` keys.
2.  **Fallback Priority**: O sistema agora é **Shopee Exclusive**. Fallbacks para Amazon/ML foram desativados.
3.  **Amazon / ML Builders**: (DEPRECATED) Mantidos apenas no arquivo de legacy.
4.  **Shopee**: Calls `buildShopeeAffiliateUrl`.
    - **Verified Links**: High-priority short links (`s.shopee.com.br`).
    - **Dynamic Search**: Uses the `https://shopee.com.br/list/{keyword}` path. This path is essential for mobile-first redirection as it prevents the app from misidentifying "search" as a shop username.

### Interactive Brand Tabs (v2026_v2)
Implementado como um seletor de lojas multi-camada nos cards de categoria:
- **On-the-Fly Category Switching**: Permite ao usuário alternar instantaneamente entre categorias Shopee sem sair do card.
- **Dynamic CSS State**: Classes dinâmicas (`.active[data-store="..."]`) que alteram cores, sombras e brilhos exclusivos Shopee em tempo real.
- **Interactivity Engineering**: Uso de `z-index: 120` e `backdrop-filter: blur(15px)` nos tabs para garantir que o controle de navegação seja sempre soberano e legível sobre as imagens do banner.

### 3. Boutique Shopee Design (v2.0)
Foco exclusivo na plataforma Shopee com estética de vitrine premium.

#### **A. Estrutura dos Cards (Clean White)**
- **Background**: Branco absoluto (`#FFFFFF`) com bordas suaves (`#f1f3f5`).
- **Shadow**: `0 4px 15px rgba(0,0,0,0.03)` (efeito flutuação).
- **Aspect Ratio**: 1:1 para imagens, garantindo visualização simétrica.

#### **B. Selos de Autoridade (Dynamic Badges)**
1.  **Campeão de Vendas (Roxo)**: `#8e44ad` - Para produtos com alta temperatura.
2.  **Oferta Relâmpago (Laranja)**: `#FF4500` - Para descontos acima de 20%.
3.  **Link Seguro Verificado (Verde)**: Selo de confiança injetado via `app.js` após auditoria do Titanium Link Auditor v3.8.

#### **C. Call to Action (CTA)**
- **Botão Shopee Premium**: Cor `#2196F3` (Azul Shopee) para maximizar o CTR, diferenciando-se do laranja de navegação.

### Animation Architecture (Titanium Shine & Pulse)
Engine de micro-animações para aumento de engajamento e percepção de qualidade:
- **Titanium Shine**: Efeito de brilho linear metálico que percorre os ícones a cada 5 segundos, simulando reflexo de luxo.
- **Premium Titanium Pulse**: Animação de pulsação complexa que combina `scale`, `shadow glow` e `Y-translation` para criar um efeito de "levitação" nos botões de CTA.
- **Fade-Drop Transition**: Transição de texto nos CTAs que combina `opacity: 0` e `transform: translateY(10px)` para uma troca de frase fluida e menos agressiva aos olhos.

### Banner CTAs (Labels de Chamada)
Implementado em [style.css] e [app.js] para guiar o usuário:
- **Camada Visual**: Labels "Floating" nos banners de categoria com animação `titaniumPulse`.
- **Engagement Loop**: Mensagens dinâmicas como "Clique e descubra o menor preço" ou "Busca ativa: Veja preços reais".
- **Premium Glow**: Estilização via Glassmorphism para manter a integridade visual dos hubs.

- **Minimalist UI ("Menos é Mais")**: Ocultação intencional de grids redundantes (`.voted-deals`) para evitar poluição visual e focar o usuário nas áreas de maior conversão (Hubs e Lightning Bar).
- **Zero-Error Console (Premium Trust)**: Para um site inspirar confiança máxima e "Titanium Trust", o console do navegador do usuário deve ser limpo. A ausência de ativos estéticos raiz como `favicon.ico` gera erros silenciosos (404) que depreciam a qualidade técnica percebida pelas auditorias. É obrigatório manter todos os favicons e webmanifests presentes.
- **Security Layer (Blindagem)**:
    - **Whitelist**: Domínios oficiais Shopee.
    - **Titanium Link Auditor (v3.8)**: Injeção ativa de tags de afiliado em tempo real nos cliques do usuário com inteligência de substituição de tags de terceiros.
+    - **MutationObserver Shield**: Monitoramento em tempo real do DOM para auditar links dinâmicos assim que são injetados na tela.
+    - **Global Click Interceptor**: Captura global de cliques em links Shopee para garantir auditoria mandatória antes da navegação.
    - **Cache Busting**: Versionamento agressivo de scripts (`?v=2026v15`).
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

## 🎨 Design System & Styling Rules
- **Family Widget**: Specialized CSS for a premium, mobile-first look.
- **Micro-Animations**: Confetti triggers on seasonal cards to enhance UX.
- **Glassmorphism**: Applied to headers and card overlays for a premium feel.

### 🛡️ Styling Protection Protocols (Senior Rules)

1.  **CSS Class Isolation (Prefixing)**:
    - **NUNCA** use nomes de classes genéricos como `.best-price-badge` em elementos injetados dinamicamente.
    - O `style.css` legado possui centenas de regras que podem causar efeitos colaterais (ex: transformar um card em um banner gigante).
    - **Sempre** use prefixos específicos (ex: `.category-best-price` ou `.titanium-card`) para garantir isolamento total.

2.  **The "Relative Parent" Rule**:
    - Todo elemento com `position: absolute` (Badges, Troféus, Selos) **DEVE** ter um container pai com `position: relative` definido explicitamente.
    - Sem isso, o elemento absoluto "escapa" para o topo da Viewport (Página), quebrando o alinhamento visual no mobile e desktop.

## 💰 AdSense Content Compliance (Lição 2026-03-05)

O Google AdSense pode bloquear anúncios em sites classificados como **"Thin Affiliate"** — afiliados sem conteúdo editorial próprio. Para garantir compliance:

### Ativos Obrigatórios no `index.html`
| Ativo | Implementado | Onde |
| :--- | :--- | :--- |
| **Schema.org** (Organization + WebSite) | ✅ `v=adsense_fix_v1` | `<head>` JSON-LD |
| **Open Graph + Twitter Card** | ✅ | `<head>` meta tags |
| **Seção Editorial** ("Como funciona") | ✅ | Entre Seasonal e Daily Deals |
| **`hub-desc`** em todas as 12 categorias | ✅ | Dentro de cada `.hub-card` |
| **Alt text descritivo** nas imagens | ✅ | Cada banner de categoria |
| **Densidade Textual Simétrica** | ✅ `v26` | O `Radar de Tendências IA` gera exatos 18 itens na grade simétrica. |

### Regra Crítica de Layout: Textos Longos (Radar)
- NUNCA comprimir textos longos via `display: flex` horizontal com imagens (`flex-direction: row`).
- O Radar de Tendências (`.radar-card`) **DEVE OBRIGATORIAMENTE** usar `flex-direction: column` com imagens no topo e textos de IA ocupando largura total (`width: 100%`) alinhados à esquerda (`text-align: left`). Isso garante densidade textual elegante sem achatamento, otimizado para o AdSense ler grandes massas de texto harmoniosamente.

### Regra Crítica: `display:none` é Invisível para o Googlebot
- Seções ocultas via CSS **não são indexadas** pelo Google
- A seção `.voted-deals` está oculta no `style.css` — o texto de título e subtítulo garante algum conteúdo visível, mas os cards de produto ainda são invisíveis para crawlers
- **Se reativar o Lightning Bar:** garantir que o `#deals-grid` fique visível ou que haja texto editorial equivalente

### Proteção Pós-Deploy
- **Nunca** deixar o robô sobrescrever `index.html` com versão sem o bloco editorial
- O `index.html` é um **Ativo Estrutural Crítico** — versionado junto com `ads.txt`
- Qualquer alteração estrutural deve passar pelo fluxo **Staging → Produção** completo

---
> [!TIP]
> To update the affiliate tags globally, modify the `TITANIUM_CONFIG.TAGS` object at the top of `app.js`.

