/**
 * Family Assistant Widget Logic
 * Displays helpful tips and notifications from "Eric" and "Família Titanium"
 */

const FAMILY_CONFIG = {
    avatars: {
        eric_group: 'images/family-cartoon-2d.png',
        wife_group: 'images/family-cartoon-2d.png'
    },
    messages: [
        {
            avatar: 'eric_group',
            name: 'Família',
            text: 'Ei! Sabia que nós verificamos os preços a cada 3 horas? Pode confiar! 🤖'
        },
        {
            avatar: 'wife_group',
            name: 'Família',
            text: 'Gente, olha esse iPhone! O preço caiu muito hoje! 🔥'
        },
        {
            avatar: 'eric_group',
            name: 'Família',
            text: 'Dica de Mestre: Use o botão de busca ali em cima, ele acha ofertas escondidas.'
        },
        {
            avatar: 'wife_group',
            name: 'Família',
            text: 'Amamos comprar na Amazon pela entrega rápida. Já testaram?'
        },
        {
            avatar: 'wife_group',
            name: 'Família',
            text: 'Avisa o pessoal que as ofertas da Shopee estão com cupom de frete grátis!'
        },
        {
            avatar: 'eric_group',
            name: 'Família',
            text: 'Se virem o ícone de 🔥, é porque a oferta está muito quente!'
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
