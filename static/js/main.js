// static/js/main.js

// Importamos inicializadores globales si los tienes
// import { initClipboardListeners } from './modules/clipboard.js'; 

const AppGlobal = {
    initBootstrapComponents() {
        // Inicializa todos los tooltips (Tu código original)
        const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));

        // Inicializa todos los popovers (Tu código original)
        const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
        [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl));
    },

    init() {
        console.log('Sistema Global Iniciado 🚀');
        
        // 1. Componentes visuales de Bootstrap
        this.initBootstrapComponents();

        // 2. Otros módulos globales (descomentar si usas clipboard)
        // initClipboardListeners();
    }
};

// Punto de entrada único
document.addEventListener("DOMContentLoaded", () => {
    AppGlobal.init();
});