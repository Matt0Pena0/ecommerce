document.addEventListener('DOMContentLoaded', function() {
    // 1. Leemos la URL desde el data-attribute del body
    const urlParaAgregar = document.body.dataset.urlAgregarCarrito;

    const forms = document.querySelectorAll('.add-to-cart-form');

    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault();

            // 2. Obtenemos los datos del formulario específico que se envió
            const productoCodigo = this.dataset.codigo;
            const cantidadInput = this.querySelector('.quantity'); // Busca el input dentro de este form
            const cantidad = cantidadInput.value;
            const csrfToken = this.querySelector('input[name="csrfmiddlewaretoken"]').value;

            // 3. Enviamos la petición Fetch a la API
            fetch(urlParaAgregar, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify({
                    producto_codigo: productoCodigo,
                    cantidad: cantidad
                })
            })
            .then(response => response.json())
            .then(data => {
                // 4. Mostramos una notificación y actualizamos la UI
                if (data.status === 'ok') {
                    showToast(data.message, 'success');
                    // Actualiza el contador del carrito en la navbar
                    const cartCountElement = document.getElementById('cart-item-count');
                    if(cartCountElement) {
                        cartCountElement.textContent = data.total_items_carrito;
                    }
                } else {
                    showToast(data.message || 'Hubo un error', 'error');
                }
            })
            .catch(error => {
                console.error('Error de red:', error);
                showToast('Error de conexión.', 'error');
            });
        });
    });
});
