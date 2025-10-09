document.addEventListener('DOMContentLoaded', function () {
    const confirmDeleteModal = document.getElementById('confirmDeleteModal');
    const deleteForm = document.getElementById('deleteForm');
    const productNameEl = document.getElementById('productName');

    let productCardToDelete = null;

    // 1. Cuando el modal está a punto de mostrarse...
    confirmDeleteModal.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget; // Botón que activó el modal
        
        // Extraemos la info del botón
        const productName = button.getAttribute('data-product-name');
        const deleteUrl = button.getAttribute('data-delete-url');
        productCardToDelete = button.closest('.col'); // Guardamos la tarjeta para borrarla luego

        // Actualizamos el contenido del modal
        productNameEl.textContent = `"${productName}"`;
        deleteForm.setAttribute('action', deleteUrl);
    });

    // 2. Cuando se envía el formulario del modal...
    deleteForm.addEventListener('submit', function (event) {
        event.preventDefault(); // ¡Prevenimos la recarga de la página!

        const url = this.getAttribute('action');
        const csrfToken = this.querySelector('input[name="csrfmiddlewaretoken"]').value;

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.ok) {
                // Si la eliminación fue exitosa en el backend...
                productCardToDelete.remove(); // Eliminamos la tarjeta del producto de la vista
                bootstrap.Modal.getInstance(confirmDeleteModal).hide(); // Cerramos el modal
                // Opcional: Mostrar un toast de éxito
                // showToast('Producto eliminado con éxito', 'success');
            } else {
                // Manejar error
                alert('Hubo un error al eliminar el producto.');
                bootstrap.Modal.getInstance(confirmDeleteModal).hide();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Hubo un error de red.');
        });
    });

    confirmDeleteModal.addEventListener('hide.bs.modal', function (event) {
        // Busca el botón que originalmente abrió el modal
        const triggerButton = event.relatedTarget;

        // Si el modal se cerró con un botón (y no de otra forma),
        // devuelve el foco a ese botón para una mejor experiencia.
        if (triggerButton && triggerButton.focus) {
            triggerButton.focus();
        }
        });

});
