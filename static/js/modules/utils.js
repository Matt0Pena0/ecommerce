export const CONFIG = {
    // Leemos los data-attributes del DOM de forma segura
    urlProductos: document.getElementById('productos-container')?.dataset.urlProductos || '/api/productos/',
    urlCarrito: '/api/carrito/agregar/',
    isSuperuser: document.getElementById('productos-container')?.dataset.isSuperuser === 'true'
};

/**
 * Normaliza un valor monetario a 2 decimales.
 *
 * La API es inconsistente por diseño de DRF:
 *  - `precio_unitario` es un DecimalField del modelo -> llega como string ("12.50")
 *  - `subtotal` y `total_dinero` son SerializerMethodField que devuelven Decimal,
 *    y el JSONEncoder de DRF los castea a float -> llegan como number (12.5)
 * Number() unifica ambos casos y toFixed(2) recupera el decimal perdido.
 */
export const formatMoney = (value) => {
    const n = Number(value);
    return Number.isFinite(n) ? n.toFixed(2) : '0.00';
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

export const debounce = (func, wait) => {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
};