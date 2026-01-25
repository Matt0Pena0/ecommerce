import { ApiService } from './modules/api.js';
import { UIRenderer } from './modules/ui.js';
import { CONFIG, debounce } from './modules/utils.js';
import { showMessage } from './toast.js';
import { initDeleteModal, initProductModal } from './modules/admin.js';


const App = {
    state: {
        carrito: {} 
    },

    container: document.getElementById('productos-container'),

    async init() {
        if (!this.container) return;

        try {
            const [metadata, carritoStatus] = await Promise.all([
                ApiService.getMetadata(),
                ApiService.getCarritoStatus()
            ]);
        
            this.state.carrito = carritoStatus.items_dict || {};
        
            UIRenderer.populateSelect('filter-marca', metadata.marcas, '-- Marca --');
            UIRenderer.populateSelect('filter-categoria', metadata.categorias, '-- Categoría --');
            UIRenderer.populateSelect('filter-gondola', metadata.gondolas, '-- Góndola --');

            // --- NOTA: Orden de encendido de motores ---
            this.bindEvents();        // Activa Steppers
            this.bindFilterEvents();  // Activa Sidebar
            this.loadCatalog();       // Carga inicial de productos

        } catch (error) {
            console.error("Error inicializando app:", error);
            this.container.innerHTML = '<div class="alert alert-danger">Error conectando con el servidor</div>';
        }

        if (CONFIG.isSuperuser) {
            initProductModal();
            initDeleteModal();
        }
    },

    async loadCatalog(filtros = '') {
        this.container.innerHTML = '<div class="col-12 text-center mt-5"><div class="spinner-border text-primary"></div></div>';

        try {
        const data = await ApiService.getProductos(filtros);
        
        // NOTA: Si hay paginación, los productos están en data.results
        const listaProductos = data.results || data; 

        if (listaProductos.length === 0) {
            this.container.innerHTML = '<div class="position-absolute top-25 start-50 translate-middle text-center mt-5">No se encontraron productos.</div>';
            return;
        }

        this.container.innerHTML = listaProductos.map(p => {
            const qty = this.state.carrito[p.id] || 0;
            return UIRenderer.getProductCardHTML(p, qty);
        }).join('');

        } catch (error) {
            this.container.innerHTML = '<p class="text-danger">Error cargando productos.</p>';
        }
    },

    bindFilterEvents() {
        const inputs = document.querySelectorAll('.filter-input');
        
        const applyFilters = () => {
            const params = new URLSearchParams();
            const q = document.getElementById('filter-q')?.value;
            const codigo = document.getElementById('filter-codigo')?.value;
            const marca = document.getElementById('filter-marca')?.value;
            const cat = document.getElementById('filter-categoria')?.value;
            const gondola = document.getElementById('filter-gondola')?.value;
            const stock = document.getElementById('filter-stock')?.value;
            const order = document.getElementById('filter-order')?.value;

            if (q) params.append('search', q);
            if (codigo) params.append('codigo', codigo);
            if (marca) params.append('marca', marca);
            if (cat) params.append('categoria', cat);
            if (gondola) params.append('gondola', gondola);
            if (stock) params.append('stock_status', stock);
            if (order) params.append('ordering', order);

            this.loadCatalog(`?${params.toString()}`);
        };

        const debouncedApply = debounce(applyFilters, 400);

        inputs.forEach(input => {
            if (input.tagName === 'SELECT') {
                input.addEventListener('change', applyFilters);
            } else {
                input.addEventListener('input', debouncedApply);
            }
        });

        document.getElementById('btn-clean-filters')?.addEventListener('click', () => {
            inputs.forEach(i => i.value = '');
            applyFilters();
        });
    },

    bindEvents() {
        // Event Delegation para Steppers (Usa burbujeo de eventos)
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
    },

    async handleCartAction(form, nuevaCantidad, btnElement) {
        const productoId = form.dataset.id;
        const originalQty = parseInt(form.querySelector('input[name="quantity"]').value);

        const originalContent = btnElement.innerHTML;
        btnElement.disabled = true;
        btnElement.innerHTML = '<span class="spinner-border spinner-border-sm"></span>';
        
        try {
            const data = await ApiService.updateCarrito(productoId, nuevaCantidad);
            
            this.state.carrito[productoId] = nuevaCantidad;
            if(nuevaCantidad === 0) delete this.state.carrito[productoId];

            showMessage(data.message, 'success');
            UIRenderer.updateCardState(form, nuevaCantidad);
            
            document.dispatchEvent(new Event('cart:updated'));

        } catch (error) {
            showMessage(error.message, 'error');
            UIRenderer.updateCardState(form, originalQty);
        } finally {
            btnElement.disabled = false;
            btnElement.innerHTML = originalContent;
        }
    }
};

document.addEventListener('DOMContentLoaded', () => App.init());