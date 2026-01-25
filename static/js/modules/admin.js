import { getCookie } from './utils.js';
import { showMessage } from '../toast.js';
import { ApiService } from './api.js';
import { UIRenderer } from './ui.js';


export const initProductModal = () => {
    const modalEl = document.getElementById('productModal');
    if (!modalEl) return;

    const modal = new bootstrap.Modal(modalEl);
    const form = document.getElementById('productForm');
    const title = document.getElementById('modal-title-text');
    const saveBtn = document.getElementById('btn-save-product');

    // 1. Escuchar apertura del modal (Create vs Edit)
    modalEl.addEventListener('show.bs.modal', async (event) => {
        const btn = event.relatedTarget;
        const productId = btn.dataset.productId; // Si tiene ID, es editar
        
        // Limpiar errores previos y resetear form
        form.reset();
        document.getElementById('prod-id').value = '';

        // Poblar Selects (Usando la metadata que ya cargó la App, o pidiéndola de nuevo)
        // Truco: Podemos guardar la metadata en App.state o pedirla rápido aquí
        try {
            const metadata = await ApiService.getMetadata();

            UIRenderer.populateSelect('prod-marca', metadata.marcas, 'Seleccionar...');
            UIRenderer.populateSelect('prod-categoria', metadata.categorias, 'Seleccionar...');
            UIRenderer.populateSelect('prod-gondola', metadata.gondolas, 'Seleccionar...');
            UIRenderer.populateSelect('prod-unidad-medida', metadata.unidades, 'Seleccionar...');

        } catch (e) { console.error("Error cargando selects", e); }

        if (productId) {
            // MODO EDICIÓN
            title.textContent = "Editar Producto";
            document.getElementById('prod-id').value = productId;
            
            // Cargar datos actuales del producto
            try {
                // Petición GET al detalle para tener todos los datos frescos
                const product = await ApiService.getProducto(productId);
                
                // Llenar campos
                document.getElementById('prod-nombre').value = product.nombre;
                document.getElementById('prod-precio').value = product.precio_unitario;
                document.getElementById('prod-stock').value = product.stock;
                document.getElementById('prod-codigo').value = product.codigo_str || '';
                document.getElementById('prod-descripcion').value = product.descripcion || '';
                
                // Selects usando ids de serializer
                if(product.marca) document.getElementById('prod-marca').value = product.marca;
                if(product.categoria) document.getElementById('prod-categoria').value = product.categoria;
                if(product.gondola) document.getElementById('prod-gondola').value = product.gondola;
                if(product.unidad_medida) document.getElementById('prod-unidad-medida').value = product.unidad_medida;

            } catch (error) {
                console.log(error);
                showMessage("Error cargando datos del producto", "error");
                modal.hide();
            }

        } else {
            // MODO CREAR
            title.textContent = "Nuevo Producto";
        }
    });

    // 2. Manejar Guardado
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const productId = document.getElementById('prod-id').value;
        const isEdit = !!productId;
        const url = isEdit ? `/api/productos/${productId}/` : '/api/productos/';
        const method = isEdit ? 'PATCH' : 'POST';

        // Preparamos datos (FormData es necesario para subir imágenes)
        const formData = new FormData(form);

        // Feedback visual
        saveBtn.disabled = true;
        saveBtn.querySelector('.spinner-border').classList.remove('d-none');

        try {
            const response = await fetch(url, {
                method: method,
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    // NO poner 'Content-Type': 'application/json' cuando usas FormData,
                    // el navegador lo pone solo con el boundary correcto.
                },
                body: formData
            });

            if (response.ok) {
                showMessage(isEdit ? 'Producto actualizado' : 'Producto creado', 'success');
                modal.hide();
                // RECARGAR CATÁLOGO (Idealmente llamar a App.loadCatalog())
                // Una forma rápida es disparar un evento custom o recargar la página
                // window.location.reload(); // Opcional temporal
                document.dispatchEvent(new Event('catalog:refresh')); 
            } else {
                const errData = await response.json();
                console.error(errData);
                showMessage('Error al guardar. Verifica los datos.', 'error');
            }
        } catch (error) {
            console.error(error);
            showMessage('Error de conexión', 'error');
        } finally {
            saveBtn.disabled = false;
            saveBtn.querySelector('.spinner-border').classList.add('d-none');
        }
    });
};


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
                method: 'DELETE',
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