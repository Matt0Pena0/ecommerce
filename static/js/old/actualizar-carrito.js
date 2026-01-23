import { showToast } from './toast.js';

/**
 * =============================================================================
 * CONFIGURACIÓN Y UTILIDADES
 * =============================================================================
 */
const CONFIG = {
    urlProductos: document.getElementById('productos-container')?.dataset.urlProductos || '/api/productos/',
    urlCarrito: document.body.dataset.urlAgregarCarrito || '/api/carrito/agregar/', // Ajusta a tu URL real
    isSuperuser: document.getElementById('productos-container')?.dataset.isSuperuser === 'true'
};

const Utils = {
    getCookie: (name) => {
        const matches = document.cookie.match(new RegExp('(?:^|; )' + name + '=([^;]*)'));
        return matches ? decodeURIComponent(matches[1]) : null;
    },
    
    showMessage: (msg, type = 'success') => {
        if (typeof showToast === 'function') {
            showToast(msg, type);
        } else {
            console.log(`[${type.toUpperCase()}]: ${msg}`);
            if (type === 'error') alert(msg);
        }
    }
};

/**
 * =============================================================================
 * SERVICIO API (Comunicación con DRF)
 * =============================================================================
 */
const ApiService = {
    async getProductos(filtros = '') {
        try {
            const response = await fetch(`${CONFIG.urlProductos}${filtros}`);
            if (!response.ok) throw new Error('Error al obtener productos');
            return await response.json();
        } catch (error) {
            console.error(error);
            throw error;
        }
    },

    async updateCarrito(productoId, cantidad) {
        const csrfToken = Utils.getCookie('csrftoken');
        
        const response = await fetch(CONFIG.urlCarrito, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                producto_id: productoId,
                cantidad: parseInt(cantidad)
            })
        });

        const data = await response.json();
        if (!response.ok) throw new Error(data.message || 'Error en servidor');
        return data;
    }
};

/**
 * =============================================================================
 * RENDERIZADOR UI (Generación de HTML)
 * =============================================================================
 */
const UIRenderer = {
    // Genera el HTML de los controles (Stepper o Botón Agregar)
    getControlsHTML(qty, maxStock) {
        const isInCart = qty > 0;
        
        if (isInCart) {
            // Renderizar Stepper
            return `
                <div class="btn-stepper d-flex align-items-center m-1" role="group" aria-label="Cantidad">
                    <button type="button" class="btn btn-outline-secondary btn-sm stepper-decr" ${qty <= 0 ? 'disabled' : ''}>
                        <i class="bi bi-dash-square-fill"></i>
                    </button>
                    <div class="qty-display mx-2 text-center" data-min="0" data-max="${maxStock}">
                        <span class="fw-semibold">${qty}</span>
                    </div>
                    <button type="button" class="btn btn-outline-secondary btn-sm stepper-incr" ${qty >= maxStock ? 'disabled' : ''}>
                        <i class="bi bi-plus-square-fill"></i>
                    </button>
                </div>`;
        } else {
            // Renderizar Botón Agregar
            return `
                <div class="btn-stepper d-flex align-items-center m-1" role="group">
                    <button type="button" class="btn btn-sm btn-primary stepper-incr" aria-label="Agregar">
                        <i class="bi bi-plus-square-fill"></i>
                    </button>
                </div>`;
        }
    },

    // Genera la Tarjeta de Producto completa
    getProductCardHTML(p) {
        // NOTA: Aquí asumo qty=0. En el futuro, idealmente el API debe decirte si ya está en carrito.
        const qty = 0; 
        const maxStock = p.stock || 100;

        return `
            <div class="col g-1 g-sm-1 g-md-2 g-xl-4">
                <div class="card d-flex flex-column shadow-sm p-1 p-md-2 m-0" style="height: 300px;">
                    <div class="d-flex justify-content-center align-items-start" style="height: 80px;">
                        <img src="${p.img || '/static/img/producto.png'}" 
                             class="card-img-top w-auto img-fluid" style="max-height: 80px; object-fit:contain;">
                    </div>
                    <div class="card-body d-flex flex-column px-2 pt-1 pb-0">
                        <div class="my-0" style="min-height: 6em;">
                            <p class="card-title my-0 text-truncate-2" title="${p.nombre}">${p.nombre}</p>
                            <small class="text-muted text-truncate-2">${p.marca_nombre || ''} - ${p.categoria_nombre || ''}</small>
                        </div>
                        <div class="align-items-center mx-auto mt-2" style="height: 1.5em;">
                            <span class="fw-bold">$${p.precio_unitario}</span>
                        </div>
                        
                        <form class="add-to-cart-form d-flex flex-column m-0 align-items-center" data-id="${p.id}">
                            <input type="hidden" name="quantity" value="${qty}">
                            <div class="action-wrapper w-100 d-flex flex-column align-items-center justify-content-center">
                                ${this.getControlsHTML(qty, maxStock)}
                            </div>
                        </form>

                        ${CONFIG.isSuperuser ? this.getAdminControls(p.id) : ''}
                    </div>
                </div>
            </div>`;
    },

    getAdminControls(id) {
        return `
            <div class="card-footer d-flex justify-content-between p-0 mt-2">
                <a href="/productos/actualizar/${id}/" class="btn btn-outline-secondary btn-sm">
                    <i class="bi bi-pencil-square"></i>
                </a>
            </div>`;
    },

    // Actualiza visualmente una tarjeta existente tras una acción AJAX
    updateCardState(form, newQty) {
        const wrapper = form.querySelector('.action-wrapper');
        const hiddenInput = form.querySelector('input[name="quantity"]');
        const display = form.querySelector('.qty-display');
        const maxStock = parseInt(display?.dataset.max) || 100;

        // Actualizamos input oculto
        if (hiddenInput) hiddenInput.value = newQty;

        // Decidimos si re-renderizar todo el control (cambio de estado 0 <-> 1)
        // o solo actualizar el número (optimización)
        const isStepperVisible = wrapper.querySelector('.qty-display') !== null;
        const shouldBeStepper = newQty > 0;

        if (isStepperVisible !== shouldBeStepper) {
            // Cambio de estado drástico: Re-dibujar HTML
            wrapper.innerHTML = this.getControlsHTML(newQty, maxStock);
        } else if (shouldBeStepper) {
            // Solo actualizar número y botones
            wrapper.querySelector('.qty-display span').textContent = newQty;
            const decr = wrapper.querySelector('.stepper-decr');
            const incr = wrapper.querySelector('.stepper-incr');
            if (decr) decr.disabled = newQty <= 0;
            if (incr) incr.disabled = newQty >= maxStock;
        }
    }
};

