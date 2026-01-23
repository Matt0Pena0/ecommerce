// static/js/modules/admin.js
import { getCookie, showMessage } from './utils.js';

export const initDeleteModal = () => {
    const confirmDeleteModalEl = document.getElementById('confirmDeleteModal');
    const deleteForm = document.getElementById('deleteForm');
    const productNameEl = document.getElementById('productName');

    // Si el modal no existe en el HTML actual, no hacemos nada (evita errores)
    if (!confirmDeleteModalEl || !deleteForm) return;

    let productCardToDelete = null;

    // 1. Interceptar la apertura del modal
    // Bootstrap dispara este evento sobre el modal, pero nos dice qué botón lo abrió (relatedTarget)
    confirmDeleteModalEl.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget; // El botón <button> o <a> que clickeaste
        
        if (!button) return;

        // Extraemos datos
        const productName = button.dataset.productName;
        const deleteUrl = button.dataset.deleteUrl;
        
        // Guardamos referencia a la tarjeta completa (.col) para borrarla luego
        productCardToDelete = button.closest('.col'); 

        // Actualizamos UI del modal
        if (productNameEl) productNameEl.textContent = `"${productName}"`;
        deleteForm.setAttribute('action', deleteUrl);
    });

    // 2. Manejar el envío del formulario (Confirmar Borrado)
    deleteForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const url = this.getAttribute('action');
        // Usamos tu utilidad getCookie para consistencia
        const csrfToken = getCookie('csrftoken');
        const submitBtn = this.querySelector('button[type="submit"]');

        // Feedback visual en el botón de confirmar
        const originalBtnText = submitBtn.innerHTML;
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Borrando...';

        try {
            const response = await fetch(url, {
                method: 'POST', // Mantenemos POST según tu vista actual
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                // 1. Eliminar visualmente
                if (productCardToDelete) {
                    productCardToDelete.remove();
                }

                // 2. Cerrar modal
                // Necesitamos la instancia de Bootstrap para cerrarlo por JS
                const modalInstance = bootstrap.Modal.getInstance(confirmDeleteModalEl);
                modalInstance.hide();

                // 3. Feedback Global
                showMessage('Producto eliminado correctamente', 'success');
            } else {
                showMessage('Error al eliminar el producto', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            showMessage('Error de conexión', 'error');
        } finally {
            // Restaurar botón del modal
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalBtnText;
        }
    });
};