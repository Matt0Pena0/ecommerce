
function showToast(message, type = 'info') {
    // Verifica si ya existe el contenedor de toasts
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.style.position = 'fixed';
        container.style.top = '20px';
        container.style.right = '20px';
        container.style.zIndex = '9999';
        container.style.display = 'flex';
        container.style.flexDirection = 'column';
        container.style.gap = '10px';
        document.body.appendChild(container);
    }

    // Crea el toast individual
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;

    // Estilo básico inline (puedes moverlo a CSS luego)
    toast.style.padding = '10px 15px';
    toast.style.borderRadius = '6px';
    toast.style.boxShadow = '0 2px 6px rgba(0,0,0,0.2)';
    toast.style.color = 'white';
    toast.style.fontSize = '14px';
    toast.style.backgroundColor = {
        'info': '#2d9cdb',
        'success': '#27ae60',
        'error': '#e74c3c',
        'warning': '#f39c12'
    }[type] || '#333';

    // Agrega el toast al contenedor
    container.appendChild(toast);

    // Remueve luego de 3 segundos
    setTimeout(() => {
        toast.remove();
        // Si no quedan más, eliminamos el contenedor
        if (container.childElementCount === 0) {
            container.remove();
        }
    }, 3000);
}
