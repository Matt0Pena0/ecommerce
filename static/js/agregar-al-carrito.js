document.addEventListener('DOMContentLoaded', function() {
  const urlParaAgregar = document.body.dataset.urlAgregarCarrito || null;

  // helpers
  const getCookie = (name) => {
    const matches = document.cookie.match(new RegExp('(?:^|; )' + name + '=([^;]*)'));
    return matches ? decodeURIComponent(matches[1]) : null;
  };
  const findFallbackUrl = () => {
    const f = document.querySelector('form[data-codigo][action]');
    return f ? f.getAttribute('action') : null;
  };

  // delegación global para botones +/-
  document.addEventListener('click', (e) => {
    const incrBtn = e.target.closest('.stepper-incr');
    const decrBtn = e.target.closest('.stepper-decr');

    if (!incrBtn && !decrBtn) return;

    const btn = incrBtn || decrBtn;
    const form = btn.closest('form[data-codigo]');
    if (!form) return;

    const display = form.querySelector('.qty-display');
    const hidden = form.querySelector('input[name="quantity"]');

    if (!display || !hidden) return;

    const min = parseInt(display.dataset.min) || 1;
    const max = parseInt(display.dataset.max) || Infinity;
    let val = parseInt(display.textContent.trim()) || parseInt(hidden.value) || min;

    val += incrBtn ? 1 : -1;
    if (val < min) val = min;
    if (val > max) val = max;

    display.textContent = val;
    hidden.value = val;

    // actualizar disabled si es necesario
    const decr = form.querySelector('.stepper-decr');
    const incr = form.querySelector('.stepper-incr');
    if (decr) decr.disabled = val <= min;
    if (incr) incr.disabled = val >= max;
  });

  // inicialización: fijar displays acorde al hidden o al stock
  document.querySelectorAll('form[data-codigo]').forEach(form => {
    const display = form.querySelector('.qty-display');
    const hidden = form.querySelector('input[name="quantity"]');
    if (!display || !hidden) return;

    const min = parseInt(display.dataset.min) || 1;
    const max = parseInt(display.dataset.max) || Infinity;
    let val = parseInt(hidden.value) || min;
    if (val < min) val = min;
    if (val > max) val = max;
    display.textContent = val;
    hidden.value = val;

    const decr = form.querySelector('.stepper-decr');
    const incr = form.querySelector('.stepper-incr');
    if (decr) decr.disabled = val <= min;
    if (incr) incr.disabled = val >= max;

    // si stock = 0, desactivar todo
    if (max <= 0) {
      if (decr) decr.disabled = true;
      if (incr) incr.disabled = true;
      const submitBtn = form.querySelector('button[type="submit"]');
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = 'Sin stock';
      }
    }
  });

  // manejo del submit por AJAX (por form)
  document.querySelectorAll('form[data-codigo]').forEach(form => {
    form.addEventListener('submit', function(event) {
      event.preventDefault();

      const productoCodigo = this.dataset.codigo;
      const cantidad = this.querySelector('input[name="quantity"]').value || 1;
      const csrfInput = this.querySelector('input[name="csrfmiddlewaretoken"]');
      const csrfToken = csrfInput ? csrfInput.value : getCookie('csrftoken') || '';

      const targetUrl = urlParaAgregar || findFallbackUrl();
      if (!targetUrl) {
        console.error('No se encontró URL para agregar al carrito.');
        return;
      }

      const submitBtn = this.querySelector('button[type="submit"]');
      const originalBtnHtml = submitBtn ? submitBtn.innerHTML : null;
      if (submitBtn) {
        submitBtn.disabled = true;
        // spinner pequeño
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
      }

      fetch(targetUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
          producto_codigo: productoCodigo,
          cantidad: parseInt(cantidad, 10)
        })
      })
      .then(res => res.json().catch(() => ({ status: 'error', message: 'Respuesta inválida' })))
      .then(data => {
        if (data && data.status === 'ok') {
          if (typeof showToast === 'function') showToast(data.message || 'Agregado', 'success');
          const cartCount = document.getElementById('cart-item-count');
          if (cartCount && (data.total_items_carrito !== undefined)) cartCount.textContent = data.total_items_carrito;
        } else {
          const msg = (data && data.message) ? data.message : 'Hubo un error';
          if (typeof showToast === 'function') showToast(msg, 'error'); else alert(msg);
        }
      })
      .catch(error => {
        console.error('Error de red:', error);
        if (typeof showToast === 'function') showToast('Error de conexión', 'error'); else alert('Error de conexión');
      })
      .finally(() => {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = originalBtnHtml || '🛒';
        }
      });
    });
  });

});
