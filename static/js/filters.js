document.querySelectorAll('.option').forEach(option => {
    option.addEventListener('click', () => {
        const filter = option.closest('.filter');
        const trigger = filter.querySelector('.select-trigger');
        trigger.textContent = option.textContent;

        // Crear o actualizar input hidden
        let hidden = filter.querySelector('input[type="hidden"]');
        if (!hidden) {
            hidden = document.createElement('input');
            hidden.type = 'hidden';
            hidden.name = filter.dataset.name;
            filter.appendChild(hidden);
        }
        hidden.value = option.dataset.value;

        // Cerrar el acordeón
        filter.querySelector('.filter-toggle').checked = false;
    });
});

const toggleBtn = document.querySelector('.filters-toggle');
const filtersPanel = document.querySelector('.filters');

toggleBtn.addEventListener('click', () => {
  filtersPanel.classList.toggle('open');
});