/* Progressive enhancements. Every page remains readable without JavaScript. */
'use strict';

document.documentElement.classList.add('js');

const menuButton = document.querySelector('.menu-button');
const siteNav = document.querySelector('.site-nav');

if (menuButton && siteNav) {
  const closeMenu = (restoreFocus = false) => {
    menuButton.setAttribute('aria-expanded', 'false');
    siteNav.classList.remove('is-open');
    if (restoreFocus) menuButton.focus();
  };

  menuButton.addEventListener('click', () => {
    const open = menuButton.getAttribute('aria-expanded') !== 'true';
    menuButton.setAttribute('aria-expanded', String(open));
    siteNav.classList.toggle('is-open', open);
  });

  siteNav.addEventListener('click', (event) => {
    if (event.target.closest('a')) closeMenu();
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
      closeMenu(true);
    }
  });

  const desktop = window.matchMedia('(min-width: 761px)');
  desktop.addEventListener('change', () => closeMenu());
}

// Keep report tables keyboard-accessible only when they need horizontal scrolling.
const tableRegions = [];
document.querySelectorAll('.charter-table-wrap').forEach((region, index) => {
  const caption = region.querySelector('caption');
  region.setAttribute('role', 'region');
  if (!region.hasAttribute('aria-label')) {
    region.setAttribute('aria-label', caption ? caption.textContent.trim() : `Report table ${index + 1}`);
  }

  const hint = document.createElement('p');
  hint.className = 'table-scroll-hint';
  hint.id = `table-hint-${index + 1}`;
  hint.textContent = 'Scroll horizontally to view the full table.';
  hint.hidden = true;
  region.before(hint);

  const refresh = () => {
    const scrolls = region.scrollWidth > region.clientWidth + 2;
    hint.hidden = !scrolls;
    if (scrolls) {
      region.tabIndex = 0;
      region.setAttribute('aria-describedby', hint.id);
    } else {
      region.removeAttribute('tabindex');
      region.removeAttribute('aria-describedby');
    }
  };
  tableRegions.push(refresh);
  if ('ResizeObserver' in window) new ResizeObserver(refresh).observe(region);
  refresh();
});
window.addEventListener('load', () => tableRegions.forEach((refresh) => refresh()));

// Highlight section links without changing the report's layout.
const sectionLinks = [...document.querySelectorAll('.on-page-nav a[href^="#"]')];
const sections = sectionLinks.map((link) => ({
  link,
  section: document.getElementById(decodeURIComponent(link.hash.slice(1))),
})).filter((item) => item.section);

if (sections.length) {
  const highlight = () => {
    let active = null;
    sections.forEach((item) => {
      if (item.section.getBoundingClientRect().top <= 140) active = item;
    });
    sections.forEach((item) => {
      if (item === active) item.link.setAttribute('aria-current', 'location');
      else item.link.removeAttribute('aria-current');
    });
  };
  let scheduled = false;
  window.addEventListener('scroll', () => {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(() => {
      highlight();
      scheduled = false;
    });
  }, { passive: true });
  highlight();
}
