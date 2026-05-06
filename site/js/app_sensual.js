/**
 * 🦾 Robô Titanium: Boutique Íntima (v3.8.0)
 * Motor de Renderização e Auditoria de Links
 */

document.addEventListener('DOMContentLoaded', () => {
    console.log('🦾 Motor Íntima Titanium Ativo...');

    const CONFIG = {
        DATA_SOURCE: 'data_sensual.json',
        RADAR_SOURCE: 'ai_reviews_sensual.json',
        PLATINUM_SOURCE: 'specialist_sensual.json',
        AFFILIATE_TAG: 'an_18318830863',
        UTM_SOURCE: 'boutique_sensual',
        CACHE_BUST: `?v=${Date.now()}`
    };

    let allProducts = [];

    // 1. Auditor de Links Universal (Herdado da Titanium)
    function titaniumLinkAuditor(originalUrl) {
        if (!originalUrl || !originalUrl.includes('shopee.com.br')) return originalUrl;

        try {
            const urlObj = new URL(originalUrl);
            const params = new URLSearchParams(urlObj.search);

            // Injeção de Segurança Nuclear
            params.set('utm_source', CONFIG.UTM_SOURCE);
            params.set('utm_medium', 'affiliates');
            params.set('utm_campaign', 'sensual_elite');
            params.set('an_18318830863', ''); // Tag Universal
            params.set('mmp_pid', CONFIG.AFFILIATE_TAG);

            urlObj.search = params.toString();
            return urlObj.toString();
        } catch (e) {
            return originalUrl;
        }
    }

    // 2. Renderizador de Cards (Identico ao app.js para consistência total)
    function renderProducts(products, targetId) {
        const grid = document.getElementById(targetId);
        if (!grid) return;

        grid.innerHTML = '';
        
        // Identificar Menor Preço da Vitrine Atual
        const minPrice = Math.min(...products.map(d => parseFloat(d.price) || 999999));

        products.forEach(deal => {
            const card = document.createElement('div');
            card.className = `product-card`;
            
            const formatter = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' });
            const formattedPrice = formatter.format(deal.price);
            const formattedOldPrice = deal.old_price ? formatter.format(deal.old_price) : '';

            const leftBadges = [];
            if (deal.discount >= 30) {
                leftBadges.push(`<div class="mini-badge gold" style="background: var(--sensual-accent, #D4AF37); color: #4a0e4e; padding: 4px 8px; border-radius: 6px; font-size: 0.65rem; font-weight: 800; display: flex; align-items: center; gap: 4px; box-shadow: 0 2px 8px rgba(212,175,55,0.4);"><i class="fas fa-crown"></i> TITANIUM CHOICE</div>`);
            }
            if (deal.discount >= 20) {
                leftBadges.push(`<div class="mini-badge green" style="background: #22c55e; color: white; padding: 4px 8px; border-radius: 6px; font-size: 0.65rem; font-weight: 800; display: flex; align-items: center; gap: 4px;"><i class="fas fa-arrow-trend-down"></i> MENOR PREÇO 30D</div>`);
            } else {
                leftBadges.push(`<div class="mini-badge red" style="background: #ef4444; color: white; padding: 4px 8px; border-radius: 6px; font-size: 0.65rem; font-weight: 800; display: flex; align-items: center; gap: 4px;"><i class="fas fa-fire"></i> ESTOQUE CRÍTICO</div>`);
            }

            card.innerHTML = `
                <div class="card-image-area" style="position: relative; overflow: hidden; border-radius: 15px;">
                    <div class="badge-group-left" style="position: absolute; top: 10px; left: 10px; z-index: 10; display: flex; flex-direction: column; gap: 5px;">
                        ${leftBadges.join('')}
                    </div>
                    <div class="badge-group-right" style="position: absolute; top: 10px; right: 10px; z-index: 10; display: flex; flex-direction: column; gap: 5px; align-items: flex-end;">
                        <div class="discount-star-modern" style="background: #FF4500; color: white; width: 45px; height: 45px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.8rem; box-shadow: 0 4px 10px rgba(255,69,0,0.3);">
                            <span>${deal.discount}%</span>
                        </div>
                    </div>
                    <div class="card-image" style="width: 100%; height: 250px;">
                        <img src="${deal.image}" alt="${deal.title}" style="width: 100%; height: 100%; object-fit: cover;" loading="lazy">
                    </div>
                    <div class="shopee-pill-tag" style="position: absolute; bottom: 10px; left: 10px; background: rgba(0,0,0,0.6); backdrop-filter: blur(5px); color: white; padding: 5px 12px; border-radius: 20px; font-size: 0.7rem; font-weight: 700;">
                        <i class="fa-solid fa-bag-shopping"></i> Shopee
                    </div>
                </div>
                <div class="card-body-harmonized" style="padding: 15px;">
                    <h3 class="product-title-bold" style="font-size: 0.95rem; margin-bottom: 10px; height: 2.4em; overflow: hidden;">${deal.title}</h3>
                    <div class="price-flex" style="display: flex; align-items: baseline; gap: 10px;">
                        <div class="price-orig" style="color: #94a3b8; text-decoration: line-through; font-size: 0.8rem;">${formattedOldPrice}</div>
                        <div class="price-final" style="color: #4a0e4e; font-weight: 800; font-size: 1.2rem;">${formattedPrice}</div>
                    </div>
                    <a href="${titaniumLinkAuditor(deal.link)}" target="_blank" class="btn-shopee-blue" style="background: #4a0e4e; color: white; text-decoration: none; display: block; text-align: center; padding: 12px; border-radius: 10px; font-weight: bold; margin-top: 15px;">
                        Ver na Shopee <i class="fa-solid fa-arrow-up-right-from-square"></i>
                    </a>
                </div>
            `;
            grid.appendChild(card);
        });

        // Aplicar Interceptor de Cliques Seguro (Reativado)
        grid.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', (e) => {
                const overlay = document.getElementById('security-overlay');
                if (overlay) {
                    overlay.classList.add('active');
                    setTimeout(() => overlay.classList.remove('active'), 1200);
                }
            });
        });
    }

    // 3. Inicialização de Dados (Três Vitrines Estratégicas)
    async function initSensualBoutique() {
        try {
            // Vitrine 1: Radar (SexTech)
            loadRadar();

            // Vitrine 2: Especialista (Lingerie)
            const resPlatinum = await fetch(CONFIG.PLATINUM_SOURCE + CONFIG.CACHE_BUST);
            const dataPlatinum = await resPlatinum.json();
            renderProducts(dataPlatinum.slice(0, 24), 'platinum-grid');

            // Vitrine 3: Ofertas (Cosmética)
            const resOffers = await fetch(CONFIG.DATA_SOURCE + CONFIG.CACHE_BUST);
            const dataOffers = await resOffers.json();
            renderProducts(dataOffers.slice(0, 24), 'deals-grid');

            initAssistant();
        } catch (err) {
            console.error('[Íntima] Erro na inicialização:', err);
        }
    }

    async function loadRadar() {
        const radarGrid = document.getElementById('radar-grid');
        if (!radarGrid) return;

        try {
            const res = await fetch(CONFIG.RADAR_SOURCE + CONFIG.CACHE_BUST);
            const radarData = await res.json();
            
            // Limitado a 18 itens conforme estratégia
            radarGrid.innerHTML = radarData.slice(0, 18).map(p => `
                <a href="${titaniumLinkAuditor(p.link)}" target="_blank" class="radar-card">
                    <div style="display: flex; gap: 15px; align-items: center;">
                        <img src="${p.image}" alt="${p.title}" class="radar-img" onerror="this.src='https://placehold.co/400x400/4a0e4e/white?text=Íntima+Elite'">
                        <h4 style="font-size: 1.05rem; margin: 0; color: #f8fafc; line-height: 1.3;">${p.title.substring(0, 45)}...</h4>
                    </div>
                    <div class="radar-review" style="margin-top: 15px;">${p.ai_review}</div>
                </a>
            `).join('');
        } catch (e) {
            radarGrid.innerHTML = '<div style="color: rgba(255,255,255,0.4); font-size: 0.8rem;">Radar em calibração...</div>';
        }
    }

    // Assistente Titanium (Sensual Persona)
    function initAssistant() {
        const assistant = document.getElementById('titanium-assistant');
        const bubble = assistant.querySelector('.bubble-text');
        
        const messages = [
            "Descobrindo rituais de bem-estar...",
            "Auditando discrição das embalagens...",
            "Selecionando seda e renda de elite...",
            "Verificando tecnologia air-touch..."
        ];

        let i = 0;
        setInterval(() => {
            bubble.innerText = messages[i % messages.length];
            i++;
        }, 4000);
    }

    initSensualBoutique();
    initAssistant();

    // Shield de Última Instância (Observer)
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            mutation.addedNodes.forEach((node) => {
                if (node.nodeType === 1) {
                    const links = node.tagName === 'A' ? [node] : node.querySelectorAll('a');
                    links.forEach(link => {
                        if (link.href && link.href.includes('shopee.com.br') && !link.dataset.audited) {
                            link.href = titaniumLinkAuditor(link.href);
                            link.dataset.audited = "true";
                        }
                    });
                }
            });
        });
    });
    observer.observe(document.body, { childList: true, subtree: true });
});
