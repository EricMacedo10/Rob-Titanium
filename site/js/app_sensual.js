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
    const searchInput = document.getElementById('search-input');
    const searchButton = document.querySelector('.btn-search');

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
            const resRadar = await fetch(CONFIG.RADAR_SOURCE + CONFIG.CACHE_BUST);
            const dataRadar = await resRadar.json();
            allProducts = [...allProducts, ...dataRadar];
            loadRadar(dataRadar);

            // Vitrine 2: Especialista (Lingerie)
            const resPlatinum = await fetch(CONFIG.PLATINUM_SOURCE + CONFIG.CACHE_BUST);
            const dataPlatinum = await resPlatinum.json();
            allProducts = [...allProducts, ...dataPlatinum];
            renderProducts(dataPlatinum.slice(0, 24), 'platinum-grid');

            // Vitrine 3: Ofertas (Cosmética)
            const resOffers = await fetch(CONFIG.DATA_SOURCE + CONFIG.CACHE_BUST);
            const dataOffers = await resOffers.json();
            allProducts = [...allProducts, ...dataOffers];
            renderProducts(dataOffers.slice(0, 24), 'deals-grid');

            initAssistant();
            setupSearch();
        } catch (err) {
            console.error('[Íntima] Erro na inicialização:', err);
        }
    }

    async function loadRadar(radarData) {
        const radarGrid = document.getElementById('radar-grid');
        if (!radarGrid) return;

        try {
            if (!radarData) {
                const res = await fetch(CONFIG.RADAR_SOURCE + CONFIG.CACHE_BUST);
                radarData = await res.json();
            }
            
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
        if (!assistant) return;
        
        const bubble = assistant.querySelector('.bubble-text');
        if (!bubble) return;
        
        let messages = [
            "O seu bem-estar é a sua maior luxúria.",
            "Autocuidado não é um luxo, é a sua prioridade.",
            "Você merece momentos dedicados apenas a você.",
            "Invista em você. É o melhor retorno garantido.",
            "Descubra o prazer de cuidar de si mesma.",
            "Rotinas de beleza são rituais de amor-próprio.",
            "O luxo é ter tempo para se amar.",
            "Transforme o seu dia com pequenos gestos de carinho.",
            "Cuidar de você é o primeiro passo para conquistar o mundo.",
            "Abrace cada curva da sua jornada.",
            "A sua confiança é o seu acessório mais caro.",
            "Seja a protagonista absoluta da sua história.",
            "Uma mulher segura é uma força da natureza.",
            "O poder está nas suas mãos. E nas suas escolhas.",
            "Você é a musa da sua própria vida.",
            "Reconheça a sua força. Ela é imensurável.",
            "Vista-se de autoestima e conquiste o universo.",
            "Ninguém pode ditar os limites do seu prazer.",
            "Mulheres empoderadas empoderam outras mulheres.",
            "Respire fundo e sinta a deusa que habita em você.",
            "A verdadeira elegância começa de dentro para fora.",
            "Permita-se sentir o poder da sua própria pele.",
            "Não há nada mais sensual do que a autoconfiança.",
            "Conforto e beleza andam de mãos dadas.",
            "Sinta-se deusa em cada detalhe do seu dia.",
            "A vida é curta para não usar a sua melhor lingerie.",
            "Seja livre para explorar os seus desejos.",
            "O seu corpo é um templo. Honre-o sempre.",
            "A sua luz e energia iluminam tudo ao redor.",
            "O seu magnetismo vem da sua autenticidade.",
            "Celebre a beleza de ser exatamente quem você é.",
            "Desperte a sua melhor versão todos os dias.",
            "Sua essência é única. Deixe-a brilhar.",
            "Você é suficiente, incrível e extraordinária.",
            "A beleza começa quando você decide ser você mesma.",
            "Seu sorriso é a assinatura do seu estilo.",
            "Permita-se ser vulnerável, intensa e real.",
            "Você é uma obra de arte em constante evolução.",
            "Não siga padrões, seja a sua própria referência.",
            "O mundo é a sua passarela. Desfile."
        ];

        // Embaralha as mensagens para garantir aleatoriedade em cada visita
        messages = messages.sort(() => Math.random() - 0.5);

        let i = 0;
        
        // Exibe a primeira mensagem após 3 segundos
        setTimeout(() => {
            bubble.innerText = messages[0];
            const bubbleWrapper = assistant.querySelector('.assistant-bubble');
            if(bubbleWrapper) bubbleWrapper.classList.add('active');
            
            setTimeout(() => {
                if(bubbleWrapper) bubbleWrapper.classList.remove('active');
            }, 8000);
        }, 3000);
        
        // Rotaciona as mensagens a cada 25 segundos (visível por 8s)
        setInterval(() => {
            i++;
            bubble.innerText = messages[i % messages.length];
            const bubbleWrapper = assistant.querySelector('.assistant-bubble');
            
            if(bubbleWrapper) {
                bubbleWrapper.classList.add('active');
                setTimeout(() => {
                    bubbleWrapper.classList.remove('active');
                }, 8000);
            }
        }, 25000);
    }

    function setupSearch() {
        console.log('[Search] Configurando listeners...');
        if (searchButton && searchInput) {
            searchButton.addEventListener('click', () => {
                console.log('[Search] Botão clicado');
                performSearch();
            });
            searchInput.addEventListener('keyup', (e) => {
                if (e.key === 'Enter') {
                    console.log('[Search] Enter pressionado');
                    performSearch();
                }
            });
        } else {
            console.warn('[Search] Elementos não encontrados:', { searchButton, searchInput });
        }
    }

    function performSearch() {
        const query = searchInput.value.toLowerCase().trim();
        console.log('[Search] Iniciando busca por:', query);
        
        const dealsGrid = document.getElementById('deals-grid');
        const radarSection = document.getElementById('radar');
        const platinumSection = document.getElementById('platinum');
        const sectionTitle = document.querySelector('.voted-deals .section-title');

        if (!dealsGrid) {
            console.error('[Search] deals-grid não encontrado');
            return;
        }

        // Esconder outras seções durante a busca para focar nos resultados
        if (radarSection) radarSection.style.display = query ? 'none' : 'block';
        if (platinumSection) platinumSection.style.display = query ? 'none' : 'block';

        if (!query) {
            console.log('[Search] Query vazia, recarregando...');
            window.location.reload();
            return;
        }

        dealsGrid.innerHTML = `
            <div style="grid-column: 1/-1; text-align: center; padding: 50px;">
                <i class="fa-solid fa-circle-notch fa-spin" style="font-size: 2rem; color: #4a0e4e;"></i>
                <p style="margin-top: 15px; color: #64748b;">Buscando por "${query}" na Boutique Íntima...</p>
            </div>
        `;

        // Garantir que temos produtos
        if (allProducts.length === 0) {
            console.warn('[Search] allProducts está vazio, tentando recuperar dados...');
        }

        setTimeout(() => {
            const matches = allProducts.filter(p => {
                const title = (p.title || '').toLowerCase();
                const review = (p.ai_review || '').toLowerCase();
                const category = (p.category || '').toLowerCase();
                return title.includes(query) || review.includes(query) || category.includes(query);
            });

            console.log(`[Search] ${matches.length} resultados encontrados`);

            if (matches.length === 0) {
                if (sectionTitle) sectionTitle.innerHTML = `Busca por: "<strong>${query}</strong>"`;
                dealsGrid.innerHTML = `
                    <div style="grid-column: 1/-1; border: 2px dashed #4a0e4e; border-radius: 20px; padding: 50px 20px; background: #fff5f2; text-align: center;">
                        <div style="font-size: 4rem; margin-bottom: 20px;">🤖</div>
                        <h3 style="color: #4a0e4e; font-size: 1.8rem; margin-bottom: 15px;">O Robô Titanium está pronto!</h3>
                        <p style="color: #64748b; font-size: 1.1rem; line-height: 1.6; max-width: 600px; margin: 0 auto 30px;">
                            Não encontramos "<strong>${query}</strong>" na nossa vitrine curada de Lingerie & Bem-Estar, mas o <strong>Robô Titanium</strong> pode abrir a busca oficial agora!
                        </p>
                        
                        <div style="display: flex; flex-direction: column; gap: 15px; align-items: center;">
                            <button onclick="titaniumDeepLink('${query}')" 
                               style="background: linear-gradient(90deg, #4a0e4e, #7b2d8e); color: white; padding: 18px 40px; border: none; border-radius: 50px; font-weight: 800; font-size: 1.2rem; cursor: pointer; text-decoration: none; box-shadow: 0 10px 25px rgba(74, 14, 78, 0.3); display: flex; align-items: center; gap: 10px; transition: transform 0.2s;">
                                <i class="fas fa-search"></i> Buscar tudo na Shopee agora
                            </button>
                            
                            <button onclick="window.location.reload()" style="background: white; color: #4a0e4e; border: 2px solid #4a0e4e; padding: 12px 30px; border-radius: 50px; font-weight: 700; cursor: pointer; margin-top: 20px;">
                                <i class="fas fa-home"></i> Voltar para a Boutique
                            </button>
                        </div>
                    </div>
                `;
            } else {
                if (sectionTitle) {
                    sectionTitle.innerHTML = `Resultados para "<strong>${query}</strong>"`;
                }
                renderProducts(matches, 'deals-grid');
            }

            // Scroll suave para os resultados
            const gridPos = dealsGrid.getBoundingClientRect().top + window.pageYOffset - 100;
            window.scrollTo({ top: gridPos, behavior: 'smooth' });
        }, 400);
    }

    window.titaniumDeepLink = function(query) {
        const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
        const webUrl = `https://shopee.com.br/search?keyword=${encodeURIComponent(query)}&utm_source=${CONFIG.AFFILIATE_TAG}`;
        
        if (isMobile) {
            const appUrl = `shopeebrazil://search?keyword=${encodeURIComponent(query)}`;
            const now = Date.now();
            setTimeout(() => {
                if (Date.now() - now < 1000) window.location.href = webUrl;
            }, 500);
            window.location.href = appUrl;
        } else {
            window.open(webUrl, '_blank');
        }
    };

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
