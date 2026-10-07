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

// Report contents work with both GitHub Pages and the hosted preview.
const main = document.getElementById('main-content');
const reportSections = main ? [...main.querySelectorAll('section[id]')].filter(section => section.querySelector('h2, h3')) : [];
if (main && reportSections.length >= 3 && !main.querySelector('.home-hero')) {
  const shell = document.createElement('div');
  shell.className = 'report-shell';
  const body = document.createElement('div');
  body.className = 'report-body';
  const sidebar = document.createElement('aside');
  sidebar.className = 'report-sidebar';
  const contents = document.createElement('details');
  const summary = document.createElement('summary');
  summary.textContent = 'On this page';
  const nav = document.createElement('nav');
  nav.setAttribute('aria-label', 'Report contents');
  const list = document.createElement('ol');
  const links = new Map();
  reportSections.forEach(section => {
    const heading = section.querySelector('h2, h3');
    const li = document.createElement('li');
    const a = document.createElement('a');
    a.href = '#' + section.id;
    a.textContent = heading.textContent;
    if (section.classList.contains('doc-part')) li.className = 'contents-group';
    li.append(a); list.append(li); links.set(section.id, a);
    a.addEventListener('click', () => {
      if (!window.matchMedia('(min-width: 1100px)').matches) contents.open = false;
    });
  });
  nav.append(list); contents.append(summary, nav); sidebar.append(contents);
  [...main.children].forEach(child => { if (!child.classList.contains('breadcrumb')) body.append(child); });
  shell.append(sidebar, body); main.append(shell);
  const desktop = window.matchMedia('(min-width: 1100px)');
  const syncContents = () => { contents.open = desktop.matches; };
  syncContents(); desktop.addEventListener('change', syncContents);
  const updateActive = () => {
    let active = reportSections[0];
    reportSections.forEach(section => { if (section.getBoundingClientRect().top <= 140) active = section; });
    links.forEach((link, id) => {
      if (id === active.id) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  };
  let scheduled = false;
  window.addEventListener('scroll', () => {
    if (scheduled) return;
    scheduled = true; requestAnimationFrame(() => { updateActive(); scheduled = false; });
  }, {passive: true});
  updateActive();
}

document.querySelectorAll('.charter-table-wrap').forEach((wrap, index) => {
  const caption = wrap.querySelector('caption');
  const hint = document.createElement('p');
  hint.className = 'table-scroll-hint';
  hint.id = 'table-scroll-hint-' + index;
  hint.textContent = 'Scroll horizontally to see the full table.';
  wrap.before(hint);
  wrap.setAttribute('role', 'region');
  wrap.setAttribute('aria-label', caption ? caption.textContent : 'Report table ' + (index + 1));
  const syncTable = () => {
    const overflow = wrap.scrollWidth > wrap.clientWidth + 2;
    hint.hidden = !overflow;
    if (overflow) { wrap.tabIndex = 0; wrap.setAttribute('aria-describedby', hint.id); }
    else { wrap.removeAttribute('tabindex'); wrap.removeAttribute('aria-describedby'); }
  };
  if ('ResizeObserver' in window) new ResizeObserver(syncTable).observe(wrap);
  syncTable();
});