/**
 * =============================================================================
 * LÓGICA CORE (Controlador)
 * =============================================================================
 */
const App = {
    init() {
        this.container = document.getElementById('productos-container');
        if (!this.container) return; // No estamos en la página de catálogo

        // 1. Cargar productos iniciales
        this.loadCatalog();

        // 2. Configurar Listeners Globales (Delegación de eventos)
        this.bindEvents();
    },

    async loadCatalog(filtros = '') {
        this.container.innerHTML = '<div class="col-12 text-center mt-5"><div class="spinner-border text-primary"></div></div>';
        
        try {
            const productos = await ApiService.getProductos(filtros);
            this.container.innerHTML = productos.map(p => UIRenderer.getProductCardHTML(p)).join('');
        } catch (error) {
            this.container.innerHTML = '<div class="alert alert-danger">Error cargando productos</div>';
        }
    },

    async handleCartAction(form, nuevaCantidad, btnElement) {
        const productoId = form.dataset.id;
        const originalQty = parseInt(form.querySelector('input[name="quantity"]').value);

        // Feedback visual inmediato (loading en el botón)
        if (btnElement) {
            const originalContent = btnElement.innerHTML;
            btnElement.disabled = true;
            btnElement.innerHTML = '<span class="spinner-border spinner-border-sm"></span>';
            
            try {
                // Llamada API
                const data = await ApiService.updateCarrito(productoId, nuevaCantidad);
                
                // Éxito
                Utils.showMessage(data.message, 'success');
                UIRenderer.updateCardState(form, nuevaCantidad);
                
                // Actualizar contador global del navbar si existe
                const navbarCounter = document.getElementById('carrito-total-items');
                if (navbarCounter && data.nuevo_total_productos !== undefined) {
                    navbarCounter.textContent = data.nuevo_total_productos;
                }

            } catch (error) {
                // Error: Revertir
                Utils.showMessage(error.message, 'error');
                UIRenderer.updateCardState(form, originalQty);
            } finally {
                // Restaurar botón
                btnElement.disabled = false;
                btnElement.innerHTML = originalContent;
            }
        }
    },

    bindEvents() {
        // Un solo Listener en el documento para manejar todos los clicks de steppers
        document.addEventListener('click', (e) => {
            const btn = e.target.closest('.stepper-incr, .stepper-decr');
            if (!btn) return;

            const form = btn.closest('form');
            if (!form) return;

            e.preventDefault();

            // Determinar cantidad actual y futura
            const input = form.querySelector('input[name="quantity"]');
            let currentQty = parseInt(input.value) || 0;
            const isIncrement = btn.classList.contains('stepper-incr');
            
            // Si es el botón "Agregar" inicial, currentQty es 0, pasamos a 1
            let newQty = isIncrement ? currentQty + 1 : currentQty - 1;
            if (newQty < 0) newQty = 0;

            this.handleCartAction(form, newQty, btn);
        });

        // Listener para filtros (Si los tienes)
        const filtroCategoria = document.getElementById('filter-categoria');
        if (filtroCategoria) {
            filtroCategoria.addEventListener('change', (e) => {
                const params = new URLSearchParams();
                if(e.target.value) params.append('categoria', e.target.value);
                this.loadCatalog(`?${params.toString()}`);
            });
        }
    }
};

// Arrancar la aplicación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    App.init();
});