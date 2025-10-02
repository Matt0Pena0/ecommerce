// static/js/toast.js
export function showToast(message) {
    const toastEl = document.createElement('div');
    toastEl.className = 'toast align-items-center text-bg-primary border-0 show position-fixed bottom-0 end-0 m-3';
    toastEl.setAttribute('role', 'alert');
    toastEl.setAttribute('aria-live', 'assertive');
    toastEl.setAttribute('aria-atomic', 'true');

    const body = document.createElement('div');
    body.className = 'd-flex';
    body.innerHTML = `
        <div class="toast-body">${message}</div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
    `;

    toastEl.appendChild(body);
    document.body.appendChild(toastEl);

    const bsToast = new bootstrap.Toast(toastEl, { delay: 3000 });
    bsToast.show();

    toastEl.addEventListener('hidden.bs.toast', () => {
        toastEl.remove();
    });
}
