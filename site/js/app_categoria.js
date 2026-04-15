// ==========================================
// GUIA DO DESCONTO - CATEGORY SHOWCASE MOTOR
// ==========================================

const CATEGORY_MAP = {
    'tecnologia': { name: 'Tecnologia', icon: '📱', desc: 'Os gadgets mais desejados com preços imbatíveis.' },
    'moda': { name: 'Moda Feminina', icon: '👗', desc: 'Tendências da estação com o melhor custo-benefício.' },
    'casa': { name: 'Casa & Decor', icon: '🏠', desc: 'Tudo para deixar seu lar mais bonito e funcional.' },
    'beleza': { name: 'Beleza & Skincare', icon: '💄', desc: 'Cuidados pessoais e perfumes das melhores marcas.' },
    'esportes': { name: 'Esportes & Lazer', icon: '🏋️', desc: 'Equipamentos e vestuário para sua melhor performance.' },
    'eletro': { name: 'Eletrodomésticos', icon: '🍳', desc: 'Sua cozinha e lavanderia equipadas gastando menos.' },
    'automotivo': { name: 'Automotivo', icon: '🚗', desc: 'Acessórios e peças para seu carro ou moto.' }
};

document.addEventListener('DOMContentLoaded', () => {
    // 1. Capturar Categoria da URL (?cat=X)
    const params = new URLSearchParams(window.location.search);
    const catSlug = (params.get('cat') || 'tecnologia').toLowerCase();
    const currentCategory = CATEGORY_MAP[catSlug] || { name: 'Ofertas Selecionadas', icon: '🎁', desc: 'Curadoria especial do Robô Titanium.' };

    // 2. Atualizar UI Inicial
    document.title = `${currentCategory.name} | Guia do Desconto`;
    document.getElementById('current-category-name').textContent = currentCategory.name;
    document.getElementById('category-title').textContent = `${currentCategory.icon} ${currentCategory.name}`;

    // 3. Carregar Dados
    let allProducts = [];
    let currentStoreFilter = 'all';

    async function initCategoryPage() {
        try {
            const response = await fetch('data.json?v=' + Date.now());
            if (!response.ok) throw new Error('Falha no banco de dados');
            
            const data = await response.json();
            
            // Filtro por categoria (campo "category" no JSON ou fallback por keywords no título)
            allProducts = data.filter(p => {
                const matchesSlug = p.category === catSlug;
                const matchesTitle = p.title.toLowerCase().includes(catSlug);
                return matchesSlug || matchesTitle;
            });

            renderCategoryGrid(allProducts);
            updateProductCount(allProducts.length);

        } catch (err) {
            console.error('[Titanium] Erro ao carregar categoria:', err);
            showErrorState();
        }
    }

    // 4. Renderização
    function renderCategoryGrid(products) {
        const grid = document.getElementById('category-grid');
        grid.innerHTML = '';

        if (products.length === 0) {
            showEmptyState(grid);
            return;
        }

        // Filtro de Loja (Fixo para Shopee v3.2.0)
        const filtered = products.filter(p => p.store.toLowerCase().includes('shopee'));

        // Encontrar Menor Preço da Categoria para o Badge 🏆
        const minPrice = filtered.length > 0 ? Math.min(...filtered.map(p => parseFloat(p.price) || 999999)) : 0;

        filtered.forEach(p => {
            const isBestPrice = (parseFloat(p.price) === minPrice) && filtered.length > 1;
            const card = createProductCard(p, isBestPrice);
            grid.appendChild(card);
        });
    }

    function createProductCard(product, isBestPrice) {
        const div = document.createElement('div');
        div.className = `deal-card ${isBestPrice ? 'category-best-price' : ''}`;
        
        // Formatadores
        const formatter = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' });
        const price = parseFloat(product.price) || 0;
        const oldPrice = product.old_price ? parseFloat(product.old_price) : price * 1.25;

        div.innerHTML = `
            <div class="card-header">
                <div class="discount-badge-titanium">
                    <div class="titanium-star">
                        <span class="star-text">-${Math.round((1 - price/oldPrice) * 100)}%</span>
                    </div>
                </div>
                <div class="image-container">
                    <img src="${product.image}" loading="lazy" alt="${product.title}">
                </div>
                <div class="store-badge ${product.store.toLowerCase()}">
                    ${product.store}
                </div>
            </div>
            <div class="card-body">
                <h3 class="card-title">${product.title.substring(0, 55)}...</h3>
                <div class="price-container">
                    <div class="old-price">${formatter.format(oldPrice)}</div>
                    <div class="new-price">${formatter.format(price)}</div>
                </div>
                <a href="${window.titaniumLinkAuditor ? window.titaniumLinkAuditor(product.link, product.store) : product.link}" target="_blank" class="btn-deal">
                    Ver Oferta <i class="fas fa-external-link-alt"></i>
                </a>
            </div>
        `;
        return div;
    }

    // 5. Controles e Filtros
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentStoreFilter = btn.dataset.store;
            renderCategoryGrid(allProducts);
        });
    });

    function updateProductCount(count) {
        document.getElementById('category-count').textContent = `${count} produtos encontrados para você.`;
    }

    function showEmptyState(grid) {
        grid.innerHTML = `
            <div class="no-results" style="grid-column: 1/-1; text-align: center; padding: 60px 20px;">
                <i class="fas fa-search" style="font-size: 3rem; color: #ddd; margin-bottom: 20px;"></i>
                <h3>Nenhuma oferta local em "${currentCategory.name}"</h3>
                <p>O Robô Titanium pode buscar ofertas frescas agora mesmo nas lojas oficiais:</p>
                <div style="margin-top: 25px; display: flex; gap: 10px; justify-content: center;">
                    <button class="btn-deal" onclick="window.location.href='index.html'">Voltar ao Início</button>
                </div>
            </div>
        `;
    }

    initCategoryPage();
});
