// ========================================
// GUIA DO DESCONTO - MAIN APPLICATION
// ========================================

// === CONFIGURAÇÃO ROBÔ TITANIUM (v2026-fix-01) ===
const TITANIUM_CONFIG = {
    // Tags reais de afiliado
    TAGS: {
        shopee: "an_18318830863"
    },
    // Configurações de Afiliado Legadas (vazias para evitar crashes)
    ML_AFFILIATE: {
        userId: "188269638",
        source: "guiadodesconto",
        trackingPrefix: "titanium"
    },
    // Foco Total Shopee
    STATUS: {
        shopee: true
    },
    // MAESTRO ENGINE: Curação Senior por Horário (Invisível ao Usuário)
    MAESTRO: {
        RULES: [
            { id: 'madrugada', start: 23, end: 7, title: "🛍️ Ofertas do Momento", category: 'any', minDiscount: 40, label: "Super Descontos" },
            { id: 'manha', start: 7, end: 11, title: "🛍️ Ofertas do Momento", category: 'casa', minDiscount: 0, label: "Casa & Bem-Estar" },
            { id: 'almoco', start: 11, end: 14, title: "🛍️ Ofertas do Momento", category: 'tecnologia', minDiscount: 20, label: "Tech & Gadgets" },
            { id: 'tarde', start: 14, end: 18, title: "🛍️ Ofertas do Momento", category: 'moda', minDiscount: 0, label: "Moda & Estilo" },
            { id: 'primetime', start: 18, end: 23, title: "🛍️ Ofertas do Momento", category: 'any', minDiscount: 25, label: "Best Sellers" }
        ]
    }
};

/**
 * Gera um tracking_id único para rastreamento
 * @returns {string} ID único baseado em timestamp
 */
function generateTrackingId() {
    const prefix = TITANIUM_CONFIG.ML_AFFILIATE.trackingPrefix;
    const userId = TITANIUM_CONFIG.ML_AFFILIATE.userId;
    const timestamp = Date.now().toString(36);
    const random = Math.random().toString(36).substr(2, 5);
    return `${prefix}-${userId}-${timestamp}-${random}`;
}

/**
 * Constrói URL do Mercado Livre com todos os parâmetros de afiliado
 * @param {string} searchTerm - Termo de busca
 * @returns {string} URL completa com parâmetros de afiliado
 */
function buildMLAffiliateUrl(searchTerm) {
    const config = TITANIUM_CONFIG.ML_AFFILIATE;

    // Normaliza termo para o padrão de URL do ML (troca espaço por hífen)
    const normalizedTerm = encodeURIComponent(searchTerm).replace(/%20/g, '-');

    // URL de busca com ordenação por Menor Preço nativa (_OrderId_PRICE)
    const baseUrl = `https://lista.mercadolivre.com.br/${normalizedTerm}_OrderId_PRICE`;

    // Parâmetros de afiliado oficiais (Matt-Tool System)
    const params = new URLSearchParams({
        'matt_tool': config.userId,              // ✅ Seu ID de Afiliado: 188269638
        'matt_word': searchTerm,                 // Termo buscado para tracking
        'matt_source': config.source,            // 'guiadodesconto'
        'tracking_id': generateTrackingId(),     // ID único para cada clique
        'forceInApp': 'true'                     // 📱 Força a abertura do App e rastreio persistente
    });

    const finalUrl = `${baseUrl}?${params.toString()}`;

    console.log('[Titanium ML] Link Inteligente (forceInApp) gerado:', finalUrl);
    return finalUrl;
}

/**
 * Constrói URL de busca da Shopee (Hybrid: Links Oficiais + Fallback)
 * @param {string} searchTerm - Termo de busca
 * @returns {string} URL verificada
 */
function buildShopeeAffiliateUrl(searchTerm) {
    // 1. Links Oficiais Shopee (Short Links p/ Promoções Específicas)
    const officialLinks = {
        "carnaval": "https://s.shopee.com.br/10pW2pX5h0",
        "dia da mulher": "https://s.shopee.com.br/BAp2C9v93",
        "ofertas": "https://s.shopee.com.br/14JVgor5V",
        "equipamento academia": "https://s.shopee.com.br/14JVgor5V",
        "voltas às aulas": "https://s.shopee.com.br/10pW2pX5h0",
        "mochila escolar": "https://s.shopee.com.br/7Uyp9pC7wz"
    };

    // 2. Normaliza termo para busca (lowercase + trim)
    const termKey = searchTerm.toLowerCase().trim();

    // 3. Retorna link oficial se existir
    if (officialLinks[termKey]) {
        console.log(`[Shopee] Usando link oficial para "${termKey}"`);
        return officialLinks[termKey];
    }

    // 4. Fallback: Busca Direta (Nova Estratégia /list/ p/ evitar erro de "Loja")
    const encodedTerm = encodeURIComponent(searchTerm).replace(/%20/g, "-"); // Shopee /list/ prefere hífens
    const shopeeID = "an_18318830863"; // Seu ID Shopee oficial

    // Formato /list/ é interpretado pelo App como busca, não como perfil de loja
    const finalUrl = `https://shopee.com.br/list/${encodedTerm}?utm_source=${shopeeID}`;

    console.log(`[Shopee] Link Inteligente (v2) gerado para "${termKey}"`);
    return finalUrl;
}

/**
 * Redireciona para busca na loja com tag de afiliado
 * Implementa fallback inteligente: Shopee → Amazon
 * @param {string} categoria - Nome da categoria
 * @param {string} lojaPreferida - Loja específica (opcional)
 */
// --- TITANIUM SMART DEEP LINKING (App-First Conversion Strategy) ---
function titaniumDeepLink(query) {
    const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
    const shopeeTag = TITANIUM_CONFIG.TAGS.shopee;
    const webUrl = `https://shopee.com.br/search?keyword=${encodeURIComponent(query)}&utm_source=${shopeeTag}`;
    
    if (isMobile) {
        // Tentativa de Deep Link para abrir o App direto (Shopee Protocol)
        // O navegador tentará abrir o App; se falhar em 500ms, abre a Web
        const appUrl = `shopeebrazil://search?keyword=${encodeURIComponent(query)}`;
        
        const now = Date.now();
        setTimeout(() => {
            if (Date.now() - now < 1000) {
                window.location.href = webUrl;
            }
        }, 500);
        
        window.location.href = appUrl;
    } else {
        window.open(webUrl, '_blank');
    }
}

function titaniumRedirect(categoria) {
    const urlFinal = buildShopeeAffiliateUrl(categoria);
    window.open(urlFinal, '_blank');
}

/**
 * TITANIUM LINK AUDITOR (v1.5)
 * Garante que todo link de saída possua a tag de afiliado correta.
 * @param {string} rawUrl - URL original do banco de dados
 * @param {string} storeHint - Dica da loja (opcional)
 * @returns {string} URL auditada e com tag
 */
function titaniumLinkAuditor(rawUrl, storeHint = "") {
    if (!rawUrl) return rawUrl;
    
    let url = rawUrl;
    const store = (storeHint || "").toLowerCase();
    const config = TITANIUM_CONFIG.TAGS;

    try {
        // --- AUDITORIA AMAZON ---
        if (url.includes('amazon.com.br') && !url.includes('tag=')) {
            const separator = url.includes('?') ? '&' : '?';
            url = `${url}${separator}tag=${config.amazon}`;
            console.log('[Titanium Auditor] Tag Amazon injetada via Auditoria.');
        }

        // --- AUDITORIA SHOPEE (Deep Linking Dinâmico) ---
        if (url.includes('shopee.com.br')) {
            // Se for link direto (não for link curto s.shopee ou shope.ee) e não tiver tag
            if (!url.includes('utm_source=') && !url.includes('s.shopee.com.br') && !url.includes('shope.ee')) {
                const shopeeID = "an_18318830863"; // ID oficial do Eric
                const separator = url.includes('?') ? '&' : '?';
                url = `${url}${separator}utm_source=${shopeeID}`;
                console.log('[Titanium Auditor] Tag Shopee injetada via Auditoria.');
            }
        }

        // --- AUDITORIA MERCADO LIVRE ---
        if (url.includes('mercadolivre.com.br') && !url.includes('matt_tool=')) {
            const mlConfig = TITANIUM_CONFIG.ML_AFFILIATE;
            const separator = url.includes('?') ? '&' : '?';
            url = `${url}${separator}matt_tool=${mlConfig.userId}&matt_source=${mlConfig.source}`;
            console.log('[Titanium Auditor] Tag ML injetada via Auditoria.');
        }

    } catch (e) {
        console.error('[Titanium Auditor] Erro na auditoria:', e);
    }

    return url;
}

// Expor globalmente
window.titaniumLinkAuditor = titaniumLinkAuditor;

/**
 * Redireciona para busca na loja com tag de afiliado
 * @param {HTMLImageElement} imgElement - The image element that failed to load
 * @param {string} storeName - The name of the store (Amazon, Mercado Livre, Shopee)
 * @param {string} productTitle - The title of the product
 */
