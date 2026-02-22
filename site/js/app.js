// ========================================
// GUIA DO DESCONTO - MAIN APPLICATION
// ========================================

// === CONFIGURAÇÃO ROBÔ TITANIUM (v2026-fix-01) ===
const TITANIUM_CONFIG = {
    // Tags reais de afiliado
    TAGS: {
        amazon: "guiadodesco00-20",     // ✅ Amazon Associates
        mercadolivre: "ericmacedo",     // ✅ ML Afiliados (via Share Flow)
        shopee: "ericmacedo"            // ✅ Tag Shopee (Mantida p/ compatibilidade)
    },
    // Mercado Livre - Configuração OAuth
    ML_AFFILIATE: {
        userId: "188269638",             // User ID obtido via OAuth
        source: "guiadodesconto",        // Identificador da fonte
        trackingPrefix: "gdd"            // Prefixo para tracking_id
    },
    // Prioridade de redirecionamento (fallback)
    PRIORIDADE: ['amazon', 'mercadolivre', 'shopee'],
    // Status das lojas
    STATUS: {
        amazon: true,
        mercadolivre: true,
        shopee: true,
        lomadee: true
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
        'tracking_id': generateTrackingId()      // ID único para cada clique
    });

    const finalUrl = `${baseUrl}?${params.toString()}`;

    console.log('[Titanium ML] Link Inteligente (Price Sort) gerado:', finalUrl);
    return finalUrl;
}

/**
 * Constrói URL de busca da Shopee (Hybrid: Links Oficiais + Fallback)
 * @param {string} searchTerm - Termo de busca
 * @returns {string} URL verificada
 */
