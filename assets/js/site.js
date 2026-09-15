document.documentElement.classList.add('js');

const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const menuButton = document.querySelector('.menu-button');
const siteNav = document.querySelector('.site-nav');
const marquee = document.querySelector('.signal-marquee');
const marqueeToggle = document.querySelector('[data-marquee-toggle]');

requestAnimationFrame(() => {
  document.documentElement.classList.add('is-ready');
});

function closeMenu({ restoreFocus = false } = {}) {
  if (!menuButton || !siteNav) return;

  menuButton.setAttribute('aria-expanded', 'false');
  siteNav.classList.remove('is-open');

  if (restoreFocus) menuButton.focus();
}

if (menuButton && siteNav) {
  menuButton.addEventListener('click', () => {
    const willOpen = menuButton.getAttribute('aria-expanded') !== 'true';
    menuButton.setAttribute('aria-expanded', String(willOpen));
    siteNav.classList.toggle('is-open', willOpen);
  });

  siteNav.addEventListener('click', (event) => {
    if (event.target.closest('a')) closeMenu();
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') closeMenu({ restoreFocus: true });
  });
}

if (marquee && marqueeToggle) {
  marqueeToggle.addEventListener('click', () => {
    const isPaused = marquee.classList.toggle('is-paused');
    marqueeToggle.setAttribute('aria-pressed', String(isPaused));
    marqueeToggle.textContent = isPaused ? 'Resume motion' : 'Pause motion';
  });
}

const revealItems = document.querySelectorAll('.reveal');

if ('IntersectionObserver' in window && revealItems.length && !reducedMotion.matches) {
  const revealObserver = new IntersectionObserver(
    (entries, observer) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;

        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      });
    },
    { threshold: 0.12 }
  );

  revealItems.forEach((item) => revealObserver.observe(item));
} else {
  revealItems.forEach((item) => item.classList.add('is-visible'));
}
