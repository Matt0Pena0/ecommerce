/**
 * Crea y muestra un Toast de Bootstrap 5 de forma dinámica.
 * @param {string} msg - El mensaje a mostrar.
 * @param {string} type - 'success', 'error', 'info'.
 */
export const showMessage = (msg, type = 'success') => {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const bgClass = type === 'success' ? 'bg-success' : (type === 'error' ? 'bg-danger' : 'bg-info');
    const icon = type === 'success' ? 'bi-check-circle' : 'bi-exclamation-triangle';

    const toastHtml = `
        <div class="toast align-items-center text-white ${bgClass} border-0" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="bi ${icon} me-2"></i> ${msg}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;

    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = toastHtml;
    const toastElement = tempDiv.firstElementChild;
    container.appendChild(toastElement);

    // Inicialización manual con la API de Bootstrap
    const bsToast = new bootstrap.Toast(toastElement, { delay: 3000 });
    bsToast.show();

    // Limpieza del DOM al ocultarse
    toastElement.addEventListener('hidden.bs.toast', () => toastElement.remove());
};

// Si otros archivos (como utils.js) necesitan usarlo, 
// asegúrate de que importen este archivo específicamente.