import { ApiService } from './modules/api.js';


const GlobalApp = {
    // Definimos el ID aquí para usarlo en todo el objeto
    // ¡IMPORTANTE! Este ID debe coincidir con el del HTML
    badgeId: 'carrito-total-items', 

    init() {
        console.log('Global App Iniciada 🚀');
        this.initBootstrap();
        this.initBadge();
    },

    initBootstrap() {
        // Inicializa Tooltips
        const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        [...tooltipTriggerList].map(el => new bootstrap.Tooltip(el));

        // Inicializa Popovers
        const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
        [...popoverTriggerList].map(el => new bootstrap.Popover(el));
    },

    async initBadge() {
        // 1. Actualización inicial al cargar página
        await this.updateBadge();

        // 2. Escuchar evento global 'cart:updated'
        // Esto permite que otras partes (catalogo, carrito) pidan actualizar el badge
        document.addEventListener('cart:updated', () => this.updateBadge());
    },

    async updateBadge() {
        const badgeEl = document.getElementById(this.badgeId);
        if (!badgeEl) return;

        try {
            const status = await ApiService.getCarritoStatus();
            const count = status.total_items;

            badgeEl.innerText = count;

            // Mostrar u ocultar según la cantidad
            if (count > 0) {
                badgeEl.classList.remove('d-none');
            } else {
                badgeEl.classList.add('d-none');
            }

        } catch (error) {
            console.warn('No se pudo sincronizar el badge global', error);
        }
    }
};

document.addEventListener("DOMContentLoaded", () => GlobalApp.init());