function buildShopeeAffiliateUrl(searchTerm) {
    // 1. Mapa de Links Oficiais (Gerados via API SHA256)
    const officialLinks = {
        "decoração casa": "https://s.shopee.com.br/4fq94GOI3B",
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

    // 4. Fallback: Busca Direta (Search URL)
    const baseUrl = "https://shopee.com.br/search";
    const encodedTerm = encodeURIComponent(searchTerm).replace(/%20/g, "+");
    const tag = TITANIUM_CONFIG.TAGS.shopee || "shopee_affiliate";
    console.log(`[Shopee] Usando fallback search para "${termKey}" com tag ${tag}`);
    return `${baseUrl}?keyword=${encodedTerm}&sortBy=price&order=asc&utm_source=${tag}`; // ✅ Tag Injetada
}

/**
 * Redireciona para busca na loja com tag de afiliado
 * Implementa fallback inteligente: Shopee → Amazon
 * @param {string} categoria - Nome da categoria
 * @param {string} lojaPreferida - Loja específica (opcional)
 */
function titaniumRedirect(categoria, lojaPreferida = null) {
    let loja = lojaPreferida;

    // Se não especificou loja ou loja não está disponível, usa fallback
    if (!loja || !TITANIUM_CONFIG.STATUS[loja]) {
        loja = TITANIUM_CONFIG.PRIORIDADE.find(l => TITANIUM_CONFIG.STATUS[l]);
    }

    // Normalizar nome da loja para garantir o match no switch
    // Ex: "Mercado Livre" -> "mercadolivre"
    loja = loja.toLowerCase().replace(/\s+/g, '');

    const tag = TITANIUM_CONFIG.TAGS[loja];
    let urlFinal = "";

    console.log(`[Titanium] Redirecionando "${categoria}" para ${loja} (tag: ${tag})`);

    switch (loja) {
        case 'amazon':
            // Amazon: busca com tag de afiliado + filtro menor preço
            urlFinal = `https://www.amazon.com.br/s?k=${encodeURIComponent(categoria)}&tag=${tag}&s=price-asc-rank`;
            break;

        case 'mercadolivre':
            // ML: usa função otimizada para garantir tracking
            urlFinal = buildMLAffiliateUrl(categoria);
            break;

        case 'shopee':
            // Shopee: Fallback para busca direta (MVP)
            urlFinal = buildShopeeAffiliateUrl(categoria);
            break;

        default:
            // Fallback padrão: Amazon
            urlFinal = `https://www.amazon.com.br/s?k=${encodeURIComponent(categoria)}&tag=${tag}`;
            break;
    }

    // === SECURITY: VALIDAÇÃO DE URL (v1140) ===
    const dominiosPermitidos = ['amazon.com.br', 'mercadolivre.com.br', 'shopee.com.br'];
    const isUrlSegura = dominiosPermitidos.some(d => urlFinal.includes(d));

    if (!isUrlSegura) {
        console.error('[Titanium Security] Bloqueio de Redirecionamento Suspeito:', urlFinal);
        return;
    }

    if (urlFinal) {
        // Abre em nova aba
        window.open(urlFinal, '_blank');

        // Log para debug
        console.log('[Titanium] URL final:', urlFinal);
    }
}

// Expor função globalmente para uso no HTML
window.titaniumRedirect = titaniumRedirect;

/**
 * Handles image load errors by replacing the image with a store-branded fallback card
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

    async function loadDeals() {
        try {
            console.log('[Titanium] Carregando ofertas sincronizadas...');
            const response = await fetch('data.json?v=' + Date.now());
            if (!response.ok) throw new Error('Falha ao carregar data.json');
            allDeals = await response.json();
            console.log(`[Titanium] ${allDeals.length} ofertas carregadas com sucesso.`);

            // Renderiza ofertas iniciais (Recentes)
            renderDeals(allDeals);

            // Garante visibilidade da seção se houver ofertas
            const dealsSection = document.querySelector('.voted-deals');
            if (dealsSection && allDeals.length > 0) {
                dealsSection.style.display = 'block';
            }
        } catch (err) {
            console.error('[Titanium] Erro ao carregar ofertas:', err);
            allDeals = getFallbackData();
        }
    }

    // Inicializa carregamento
    loadDeals();

    // === Render Functions ===
    function renderDeals(deals) {
        dealsGrid.innerHTML = '';

        if (deals.length === 0) {
            dealsGrid.innerHTML = `
                <div class="loading-state">
                    <i class="fas fa-search"></i>
                    <p>Nenhuma oferta encontrada.</p>
                </div>
            `;
            return;
        }

        // Sort deals
        const sortedDeals = sortDeals(deals, currentSort);

        // Limit to 18 products for a rich display
        const displayDeals = sortedDeals.slice(0, 18);

        displayDeals.forEach(deal => {
            const card = createDealCard(deal);
            dealsGrid.appendChild(card);
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
        card.className = 'product-card';
        card.dataset.id = deal.id;

        // Check if image is in blocklist
        let forceFallback = false;
        if (!deal.image || BLOCKED_IMAGES.some(blocked => deal.image.includes(blocked))) {
            forceFallback = true;
        }

        // Format prices
        const formatter = new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        });

        const formattedPrice = formatter.format(deal.price);
        const formattedOldPrice = deal.old_price ? formatter.format(deal.old_price) : '';

        // Truncate title to 60 characters with tooltip
        const MAX_TITLE_LENGTH = 60;
        const fullTitle = deal.title;
        const displayTitle = fullTitle.length > MAX_TITLE_LENGTH
            ? fullTitle.substring(0, MAX_TITLE_LENGTH) + '...'
            : fullTitle;

        // Store badge styling
        let storeIcon = '';
        let storeColor = '';
        const storeLower = deal.store.toLowerCase();

        if (storeLower.includes('amazon')) {
            storeIcon = '<i class="fa-brands fa-amazon"></i>';
            storeColor = '#FF9900';
        } else if (storeLower.includes('shopee')) {
            storeIcon = 'S';
            storeColor = '#ee4d2d';
        } else {
            storeIcon = '<i class="fa-solid fa-handshake"></i>';
            storeColor = '#ffe600';
        }

        // Vote status
        const userVote = userVotes[deal.id] || 0;
        const voteCount = (deal.votes || 0) + (userVote === 1 ? 1 : userVote === -1 ? -1 : 0);

        // Check for blocked images

        // Pre-calculate fallback HTML if forced
        let imageHTML = '';
        if (forceFallback) {
            const storeLower = deal.store.toLowerCase().replace(/\s+/g, '');
            let contentHTML = '';

            if (storeLower.includes('amazon')) {
                contentHTML = '<i class="fa-brands fa-amazon"></i>';
            } else if (storeLower.includes('mercadolivre')) {
                contentHTML = '<img src="images/logo-mercadolivre.png" class="fallback-logo ml-logo" alt="Mercado Livre">';
            } else if (storeLower.includes('shopee')) {
                // Shopee: Construct a "Logo" using Icon + Text to ensure it looks good (White Bag + Color S)
                contentHTML = `
                    <div class="shopee-logo-composite">
                        <i class="fa-solid fa-bag-shopping"></i>
                        <span class="shopee-s">S</span>
                    </div>`;
            } else {
                contentHTML = '<i class="fa-solid fa-shopping-bag"></i>';
            }

            imageHTML = `
                <div class="image-container" style="width: 100%; height: 100%;">
                    <div class="fallback-card ${storeLower}">
                        ${contentHTML}
                    </div>
                </div>`;
        } else {
            imageHTML = `
                <div class="image-container" style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
                    <img src="${deal.image}" alt="${fullTitle}" loading="lazy" onerror="handleImageError(this, '${deal.store}', '${fullTitle}')" style="max-width: 100%; max-height: 100%; object-fit: contain;">
                </div>`;
        }

        card.innerHTML = `
            <div class="card-header">
                <div class="discount-badge-titanium">
                    <div class="titanium-star">
                        <span class="star-text">-${deal.discount}%</span>
                    </div>
                    <div class="titanium-hand">
                        <i class="fa-solid fa-hand-holding"></i>
                    </div>
                </div>
                <div class="vote-container">
                    <button class="vote-btn vote-up ${userVote === 1 ? 'active' : ''}" data-id="${deal.id}">
                        <i class="fas fa-chevron-up"></i>
                    </button>
                    <span class="vote-count" title="Temperatura da Oferta (Saldo de Votos)">🔥 ${voteCount}</span>
                    <button class="vote-btn vote-down ${userVote === -1 ? 'active' : ''}" data-id="${deal.id}">
                        <i class="fas fa-chevron-down"></i>
                    </button>
                </div>
                ${imageHTML}
                <div class="store-badge" style="background:${storeColor}">
                    ${storeIcon} ${deal.store}
                </div>
            </div>
            <div class="card-body">
                <div class="reason-badge">
                    <i class="fa-solid fa-chart-line"></i> ${deal.reason}
                </div>
                <h3 class="card-title" title="${fullTitle}">${displayTitle}</h3>
                <div class="price-container">
                    <div class="old-price">${formattedOldPrice}</div>
                    <div class="new-price">${formattedPrice} <small>à vista</small></div>
                </div>
                <a href="${deal.link}" target="_blank" class="btn-deal">
                    Ver Oferta <i class="fa-solid fa-arrow-up-right-from-square"></i>
                </a>
            </div>
        `;

        // Add vote listeners
        const voteUpBtn = card.querySelector('.vote-up');
        const voteDownBtn = card.querySelector('.vote-down');

        voteUpBtn.addEventListener('click', (e) => {
            e.preventDefault();
            handleVote(deal.id, 1);
        });

        voteDownBtn.addEventListener('click', (e) => {
            e.preventDefault();
            handleVote(deal.id, -1);
        });

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
            const storeName = storeNames[currentStoreFilter] || 'Todas as Lojas';
            sectionTitle.textContent = `${catName} - ${storeName} (Menor Preço)`;
        }

        if (sortedByPrice.length === 0) {
            dealsGrid.innerHTML = `
                <div class="no-results" style="grid-column: 1/-1; text-align: center; padding: 40px 20px; background: #f9fafb; border-radius: 15px;">
                    <i class="fas fa-ghost" style="font-size: 3rem; color: #d1d5db; margin-bottom: 20px;"></i>
                    <h3 style="color: #374151;">Ops! Sem ofertas locais nesta categoria...</h3>
                    <p style="color: #6b7280; margin-bottom: 20px;">Mas não se preocupe! O Robô Titanium pode buscar ofertas frescas agora mesmo:</p>
                    <div style="display: flex; gap: 10px; justify-content: center; flex-wrap: wrap;">
                        <button onclick="titaniumRedirect('${category}', 'mercadolivre')" style="background: #FFE600; color: #333; padding: 12px 20px; border: none; border-radius: 8px; font-weight: 700; cursor: pointer;">
                            <i class="fas fa-rocket"></i> Buscar no Mercado Livre
                        </button>
                        <button onclick="titaniumRedirect('${category}', 'amazon')" style="background: #FF9900; color: white; padding: 12px 20px; border: none; border-radius: 8px; font-weight: 700; cursor: pointer;">
                            <i class="fa-brands fa-amazon"></i> Buscar na Amazon
                        </button>
                    </div>
                </div>
            `;
        } else {
            renderDeals(sortedByPrice);
        }
    }

    // === Category Hub Navigation ===
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
                // Update section title to show the query
                const sectionTitle = document.querySelector('.section-title');
                if (sectionTitle) sectionTitle.innerHTML = `Busca por: "<strong>${query}</strong>"`;

                dealsGrid.innerHTML = `
                    <div class="no-results" style="grid-column: 1/-1; text-align: center; padding: 60px 20px; background: #f9fafb; border-radius: 20px; border: 2px dashed #e5e7eb;">
                        <i class="fas fa-search" style="font-size: 3.5rem; color: #d1d5db; margin-bottom: 25px;"></i>
                        <h3 style="font-size: 1.5rem; color: #374151; margin-bottom: 10px;">Ainda não temos essa oferta salva...</h3>
                        <p style="color: #6b7280; max-width: 500px; margin: 0 auto 30px;">
                            Não encontramos "<strong>${query}</strong>" no nosso cache local, mas o <strong>Robô Titanium</strong> pode buscar em tempo real para você no Mercado Livre!
                        </p>
                        <div style="display: flex; gap: 15px; justify-content: center; flex-wrap: wrap;">
                            <button onclick="titaniumRedirect('${query}', 'mercadolivre')" style="background: #FFE600; color: #333; padding: 15px 30px; border: none; border-radius: 12px; font-weight: 700; font-size: 1.1rem; cursor: pointer; display: flex; align-items: center; gap: 10px; box-shadow: 0 4px 15px rgba(255, 230, 0, 0.3);">
                                <i class="fas fa-rocket"></i> Buscar no Mercado Livre (Menor Preço)
                            </button>
                            <button onclick="titaniumRedirect('${query}', 'amazon')" style="background: #FF9900; color: white; padding: 15px 30px; border: none; border-radius: 12px; font-weight: 700; font-size: 1.1rem; cursor: pointer; display: flex; align-items: center; gap: 10px; box-shadow: 0 4px 15px rgba(255, 153, 0, 0.3);">
                                <i class="fa-brands fa-amazon"></i> Buscar na Amazon
                            </button>
                        </div>
                    </div>
                `;
            } else {
                // Update section title
                const sectionTitle = document.querySelector('.section-title');
                if (sectionTitle) sectionTitle.innerHTML = `Resultados para "<strong>${query}</strong>"`;

                renderDeals(matches);
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
function trackClick(store, category, title) {
    const data = JSON.stringify({
        store: store,
        category: category,
        title: title,
        timestamp: new Date().toISOString(),
        url: window.location.href
    });

    // Environment Detection
    const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';

    // Use 127.0.0.1 instead of localhost for better compatibility in local dev
    // Use PHP tracker in Staging/Production (Hostinger)
    const trackerUrl = isLocal
        ? 'http://127.0.0.1:5001/api/track-click'
        : 'track_clicks.php'; // Movido para a raiz para evitar 401/404 em pastas protegidas
    const success = navigator.sendBeacon(trackerUrl, data);

    if (success) {
        console.log(`📊 Titanium Metrics: Click tracked [${store} - ${category}]`);
    } else {
        // Fallback for older browsers or specific security blocks
        fetch(trackerUrl, { method: 'POST', body: data, keepalive: true }).catch(() => { });
    }
}

// Inicializar ouvintes de clique após o DOM carregar
document.addEventListener('DOMContentLoaded', () => {
    // Capturar cliques em cards de oferta e hubs
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

        // --- Logic: ROUND-ROBIN Balanced Selection (v10 fix) ---
        // Garante que TODAS as lojas aparecem alternadamente na barra
        const storesMap = {
            'amazon': [],
            'mercado livre': [],
            'shopee': [],
            'lomadee': []
        };

        allDeals.forEach(d => {
            if (!d.store || !d.price || !d.link) return;
            const storeKey = d.store.toLowerCase().trim();
            if (storeKey.includes('amazon')) storesMap['amazon'].push(d);
            else if (storeKey.includes('mercado')) storesMap['mercado livre'].push(d);
            else if (storeKey.includes('shopee')) storesMap['shopee'].push(d);
            else if (storeKey.includes('lomadee')) storesMap['lomadee'].push(d);
        });

        // Diagnostic: Log per-store counts
        console.log('[Titanium Bar] Produtos por loja:', {
            amazon: storesMap['amazon'].length,
            mercadoLivre: storesMap['mercado livre'].length,
            shopee: storesMap['shopee'].length,
            lomadee: storesMap['lomadee'].length
        });

        // Shuffle each store's pool internally
        Object.keys(storesMap).forEach(store => {
            storesMap[store].sort(() => 0.5 - Math.random());
        });

        // ROUND-ROBIN: Alterna entre lojas garantindo visibilidade de TODAS
        const storeOrder = ['amazon', 'mercado livre', 'shopee', 'lomadee'];
        const finalSelection = [];
        const maxPerStore = 8; // Aumentado para mais variedade

        for (let i = 0; i < maxPerStore; i++) {
            storeOrder.forEach(store => {
                if (storesMap[store][i]) {
                    finalSelection.push(storesMap[store][i]);
                }
            });
        }

        if (finalSelection.length === 0) {
            console.warn('[Titanium Bar] Nenhum produto filtrado para a barra.');
            return;
        }

        // Duplicar para loop contínuo (sem shuffle — manter ordem round-robin!)
        const loopDeals = [...finalSelection, ...finalSelection];

        console.log('[Titanium Bar] Seleção final (round-robin):', finalSelection.map(d => d.store + ': ' + (d.title || '').substring(0, 25)));

        let html = '';
        loopDeals.forEach((deal, index) => {
            try {
                const storeLower = deal.store.toLowerCase();
                let link = deal.link;

                // --- SMART LINK LAYER (Senior Workflow: Tags NUNCA podem ser perdidas) ---

                // AMAZON: Garantir tag de afiliado
                if (storeLower.includes('amazon')) {
                    if (!link.includes('tag=')) {
                        link += (link.includes('?') ? '&' : '?') + `tag=${TITANIUM_CONFIG.TAGS.amazon}`;
                    }
                }
                // MERCADO LIVRE: Usar Link Inteligente (fix v10: termo curto + try-catch)
                else if (storeLower.includes('mercado')) {
                    // Usa apenas as 3 primeiras palavras do título como busca
                    const words = (deal.title || 'ofertas').split(' ').slice(0, 3).join(' ');
                    link = buildMLAffiliateUrl(words);
                    console.log(`[Titanium] ML Smart Link OK: "${words}" → ${link.substring(0, 60)}...`);
                }
                // SHOPEE: Preservar links oficiais ou injetar tag
                else if (storeLower.includes('shopee')) {
                    if (!link.includes('s.shopee.com.br') && !link.includes('utm_source=')) {
                        link += (link.includes('?') ? '&' : '?') + `utm_source=${TITANIUM_CONFIG.TAGS.shopee}`;
                    }
                }

                const displayTitle = (deal.title || '').length > 35 ? deal.title.substring(0, 32) + '...' : deal.title;
                const safeTitle = (deal.title || '').replace(/'/g, "\\'");
                const formattedPrice = deal.price ? `R$ ${parseFloat(deal.price).toFixed(2).replace('.', ',')}` : '';

                html += `
                <a href="${link}" target="_blank" class="lightning-item" data-id="${deal.id}_${index}" 
                   data-store="${deal.store}" data-title="${safeTitle}">
                    <span class="lightning-badge">⚡ ${deal.store}</span>
                    <strong>${displayTitle}</strong>
                    <span class="lightning-price">${formattedPrice}</span>
                    <div class="price-badge">Ver Oferta →</div>
                </a>
            `;
            } catch (itemErr) {
                console.error(`[Titanium] Erro no item ${index} (${deal.store}):`, itemErr);
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
            'width: ' + (loopDeals.length * 320) + 'px',
            'animation: marquee-titanium 30s linear infinite'
        ].join('; '));

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
        container.querySelectorAll('.price-badge').forEach(price => {
            price.setAttribute('style', [
                'background: #fff',
                'color: #ee4d2d',
                'padding: 2px 10px',
                'border-radius: 20px',
                'font-weight: 800'
            ].join('; '));
        });

        // Wait for paint, then verify
        requestAnimationFrame(() => {
            const rect = bar.getBoundingClientRect();
            console.log(`[Titanium] Barra NUCLEAR. Dimensões: ${rect.width}x${rect.height}, Top: ${rect.top}`);
            console.log(`[Titanium] Bar display: ${bar.style.display}, children: ${container.children.length}`);

            if (rect.height === 0) {
                // Last resort: force height
                bar.style.height = '42px';
                console.warn('[Titanium] FORÇANDO height=42px como último recurso.');
            }
        });

        console.log(`[Titanium] Barra v6 NUCLEAR ATIVA com ${finalSelection.length} produtos.`);

    } catch (err) {
        console.error('[Titanium] Erro Crítico na Barra:', err);
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
});