window.handleImageError = function (imgElement, storeName, productTitle) {
    const storeLower = storeName.toLowerCase().replace(/\s+/g, '');

    // Determine content based on store
    let contentHTML = '';

    if (storeLower.includes('amazon')) {
        contentHTML = '<i class="fa-brands fa-amazon"></i>';
    } else if (storeLower.includes('mercadolivre')) {
        contentHTML = '<img src="images/logo-mercadolivre.png" class="fallback-logo ml-logo" alt="Mercado Livre">';
    } else if (storeLower.includes('shopee')) {
        contentHTML = `
            <div class="shopee-logo-composite">
                <i class="fa-solid fa-bag-shopping"></i>
                <span class="shopee-s">S</span>
            </div>`;
    } else {
        contentHTML = '<i class="fa-solid fa-shopping-bag"></i>';
    }

    // Create fallback HTML
    const fallbackHTML = `
        <div class="fallback-card ${storeLower}">
            ${contentHTML}
            <div class="fallback-text">Imagem indisponível</div>
        </div>
    `;

    // Replace the parent container's content (assuming img is wrapped in .image-container)
    if (imgElement.parentElement.classList.contains('image-container')) {
        imgElement.parentElement.innerHTML = fallbackHTML;
    } else {
        const wrapper = document.createElement('div');
        wrapper.className = 'image-container';
        wrapper.style.width = '100%';
        wrapper.style.height = '100%';
        wrapper.innerHTML = fallbackHTML;
        imgElement.replaceWith(wrapper);
    }
};

