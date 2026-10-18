/** Accessible, progressively enhanced navigation for the staging theme. */
(() => {
  'use strict';

  const normalizedPath = (path) => path.replace(/\/+$/, '') || '/';
  const currentPath = normalizedPath(window.location.pathname);
  document.querySelectorAll('.ak-nav a[href]').forEach((link) => {
    const destination = new URL(link.href, window.location.href);
    if (destination.origin === window.location.origin && normalizedPath(destination.pathname) === currentPath) {
      link.setAttribute('aria-current', 'page');
    } else {
      link.removeAttribute('aria-current');
    }
  });

  const menu = document.querySelector('.ak-menu');
  const nav = document.getElementById('ak-primary-nav');
  if (!menu || !nav) return;

  const setOpen = (open) => {
    menu.setAttribute('aria-expanded', String(open));
    nav.dataset.open = String(open);
  };
  document.body.classList.add('ak-js');
  menu.hidden = false;
  setOpen(false);

  menu.addEventListener('click', () => setOpen(menu.getAttribute('aria-expanded') !== 'true'));
  nav.addEventListener('click', (event) => {
    if (event.target.closest('a')) setOpen(false);
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') {
      setOpen(false);
      menu.focus();
    }
  });
  window.matchMedia('(max-width: 760px)').addEventListener('change', () => setOpen(false));
})();
