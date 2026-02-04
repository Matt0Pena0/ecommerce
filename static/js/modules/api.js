import { CONFIG, getCookie } from './utils.js';


export const ApiService = {
    async getProductos(filtros = '') {
        const response = await fetch(`${CONFIG.urlProductos}${filtros}`);
        if (!response.ok) throw new Error('Error al cargar productos');
        return await response.json();
    },

    async getProducto(id) {
        const response = await fetch(`${CONFIG.urlProductos}${id}`);
        if (!response.ok) throw new Error(`Error HTTP: ${response.status}`);
        return await response.json();
    },


    async getMetadata() {
        const response = await fetch('/api/productos/metadata/');
        return await response.json();
    },

    async getCarritoStatus() {
        // Asumiendo que ya creaste este endpoint en DRF
        const response = await fetch('/api/carrito/status/');
        return await response.json();
    },

    async getCarritoDetalle() {
        const response = await fetch('/api/carrito/items_detalle/');
        if (!response.ok) throw new Error('No se pudo obtener el detalle del carrito');
        return await response.json();
    },

    async updateCarrito(productoId, cantidad) {
        const response = await fetch(CONFIG.urlCarrito, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                producto_id: productoId,
                cantidad: parseInt(cantidad)
            })
        });

        const data = await response.json();

        if (!response.ok) throw new Error(data.message || 'Error en servidor');
        return data;
    },

    async eliminarDelCarrito(productoId) {
        const response = await fetch(`/api/carrito/${productoId}/eliminar/`, {
            method: 'DELETE',
            headers: { 'X-CSRFToken': getCookie('csrftoken') }
        });
        return await response.json();
    },

    async finalizarCompra() {
        const response = await fetch('/api/carrito/finalizar/', {
            method: 'POST',
            headers: { 'X-CSRFToken': getCookie('csrftoken') }
        });
        return await response.json();
    }
};
