import { ApiService } from './modules/api.js';
import { UIRenderer } from './modules/ui.js';
import { showMessage } from './modules/utils.js';


const CartApp = {
    container: document.getElementById('cart-items-container'),

    async init() {
        if (!this.container) return;
        await this.renderCart();
        this.bindEvents();
    },

    async renderCart() {
        try {
            // Pedimos el detalle completo (incluyendo el total corregido)
            const data = await ApiService.getCarritoDetalle(); // Asegúrate de tener este fetch en api.js

            if (!data.items || data.items.length === 0) {
                this.container.innerHTML = '<tr><td colspan="9" class="text-center py-5">Tu carrito está vacío.</td></tr>';
                document.getElementById('cart-summary').classList.add('d-none');
                return;
            }

            // Pintamos las filas usando el UIRenderer
            this.container.innerHTML = data.items.map(item => UIRenderer.getCartRowHTML(item)).join('');
            
            // Actualizamos el total general
            document.getElementById('cart-total-price').textContent = `$${data.total_dinero}`;
            document.getElementById('cart-summary').classList.remove('d-none');
            
            // Sincronizamos el badge del navbar
            const counter = document.getElementById('carrito-total-items');
            if (counter) counter.textContent = data.total_unidades;

        } catch (error) {
            console.error(error);
            this.container.innerHTML = '<tr><td colspan="5" class="text-center text-danger">Error al cargar el carrito.</td></tr>';
        }
    },

    bindEvents() {
        // Delegación de eventos para la tabla
        this.container.addEventListener('click', async (e) => {
            // Buscamos si el click fue en un botón de incremento, decremento o eliminar
            const btnIncr = e.target.closest('.stepper-incr');
            const btnDecr = e.target.closest('.stepper-decr');
            const btnEliminar = e.target.closest('.btn-eliminar-item');

            // Si no fue en ninguno de esos, no hacemos nada
            if (!btnIncr && !btnDecr && !btnEliminar) return;

            const row = e.target.closest('tr');
            const productoId = row.dataset.productoId;
            
            // --- LÓGICA DE INCREMENTO / DECREMENTO ---
            if (btnIncr || btnDecr) {
                const qtyElement = row.querySelector('.qty-display');
                
                // CORRECCIÓN AQUÍ:
                // Si es un input (tabla), usamos .value. Si es un span (cards), usamos .textContent
                let currentQty = 0;
                if (qtyElement.tagName === 'INPUT') {
                    currentQty = parseInt(qtyElement.value);
                } else {
                    currentQty = parseInt(qtyElement.textContent);
                }

                // Evitamos clicks múltiples mientras procesa
                btnIncr ? btnIncr.disabled = true : btnDecr.disabled = true;

                const nuevaCantidad = btnIncr ? currentQty + 1 : currentQty - 1;
                
                if (nuevaCantidad >= 1) { // Mínimo 1, para borrar usamos el botón de eliminar
                    try {
                        await ApiService.updateCarrito(productoId, nuevaCantidad);
                        await this.renderCart(); // Refrescamos la tabla
                    } catch (error) {
                        showMessage(error.message, 'error');
                        // Si falla, reactivamos botones
                        if(btnIncr) btnIncr.disabled = false;
                        if(btnDecr) btnDecr.disabled = false;
                    }
                } else {
                    // Si intenta bajar a 0, reactivamos el botón porque no hicimos nada
                    if(btnDecr) btnDecr.disabled = false;
                }
            }

            // CASO 2: Eliminar directamente
            if (btnEliminar) {
                if (confirm('¿Eliminar este producto?')) {
                    try {
                        await ApiService.eliminarDelCarrito(productoId);
                        await this.renderCart();
                    } catch (error) {
                        showMessage(error.message, 'error');
                    }
                }
            }
        });

        const btnFinalizar = document.getElementById('btn-finalizar-compra');
        btnFinalizar?.addEventListener('click', async () => {
            
            // 1. UI Feedback: Evitar doble compra
            const originalText = btnFinalizar.innerHTML;
            btnFinalizar.disabled = true;
            btnFinalizar.innerHTML = `
                <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                Procesando...
            `;

            try {
                // 2. Llamada a la API (usa el ApiService que definimos antes)
                const res = await ApiService.finalizarCompra();

                if (res.status === 'ok') {
                    showMessage(res.message, 'success');
                    
                    // 3. Redirección suave tras 1.5 segundos para que vea el mensaje
                    setTimeout(() => {
                        window.location.href = res.redirect_url;
                    }, 1500);
                } else {
                    throw new Error(res.message);
                }

            } catch (error) {
                showMessage(error.message || 'Error al procesar la compra', 'error');
                // Revertir botón si falla
                btnFinalizar.disabled = false;
                btnFinalizar.innerHTML = originalText;
            }
        });
    }
};

document.addEventListener('DOMContentLoaded', () => CartApp.init());