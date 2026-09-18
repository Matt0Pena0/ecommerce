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
        document.addEventListener('cart:updated', (e) => {
            const total = e.detail?.totalUnidades;

            // Si el emisor ya nos pasó el total, lo usamos y evitamos el request.
            // Si no vino (emisor sin payload), caemos al fetch.
            if (typeof total === 'number') {
                this.renderBadge(total);
            } else {
                this.updateBadge();
            }
        });
    },

    // Consulta el estado al servidor. Se usa en la carga inicial y como fallback.
    async updateBadge() {
        if (!document.getElementById(this.badgeId)) return;

        try {
            const status = await ApiService.getCarritoStatus();
            this.renderBadge(status.total_items);
        } catch (error) {
            console.warn('No se pudo sincronizar el badge global', error);
        }
    },

    // Pinta el badge a partir de un número ya conocido (sin red)
    renderBadge(count) {
        const badgeEl = document.getElementById(this.badgeId);
        if (!badgeEl) return;

        badgeEl.innerText = count;
        badgeEl.classList.toggle('d-none', count <= 0);
    }
};

document.addEventListener("DOMContentLoaded", () => GlobalApp.init());