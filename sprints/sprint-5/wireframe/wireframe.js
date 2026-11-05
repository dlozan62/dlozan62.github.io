'use strict';

const input = document.querySelector('#campus');
input.addEventListener('input', () => {
  const query = input.value.trim().toLowerCase().replace(/\s+/g, ' ');
  const match = !query || ['university of texas at el paso', 'utep'].some(name => name.includes(query));
  document.querySelector('.campus').hidden = !match;
  document.querySelector('#empty').hidden = match;
});

const venues = {
  venue1: { name: 'Dining Option #1', open: true, item: '[Item name]' },
  venue2: { name: 'Dining Option #2', open: false, item: '[Item name]' },
  venue3: { name: 'Chick-fil-A', open: true, item: 'Chicken sandwich' },
};

document.querySelectorAll('[data-venue]').forEach(link => {
  link.addEventListener('click', () => {
    const venue = venues[link.dataset.venue];
    document.querySelector('#venue-title').textContent = `${venue.name} at University of Texas at El Paso`;
    document.querySelector('#venue-status').textContent = `${venue.open ? 'OPEN' : 'CLOSED'} · [opening] to [closing]`;
    document.querySelector('#closed-note').hidden = venue.open;
    document.querySelector('#first-item-name').textContent = venue.item;
    document.querySelectorAll('[data-stock]').forEach(stock => {
      stock.textContent = venue.open
        ? (stock.dataset.stock === 'available' ? 'In stock (example)' : 'Out of stock (example)')
        : 'Unconfirmed — venue closed';
    });
  });
});

const locationToggle = document.querySelector('#location-toggle');
locationToggle.addEventListener('click', () => {
  const unavailable = locationToggle.getAttribute('aria-pressed') !== 'true';
  locationToggle.setAttribute('aria-pressed', String(unavailable));
  locationToggle.textContent = unavailable ? 'Restore example location' : 'Preview location unavailable';
  document.querySelector('#location-message').hidden = !unavailable;
  document.querySelector('#example-location').hidden = unavailable;
});

// Move keyboard focus as well as the viewport when following a screen link.
document.querySelectorAll('a[href^="#"]').forEach(link => {
  link.addEventListener('click', () => {
    const target = document.querySelector(link.getAttribute('href'));
    if (!target) return;
    const heading = target.querySelector('h2') || target;
    heading.setAttribute('tabindex', '-1');
    heading.focus({ preventScroll: true });
  });
});
