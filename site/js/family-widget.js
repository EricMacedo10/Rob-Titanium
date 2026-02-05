/**
 * Family Assistant Widget Logic
 * Displays helpful tips and notifications from "Eric" and "Família Titanium"
 */

const FAMILY_CONFIG = {
    avatars: {
        family: 'images/family-cartoon-2d.png'
    },
    messages: [
        {
            avatar: 'family',
            name: 'Família',
            text: 'O Robô Titanium acabou de varrer a Amazon e achou preços surreais! 🤯'
        },
        {
            avatar: 'family',
            name: 'Família',
            text: 'Minha dica: as avaliações no Mercado Livre ajudam muito a decidir. ⭐'
        },
        {
            avatar: 'family',
            name: 'Família',
            text: 'Encontrei um cupom escondido na Shopee hoje cedo. Fiquem de olho! 🕵️‍♂️'
        },
        {
            avatar: 'family',
            name: 'Família',
            text: 'Fizemos uma curadoria especial de Volta às Aulas. Tudo com desconto! 🎒'
        },
        {
            avatar: 'family',
            name: 'Família',
            text: 'Não compre sem comparar! O Robô faz isso por você em segundos. ⏱️'
        },
        {
            avatar: 'family',
            name: 'Família',
            text: 'Essa semana a Amazon está imbatível na entrega. Pedi ontem, chegou hoje! 📦'
        },
        {
            avatar: 'family',
            name: 'Família',
            text: 'Monitoramos milhões de produtos 24h por dia para você não perder nada. 🛡️'
        },
        /* {
            avatar: 'family',
            name: 'Família',
            text: 'Gente, cuidado com picos de preço! O site te avisa a hora certa de comprar. 📉'
        }, */
        {
            avatar: 'family',
            name: 'Família',
            text: 'Ei! Sabia que nós verificamos os preços a cada 3 horas? Pode confiar! 🤖'
        },
        {
            avatar: 'family',
            name: 'Família',
            text: 'Amamos comprar na Amazon pela entrega rápida. Já testaram?'
        },
        {
            avatar: 'family',
            name: 'Família',
            text: 'Gente, acabei de conferir o setor de tecnologia e os achados de hoje estão imbatíveis! 💻'
        },
        {
            avatar: 'family',
            name: 'Família',
            text: 'Nada como a sensação de encontrar exatamente o que a gente queria pelo menor preço, né? O robô brilhou hoje! ✨'
        },
        {
            avatar: 'family',
            name: 'Família',
            text: 'Dica de quem ama uma casa organizada: os itens de decoração que selecionamos hoje estão lindos e muito baratos! 🏠'
        },
        {
            avatar: 'family',
            name: 'Família',
            text: 'O Robô Titanium não descansa! Ele acaba de encontrar ofertas fresquinhas na Shopee com frete grátis. Aproveitem! 🚚'
        },
        {
            avatar: 'family',
            name: 'Família',
            text: 'Olha só esse achado que a nossa curadoria separou para quem ama esportes... a qualidade é nota 10! 💪'
        },
        {
            avatar: 'family',
            name: 'Família',
            text: 'Sempre que vejo esses preços no Mercado Livre, fico impressionado com o quanto o nosso robô economiza pra gente! 💎'
        },
        {
            avatar: 'family',
            name: 'Família',
            text: 'Preparem os carrinhos! A seleção de Volta às Aulas está com itens que esgotam super rápido. 🎒'
        },
        {
            avatar: 'family',
            name: 'Família',
            text: 'A gente testa cada link para garantir que você vá direto para a melhor oferta. Segurança e economia juntas! 🛡️'
        },
        {
            avatar: 'family',
            name: 'Família',
            text: 'O segredo do Guia do Desconto é simples: a gente busca em todo lugar para você não precisar perder tempo. ⏱️'
        },
        {
            avatar: 'family',
            name: 'Família',
            text: 'Minha parte favorita do dia é ver o relatório de ofertas e postar os melhores descontos da Amazon para vocês! 🎁'
        },
        {
            avatar: 'family',
            name: 'Família',
            text: 'Dica Titanium: Compare preços rápido clicando nos botões de marcas dentro de cada categoria! 🎯'
        }
    ],
    initialDelay: 3000, // 3 seconds before first message
    interval: 45000 // Show a new message every 45 seconds
};

class FamilyWidget {
    constructor() {
        this.container = document.createElement('div');
        this.container.className = 'family-widget-container';
        document.body.appendChild(this.container);

        this.start();
    }

    start() {
        setTimeout(() => this.showRandomMessage(), FAMILY_CONFIG.initialDelay);

        setInterval(() => {
            this.showRandomMessage();
        }, FAMILY_CONFIG.interval);
    }

    showRandomMessage() {
        // 30% chance to NOT show anything this cycle (to not be annoying)
        if (Math.random() > 0.7) return;

        const msgData = FAMILY_CONFIG.messages[Math.floor(Math.random() * FAMILY_CONFIG.messages.length)];
        this.createNotification(msgData);
    }

    createNotification(data) {
        const notification = document.createElement('div');
        notification.className = 'family-notification';

        const avatarUrl = FAMILY_CONFIG.avatars[data.avatar];

        notification.innerHTML = `
            <img src="${avatarUrl}" alt="${data.name}" class="family-avatar-img">
            <div class="family-content">
                <span class="family-name">${data.name}</span>
                <p class="family-message">${data.text}</p>
            </div>
            <button class="family-close">&times;</button>
        `;

        // Add close logic
        notification.querySelector('.family-close').addEventListener('click', () => {
            this.removeNotification(notification);
        });

        this.container.appendChild(notification);

        // Sound effect (optional, verify with user first - disabled for now)
        // const audio = new Audio('notification.mp3'); audio.play();

        // Animate in
        requestAnimationFrame(() => {
            notification.classList.add('show');
        });

        // Auto remove after 8 seconds
        setTimeout(() => {
            this.removeNotification(notification);
        }, 8000);
    }

    removeNotification(element) {
        element.classList.remove('show');
        setTimeout(() => {
            if (element.parentElement) {
                element.remove();
            }
        }, 600); // Wait for transition
    }
}

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    new FamilyWidget();
});
