import { CONFIG } from './modules/utils.js';
import { ApiService } from './modules/api.js';
import { UIRenderer } from './modules/ui.js';
import { showMessage } from './modules/utils.js';
import { initDeleteModal } from './modules/admin.js';


const App = {
    state: {
        carrito: {} 
    },

    container: document.getElementById('productos-container'),

    async init() {
        if (!this.container) return;

        // 1. Carga paralela de Metadata y Estado
        try {
            const [metadata, carritoStatus] = await Promise.all([
                ApiService.getMetadata(),
                ApiService.getCarritoStatus()
            ]);

            this.state.carrito = carritoStatus.items_dict || {};
            
            // 2. Pintar Filtros y Navbar
            UIRenderer.populateSelect('filter-marca', metadata.marcas, '-- Marca --');
            UIRenderer.populateSelect('filter-categoria', metadata.categorias, '-- Categoría --');
            UIRenderer.populateSelect('filter-gondola', metadata.gondolas, '-- Góndola --');
            
            const counter = document.getElementById('carrito-total-items');
            if(counter) counter.textContent = carritoStatus.total_items;

            // 3. Cargar catálogo
            this.loadCatalog();
            this.bindEvents();

        } catch (error) {
            console.error("Error inicializando app:", error);
            this.container.innerHTML = '<div class="alert alert-danger">Error conectando con el servidor</div>';
        }

        if (CONFIG.isSuperuser) {
            initDeleteModal();
        }
    },

    async loadCatalog(filtros = '') {
        this.container.innerHTML = '<div class="col-12 text-center mt-5"><div class="spinner-border text-primary"></div></div>';
        try {
            const productos = await ApiService.getProductos(filtros);
            this.container.innerHTML = productos.map(p => {
                const qty = this.state.carrito[p.id] || 0;
                return UIRenderer.getProductCardHTML(p, qty);
            }).join('');
        } catch (error) {
            this.container.innerHTML = '<p class="text-danger">Error cargando productos.</p>';
        }
    },

    async handleCartAction(form, nuevaCantidad, btnElement) {
        const productoId = form.dataset.id;
        const originalQty = parseInt(form.querySelector('input[name="quantity"]').value);

        if (btnElement) {
            const originalContent = btnElement.innerHTML;
            btnElement.disabled = true;
            btnElement.innerHTML = '<span class="spinner-border spinner-border-sm"></span>';
            
            try {
                const data = await ApiService.updateCarrito(productoId, nuevaCantidad);
                
                // Actualizar estado local
                this.state.carrito[productoId] = nuevaCantidad;
                if(nuevaCantidad === 0) delete this.state.carrito[productoId];

                // Actualizar UI
                showMessage(data.message, 'success');
                UIRenderer.updateCardState(form, nuevaCantidad);
                
                const counter = document.getElementById('carrito-total-items');
                if (counter && data.nuevo_total_productos !== undefined) {
                    counter.textContent = data.nuevo_total_productos;
                }
            } catch (error) {
                showMessage(error.message, 'error');
                UIRenderer.updateCardState(form, originalQty);
            } finally {
                btnElement.disabled = false;
                btnElement.innerHTML = originalContent;
            }
        }
    },

    bindEvents() {
        // Event Delegation para Steppers
        document.addEventListener('click', (e) => {
            const btn = e.target.closest('.stepper-incr, .stepper-decr');
            if (!btn) return;
            e.preventDefault();

            const form = btn.closest('form');
            const input = form.querySelector('input[name="quantity"]');
            let currentQty = parseInt(input.value) || 0;
            const isIncrement = btn.classList.contains('stepper-incr');
            
            let newQty = isIncrement ? currentQty + 1 : currentQty - 1;
            if (newQty < 0) newQty = 0;

            this.handleCartAction(form, newQty, btn);
        });

        // Listeners para Filtros
        ['filter-categoria', 'filter-marca', 'filter-gondola'].forEach(id => {
            const el = document.getElementById(id);
            if(el) {
                el.addEventListener('change', () => this.aplicarFiltros());
            }
        });
    },

    aplicarFiltros() {
        const params = new URLSearchParams();
        const cat = document.getElementById('filter-categoria')?.value;
        const marca = document.getElementById('filter-marca')?.value;
        const gondola = document.getElementById('filter-gondola')?.value;

        if (cat) params.append('categoria', cat);
        if (marca) params.append('marca', marca);
        if (gondola) params.append('gondola', gondola);
        
        // También podrías agregar ordenamiento aquí

        this.loadCatalog(`?${params.toString()}`);
    }
};

document.addEventListener('DOMContentLoaded', () => App.init());