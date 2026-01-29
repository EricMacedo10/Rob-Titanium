// ========================================
// GUIA DO DESCONTO - MAIN APPLICATION
// ========================================

// === CONFIGURAÇÃO ROBÔ TITANIUM ===
const TITANIUM_CONFIG = {
    // Tags reais de afiliado
    TAGS: {
        amazon: "guiadodesco00-20",     // ✅ Amazon Associates
        mercadolivre: "ericmacedo",     // ✅ ML Afiliados (via Share Flow)
        shopee: null                     // ⏳ Aguardando API (23/01)
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
        shopee: true   // ✅ Ativo (Fallback MVP)
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
 * Isso garante que o cookie de afiliado seja setado no browser
 * @param {string} searchTerm - Termo de busca
 * @returns {string} URL completa com parâmetros de afiliado
 */
function buildMLAffiliateUrl(searchTerm) {
    const config = TITANIUM_CONFIG.ML_AFFILIATE;
    const baseUrl = `https://lista.mercadolivre.com.br/${encodeURIComponent(searchTerm)}`;

    // Parâmetros de afiliado do ML
    const params = new URLSearchParams({
        'matt_tool': config.userId,              // ID do afiliado (obrigatório)
        'matt_word': searchTerm,                  // Palavra-chave
        'matt_source': config.source,             // Fonte do tráfego
        'tracking_id': generateTrackingId(),      // ID único de rastreamento
        '_Sort': 'price_asc'                      // ✅ Filtro Menor Preço
    });

    const fullUrl = `${baseUrl}?${params.toString()}`;

    console.log('[ML Affiliate] URL gerada:', fullUrl);
    console.log('[ML Affiliate] User ID:', config.userId);

    return fullUrl;
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
        "equipamento academia": "https://s.shopee.com.br/14JVgor5V"
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
    console.log(`[Shopee] Usando fallback search para "${termKey}"`);
    return `${baseUrl}?keyword=${encodedTerm}&sortBy=price&order=asc`; // ✅ Filtro Menor Preço
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
        // Amazon keeps the FontAwesome icon as user liked it
        contentHTML = '<i class="fa-brands fa-amazon"></i>';
    } else if (storeLower.includes('mercadolivre')) {
        // Mercado Livre uses the image logo
        contentHTML = '<img src="images/logo-mercadolivre.png" class="fallback-logo ml-logo" alt="Mercado Livre">';
    } else if (storeLower.includes('shopee')) {
        // Shopee: Construct a "Logo" using Icon + Text to ensure it looks good (White Bag + Color S)
        contentHTML = `
            <div class="shopee-logo-composite">
                <i class="fa-solid fa-bag-shopping"></i>
                <span class="shopee-s">S</span>
            </div>`;
    } else {
        // Default fallback
        contentHTML = '<i class="fa-solid fa-shopping-bag"></i>';
    }

    // Create fallback HTML
    const fallbackHTML = `
        <div class="fallback-card ${storeLower}">
            ${contentHTML}
        </div>
    `;

    // Replace the parent container's content (assuming img is wrapped in .image-container)
    if (imgElement.parentElement.classList.contains('image-container')) {
        imgElement.parentElement.innerHTML = fallbackHTML;
    } else {
        // Fallback if structure is different
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

    // === Data Loading ===
    // MVP v1.0: Ativado carregamento automático de produtos
    loadDeals();

    function loadDeals() {
        // Cache busting with timestamp
        const cacheBuster = `?t=${new Date().getTime()}`;
        fetch('data.json' + cacheBuster)
            .then(response => {
                if (!response.ok) throw new Error('Falha ao carregar data.json');
                return response.json();
            })
            .then(data => {
                allDeals = data;
                renderDeals(allDeals);
            })
            .catch(error => {
                console.warn('Usando dados de demonstração (modo local)');
                allDeals = getFallbackData();
                renderDeals(allDeals);
            });
    }

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
        const filtered = allDeals.filter(deal =>
            deal.category.toLowerCase() === category.toLowerCase()
        );

        // Apply store filter
        const storeFiltered = filterByStore(filtered, currentStoreFilter);

        // Sort by price
        const sortedByPrice = storeFiltered.sort((a, b) => a.price - b.price);

        // Update title
        const sectionTitle = document.querySelector('.voted-deals .section-title');
        if (sectionTitle) {
            const categoryNames = {
                'tecnologia': 'Tecnologia',
                'casa': 'Casa & Decoração',
                'moda': 'Moda & Beleza',
                'esportes': 'Esportes & Lazer',
                'recent': 'Ofertas Recentes'
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

        renderDeals(sortedByPrice);
    }

    // === Category Hub Navigation ===
    hubCards.forEach(card => {
        card.addEventListener('click', () => {
            const category = card.dataset.category;
            currentStoreFilter = 'all'; // Reset filter

            // Scroll to deals section
            const dealsSection = document.querySelector('.voted-deals');
            if (dealsSection) {
                dealsSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });

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
            }
        });
    });

    // === Main Search Functionality ===
    function performSearch() {
        if (!searchInput) return;

        const query = searchInput.value.toLowerCase().trim();

        // Show loading state
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
                            Não encontramos "<strong>${query}</strong>" no nosso cache local, mas podemos buscar em tempo real para você!
                        </p>
                        <div style="display: flex; gap: 15px; justify-content: center; flex-wrap: wrap;">
                            <button onclick="titaniumRedirect('${query}')" style="background: var(--primary-blue); color: white; padding: 15px 30px; border: none; border-radius: 12px; font-weight: 700; font-size: 1.1rem; cursor: pointer; display: flex; align-items: center; gap: 10px; box-shadow: 0 4px 15px rgba(33, 150, 243, 0.3);">
                                <i class="fas fa-rocket"></i> Buscar na Amazon/Shopee/ML
                            </button>
                            <button onclick="window.location.reload()" style="background: white; color: #374151; padding: 15px 30px; border: 2px solid #e5e7eb; border-radius: 12px; font-weight: 600; cursor: pointer;">
                                Voltar ao Início
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
                "link": "https://shopee.com.br/product/12345/67890?utm_source=ericmacedo",
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
                "link": "https://shopee.com.br/product/2222/33333?utm_source=ericmacedo",
                "reason": "Desconto exclusivo",
                "votes": 47,
                "added_date": "2026-01-15"
            }
        ];
    }
});
