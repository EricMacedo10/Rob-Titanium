/**
 * Family Assistant Widget Logic
 * Displays helpful tips and notifications from "Eric" and "Família Titanium"
 */

const FAMILY_CONFIG = {
    avatars: {
        family: 'images/family-cartoon-2d.png'
    },
    messages: [
        /* 💐 Frases Dia da Mulher (Aprovadas) - Ocultas após o dia 8
        {
            avatar: 'family',
            name: 'Família',
            text: 'Mulheres incríveis fazem o mundo girar! Hoje e sempre, nossa admiração. 💐'
        },
        {
            avatar: 'family',
            name: 'Família',
            text: 'A força e a delicadeza de vocês inspiram a Família Titanium todos os dias. ❤️'
        },
        {
            avatar: 'family',
            name: 'Família',
            text: 'Que o Dia da Mulher seja repleto de carinho, respeito e, claro, presentinhos! 🎁'
        },
        {
            avatar: 'family',
            name: 'Família',
            text: 'Mulher é sinônimo de garra e conquista. Parabéns por serem tudo o que são! ✨'
        },
        */

        // 🔥 Frases Ofertas do Dia (Aprovadas)
        {
            avatar: 'family',
            name: 'Família',
            text: 'Corre que as ofertas relâmpago não esperam ninguém! ⚡'
        },
        {
            avatar: 'family',
            name: 'Família',
            text: 'A Amazon e o Mercado Livre liberaram promoções exclusivas hoje. Aproveite! 🛒'
        },

        // 🤖 Frases Gerais do Robô (Mantidas)
        {
            avatar: 'family',
            name: 'Família',
            text: 'Monitoramos milhões de produtos 24h por dia para você não perder nada. 🛡️'
        },
        {
            avatar: 'family',
            name: 'Família',
            text: 'Ei! Sabia que nós verificamos os preços a cada 3 horas? Pode confiar! 🤖'
        },
        {
            avatar: 'family',
            name: 'Família',
            text: 'A gente testa cada link para garantir que você vá direto para a melhor oferta. Segurança e economia juntas! 🛡️'
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
        // Mutex Global: Se o Robô ou a Família já estiverem na tela, ignora o ciclo
        if (window.titaniumBusy || document.querySelector('.assistant-bubble.active')) {
            return;
        }

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

        // Show notification
        window.titaniumBusy = true; // Ativa a trava de exclusividade
        this.container.appendChild(notification);

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
            window.titaniumBusy = false; // Libera a trava para o próximo (ou para o robô)
        }, 600); // Wait for transition
    }
}

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    new FamilyWidget();
});
