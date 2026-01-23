// static/js/modules/toast.js

/**
 * Muestra un mensaje flotante (Toast) usando Bootstrap 5
 * @param {string} message - El mensaje a mostrar
 * @param {string} type - 'success' (verde/azul) o 'error' (rojo)
 */
export function showToast(message, type = 'success') {
    // 1. Definir el color según el tipo
    // Usamos 'text-bg-danger' para error y 'text-bg-primary' (o success) para éxito
    const bgClass = type === 'error' ? 'text-bg-danger' : 'text-bg-primary';

    // 2. Crear el contenedor
    const toastEl = document.createElement('div');
    // Agregamos las clases dinámicas
    toastEl.className = `toast align-items-center ${bgClass} border-0 position-fixed bottom-0 end-0 m-3`;
    toastEl.setAttribute('role', 'alert');
    toastEl.setAttribute('aria-live', 'assertive');
    toastEl.setAttribute('aria-atomic', 'true');
    // Importante: z-index alto para que se vea sobre todo
    toastEl.style.zIndex = '1050'; 

    // 3. Crear el cuerpo (Header + Body + Close Button)
    const body = document.createElement('div');
    body.className = 'd-flex';
    body.innerHTML = `
        <div class="toast-body">
            ${message}
        </div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
    `;

    toastEl.appendChild(body);
    document.body.appendChild(toastEl);

    // 4. Inicializar y Mostrar (Verificamos que Bootstrap exista)
    if (window.bootstrap) {
        const bsToast = new window.bootstrap.Toast(toastEl, { delay: 3000 });
        bsToast.show();

        // 5. Limpieza automática del DOM al ocultarse
        toastEl.addEventListener('hidden.bs.toast', () => {
            toastEl.remove();
        });
    } else {
        console.error('Bootstrap no está cargado. No se puede mostrar el Toast.');
        alert(message); // Fallback por si falla Bootstrap
    }
}