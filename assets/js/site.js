document.documentElement.classList.add('js');

const menuButton = document.querySelector('.menu-button');
const siteNav = document.querySelector('.site-nav');

if (menuButton && siteNav) {
  function closeMenu(restoreFocus = false) {
    menuButton.setAttribute('aria-expanded', 'false');
    siteNav.classList.remove('is-open');
    if (restoreFocus) menuButton.focus();
  }

  menuButton.addEventListener('click', () => {
    const willOpen = menuButton.getAttribute('aria-expanded') !== 'true';
    menuButton.setAttribute('aria-expanded', String(willOpen));
    siteNav.classList.toggle('is-open', willOpen);
  });

  siteNav.addEventListener('click', (event) => {
    if (event.target.closest('a')) closeMenu();
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
      closeMenu(true);
    }
  });
}
