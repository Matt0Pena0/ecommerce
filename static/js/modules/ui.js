import { CONFIG } from './utils.js';


export const UIRenderer = {
    populateSelect(selectId, data, placeholder) {
        const select = document.getElementById(selectId);
        if (!select) return;
        select.innerHTML = `<option value="">${placeholder}</option>` + 
            data.map(item => `<option value="${item.id}">${item.nombre}</option>`).join('');
    },

    getControlsHTML(qty, maxStock) {
        const isInCart = qty > 0;
        
        const isMobile = window.innerWidth < 768;

        const btnSizeClass = isMobile ? 'btn-xs' : 'btn btn-sm';

        if (isInCart) {
            return `
                <div class="btn-stepper d-flex align-items-center m-1" role="group">
                    <button type="button" class="${btnSizeClass} bg-primary-subtle stepper-decr" ${qty <= 0 ? 'disabled' : ''}>
                        <i class="bi bi-dash-square-fill"></i>
                    </button>
                    <div class="qty-display mx-2 text-center" data-min="0" data-max="${maxStock}">
                        <span class="fw-semibold">${qty}</span>
                    </div>
                    <button type="button" class="${btnSizeClass} bg-primary-subtle stepper-incr" ${qty >= maxStock ? 'disabled' : ''}>
                        <i class="bi bi-plus-square-fill"></i>
                    </button>
                </div>`;
        }
        return `
            <div class="btn-stepper d-flex align-items-center m-1" role="group">
                <button type="button" class="${btnSizeClass} btn-primary stepper-incr">
                    <i class="bi bi-plus-square-fill"></i>
                </button>
            </div>`;
    },

    getProductCardHTML(p, qtyInCart = 0) {
        const maxStock = p.stock || 100;
        
        return `
            <div class="col g-1 g-sm-1 g-md-2 g-xl-4">
                <div class="card d-flex flex-column shadow-sm p-1 p-md-2 m-0" >
                    <div class="d-flex justify-content-center align-items-start" style="height: 80px;">
                        <img src="${p.img || '/static/img/producto.png'}" class="card-img-top w-auto img-fluid" style="max-height: 80px; object-fit:contain;">
                    </div>
                    <div class="card-body d-flex flex-column px-2 pt-1 pb-0">
                        <div class="my-0" style="min-height: 4rem;">
                            <p class="card-title my-0 text-truncate-2" title="${p.nombre}">${p.nombre}</p>
                            <p class="text-muted text-truncate-2">${p.marca_nombre || ''}</p>
                        </div>
                        <div class="align-items-center mx-auto mt-2" style="height: 1.5em;">
                            <span class="fw-bold">$${p.precio_unitario}</span>
                        </div>
                        
                        <form class="add-to-cart-form d-flex flex-column m-0 align-items-center" data-id="${p.id}">
                            <input type="hidden" name="quantity" value="${qtyInCart}">
                            <div class="action-wrapper w-100 d-flex flex-column align-items-center justify-content-center">
                                ${this.getControlsHTML(qtyInCart, maxStock)}
                            </div>
                        </form>

                        ${CONFIG.isSuperuser ? this.getAdminControls(p) : ''}
                    </div>
                </div>
            </div>`;
    },

    getAdminControls(p) {
            // Generamos la URL de borrado. 
            const deleteUrl = `/productos/eliminar/${p.id}/api`; 

            return `
                <div class="card-footer d-flex justify-content-between gap-2 p-0 mt-2">
                    <button data-bs-toggle="modal" data-bs-target="#productModal" data-product-id="${p.id}"
                            class="btn btn-outline-secondary btn-sm flex-grow-1">
                        <i class="bi bi-pencil-square"></i>
                        <span class="d-none d-md-inline">Editar</span>
                    </button>
                    
                    <button type="button" 
                            class="btn btn-outline-danger btn-sm" 
                            data-bs-toggle="modal" 
                            data-bs-target="#confirmDeleteModal"
                            data-product-name="${p.nombre}"
                            data-delete-url="${deleteUrl}">
                        <i class="bi bi-trash3-fill"></i>
                    </button>
                </div>`;
        },

    // Optimización visual: Solo cambia lo necesario en el DOM
    updateCardState(form, newQty) {
        const wrapper = form.querySelector('.action-wrapper');
        const hiddenInput = form.querySelector('input[name="quantity"]');
        const display = form.querySelector('.qty-display');
        const maxStock = parseInt(display?.dataset.max) || 100;

        if (hiddenInput) hiddenInput.value = newQty;

        const isStepperVisible = wrapper.querySelector('.qty-display') !== null;
        const shouldBeStepper = newQty > 0;

        if (isStepperVisible !== shouldBeStepper) {
            wrapper.innerHTML = this.getControlsHTML(newQty, maxStock);
        } else if (shouldBeStepper) {
            wrapper.querySelector('.qty-display span').textContent = newQty;
            const decr = wrapper.querySelector('.stepper-decr');
            const incr = wrapper.querySelector('.stepper-incr');
            if(decr) decr.disabled = newQty <= 0;
            if(incr) incr.disabled = newQty >= maxStock;
        }
    },

    getCartRowHTML(item) {
        const p = item.producto; // Gracias al nuevo serializer
        const subtotal = item.subtotal; 

        return `
            <tr data-producto-id="${p.id}">
                <td class="fw-bold text-primary">${p.nombre}</td>
                
                <td>${p.marca_nombre || '-'}</td>
                
                <td>${p.unidad_nombre || 'Unid.'}</td>
                
                <td title="${p.descripcion || ''}" class="text-truncate" style="max-width: 150px;">
                ${p.descripcion || '-'}
                </td>
                
                <td><span class="badge text-primary-emphasis text-dark border">${p.stock}</span></td>
                
                <td>
                <div class="input-group input-group-sm" style="width: 120px;">
                <button class="btn btn-outline-secondary stepper-decr" type="button">-</button>
                <input type="text" class="form-control text-center qty-display" value="${item.cantidad}" readonly>
                <button class="btn btn-outline-secondary stepper-incr" type="button">+</button>
                </div>
                </td>
                
                <td>$${p.precio_unitario}</td>
                
                <td class="fw-bold">$${subtotal}</td>
                
                <td>
                    <button type="button" 
                            class="btn btn-danger btn-sm btn-eliminar-item" 
                            title="Eliminar del carrito">
                        <i class="bi bi-trash"></i>
                    </button>
                </td>
            </tr>
        `;
    }
};