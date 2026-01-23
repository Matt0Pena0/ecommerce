export const CONFIG = {
    // Leemos los data-attributes del DOM de forma segura
    urlProductos: document.getElementById('productos-container')?.dataset.urlProductos || '/api/productos/',
    urlCarrito: '/api/carrito/agregar/',
    isSuperuser: document.getElementById('productos-container')?.dataset.isSuperuser === 'true'
};

export const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

// Wrapper simple para tus Toasts
export const showMessage = (msg, type = 'success') => {
    // Asumiendo que showToast es global o importado de otro lado
    if (window.showToast) {
        window.showToast(msg, type);
    } else {
        console.log(`[${type.toUpperCase()}]: ${msg}`);
    }
};