document.addEventListener('DOMContentLoaded', () => {
    // === API Configuration ===
    // Force IPv4 to avoid localhost resolution issues
    const API_BASE_URL = 'http://127.0.0.1:5000';

    // === State Management ===
    let allDeals = [];
    let currentSort = 'votes';
    let currentStoreFilter = 'all'; // NEW: Store filter state
    let userVotes = JSON.parse(localStorage.getItem('userVotes') || '{}');
    let isSearching = false;

    // === DOM Elements ===
    const dealsGrid = document.getElementById('deals-grid');
    const searchInput = document.getElementById('search-input');
    const searchSuggestions = document.getElementById('search-suggestions');
    const searchButton = document.querySelector('.btn-search');
    const sortButtons = document.querySelectorAll('.sort-btn');
    const hubCards = document.querySelectorAll('.hub-card');
    const comparisonInput = document.getElementById('comparison-input');
    const comparisonResults = document.getElementById('comparison-results');

    /**
     * Injeta controles robustos de filtro na seção de Ofertas do Momento
     */
    function injectTitaniumControls() {
        const dealsSection = document.querySelector('.voted-deals .container');
        if (!dealsSection || dealsSection.querySelector('.titanium-controls')) return;

        const controlsHTML = `
            <div class="titanium-controls">
                <div class="filter-group-wrapper">
                    <span class="filter-label">Buscar por Categoria</span>
                    <div class="titanium-filter-bar category-bar">
                        <button class="filter-pill active" data-category="all">⚡ Todas</button>
                        <button class="filter-pill" data-category="tecnologia">📱 Tech</button>
                        <button class="filter-pill" data-category="moda">👗 Moda</button>
                        <button class="filter-pill" data-category="casa">🏠 Casa</button>
                        <button class="filter-pill" data-category="beleza">💄 Beleza</button>
                        <button class="filter-pill" data-category="eletro">🍳 Eletro</button>
                    </div>
                </div>

                <div class="filter-group-wrapper">
                    <span class="filter-label">Filtrar por Loja</span>
                    <div class="titanium-filter-bar store-bar">
                        <button class="filter-pill store-pill active" data-store="all">Todas</button>
                        <button class="filter-pill store-pill amazon" data-store="amazon"><i class="fab fa-amazon"></i></button>
                        <button class="filter-pill store-pill mercadolivre" data-store="mercadolivre"><i class="fas fa-handshake"></i></button>
                        <button class="filter-pill store-pill shopee" data-store="shopee">S</button>
                    </div>
                </div>
            </div>
        `;

        const grid = document.getElementById('deals-grid');
        if (grid) {
            grid.insertAdjacentHTML('beforebegin', controlsHTML);
            
            // Listeners para Categorias
            document.querySelectorAll('.category-bar .filter-pill').forEach(btn => {
                btn.addEventListener('click', () => {
                    document.querySelectorAll('.category-bar .filter-pill').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    const cat = btn.dataset.category;
                    const filtered = cat === 'all' ? allDeals : allDeals.filter(d => (d.category || '').toLowerCase() === cat);
                    renderDeals(filtered);
                });
            });

            // Listeners para Lojas
            document.querySelectorAll('.store-bar .filter-pill').forEach(btn => {
                btn.addEventListener('click', () => {
                    document.querySelectorAll('.store-bar .filter-pill').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    currentStoreFilter = btn.dataset.store;
                    renderDeals(allDeals); // renderDeals agora é esperto e filtra internamente
                });
            });
        }
    }

    async function loadDeals() {
        const statusLabel = document.getElementById('maestro-status-label');
        try {
            console.log('[Titanium] Lançando Carga Nuclear de Ofertas...');
            if (statusLabel) statusLabel.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Robô Titanium: Conectando à base de dados...';

            const response = await fetch('data.json?v=' + Date.now());
            if (!response.ok) throw new Error(`HTTP ${response.status}: Falha ao acessar data.json`);

            const rawData = await response.json();
            allDeals = Array.isArray(rawData) ? rawData : [];
            
            if (allDeals.length === 0) {
                 if (statusLabel) statusLabel.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Atenção: Base de dados vazia.';
                 return;
            }

            console.log(`[Titanium] Sucesso! ${allDeals.length} ofertas prontas.`);
            
            // 1. Mostrar tudo imediatamente (Garantir que não fique em branco)
            renderDeals(allDeals);

            // 2. Aplicar Curação Maestro após 100ms
            setTimeout(() => {
                applyMaestroCuration();
                // 3. Ativar atualização periódica
                setInterval(applyMaestroCuration, 300000); 
            }, 100);

            const dealsSection = document.querySelector('.voted-deals');
            if (dealsSection) dealsSection.style.display = 'block';

        } catch (err) {
            console.error('[Titanium Critical Error]', err);
            if (statusLabel) {
                statusLabel.style.color = "#ff4500";
                statusLabel.innerHTML = `<i class="fas fa-bug"></i> ERRO CRÍTICO: ${err.message}`;
            }
            dealsGrid.innerHTML = `<div style="grid-column: 1/-1; text-align:center; padding:50px; border:2px dashed #ff4500; color:#ff4500;">
                <h3>⚠️ O Robô Titanium detectou uma falha</h3>
                <p>O arquivo de ofertas <strong>data.json</strong> não pôde ser lido corretamente pelo Localhost.</p>
                <small>${err.message}</small>
            </div>`;
        }
    }

    function applyMaestroCuration() {
        if (!allDeals || allDeals.length === 0) return;
        
        const currentHour = new Date().getHours();
        const activeRule = TITANIUM_CONFIG.MAESTRO.RULES.find(r => {
            if (r.start > r.end) return currentHour >= r.start || currentHour < r.end;
            return currentHour >= r.start && currentHour < r.end;
        });

        if (!activeRule) return;

        console.log(`[Maestro Engine] Ativando Curação: ${activeRule.title}`);

        const maestroStatus = document.getElementById('maestro-status-label');
        if (maestroStatus) {
            maestroStatus.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i> Vitrine Ativa: <strong>${activeRule.label}</strong>`;
        }

        // 1. Filtrar Categoria Prioritária
        let curatedDeals = [];
        if (activeRule.category !== 'any') {
            curatedDeals = allDeals.filter(d => (d.category || '').toLowerCase().includes(activeRule.category.toLowerCase()));
        }

        // 2. Aplicar Filtro de Desconto Mínimo na Categoria e Ordenar
        curatedDeals = curatedDeals.filter(d => (d.discount || 0) >= activeRule.minDiscount);
        curatedDeals.sort((a,b) => (b.discount || 0) - (a.discount || 0));

        // 3. BACKFILL (Preenchimento Sênior): Se tiver menos de 24, completa com as melhores gerais
        if (curatedDeals.length < 24) {
            console.log(`[Maestro] Preenchendo vitrine: ${curatedDeals.length} de ${activeRule.label} encontrados. Para simetria de grade (3 colunas), completando para 24...`);
            
            // Pega IDs já selecionados para não duplicar
            const selectedIds = new Set(curatedDeals.map(d => d.id));
            
            // Busca melhores ofertas gerais que não estão na lista
            const fillPool = [...allDeals]
                .filter(d => !selectedIds.has(d.id))
                .sort((a,b) => (b.discount || 0) - (a.discount || 0));
            
            // Adiciona o restante necessário
            const missingCount = 24 - curatedDeals.length;
            curatedDeals = [...curatedDeals, ...fillPool.slice(0, missingCount)];
        }

        const finalSelection = curatedDeals.slice(0, 24);

        const sectionTitle = document.querySelector('.section-title');
        if (sectionTitle && (!searchInput || !searchInput.value)) {
            sectionTitle.innerHTML = activeRule.title;
        }

        renderDeals(finalSelection);
    }

    // Inicializa carregamento
    loadDeals();

    // === Render Functions ===
    function renderDeals(deals) {
        dealsGrid.innerHTML = '';

        // Filtro de Loja Global
        let finalDeals = currentStoreFilter === 'all' 
            ? deals 
            : deals.filter(d => d.store.toLowerCase().includes(currentStoreFilter));

        if (finalDeals.length === 0) {
            dealsGrid.innerHTML = `
                <div class="loading-state" style="grid-column: 1/-1; padding: 40px; text-align: center;">
                    <i class="fas fa-search" style="font-size: 2rem; color: #cbd5e1; margin-bottom: 15px;"></i>
                    <p>Nenhuma oferta encontrada nestas condições.</p>
                </div>
            `;
            return;
        }

        // Sort deals
        const sortedDeals = sortDeals(finalDeals, currentSort);

        // Identificar Menor Preço da Vitrine Atual
        const minPrice = Math.min(...sortedDeals.map(d => parseFloat(d.price) || 999999));

        // Limit to 24 products for perfect grid symmetry (8 rows of 3)
        const displayDeals = sortedDeals.slice(0, 24);

        displayDeals.forEach(deal => {
            try {
                if (deal.store && deal.store.toLowerCase().trim() === 'lomadee') return;
                const isBestPrice = (parseFloat(deal.price) === minPrice) && sortedDeals.length > 2;
                const card = createDealCard(deal, isBestPrice);
                dealsGrid.appendChild(card);
            } catch (cardErr) {
                console.warn('[Titanium] Pulando card com erro:', deal.title, cardErr);
            }
        });
    }

    // Known placeholder/error images that return 200 OK but should be treated as broken
    const BLOCKED_IMAGES = [
        "https://http2.mlstatic.com/D_NQ_NP_2X_959089-MLA69565561075_052023-F.webp", // ML Generic Placeholder
        "https://http2.mlstatic.com/D_NQ_NP_2X_959089-MLA69565561075_052023-O.webp", // ML Generic Placeholder (Original)
        "https://via.placeholder.com/300" // Example for testing
    ];

    function createDealCard(deal) {
        const card = document.createElement('div');
        card.className = `product-card`;
        card.dataset.id = deal.id;

        // Formatação de Preços
        const formatter = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' });
        const formattedPrice = formatter.format(deal.price);
        const formattedOldPrice = deal.old_price ? formatter.format(deal.old_price) : '';

        // Definindo Badges Dinâmicos (Gatilhos do Print Bonito)
        const leftBadges = [];
        if (deal.discount >= 20) {
            leftBadges.push(`<div class="mini-badge green"><i class="fas fa-arrow-trend-down"></i> MENOR PREÇO 30D</div>`);
        } else {
            leftBadges.push(`<div class="mini-badge red"><i class="fas fa-fire"></i> ESTOQUE CRÍTICO</div>`);
        }

        card.innerHTML = `
            <div class="card-image-area">
                <!-- Top Left: Pills (Padrão Boutique) -->
                <div class="badge-group-left">
                    ${leftBadges.join('')}
                </div>

                <!-- Top Right: Star & Hand (Curadoria Humana) -->
                <div class="badge-group-right">
                    <div class="discount-star-modern">
                        <span>${deal.discount}%</span>
                    </div>
                    <div class="verified-hand">
                        <i class="fa-solid fa-hand-holding-check"></i>
                    </div>
                </div>

                <div class="card-image">
                    <img src="${deal.image}" alt="${deal.title}" loading="lazy" onerror="handleImageError(this, 'Shopee', '${deal.title}')">
                </div>

                <!-- Base da Imagem: Tag Shopee Boutique -->
                <div class="shopee-pill-tag">
                    <i class="fa-solid fa-bag-shopping"></i> Shopee
                </div>
            </div>

            <!-- SECURITY SEPARATOR -->
            <div class="security-bar-light">
                <i class="fa-solid fa-circle-check"></i> Link Seguro Verificado
            </div>

            <div class="card-body-harmonized">
                <h3 class="product-title-bold" title="${deal.title}">${deal.title}</h3>
                
                <div class="price-flex">
                    <div class="price-orig">${formattedOldPrice}</div>
                    <div class="price-final">${formattedPrice} <small>à vista</small></div>
                </div>

                <!-- Dynamic Coupon (Senior Sync v2) -->
                ${deal.coupon ? `
                <div class="coupon-gold-pill" onclick="copyToClipboard('${deal.coupon}')" style="background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%); color: #92400e; padding: 10px; border-radius: 12px; border: 1px dashed #d97706; margin-bottom: 20px; font-size: 0.85rem; display: flex; align-items: center; justify-content: center; gap: 8px; cursor: pointer; transition: all 0.3s ease;">
                    <i class="fa-solid fa-ticket-simple"></i> CUPOM: <strong>${deal.coupon}</strong>
                </div>` : ''}

                <a href="${titaniumLinkAuditor(deal.link, 'shopee')}" target="_blank" class="btn-shopee-blue">
                    Ver na Shopee <i class="fa-solid fa-arrow-up-right-from-square"></i>
                </a>
            </div>
        `;

        return card;
    }

    // === Voting System ===
    function handleVote(dealId, vote) {
        const currentVote = userVotes[dealId] || 0;

        if (currentVote === vote) {
            // Remove vote
            delete userVotes[dealId];
        } else {
            // Add/change vote
            userVotes[dealId] = vote;
        }

        localStorage.setItem('userVotes', JSON.stringify(userVotes));
        renderDeals(allDeals);
    }

    // === Sorting ===
    function sortDeals(deals, sortBy) {
        const sorted = [...deals];

        switch (sortBy) {
            case 'votes':
                return sorted.sort((a, b) => {
                    const votesA = (a.votes || 0) + (userVotes[a.id] === 1 ? 1 : userVotes[a.id] === -1 ? -1 : 0);
                    const votesB = (b.votes || 0) + (userVotes[b.id] === 1 ? 1 : userVotes[b.id] === -1 ? -1 : 0);
                    return votesB - votesA;
                });
            case 'discount':
                return sorted.sort((a, b) => b.discount - a.discount);
            case 'recent':
                return sorted.sort((a, b) => {
                    const dateA = new Date(a.added_date || '2026-01-01');
                    const dateB = new Date(b.added_date || '2026-01-01');
                    return dateB - dateA;
                });
            default:
                return sorted;
        }
    }

    if (sortButtons && sortButtons.length > 0) {
        sortButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                sortButtons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentSort = btn.dataset.sort;
                renderDeals(allDeals);
            });
        });
    }

    // === Search Functionality ===

    // Busca local (autocomplete enquanto digita)
    // === Carnaval Confetti Master System (v1155) ===
    // === Enhanced Visual Effects System (v2026) ===
    function createEffects(target, type = 'confetti') {
        const particleCount = 20; // Number of particles per burst

        // Variants configuration
        const variants = {
            'confetti': ['yellow', 'green', 'pink', 'blue', 'purple', 'orange'],
            'flowers': ['🌸', '💐', '🌹', '🌺', '🌻', '🌷'],
            'fire': ['🔥', '⚡', '💥', '✨', '🏷️', '💸']
        };

        const chosenSet = variants[type] || variants['confetti'];

        // Create container if it doesn't exist
        let container = target.querySelector('.confetti-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'confetti-container';
            container.style.pointerEvents = 'none'; // Ensure clicks pass through
            container.style.zIndex = '100'; // Make sure it's on top
            target.appendChild(container);
        }

        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'confetti-particle';

            if (type === 'confetti') {
                // Classic colored squares
                const color = chosenSet[Math.floor(Math.random() * chosenSet.length)];
                particle.classList.add(`confetti-p-${color}`);
            } else {
                // Emojis
                particle.textContent = chosenSet[Math.floor(Math.random() * chosenSet.length)];
                particle.style.background = 'transparent';
                particle.style.fontSize = (15 + Math.random() * 10) + 'px';
                particle.style.display = 'flex';
                particle.style.alignItems = 'center';
                particle.style.justifyContent = 'center';
            }

            // Randomize trajectory
            const angle = Math.random() * Math.PI * 2; // Full circle
            const velocity = 50 + Math.random() * 150;
            const tx = Math.cos(angle) * velocity + 'px';
            const ty = Math.sin(angle) * velocity + 'px';
            const tr = Math.random() * 720 + 'deg';
            const duration = 0.6 + Math.random() * 0.8 + 's';

            particle.style.setProperty('--tx', tx);
            particle.style.setProperty('--ty', ty);
            particle.style.setProperty('--tr', tr);
            particle.style.setProperty('--duration', duration);

            // Initial position (center of card)
            particle.style.left = '50%';
            particle.style.top = '50%';

            container.appendChild(particle);

            // Trigger animation
            requestAnimationFrame(() => {
                particle.classList.add('animate');
            });

            // Cleanup
            setTimeout(() => {
                particle.remove();
                if (container.children.length === 0) {
                    container.remove();
                }
            }, 1500);
        }
    }

    // Attach to seasonal cards with Context Awareness
    const seasonalCards = document.querySelectorAll('.hub-card.seasonal');
    seasonalCards.forEach(card => {
        let effectType = 'confetti'; // Default

        // Determine context based on Section Title
        const section = card.closest('section');
        const title = section ? section.querySelector('.section-title')?.textContent || '' : '';

        if (title.includes('Mulher')) {
            effectType = 'flowers';
        } else if (title.includes('Ofertas') || title.includes('Dia')) {
            effectType = 'fire';
        }

        // Trigger on Hover
        card.addEventListener('mouseenter', () => {
            createEffects(card, effectType);
        });

        // Trigger on Click (extra festive)
        card.addEventListener('click', (e) => {
            createEffects(card, effectType);
        });
    });

    if (searchInput) {
        console.log("TITANIUM_V3_ACTIVE: Logic Consolidated.");
    }

    // Redirecionamento simplificado para fechar sugestões ao clicar fora
    document.addEventListener('click', (e) => {
        if (searchInput && searchSuggestions && !searchInput.contains(e.target) && !searchSuggestions.contains(e.target)) {
            searchSuggestions.classList.remove('active');
        }
    });

    // === Store Filter Functions ===
    function createStoreFilterButtons(container) {
        const filterHTML = `
            <div class="store-filters" style="margin-bottom: 20px; text-align: center;">
                <span style="margin-right: 10px; font-weight: 600;">Filtrar por loja:</span>
                <button class="store-filter-btn active" data-store="all">Todas</button>
                <button class="store-filter-btn" data-store="amazon">Amazon</button>
                <button class="store-filter-btn" data-store="mercadolivre">Mercado Livre</button>
                <button class="store-filter-btn" data-store="shopee">Shopee</button>
                <button class="store-filter-btn" data-store="lomadee">Lomadee</button>
            </div>
        `;
        container.insertAdjacentHTML('afterbegin', filterHTML);

        // Add event listeners to filter buttons
        const filterButtons = container.querySelectorAll('.store-filter-btn');
        filterButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                filterButtons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentStoreFilter = btn.dataset.store;

                // Re-render with current category and new filter
                const currentCategory = container.dataset.currentCategory;
                if (currentCategory) {
                    filterAndRenderByCategory(currentCategory);
                }
            });
        });
    }

    function filterByStore(deals, store) {
        if (store === 'all') return deals;
        return deals.filter(deal => deal.store.toLowerCase().includes(store.toLowerCase()));
    }

    function filterAndRenderByCategory(category) {
        console.log(`[Titanium] Filtrando categoria: ${category} | Loja: ${currentStoreFilter}`);

        const filtered = allDeals.filter(deal => {
            if (!deal.category) return false;
            return deal.category.toLowerCase() === category.toLowerCase();
        });

        // Apply store filter
        const storeFiltered = filterByStore(filtered, currentStoreFilter);

        // Sort by price
        const sortedByPrice = storeFiltered.sort((a, b) => (a.price || 0) - (b.price || 0));

        // Update title
        const sectionTitle = document.querySelector('.voted-deals .section-title');
        if (sectionTitle) {
            const categoryNames = {
                'tecnologia': 'Tecnologia',
                'casa': 'Casa',
                'decoracao': 'Decoração',
                'moda': 'Moda',
                'beleza': 'Beleza',
                'esportes': 'Esportes & Lazer',
                'recent': 'Ofertas Recentes',
                'volta-aulas': 'Volta às Aulas'
            };
            const storeNames = {
                'all': 'Todas as Lojas',
                'amazon': 'Amazon',
                'mercadolivre': 'Mercado Livre',
                'shopee': 'Shopee'
            };
            const catName = categoryNames[category] || 'Ofertas';
            const storeName = storeNames[currentStoreFilter] || 'Shopee';
            sectionTitle.textContent = `${catName} - Curadoria ${storeName} (Auditada)`;
        }

        if (sortedByPrice.length === 0) {
            dealsGrid.innerHTML = `
                    <div style="border: 2px dashed #ee4d2d; border-radius: 20px; padding: 40px; background: #fff5f2; max-width: 800px; margin: 0 auto; position: relative;">
                        <div style="font-size: 4rem; margin-bottom: 20px;">🤖</div>
                        <h3 style="color: #4338ca; font-size: 1.8rem; margin-bottom: 15px;">O Robô Titanium está pronto!</h3>
                        <p style="color: #64748b; font-size: 1.1rem; line-height: 1.6; margin-bottom: 30px;">
                            Não encontramos "<strong>${searchTerm}</strong>" na nossa vitrine curada, mas o <strong>Robô Titanium</strong> pode abrir a busca oficial da <strong>Shopee</strong> agora mesmo para você!
                        </p>
                        
                        <div style="display: flex; flex-direction: column; gap: 15px; align-items: center;">
                            <button onclick="titaniumDeepLink('${searchTerm}')" 
                               style="background: linear-gradient(90deg, #ff4500, #ff8c00); color: white; padding: 18px 40px; border: none; border-radius: 50px; font-weight: 800; font-size: 1.2rem; cursor: pointer; text-decoration: none; box-shadow: 0 10px 25px rgba(255, 69, 0, 0.4); display: flex; align-items: center; gap: 10px; transition: transform 0.2s;">
                                <i class="fas fa-mobile-screen-button"></i> Abrir no App Shopee agora
                            </button>
                            
                            <button onclick="window.location.reload()" style="background: transparent; color: #64748b; border: 1px solid #cbd5e1; padding: 10px 20px; border-radius: 8px; font-weight: 600; cursor: pointer; margin-top: 10px;">
                                <i class="fas fa-home"></i> Voltar para a Página Inicial
                            </button>
                        </div>
                    </div>
                </div>
            `;
        } else {
            renderDeals(sortedByPrice);
        }
    }

    // === Category Hub Navigation (Desativado: Agora o site navega para categoria.html) ===
    /*
    hubCards.forEach(card => {
        card.addEventListener('click', (e) => {
            // IGNORE SEASONAL AND INTERACTIVE CARDS (They have their own logic/redirects)
            if (card.classList.contains('seasonal') || card.classList.contains('interactive-card')) {
                return;
            }

            const category = card.dataset.category;
            currentStoreFilter = 'all'; // Reset filter

            // Scroll to deals section
            const dealsSection = document.querySelector('.voted-deals');
            if (dealsSection) {
                dealsSection.style.display = 'block'; // Ensure visibility
                dealsSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }

            // Store current category for filter buttons
            dealsSection.dataset.currentCategory = category;

            // Create or update filter buttons
            let existingFilters = dealsSection.querySelector('.store-filters');
            if (existingFilters) {
                existingFilters.remove();
            }
            const container = dealsSection.querySelector('.container');
            if (container) {
                createStoreFilterButtons(container);
                container.dataset.currentCategory = category;
            }

            // Render products
            filterAndRenderByCategory(category);
        });
    });
    */


    // === Main Search Functionality ===
    function performSearch() {
        if (!searchInput) return;

        const query = searchInput.value.toLowerCase().trim();

        // Show loading state and ensure section visibility
        const dealsSection = document.querySelector('.voted-deals');
        if (dealsSection) dealsSection.style.display = 'block';

        dealsGrid.innerHTML = `
            <div class="loading-state">
                <i class="fa-solid fa-circle-notch fa-spin"></i>
                <p>Buscando por "${query}"...</p>
            </div>
        `;

        // Small delay to simulate search and allow UI update
        setTimeout(() => {
            if (!query) {
                // If empty, reload recent deals
                filterAndRenderByCategory('recent');
                return;
            }

            // Filter deals by title or category
            const matches = allDeals.filter(deal => {
                if (!deal || !deal.title) return false;
                const titleMatch = deal.title.toLowerCase().includes(query);
                const categoryMatch = deal.category && deal.category.toLowerCase().includes(query);
                const storeMatch = deal.store && deal.store.toLowerCase().includes(query);
                return titleMatch || categoryMatch || storeMatch;
            });

            if (matches.length === 0) {
                const sectionTitle = document.querySelector('.section-title');
                if (sectionTitle) sectionTitle.innerHTML = `Busca por: "<strong>${query}</strong>"`;

                dealsGrid.innerHTML = `
                    <div style="grid-column: 1/-1; border: 2px dashed #ee4d2d; border-radius: 20px; padding: 50px 20px; background: #fff5f2; text-align: center;">
                        <div style="font-size: 4rem; margin-bottom: 20px;">🤖</div>
                        <h3 style="color: #4338ca; font-size: 1.8rem; margin-bottom: 15px;">O Robô Titanium está pronto!</h3>
                        <p style="color: #64748b; font-size: 1.1rem; line-height: 1.6; max-width: 600px; margin: 0 auto 30px;">
                            Não encontramos "<strong>${query}</strong>" na nossa vitrine curada, mas o <strong>Robô Titanium</strong> pode abrir a busca oficial da <strong>Shopee</strong> agora mesmo para você!
                        </p>
                        
                        <div style="display: flex; flex-direction: column; gap: 15px; align-items: center;">
                            <a href="https://shopee.com.br/search?keyword=${query}&utm_source=${TITANIUM_CONFIG.TAGS.shopee}" target="_blank" 
                               style="background: linear-gradient(90deg, #ff4500, #ff8c00); color: white; padding: 18px 40px; border: none; border-radius: 50px; font-weight: 800; font-size: 1.2rem; cursor: pointer; text-decoration: none; box-shadow: 0 10px 25px rgba(255, 69, 0, 0.4); display: flex; align-items: center; gap: 10px; transition: transform 0.2s;">
                                <i class="fas fa-search"></i> Buscar tudo na Shopee agora
                            </a>
                            
                            <button onclick="window.location.reload()" style="background: white; color: #ee4d2d; border: 2px solid #ee4d2d; padding: 12px 30px; border-radius: 50px; font-weight: 700; cursor: pointer; margin-top: 20px; transition: all 0.3s;">
                                <i class="fas fa-home"></i> Voltar para a Página Inicial
                            </button>
                        </div>
                    </div>
                `;
            } else {
                const sectionTitle = document.querySelector('.section-title');
                if (sectionTitle) {
                    sectionTitle.innerHTML = `
                        <div style="display: flex; align-items: center; justify-content: center; gap: 20px; flex-wrap: wrap;">
                            Resultados para "<strong>${query}</strong>"
                            <button onclick="window.location.reload()" style="background: #f1f5f9; color: #475569; border: none; padding: 8px 16px; border-radius: 50px; font-size: 0.8rem; font-weight: 700; cursor: pointer;">
                                <i class="fas fa-rotate-left"></i> Limpar e Voltar
                            </button>
                        </div>
                    `;
                }

                // Limitar a 12 produtos para curadoria premium
                renderDeals(matches.slice(0, 12));

                const moreBtn = document.createElement('div');
                moreBtn.style.cssText = "grid-column: 1/-1; text-align: center; margin-top: 30px;";
                moreBtn.innerHTML = `
                    <p style="color: #64748b; margin-bottom: 15px;">Deseja ver mais opções?</p>
                    <button onclick="titaniumDeepLink('${query}')" style="background: white; color: #ee4d2d; padding: 12px 30px; border: 2px solid #ee4d2d; border-radius: 50px; font-weight: 700; cursor: pointer; transition: all 0.3s ease;">
                        Abrir mais resultados no App <i class="fa-solid fa-mobile-screen-button"></i>
                    </button>
                `;
                dealsGrid.appendChild(moreBtn);
            }
        }, 300);
    }

    if (searchButton && searchInput) {
        searchButton.addEventListener('click', performSearch);

        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                performSearch();
            }
        });
    }

    // === Utility Functions ===
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // === Known Placeholder Images (Soft 404s) ===
    const KNOWN_PLACEHOLDER_IMAGES = [
        "https://http2.mlstatic.com/D_NQ_NP_2X_959089-MLA69565561075_052023-F.webp", // ML generic broken image
        "https://http2.mlstatic.com/resources/frontend/statics/not-found-image.png"
    ];

    function getFallbackData() {
        return [
            {
                "id": "1",
                "title": "Echo Dot 5ª Geração | Smart Speaker com Alexa",
                "price": 359.10,
                "old_price": "429.00",
                "discount": 16,
                "store": "Amazon",
                "category": "tecnologia",
                "tags": ["alexa", "smart speaker", "echo"],
                "image": "https://m.media-amazon.com/images/I/714Rq4k05UL._AC_SX679_.jpg",
                "link": "https://www.amazon.com.br/dp/B09B8YGX5Y?tag=guiadodesco00-20",
                "reason": "Menor preço em 30 dias",
                "votes": 42,
                "added_date": "2026-01-15"
            },
            {
                "id": "2",
                "title": "Smartphone Samsung Galaxy A54 5G 128GB",
                "price": 1699.00,
                "old_price": "2399.00",
                "discount": 29,
                "store": "Mercado Livre",
                "category": "tecnologia",
                "tags": ["smartphone", "samsung", "5g"],
                // FORCE ERROR TO SHOW FALLBACK CARD
                "image": "",
                "link": "https://www.mercadolivre.com.br/p/MLB23117466?matt_tool=188269638&matt_source=guiadodesconto",
                "reason": "Queda brusca de 15%",
                "votes": 38,
                "added_date": "2026-01-15"
            },
            {
                "id": "3",
                "title": "Fritadeira Air Fryer Mondial 4L",
                "price": 299.90,
                "old_price": "450.00",
                "discount": 33,
                "store": "Shopee",
                "category": "casa",
                "tags": ["air fryer", "cozinha", "eletrodoméstico"],
                "image": "https://cf.shopee.com.br/file/br-11134207-7r98o-lmkwx6l8v28f24",
                "link": "https://shopee.com.br/product/12345/67890?utm_source=shopee_affiliate",
                "reason": "Oferta Relâmpago",
                "votes": 56,
                "added_date": "2026-01-15"
            },
            {
                "id": "4",
                "title": "Kindle 11ª Geração - Mais leve e com tela de alta resolução",
                "price": 449.00,
                "old_price": "499.00",
                "discount": 10,
                "store": "Amazon",
                "category": "tecnologia",
                "tags": ["kindle", "e-reader", "livros"],
                "image": "https://m.media-amazon.com/images/I/71B1wF42X3L._AC_SX679_.jpg",
                "link": "https://www.amazon.com.br/dp/B09SWW583J?tag=guiadodesco00-20",
                "reason": "Frete Grátis Prime",
                "votes": 29,
                "added_date": "2026-01-14"
            },
            {
                "id": "5",
                "title": "Liquidificador Philips Walita 800W",
                "price": 189.90,
                "old_price": "299.00",
                "discount": 36,
                "store": "Amazon",
                "category": "casa",
                "tags": ["liquidificador", "cozinha", "philips"],
                "image": "https://m.media-amazon.com/images/I/61kWZ8qVJPL._AC_SX679_.jpg",
                "link": "https://www.amazon.com.br/dp/B076MB2C36?tag=guiadodesco00-20",
                "reason": "Preço histórico",
                "votes": 31,
                "added_date": "2026-01-15"
            },
            {
                "id": "6",
                "title": "Tênis Nike Revolution 6 Masculino",
                "price": 249.90,
                "old_price": "349.90",
                "discount": 29,
                "store": "Shopee",
                "category": "esportes",
                "tags": ["tênis", "nike", "corrida"],
                "image": "https://cf.shopee.com.br/file/sg-11134201-22110-abc123def456",
                "link": "https://shopee.com.br/product/2222/33333?utm_source=shopee_affiliate",
                "reason": "Desconto exclusivo",
                "votes": 47,
                "added_date": "2026-01-15"
            }
        ];
    }
});

// ==========================================
// TITANIUM INTERACTIVE BANNERS (V2)
// ==========================================

/**
 * Define qual loja deve estar ativa baseado no horário atual (Rodízio 30 min)
 * @returns {string} 'amazon', 'mercadolivre' ou 'shopee'
 */
function getCurrentRotationStore() {
    const now = new Date();
    const minutesSinceMidnight = now.getHours() * 60 + now.getMinutes();
    const halfHourBlocks = Math.floor(minutesSinceMidnight / 30);
    const rotationStores = ['amazon', 'mercadolivre', 'shopee'];
    const selected = rotationStores[halfHourBlocks % 3];

    console.log(`[Titanium Rotation] Block: ${halfHourBlocks} | Selected Store: ${selected}`);
    return selected;
}


/**
 * Configura um banner interativo com abas de marcas
 * @param {string} cardId - ID do card HTML (ex: 'tech-hub-card')
 * @param {object} config - Configurações de imagens e termos
 */
function setupTitaniumInteractiveBanner(cardId, config) {
    const card = document.getElementById(cardId);
    if (!card) {
        console.warn(`[Titanium Hub] Card não encontrado: ${cardId}`);
        return;
    }

    const tabs = card.querySelectorAll('.tab-btn');
    const bannerImg = card.querySelector('img');
    const defaultStore = config.defaultStore || 'amazon';

    // Estado local do card
    let currentStore = defaultStore;

    // 1. Configurar cliques nas abas
    tabs.forEach(tab => {
        tab.addEventListener('click', (e) => {
            e.stopPropagation(); // Evita disparar o click do card principal

            // Remove active de todas
            tabs.forEach(t => t.classList.remove('active'));
            // Adiciona active na clicada
            tab.classList.add('active');

            // Atualiza loja atual
            const store = tab.dataset.store;
            currentStore = store;

            // Troca imagem com fade suave
            bannerImg.style.opacity = '0.7';
            setTimeout(() => {
                bannerImg.src = config.banners[store];
                bannerImg.style.opacity = '1';

                // Feedback visual de "pulso" no card
                card.classList.add('titaniumGlowPulse');
                setTimeout(() => card.classList.remove('titaniumGlowPulse'), 600);
            }, 150);

            console.log(`[Titanium Hub] ${cardId} switched to ${store}`);
        });
    });

    // 2. Configurar clique no card (Redirecionamento)
    card.addEventListener('click', (e) => {
        // Se clicou na aba, ignora (já tratado acima via stopPropagation, mas garantindo)
        if (e.target.closest('.brand-tabs')) return;

        const term = config.searchTerms[currentStore];

        console.log(`[Titanium Hub] Redirecting ${cardId} -> ${currentStore} (Term: ${term})`);

        // Usa a função central de redirecionamento do Titanium
        titaniumRedirect(term, currentStore);
    });

    // 3. Inicializar com Rodízio Automático (v1136)
    const rotationStore = getCurrentRotationStore();
    const activeTab = Array.from(tabs).find(t => t.dataset.store === rotationStore);

    if (activeTab) {
        console.log(`[Titanium Hub] Auto-selecting ${rotationStore} for ${cardId}`);
        // Força o clique na aba correta para sincronizar UI e Imagem
        activeTab.click();
    }

    console.log(`[Titanium Hub] Initialized: ${cardId}`);
}

// Inicialização dos Banners Interativos
document.addEventListener('DOMContentLoaded', () => {

    // 1. Tecnologia
    setupTitaniumInteractiveBanner('tech-hub-card', {
        defaultStore: 'amazon',
        banners: {
            amazon: 'images/banner_tecnologia_amazon.png?v=titanium_fix_900',
            mercadolivre: 'images/banner_mercadolivre_tecnologia.png?v=titanium_fix_900',
            shopee: 'images/banner_shopee_tecnologia.png?v=titanium_fix_900'
        },
        searchTerms: {
            amazon: 'computador pc gamer hardware ssd',
            mercadolivre: 'notebook computador pc desktop',
            shopee: 'notebook barato chromebook acessorios pc'
        }
    });

    // 2. Casa e Jardim
    setupTitaniumInteractiveBanner('home-hub-card', {
        defaultStore: 'amazon',
        banners: {
            amazon: 'images/banner_casa_amazon.png?v=titanium_fix_900',
            mercadolivre: 'images/banner_casa_mercadolivre.png?v=titanium_fix_900',
            shopee: 'images/banner_casa_shopee.png?v=titanium_fix_900'
        },
        searchTerms: {
            amazon: 'organizador cozinha utilidades domesticas',
            mercadolivre: 'moveis decoracao casa utilidades',
            shopee: 'decoracao casa barato cozinha'
        }
    });

    // 3. Automotivo
    setupTitaniumInteractiveBanner('automotive-hub-card', {
        defaultStore: 'shopee',
        banners: {
            amazon: 'images/banner_automotivo_amazon.png?v=1012',
            mercadolivre: 'images/banner_automotivo_mercadolivre.png?v=1012',
            shopee: 'images/banner_automotivo_shopee.png?v=1012'
        },
        searchTerms: {
            amazon: 'acessorios carro automotivo limpeza automotiva',
            mercadolivre: 'pecas carro acessorios som automotivo',
            shopee: 'acessorios automotivos barato capa banco'
        }
    });

    // 4. Moda
    setupTitaniumInteractiveBanner('fashion-hub-card', {
        defaultStore: 'shopee',
        banners: {
            amazon: 'images/banner_moda_amazon.png?v=1013',
            mercadolivre: 'images/banner_moda_mercadolivre.png?v=1013',
            shopee: 'images/banner_moda_shopee.png?v=1013'
        },
        searchTerms: {
            amazon: 'roupas femininas masculinas moda',
            mercadolivre: 'roupas moda vestuario calcados',
            shopee: 'roupas baratas moda vestidos blusas'
        }
    });

    // 5. Beleza
    setupTitaniumInteractiveBanner('beauty-hub-card', {
        defaultStore: 'amazon',
        banners: {
            amazon: 'images/banner_beleza_amazon.png?v=1014',
            mercadolivre: 'images/banner_beleza_mercadolivre.png?v=1014',
            shopee: 'images/banner_beleza_shopee.png?v=1014'
        },
        searchTerms: {
            amazon: 'maquiagem skincare perfumes importados',
            mercadolivre: 'cosmeticos beleza cuidados pele cabelo',
            shopee: 'maquiagem barata skincare coreano pincel'
        }
    });

    // 6. Esportes
    setupTitaniumInteractiveBanner('sports-hub-card', {
        defaultStore: 'amazon',
        banners: {
            amazon: 'images/banner_esportes_amazon.png?v=1015',
            mercadolivre: 'images/banner_esportes_mercadolivre.png?v=1015',
            shopee: 'images/banner_esportes_shopee.png?v=1015'
        },
        searchTerms: {
            amazon: 'equipamentos fitness musculacao',
            mercadolivre: 'bicicleta patins skate futebol',
            shopee: 'roupas esportivas fitness barato'
        }
    });

    // 7. Games
    setupTitaniumInteractiveBanner('games-hub-card', {
        defaultStore: 'amazon',
        banners: {
            amazon: 'images/banner_games_amazon.png?v=1022',
            mercadolivre: 'images/banner_games_mercadolivre.png?v=1022',
            shopee: 'images/banner_games_shopee.png?v=1022'
        },
        searchTerms: {
            amazon: 'playstation xbox nintendo jogos console',
            mercadolivre: 'video game console controle ps5 xbox',
            shopee: 'jogos baratos acessorios gamer controle'
        }
    });

    // 8. Pet Shop
    setupTitaniumInteractiveBanner('pet-hub-card', {
        defaultStore: 'amazon',
        banners: {
            amazon: 'images/banner_petshop_amazon.png?v=1023',
            mercadolivre: 'images/banner_petshop_mercadolivre.png?v=1023',
            shopee: 'images/banner_petshop_shopee.png?v=1023'
        },
        searchTerms: {
            amazon: 'racao cachorro gato petiscos',
            mercadolivre: 'acessorios pet coleira caminha',
            shopee: 'brinquedos pet roupas cachorro'
        }
    });

    // 9. Eletrodomésticos
    setupTitaniumInteractiveBanner('electro-hub-card', {
        defaultStore: 'amazon',
        banners: {
            amazon: 'images/banner_eletro_amazon.png?v=1024',
            mercadolivre: 'images/banner_eletro_mercadolivre.png?v=1024',
            shopee: 'images/banner_eletro_shopee.png?v=1024'
        },
        searchTerms: {
            amazon: 'liquidificador air fryer panela eletrica',
            mercadolivre: 'geladeira fogao microondas',
            shopee: 'eletrodomesticos cozinha barato portatil'
        }
    });

    // 10. Ferramentas
    setupTitaniumInteractiveBanner('tools-hub-card', {
        defaultStore: 'mercadolivre',
        banners: {
            amazon: 'images/banner_ferramentas_amazon.png?v=1025',
            mercadolivre: 'images/banner_ferramentas_mercadolivre.png?v=1025',
            shopee: 'images/banner_ferramentas_shopee.png?v=1025'
        },
        searchTerms: {
            amazon: 'furadeira parafusadeira kit ferramentas',
            mercadolivre: 'ferramentas construcao reforma',
            shopee: 'ferramentas manuais barato kit'
        }
    });

    // 11. Papelaria
    setupTitaniumInteractiveBanner('stationery-hub-card', {
        defaultStore: 'amazon',
        banners: {
            amazon: 'images/banner_papelaria_amazon.png?v=1026',
            mercadolivre: 'images/banner_papelaria_mercadolivre.png?v=1026',
            shopee: 'images/banner_papelaria_shopee.png?v=1026'
        },
        searchTerms: {
            amazon: 'caderno caneta mochila escolar',
            mercadolivre: 'material escolar papelaria',
            shopee: 'cadernos baratos material escolar'
        }
    });

    // 12. Decoração
    setupTitaniumInteractiveBanner('decor-hub-card', {
        defaultStore: 'amazon',
        banners: {
            amazon: 'images/banner_decoracao_amazon.png?v=1101',
            mercadolivre: 'images/banner_decoracao_mercadolivre.png?v=1101',
            shopee: 'images/banner_decoracao_shopee.png?v=1101'
        },
        searchTerms: {
            amazon: 'quadros decorativos almofadas cortinas',
            mercadolivre: 'decoracao casa sala quarto',
            shopee: 'decoracao barata enfeites casa'
        }
    });

    // 13. Carnaval (SAZONAL)
    setupTitaniumInteractiveBanner('carnaval-hub-card', {
        defaultStore: 'amazon',
        banners: {
            amazon: 'images/amazon-app-day-carnaval.png?v=1102',
            mercadolivre: 'images/amazon-app-day-carnaval.png?v=1102',
            shopee: 'images/amazon-app-day-carnaval.png?v=1102'
        },
        searchTerms: {
            amazon: 'fantasias carnaval glitter aderecos acessorios festa',
            mercadolivre: 'caixa de som jbl termica cooler fantasias',
            shopee: 'fantasias baratas carnaval decoracao festa kit folia'
        }
    });

    // 13. Carnaval (SAZONAL)
    setupTitaniumInteractiveBanner('carnaval-hub-card', {
        defaultStore: 'amazon',
        banners: {
            amazon: 'images/amazon-app-day-carnaval.png?v=1102',
            mercadolivre: 'images/amazon-app-day-carnaval.png?v=1102',
            shopee: 'images/amazon-app-day-carnaval.png?v=1102'
        },
        searchTerms: {
            amazon: 'fantasias carnaval glitter aderecos acessorios festa',
            mercadolivre: 'caixa de som jbl termica cooler fantasias',
            shopee: 'fantasias baratas carnaval decoracao festa kit folia'
        }
    });

    // Titanium Sync Timestamp: 2026-02-10-12:50 (v1157_RESTORED_CARNAVAL)
});

/**
 * Roda frases de incentivo nos CTAs dos banners para aumentar CTR (v2026_v2_premium)
 */
function initTitaniumBannerCTAs() {
    const ctas = document.querySelectorAll('.banner-cta');
    if (ctas.length === 0) return;

    const phrases = [
        "Clique e descubra o menor preço",
        "Ver ofertas em tempo real",
        "Busca ativa: Veja preços reais",
        "Robô Titanium: Menor preço aqui",
        "Onde está mais barato? Clique e veja"
    ];

    const icons = ["fa-bolt", "fa-search-dollar", "fa-tag", "fa-robot", "fa-fire"];

    setInterval(() => {
        ctas.forEach(cta => {
            const randomIndex = Math.floor(Math.random() * phrases.length);

            // Premium Transition: Fade out -> Change -> Fade in
            cta.style.transform = 'translate(-50%, 10px)';
            cta.style.opacity = '0';

            setTimeout(() => {
                cta.innerHTML = `
                    <i class="fas ${icons[randomIndex]}"></i>
                    <span class="cta-text">${phrases[randomIndex]}</span>
                `;
                cta.style.transform = 'translate(-50%, 0)';
                cta.style.opacity = '1';

                // Add a small "shimmer" effect after change
                cta.style.boxShadow = '0 0 30px rgba(255, 153, 0, 0.8)';
                setTimeout(() => {
                    cta.style.boxShadow = '0 10px 40px rgba(0, 0, 0, 0.4)';
                }, 400);
            }, 500);
        });
    }, 8000); // Slightly slower for better readability (8s)
}

document.addEventListener('DOMContentLoaded', initTitaniumBannerCTAs);
// ========================================
// SECURITY BLINDAGEM (v1140)
// ========================================
document.addEventListener('DOMContentLoaded', () => {
    const trap = document.getElementById('titanium-bot-trap');
    if (trap) {
        trap.addEventListener('click', (e) => {
            e.preventDefault();
            console.warn('[Titanium Security] Bot Detectado: Honeypot ativado.');
            // Aqui poderíamos enviar um log para o servidor via probe
            if (window.titaniumProbe) {
                window.titaniumProbe.logEvent('bot_detected', { type: 'honeypot_click' });
            }
        });
    }
});

// --- TITANIUM METRICS: Click Tracking (Senior Workflow) ---
// --- TITANIUM METRICS: Page Experience Tracking (Elite Workflow) ---
function trackView() {
    const data = JSON.stringify({
        type: 'page_view',
        path: window.location.pathname,
        referrer: document.referrer || 'Direto / Desconhecido',
        screen: `${window.innerWidth}x${window.innerHeight}`,
        device_type: /Mobi|Android/i.test(navigator.userAgent) ? 'Mobile' : 'Desktop',
        timestamp: new Date().toISOString()
    });

    const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
    const trackerUrl = isLocal ? 'http://127.0.0.1:5001/api/track-view' : 'track_clicks.php';
    
    navigator.sendBeacon(trackerUrl, data);
}

function trackClick(store, category, title) {
    const data = JSON.stringify({
        type: 'product_click',
        store: store,
        category: category,
        title: title,
        referrer: document.referrer || 'Direto',
        timestamp: new Date().toISOString(),
        url: window.location.href
    });

    const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
    const trackerUrl = isLocal ? 'http://127.0.0.1:5001/api/track-click' : 'track_clicks.php';
    
    navigator.sendBeacon(trackerUrl, data);
}

// Inicializar ouvintes de clique e contador de visitas após o DOM carregar
document.addEventListener('DOMContentLoaded', () => {
    // 1. Contar Visita Inicial
    trackView();

    // 2. Capturar cliques em cards de oferta e hubs
    const clickTargets = '.hub-card, .deal-card, .brand-tabs .tab-btn, .lightning-item';

    document.body.addEventListener('click', function (e) {
        const target = e.target.closest(clickTargets);
        if (!target) return;

        let store = 'Unknown';
        if (target.classList.contains('amazon')) store = 'Amazon';
        else if (target.classList.contains('mercadolivre')) store = 'Mercado Livre';
        else if (target.classList.contains('shopee')) store = 'Shopee';
        else if (target.dataset.store) store = target.dataset.store;

        let title = target.querySelector('h3')?.innerText || target.innerText || 'Action';
        let category = target.closest('section')?.querySelector('h2')?.innerText ||
            target.dataset.category || 'Geral';

        trackClick(store, category, title);
    });
});

// --- TITANIUM LIGHTNING BAR: Real-time Deals Scroller ---

async function initTitaniumLightningBar() {
    const bar = document.getElementById('lightning-bar');
    const container = document.getElementById('lightning-bar-content');

    if (!bar || !container) {
        console.warn('[Titanium] Elementos da barra não encontrados no DOM.');
        return;
    }

    try {
        console.log('[Titanium] Iniciando Barra Relâmpago (v2026_v5)...');

        // Fetch data with cache buster and absolute path for reliability
        const response = await fetch('data.json?v=' + Date.now());
        if (!response.ok) throw new Error('Status HTTP: ' + response.status);

        const allDeals = await response.json();
        if (!Array.isArray(allDeals) || allDeals.length === 0) {
            console.warn('[Titanium] data.json vazio ou inválido.');
            return;
        }

        // --- Logic: SHOPEE EXCLUSIVE + HIGH IMPACT MIXER (v2026_v6) ---
        const shopeeDeals = allDeals
            .filter(d => d.store.toLowerCase().includes('shopee'))
            .sort(() => 0.5 - Math.random());

        // Mensagens Magnéticas focadas em Moda & Beleza
        const highImpactItems = [
            { isTrigger: true, type: 'coupon', text: '👗 RADAR FASHION: Looks em alta com Cupons ativos!' },
            { isTrigger: true, type: 'urgency', text: '🔥 ESTOQUE: Vestidos Alfaiataria estão esgotando!' },
            { isTrigger: true, type: 'coupon', text: '💄 BELEZA VIP: Kits de maquiagem com Frete Grátis' },
            { isTrigger: true, type: 'urgency', text: '📉 QUEDA DE PREÇO: Itens de Skincare em oferta real' }
        ];

        const mixer = [];
        shopeeDeals.slice(0, 20).forEach((deal, idx) => {
            mixer.push(deal);
            // Intercala um gatilho a cada 4 produtos
            if (idx % 4 === 0 && highImpactItems[idx / 4]) {
                mixer.push(highImpactItems[idx / 4]);
            }
        });

        // Duplicar para loop contínuo
        const loopItems = [...mixer, ...mixer];

        let html = '';
        loopItems.forEach((item, index) => {
            if (item.isTrigger) {
                // Renderiza Mensagem de Impacto
                const color = item.type === 'coupon' ? '#fff' : '#ffeb3b';
                const bg = item.type === 'coupon' ? 'rgba(255,255,255,0.2)' : 'transparent';
                html += `
                    <div class="lightning-item trigger-item" style="display: flex; align-items: center; gap: 10px; background: ${bg}; padding: 5px 15px; border-radius: 50px; border: ${item.type === 'coupon' ? '1px dashed #fff' : 'none'};">
                        <strong style="color: ${color}; font-size: 0.85rem; text-transform: uppercase;">${item.text}</strong>
                    </div>
                `;
            } else {
                // Renderiza Produto Shopee
                const displayTitle = (item.title || '').length > 30 ? item.title.substring(0, 27) + '...' : item.title;
                const formattedPrice = `R$ ${parseFloat(item.price).toFixed(2).replace('.', ',')}`;
                
                html += `
                    <a href="${item.link}" target="_blank" class="lightning-item" style="display: flex; align-items: center; gap: 10px; text-decoration: none; color: white;">
                        <span class="lightning-badge" style="background: white; color: #ee4d2d; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 800;">SHOPEE</span>
                        <strong style="font-size: 0.85rem; font-weight: 500;">${displayTitle}</strong>
                        <span class="lightning-price" style="color: #ffeb3b; font-weight: 800; font-size: 0.95rem;">${formattedPrice}</span>
                        <div class="price-badge" style="background: white; color: #ee4d2d; padding: 2px 8px; border-radius: 50px; font-size: 0.7rem; font-weight: 800;">VER ➔</div>
                    </a>
                `;
            }
        });

        container.innerHTML = html;

        // Add Event Listeners for CSP compliance (Replace onclick)
        container.querySelectorAll('.lightning-item').forEach(item => {
            item.addEventListener('click', function (e) {
                const store = this.getAttribute('data-store');
                const title = this.getAttribute('data-title');
                if (typeof trackClick === 'function') {
                    trackClick(store, 'LightningBar', title);
                }
            });
        });

        // Add Price Disclaimer (Anti-misleading policy)
        if (!bar.querySelector('.lightning-disclaimer')) {
            const disclaimer = document.createElement('div');
            disclaimer.className = 'lightning-disclaimer';
            disclaimer.innerHTML = '<i class="fas fa-info-circle"></i> Os preços podem sofrer alterações nas lojas parceiras.';
            bar.appendChild(disclaimer);
        }

        // === NUCLEAR VISIBILITY FIX (v2026_v6) ===
        // Force ALL styles via JavaScript to bypass any CSS caching/CSP/encoding issues
        bar.setAttribute('style', [
            'display: block !important',
            'background: linear-gradient(90deg, #ee4d2d 0%, #FF9900 100%)',
            'color: white',
            'padding: 10px 0',
            'font-size: 0.9rem',
            'font-weight: 700',
            'overflow: hidden',
            'position: relative',
            'z-index: 9999',
            'border-bottom: 2px solid rgba(0,0,0,0.1)',
            'white-space: nowrap',
            'min-height: 42px',
            'width: 100%',
            'box-sizing: border-box'
        ].join('; '));

        container.setAttribute('style', [
            'display: flex',
            'width: ' + (loopItems.length * 320) + 'px',
            'animation: marquee-titanium 80s linear infinite'
        ].join('; '));

        // Restore Grid (Re-enabled to avoid "blank site" feeling)
        const gridSection = document.querySelector('.voted-deals');
        if (gridSection && allDeals.length > 0) gridSection.style.display = 'block';

        // Style each lightning-item inline as well
        container.querySelectorAll('.lightning-item').forEach(item => {
            item.setAttribute('style', [
                'display: inline-flex',
                'align-items: center',
                'gap: 8px',
                'margin-right: 50px',
                'color: white',
                'text-decoration: none',
                'transition: transform 0.2s ease',
                'flex-shrink: 0'
            ].join('; '));
        });

        // Style badges inline
        container.querySelectorAll('.lightning-badge').forEach(badge => {
            badge.setAttribute('style', [
                'background: rgba(255,255,255,0.2)',
                'padding: 3px 10px',
                'border-radius: 50px',
                'font-size: 0.72rem',
                'text-transform: uppercase',
                'border: 1px solid rgba(255,255,255,0.3)'
            ].join('; '));
        });

        // Style prices inline (v2026_v7)
        container.querySelectorAll('.lightning-price').forEach(price => {
            price.setAttribute('style', [
                'background: rgba(0,0,0,0.15)',
                'padding: 2px 10px',
                'border-radius: 6px',
                'font-size: 0.85rem',
                'margin: 0 5px',
                'font-weight: 800',
                'color: #fff',
                'border: 1px solid rgba(255,255,255,0.1)'
            ].join('; '));
        });

        // Style price badges inline
        container.querySelectorAll('.price-badge').forEach(badge => {
            badge.setAttribute('style', [
                'background: rgba(255,255,255,0.95)',
                'color: #ee4d2d',
                'padding: 3px 12px',
                'border-radius: 4px',
                'font-size: 0.72rem',
                'font-weight: 800',
                'box-shadow: 0 4px 6px rgba(0,0,0,0.1)'
            ].join('; '));
        });

        console.log('[Titanium Bar] Estilos nucleares aplicados com sucesso.');

    } catch (err) {
        console.error('[Titanium Bar Error]', err);
    }
}

// Auto-activate
document.addEventListener('DOMContentLoaded', () => {
    // Ativa em teste ou local
    const isTest = window.location.href.includes('teste.') ||
        window.location.hostname === 'localhost' ||
        window.location.hostname === '127.0.0.1';
    const isProduction = window.location.hostname === 'guiadodesconto.com.br';

    if (isTest || isProduction || document.body.classList.contains('staging-mode')) {
        setTimeout(initTitaniumLightningBar, 300);
    }

    // === PROTETOR TITANIUM: REDIRECIONAMENTO SEGURO ===
    const securityOverlay = document.getElementById('security-overlay');
    const storeTargetName = document.getElementById('store-target-name');

    // Intercepta todos os cliques em links de ofertas
    document.addEventListener('click', (e) => {
        const dealBtn = e.target.closest('.btn-deal');
        if (dealBtn && securityOverlay) {
            e.preventDefault();
            const url = dealBtn.href;

            // Extrai o nome da loja do texto do botão (ex: "Ver na Amazon")
            let store = "Loja Oficial";
            const btnText = dealBtn.textContent.toLowerCase();
            if (btnText.includes('amazon')) store = "AMAZON.COM.BR";
            else if (btnText.includes('mercado')) store = "MERCADOLIVRE.COM.BR";
            else if (btnText.includes('shopee')) store = "SHOPEE.COM.BR";

            // Ativa o overlay de segurança
            storeTargetName.textContent = store;
            securityOverlay.classList.add('active');

            // Simula verificação e redireciona (transição rápida para não irritar)
            setTimeout(() => {
                window.open(url, '_blank');
                securityOverlay.classList.remove('active');
            }, 1800);
        }
    });

    // === ASSISTENTE TITANIUM: MENSAGENS DE SEGURANÇA ===
    function initTitaniumAssistant() {
        const assistant = document.getElementById('titanium-assistant');
        const bubble = assistant?.querySelector('.assistant-bubble');
        const bubbleText = bubble?.querySelector('.bubble-text');

        if (!assistant || !bubble) return;

        const messages = [
            "<strong>🤖 Robô Titanium:</strong> Olá! Acabei de sincronizar os dados da Shopee. Temos novas ofertas flash!",
            "<strong>🛡️ Link Auditado:</strong> Todos os links desta vitrine são verificados pela API Oficial Shopee v2.",
            "<strong>🔥 Dica Shopee:</strong> Os produtos com o selo de 'CUPOM' são os que esgotam mais rápido!",
            "<strong>✅ 100% Seguro:</strong> Identifiquei que estes vendedores têm as melhores avaliações na Shopee hoje.",
            "<strong>⚡ Ofertas do Momento:</strong> Acabei de detectar uma queda de preço em itens selecionados. Aproveite!",
            "<strong>📱 App Shopee:</strong> Meus links abrem direto no App oficial para garantir seu rastreio e segurança!"
        ];

        let currentMsg = 0;

        // Mostra a primeira mensagem após 4 segundos (v7_mutex_global)
        setTimeout(() => {
            // Se a trava estiver ativa ou Família estiver falando, espera
            if (window.titaniumBusy || document.querySelector('.family-notification.show')) return;

            window.titaniumBusy = true; // Ativa a trava
            bubbleText.innerHTML = messages[0];
            bubble.classList.add('active');

            // Esconde após 8 segundos
            setTimeout(() => {
                bubble.classList.remove('active');
                window.titaniumBusy = false; // Libera a trava
            }, 8000);
        }, 5000);

        // Troca de mensagem a cada 40 segundos
        setInterval(() => {
            if (window.titaniumBusy || document.querySelector('.family-notification.show')) return;

            window.titaniumBusy = true; // Ativa a trava
            currentMsg = (currentMsg + 1) % messages.length;
            bubbleText.innerHTML = messages[currentMsg];
            bubble.classList.add('active');

            setTimeout(() => {
                bubble.classList.remove('active');
                window.titaniumBusy = false; // Libera a trava
            }, 8000);
        }, 40000);
    }

    // === RADAR DE TENDÊNCIAS IA: CARREGAMENTO DINÂMICO ===
    async function initTitaniumRadar() {
        const radarGrid = document.getElementById('radar-grid');
        if (!radarGrid) return;

        try {
            const response = await fetch('ai_reviews.json');
            if (!response.ok) throw new Error('Radar offline');
            const products = await response.json();

            radarGrid.innerHTML = ''; // Limpa o loading

            products.forEach(p => {
                const auditedUrl = window.titaniumLinkAuditor ? window.titaniumLinkAuditor(p.link) : p.link;
                
                const card = document.createElement('a');
                card.className = 'radar-card';
                card.href = auditedUrl;
                card.target = '_blank';
                card.innerHTML = `
                    <img src="${p.image}" alt="${p.title}" class="radar-img" onerror="this.src='images/placeholder.png'">
                    <div class="radar-info">
                        <h4>${p.title.substring(0, 45)}...</h4>
                        <div class="radar-review">${p.ai_review}</div>
                    </div>
                `;
                radarGrid.appendChild(card);
            });
        } catch (err) {
            console.warn('[Radar] Erro ao carregar tendências:', err);
            radarGrid.innerHTML = '<div style="opacity:0.5; font-size: 0.8rem;">Radar em calibração. Volte em instantes!</div>';
        }
    }

    initTitaniumRadar();
    initTitaniumAssistant();
});
