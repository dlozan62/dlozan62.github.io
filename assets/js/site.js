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

// Fictional concept demo. All updates stay in this page; no data is submitted.
const demo = document.querySelector('.demo-shell');
if (demo) {
  const openFilter = document.getElementById('demo-open');
  const dietFilter = document.getElementById('demo-diet');
  const results = document.getElementById('demo-results');
  const staffButton = document.getElementById('demo-staff-button');
  const locations = [...demo.querySelectorAll('.demo-location')];
  const items = [...demo.querySelectorAll('.demo-items li')];
  const initialSold = items.map((item) => item.dataset.sold === 'true');
  const timestamps = locations.map((location) => location.querySelector('.demo-updated')?.textContent);
  let staffMode = false;

  demo.querySelector('.demo-filters').hidden = false;
  staffButton.hidden = false;

  const filter = (announcement = '') => {
    let locationCount = 0;
    let itemCount = 0;
    locations.forEach((location) => {
      const locationItems = [...location.querySelectorAll('.demo-items li')];
      locationItems.forEach((item) => {
        item.hidden = dietFilter.value !== 'all' && item.dataset.diet !== dietFilter.value;
      });
      const visibleItems = locationItems.filter((item) => !item.hidden);
      location.hidden = (openFilter.checked && location.dataset.open !== 'true') ||
        (dietFilter.value !== 'all' && visibleItems.length === 0);
      if (!location.hidden) {
        locationCount++;
        itemCount += visibleItems.length;
      }
    });
    results.textContent = `${announcement}${locationCount} sample location${locationCount === 1 ? '' : 's'} · ${itemCount} matching menu item${itemCount === 1 ? '' : 's'}.`;
  };
  const updateItem = (item, sold) => {
    item.dataset.sold = String(sold);
    const status = item.querySelector('.item-status');
    status.textContent = sold ? 'Sold out' : 'Available';
    status.classList.toggle('status--sold', sold);
    status.classList.toggle('status--open', !sold);
    const button = item.querySelector('.staff-toggle');
    const action = sold ? 'available' : 'sold out';
    button.textContent = `Mark ${action}`;
    button.setAttribute('aria-label', `Mark ${item.querySelector('strong').textContent} ${action}`);
  };
  openFilter.addEventListener('change', () => filter());
  dietFilter.addEventListener('change', () => filter());
  staffButton.addEventListener('click', () => {
    staffMode = !staffMode;
    staffButton.setAttribute('aria-pressed', String(staffMode));
    staffButton.textContent = staffMode ? 'Hide staff controls' : 'Show staff controls';
    demo.querySelectorAll('.staff-toggle').forEach((button) => { button.hidden = !staffMode; });
    filter(`Staff controls ${staffMode ? 'shown' : 'hidden'}. `);
  });
  items.forEach((item) => {
    item.querySelector('.staff-toggle').addEventListener('click', () => {
      const sold = item.dataset.sold !== 'true';
      updateItem(item, sold);
      item.closest('.demo-location').querySelector('.demo-updated').textContent = 'Last updated: just now (simulated staff update)';
      filter(`${item.querySelector('strong').textContent} marked ${sold ? 'sold out' : 'available'}. `);
    });
  });
  document.getElementById('demo-reset').addEventListener('click', () => {
    openFilter.checked = false;
    dietFilter.value = 'all';
    staffMode = false;
    staffButton.setAttribute('aria-pressed', 'false');
    staffButton.textContent = 'Show staff controls';
    items.forEach((item, index) => {
      updateItem(item, initialSold[index]);
      item.querySelector('.staff-toggle').hidden = true;
    });
    locations.forEach((location, index) => {
      const timestamp = location.querySelector('.demo-updated');
      if (timestamp) timestamp.textContent = timestamps[index];
    });
    filter('Demo reset. ');
  });
  filter();
}
