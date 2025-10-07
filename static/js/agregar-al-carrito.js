document.addEventListener('DOMContentLoaded', function() {
    // URL principal para agregar/actualizar/eliminar del carrito.
    const urlParaAgregar = document.body.dataset.urlAgregarCarrito || null;

    // --- Helpers ---
    const getCookie = (name) => {
        const matches = document.cookie.match(new RegExp('(?:^|; )' + name + '=([^;]*)'));
        return matches ? decodeURIComponent(matches[1]) : null;
    };
    
    const showMessage = (msg, type = 'success') => {
        if (typeof showToast === 'function') {
            showToast(msg, type);
        } else {
            console.log(`[${type.toUpperCase()}]: ${msg}`);
            if (type === 'error') alert(msg);
        }
    };

    // --- Lógica de Renderizado con Template Literals ---
    
    /**
     * Renderiza el estado de la tarjeta cuando el producto está en el carrito (Stepper).
     * Nota: Ya NO incluye el botón submit redundante.
     */
    const renderStepper = (qty, maxStock) => {
        const isDisabled = qty >= maxStock;
        const decrDisabled = qty <= 0;
        
        // Renderizamos la estructura de 3 partes: [-] [QTY] [+]
        return `
            <div class="action-wrapper w-100 d-flex flex-column flex-md-row justify-content-between align-items-center">
                <div class="btn-stepper d-flex align-items-center mb-2 mb-md-0 me-0 me-md-2" role="group" aria-label="Cantidad">
                    <button type="button" class="btn btn-outline-secondary btn-sm stepper-decr" aria-label="Disminuir cantidad" ${decrDisabled ? 'disabled' : ''}>−</button>

                    <div class="qty-display mx-2 text-center"
                        data-min="0"
                        data-max="${maxStock}">
                        <span class="fw-semibold">${qty}</span>
                    </div>

                    <button type="button" class="btn btn-outline-secondary btn-sm stepper-incr" aria-label="Aumentar cantidad" ${isDisabled ? 'disabled' : ''}>+</button>
                </div>
                
                <!-- El botón de submit ya no se genera aquí -->
            </div>
        `;
    };

    /**
     * Renderiza el estado de la tarjeta cuando el producto NO está en el carrito (Solo botón Agregar).
     */
    const renderAddButton = () => {
        return `
            <div class="action-wrapper w-100 d-flex flex-column flex-md-row justify-content-between align-items-center">
                <div class="btn-stepper d-flex align-items-center mb-2 mb-md-0 me-0 me-md-2" role="group" aria-label="Cantidad">
                    <button type="button" class="btn btn-sm btn-primary stepper-incr" aria-label="Agregar al carrito">
                        <i class="bi bi-cart-plus"></i>
                    </button>
                </div>
            </div>
        `;
    };

    // --- Lógica de Actualización de Tarjeta (Mini-Carrito Persistente) ---
    
    /**
     * Reemplaza el HTML del contenedor de acciones o actualiza el display de cantidad.
     */
    const updateCardDisplay = (form, newQty) => {
        const hiddenInput = form.querySelector('input[name="quantity"]');
        const actionWrapper = form.querySelector('.action-wrapper'); // Contenedor que reemplazaremos
        
        // Buscamos el stock máximo del producto.
        const maxStock = parseInt(form.querySelector('.qty-display')?.dataset.max) || Infinity;

        if (!hiddenInput || !actionWrapper) return;
        
        // CLAVE: Determinar si el estado visual (qty > 0) ha cambiado.
        const isCurrentlyInStepper = actionWrapper.querySelector('.stepper-decr') !== null;
        const shouldBeInStepper = newQty > 0;
        
        // Si el estado visual actual NO coincide con el estado visual deseado: RE-RENDERIZAR
        if (isCurrentlyInStepper !== shouldBeInStepper) { 
            
            // Preservamos CSRF y el Input de Cantidad.
            
            if (shouldBeInStepper) {
                 // Transición a Stepper (1 -> >0)
                 actionWrapper.innerHTML = renderStepper(newQty, maxStock);
            } else {
                 // Transición a Botón Agregar (1 -> 0)
                 actionWrapper.innerHTML = renderAddButton();
            }
            
            // Si reemplazamos el HTML, debemos re-adjuntar el listener al formulario
            // (Aunque el listener del document.addEventListener('click', stepperHandler) es global,
            // si el formulario se reemplaza completamente, es mejor re-adjuntarlo).
            // Ya que solo reemplazamos el innerHTML del wrapper, los listeners globales deben seguir funcionando.
            
        } else if (newQty > 0) { 
            // Estado >0, solo actualizamos el display visible sin re-renderizar todo
            const qtyDisplaySpan = form.querySelector('.qty-display span');
            if (qtyDisplaySpan) qtyDisplaySpan.textContent = newQty;
            
            const decr = form.querySelector('.stepper-decr');
            const incr = form.querySelector('.stepper-incr');
            if (decr) decr.disabled = newQty <= 0;
            if (incr) incr.disabled = newQty >= maxStock;
        }

        // Siempre actualizar el hidden input con el valor final
        hiddenInput.value = newQty;

        // Feedback visual rápido
        // NOTA: EL submit button ya no existe en el estado Stepper, este feedback debe ir al +
        const submitBtn = form.querySelector('.stepper-incr');
        if (submitBtn) {
            submitBtn.innerHTML = newQty > 0 ? `+` : `<i class="bi bi-cart-plus"></i>`;
            setTimeout(() => {
                 if(newQty > 0) submitBtn.innerHTML = `+`;
                 else if (newQty === 0) submitBtn.innerHTML = `<i class="bi bi-cart-plus"></i>`;
            }, 500);
        }
    };

    // ... (El resto del código JS, incluyendo handleCartUpdate y stepperHandler, sigue igual)
    
// Finalizamos el bloque de código

    // --- Lógica de Envío AJAX Centralizada (Disparada por Stepper o Botón) ---
    
    /**
     * Envía la solicitud AJAX para actualizar/eliminar el carrito.
     */
    const handleCartUpdate = (form, cantidad) => {
        const productoCodigo = form.dataset.codigo;
        const csrfInput = form.querySelector('input[name="csrfmiddlewaretoken"]');
        const csrfToken = csrfInput ? csrfInput.value : getCookie('csrftoken') || '';

        const targetUrl = urlParaAgregar;
        if (!targetUrl) {
            showMessage('Error de configuración: No se encontró URL para el carrito.', 'error');
            return;
        }
        
        // Capturamos el valor original antes de la operación para revertir en caso de fallo
        const hiddenInput = form.querySelector('input[name="quantity"]');
        const originalQty = hiddenInput ? parseInt(hiddenInput.value) : 0;
        
        let finalCantidad = parseInt(cantidad, 10);
        if (finalCantidad < 0) finalCantidad = 0; 
        
        // UI Feedback: Determinar el botón visual a deshabilitar
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalBtnHtml = submitBtn ? submitBtn.innerHTML : null;
        
        const targetBtn = form.querySelector(finalCantidad === 0 ? '.stepper-decr' : '.stepper-incr') || submitBtn;
        
        if (targetBtn) {
            targetBtn.disabled = true;
            if (targetBtn !== submitBtn) {
                 targetBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
            }
        }
        
        fetch(targetUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                producto_codigo: productoCodigo,
                cantidad: finalCantidad 
            })
        })
        .then(res => res.json().catch(() => ({ status: 'error', message: 'Respuesta inválida o error 500' })))
        .then(data => {
            if (data && data.status === 'ok') {
                showMessage(data.message || (finalCantidad === 0 ? 'Eliminado del carrito' : 'Carrito actualizado'), 'success');
                
                const cartCount = document.getElementById('cart-item-count');
                if (cartCount && (data.total_items_carrito !== undefined)) cartCount.textContent = data.total_items_carrito;
                
                // Actualizar la UI de la tarjeta local
                updateCardDisplay(form, finalCantidad);

            } else {
                const msg = (data && data.message) ? data.message : 'Hubo un error en el servidor.';
                showMessage(msg, 'error');
                
                // 💡 CLAVE: Revertir la cantidad a la original si la operación falla
                updateCardDisplay(form, originalQty); 
                window.location.reload(); 
            }
        })
        .catch(error => {
            console.error('Error de red:', error);
            showMessage('Error de conexión con el servidor.', 'error');
            // Revertir a la cantidad original si hay error de red
            updateCardDisplay(form, originalQty); 
            window.location.reload();
        })
        .finally(() => {
            if (targetBtn) {
                 targetBtn.disabled = false;
                 if (targetBtn !== submitBtn) {
                     targetBtn.innerHTML = targetBtn.classList.contains('stepper-decr') ? '−' : '+';
                 }
            }
        });
    };

    // --- Funciones para re-adjuntar listeners y lógica del Stepper ---

    const stepperHandler = (e) => {
        const incrBtn = e.target.closest('.stepper-incr');
        const decrBtn = e.target.closest('.stepper-decr');
        if (!incrBtn && !decrBtn) return;
        
        const targetBtn = incrBtn || decrBtn;
        const form = targetBtn.closest('form[data-codigo]');
        if (!form) return;

        // Intentar leer la cantidad del SPAN dentro del display
        const display = form.querySelector('.qty-display');
        const qtySpan = display ? display.querySelector('span') : null;
        const hidden = form.querySelector('input[name="quantity"]');
        
        if (!hidden) return; // Hidden input siempre debe existir

        // Lógica: Si no hay span (es el botón Agregar), la cantidad actual es 0.
        let val = (qtySpan && parseInt(qtySpan.textContent.trim())) || parseInt(hidden.value) || 0;
        
        // Forzar el valor inicial a 0 si estamos en el estado AGREGAR simple
        if (form.querySelector('.stepper-decr') === null && incrBtn) {
            val = 0;
        }

        let newQty = val + (incrBtn ? 1 : -1);
        
        const max = parseInt(display?.dataset.max) || Infinity;
        
        // Aplicamos límites (0 para eliminar, maxStock para tope)
        if (newQty < 0) newQty = 0; 
        if (newQty > max) newQty = max;

        if (newQty === val) return;
        
        // Actualizar temporalmente la UI antes de AJAX
        if (qtySpan) qtySpan.textContent = newQty;
        if (hidden) hidden.value = newQty;
        
        // Llamar a la lógica AJAX para enviar el nuevo valor
        handleCartUpdate(form, newQty);
    };

    const submitHandler = (e) => {
         e.preventDefault();
         const form = e.target.closest('form[data-codigo]');
         const hidden = form.querySelector('input[name="quantity"]');
         const cantidad = hidden ? parseInt(hidden.value) : 1;
         
         handleCartUpdate(form, cantidad);
    };
    
    /**
     * Adjunta los listeners al nuevo DOM después de un re-renderizado.
     */
    const attachSubmitAndStepperListeners = (form) => {
        // Remover listeners anteriores para evitar duplicados si el form fue re-renderizado
        form.removeEventListener('submit', submitHandler);
        
        // Adjuntar el listener de submit
        form.addEventListener('submit', submitHandler);
    };


    // --- Inicialización y Binding de Eventos ---
    
    // Delegación global para botones +/- (para que funcione en elementos renderizados por JS)
    document.addEventListener('click', stepperHandler);

    // Inicialización de todas las tarjetas y binding de Submit
    document.querySelectorAll('form[data-codigo]').forEach(form => {
        const hidden = form.querySelector('input[name="quantity"]');
        const display = form.querySelector('.qty-display');
        
        if (!hidden) return;

        // 1. Asegurar que el display muestre el valor correcto inicialmente (si existe)
        if (display) {
            const qtySpan = display.querySelector('span');
            let initialVal = parseInt(hidden.value) || 0;
            if (qtySpan) qtySpan.textContent = initialVal;
            
            // 2. Deshabilitar botones al inicio
            const max = parseInt(display.dataset.max) || Infinity;
            const decr = form.querySelector('.stepper-decr');
            const incr = form.querySelector('.stepper-incr');
            if (decr) decr.disabled = initialVal <= 0;
            if (incr) incr.disabled = initialVal >= max;
        }

        // 3. Adjuntar el listener de submit
        attachSubmitAndStepperListeners(form);
    });

});
