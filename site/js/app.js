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
        'tracking_id': generateTrackingId()       // ID único de rastreamento
    });

    const fullUrl = `${baseUrl}?${params.toString()}`;

    console.log('[ML Affiliate] URL gerada:', fullUrl);
    console.log('[ML Affiliate] User ID:', config.userId);

    return fullUrl;
}

/**
 * Constrói URL de busca da Shopee (Fallback MVP)
 * @param {string} searchTerm - Termo de busca
 * @returns {string} URL de busca direta
 */
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
    return `${baseUrl}?keyword=${encodedTerm}`;
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

    const tag = TITANIUM_CONFIG.TAGS[loja];
    let urlFinal = "";

    console.log(`[Titanium] Redirecionando "${categoria}" para ${loja} (tag: ${tag})`);

    switch (loja) {
        case 'amazon':
            // Amazon: busca com tag de afiliado
            urlFinal = `https://www.amazon.com.br/s?k=${encodeURIComponent(categoria)}&tag=${tag}`;
            break;

        case 'mercadolivre':
            // ML: usa função otimizada para garantir tracking
            urlFinal = buildMLAffiliateUrl(categoria);
            break;

        case 'shopee':
            // Shopee: Fallback para busca direta (MVP)
            urlFinal = buildShopeeAffiliateUrl(categoria);
            break;

        case 'amazon':
        default:
            // Amazon: Standard search with tag
            const amzConfig = config.AMAZON_AFFILIATE;
            // Garantir fallabck seguro se tag não existir
            const amzTag = amzConfig ? amzConfig.tag : "guiadodesco00-20";
            urlFinal = `https://www.amazon.com.br/s?k=${encodeURIComponent(categoria)}&tag=${amzTag}`;
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

document.addEventListener('DOMContentLoaded', () => {
    // === API Configuration ===
    const API_BASE_URL = 'http://localhost:5000';

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
    // MVP v1.0: Desativado carregamento de produtos
    // loadDeals();

    function loadDeals() {
        fetch('data.json')
            .then(response => response.json())
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

        // Limit to 6 products for consistent 3x2 grid layout
        const displayDeals = sortedDeals.slice(0, 6);

        displayDeals.forEach(deal => {
            const card = createDealCard(deal);
            dealsGrid.appendChild(card);
        });
    }

    function createDealCard(deal) {
        const card = document.createElement('div');
        card.className = 'product-card';
        card.dataset.id = deal.id;

        // Format price
        const formattedPrice = new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        }).format(deal.price);

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

        card.innerHTML = `
            <div class="card-header">
                <span class="discount-badge">-${deal.discount}%</span>
                <div class="vote-container">
                    <button class="vote-btn vote-up ${userVote === 1 ? 'active' : ''}" data-id="${deal.id}">
                        <i class="fas fa-chevron-up"></i>
                    </button>
                    <span class="vote-count">${voteCount}</span>
                    <button class="vote-btn vote-down ${userVote === -1 ? 'active' : ''}" data-id="${deal.id}">
                        <i class="fas fa-chevron-down"></i>
                    </button>
                </div>
                <img src="${deal.image}" alt="${fullTitle}" loading="lazy">
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
                    <div class="old-price">R$ ${deal.old_price}</div>
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

    sortButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            sortButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentSort = btn.dataset.sort;
            renderDeals(allDeals);
        });
    });

    // === Search Functionality ===

    // Busca local (autocomplete enquanto digita)
    searchInput.addEventListener('input', debounce((e) => {
        const query = e.target.value.toLowerCase().trim();

        if (query.length < 2) {
            searchSuggestions.classList.remove('active');
            return;
        }

        const filtered = allDeals.filter(deal =>
            deal.title.toLowerCase().includes(query) ||
            (deal.tags && deal.tags.some(tag => tag.toLowerCase().includes(query))) ||
            deal.category.toLowerCase().includes(query)
        );

        showSuggestions(filtered.slice(0, 5));
    }, 300));

    // Busca em tempo real (ao clicar no botão ou Enter)
    if (searchButton) {
        searchButton.addEventListener('click', () => searchRealTime());
    }

    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            searchRealTime();
        }
    });

    async function searchRealTime() {
        const query = searchInput.value.trim();

        if (!query || query.length < 3) {
            showNotification('Digite pelo menos 3 caracteres para buscar', 'warning');
            return;
        }

        if (isSearching) {
            return; // Evita múltiplas buscas simultâneas
        }

        isSearching = true;
        searchSuggestions.classList.remove('active');

        // Mostra loading
        dealsGrid.innerHTML = `
            <div class="loading-state real-time-search">
                <i class="fa-solid fa-circle-notch fa-spin"></i>
                <p>Buscando "<strong>${query}</strong>" nas 3 lojas...</p>
                <div class="search-progress">
                    <span class="store-status" data-store="amazon">🟡 Amazon</span>
                    <span class="store-status" data-store="ml">🟡 Mercado Livre</span>
                    <span class="store-status" data-store="shopee">🟡 Shopee</span>
                </div>
            </div>
        `;

        // Scroll para resultados
        document.querySelector('.voted-deals').scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });

        try {
            const response = await fetch(`${API_BASE_URL}/api/search?q=${encodeURIComponent(query)}`);

            if (!response.ok) {
                throw new Error(`Erro HTTP: ${response.status}`);
            }

            const data = await response.json();
            renderSearchResults(data);

        } catch (error) {
            console.error('Erro na busca:', error);
            dealsGrid.innerHTML = `
                <div class="loading-state error-state">
                    <i class="fas fa-exclamation-triangle"></i>
                    <p>Erro ao buscar produtos</p>
                    <small>${error.message}</small>
                    <button onclick="location.reload()" class="btn-retry">Tentar novamente</button>
                </div>
            `;
        } finally {
            isSearching = false;
        }
    }

    function renderSearchResults(data) {
        const { query, results, best_price, from_cache } = data;

        // Atualiza título da seção
        const sectionTitle = document.querySelector('.voted-deals .section-title');
        sectionTitle.innerHTML = `Resultados para "<span style="color: #667eea;">${query}</span>"${from_cache ? ' <small>(cache)</small>' : ''}`;

        if (!results || results.length === 0) {
            dealsGrid.innerHTML = `
                <div class="loading-state">
                    <i class="fas fa-search"></i>
                    <p>Nenhum resultado encontrado para "${query}"</p>
                </div>
            `;
            return;
        }

        // Renderiza cards de comparação
        dealsGrid.innerHTML = '';

        results.forEach(result => {
            const card = createSearchResultCard(result, best_price);
            dealsGrid.appendChild(card);
        });
    }

    function createSearchResultCard(result, best_price) {
        const card = document.createElement('div');
        card.className = 'product-card search-result-card';

        const isBestPrice = best_price &&
            result.available &&
            result.price === best_price.price;

        // Store styling
        let storeIcon = '';
        let storeColor = '';
        const storeLower = result.store.toLowerCase();

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

        if (!result.available) {
            // Card para loja indisponível
            card.innerHTML = `
                <div class="card-header unavailable">
                    <div class="store-badge large" style="background:${storeColor}">
                        ${storeIcon} ${result.store}
                    </div>
                </div>
                <div class="card-body">
                    <div class="unavailable-message">
                        <i class="fas fa-clock"></i>
                        <p>${result.error || 'Indisponível no momento'}</p>
                    </div>
                </div>
            `;
        } else {
            // Card com resultado
            const formattedPrice = new Intl.NumberFormat('pt-BR', {
                style: 'currency',
                currency: 'BRL'
            }).format(result.price);

            card.innerHTML = `
                <div class="card-header">
                    ${isBestPrice ? '<span class="best-price-badge">🏆 Melhor Preço</span>' : ''}
                    ${result.image ? `<img src="${result.image}" alt="${result.title}" loading="lazy">` : '<div class="no-image"><i class="fas fa-image"></i></div>'}
                    <div class="store-badge" style="background:${storeColor}">
                        ${storeIcon} ${result.store}
                    </div>
                </div>
                <div class="card-body">
                    <h3 class="card-title">${result.title}</h3>
                    <div class="price-container">
                        <div class="new-price ${isBestPrice ? 'highlight' : ''}">${formattedPrice}</div>
                    </div>
                    <a href="${result.link}" target="_blank" class="btn-deal ${isBestPrice ? 'best' : ''}">
                        ${isBestPrice ? 'Aproveitar Oferta' : 'Ver na Loja'} <i class="fa-solid fa-arrow-up-right-from-square"></i>
                    </a>
                </div>
            `;
        }

        if (isBestPrice) {
            card.classList.add('best-price');
        }

        return card;
    }

    function showNotification(message, type = 'info') {
        // Cria notificação temporária
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `<i class="fas fa-info-circle"></i> ${message}`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'warning' ? '#f59e0b' : '#667eea'};
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            z-index: 9999;
            animation: slideIn 0.3s ease;
        `;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    function showSuggestions(deals) {
        if (deals.length === 0) {
            searchSuggestions.classList.remove('active');
            return;
        }

        searchSuggestions.innerHTML = deals.map(deal => `
            <div class="suggestion-item" data-id="${deal.id}">
                <strong>${deal.title}</strong>
                <div style="font-size: 0.85rem; color: #6B7280;">
                    ${deal.store} - ${new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(deal.price)}
                </div>
            </div>
        `).join('');

        searchSuggestions.classList.add('active');

        // Add click listeners
        searchSuggestions.querySelectorAll('.suggestion-item').forEach(item => {
            item.addEventListener('click', () => {
                const dealId = item.dataset.id;
                const deal = allDeals.find(d => d.id === dealId);
                if (deal) {
                    searchInput.value = deal.title;
                    searchSuggestions.classList.remove('active');
                    renderDeals([deal]);
                }
            });
        });
    }

    // Close suggestions when clicking outside
    document.addEventListener('click', (e) => {
        if (!searchInput.contains(e.target) && !searchSuggestions.contains(e.target)) {
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
        const categoryNames = {
            'tecnologia': 'Tecnologia',
            'casa': 'Casa & Decoração',
            'moda': 'Moda & Beleza',
            'esportes': 'Esportes & Lazer'
        };
        const storeNames = {
            'all': 'Todas as Lojas',
            'amazon': 'Amazon',
            'mercadolivre': 'Mercado Livre',
            'shopee': 'Shopee'
        };
        sectionTitle.textContent = `${categoryNames[category]} - ${storeNames[currentStoreFilter]} (Menor Preço)`;

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

    // === Price Comparison Widget ===
    document.querySelector('.btn-compare').addEventListener('click', () => {
        const query = comparisonInput.value.toLowerCase().trim();

        if (!query) {
            alert('Por favor, digite o nome de um produto');
            return;
        }

        const matches = allDeals.filter(deal =>
            deal.title.toLowerCase().includes(query)
        );

        if (matches.length === 0) {
            comparisonResults.innerHTML = `
                <div style="grid-column: 1/-1; text-align: center; color: #6B7280;">
                    Produto não encontrado. Tente outro termo de busca.
                </div>
            `;
            return;
        }

        // Group by store
        const byStore = {};
        matches.forEach(deal => {
            const store = deal.store.toLowerCase();
            if (!byStore[store] || deal.price < byStore[store].price) {
                byStore[store] = deal;
            }
        });

        // Find best price
        const prices = Object.values(byStore).map(d => d.price);
        const bestPrice = Math.min(...prices);

        // Render comparison
        comparisonResults.innerHTML = Object.values(byStore).map(deal => {
            const isBest = deal.price === bestPrice;
            return `
                <div class="comparison-item ${isBest ? 'best' : ''}">
                    <h4>${deal.store}</h4>
                    <div class="price">${new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(deal.price)}</div>
                    <a href="${deal.link}" target="_blank" style="color: #2196F3; text-decoration: none; font-size: 0.9rem; margin-top: 8px; display: block;">
                        Ver oferta <i class="fas fa-external-link-alt"></i>
                    </a>
                </div>
            `;
        }).join('');
    });

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
                "link": "https://amzn.to/EXAMPLE",
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
                "image": "https://http2.mlstatic.com/D_NQ_NP_2X_959089-MLA69565561075_052023-F.webp",
                "link": "https://mercadolivre.com.br/EXAMPLE",
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
                "link": "https://shopee.com.br/EXAMPLE",
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
                "link": "https://amzn.to/EXAMPLE2",
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
                "link": "https://amzn.to/EXAMPLE3",
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
                "link": "https://shopee.com.br/EXAMPLE4",
                "reason": "Desconto exclusivo",
                "votes": 47,
                "added_date": "2026-01-15"
            }
        ];
    }
});
