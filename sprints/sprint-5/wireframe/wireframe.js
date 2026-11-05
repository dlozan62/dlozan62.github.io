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

let selectedVenue = 'venue3';
const dietForm = document.querySelector('#diet-form');
const dietStyle = document.querySelector('#diet-style');
const stockOnly = document.querySelector('#in-stock-only');
const allergenNames = { milk: 'Milk', eggs: 'Eggs', fish: 'Fish', shellfish: 'Shellfish', 'tree-nuts': 'Tree nuts', peanuts: 'Peanuts', wheat: 'Wheat', soy: 'Soy', sesame: 'Sesame' };

function readFilters() {
  return {
    diet: dietStyle.value,
    avoid: Array.from(dietForm.querySelectorAll('input[name="avoid"]:checked'), field => field.value),
    inStock: stockOnly.checked,
  };
}

function describeFilters(filters) {
  const parts = [];
  if (filters.diet) parts.push(dietStyle.selectedOptions[0].textContent);
  if (filters.avoid.length) parts.push('Avoid: ' + filters.avoid.map(value => allergenNames[value]).join(', '));
  if (filters.inStock) parts.push('In-stock examples only');
  return parts.length ? parts.join(' · ') : 'All sample menu items shown';
}

function renderMenu(filters) {
  const venue = venues[selectedVenue];
  const menu = document.querySelector('.menu-list');
  menu.replaceChildren();
  const items = dietary.menus[selectedVenue].filter(item => dietary.matches(item, filters, venue.open));
  document.querySelector('#menu-empty').hidden = items.length > 0;
  document.querySelector('#menu-filter-note').textContent = `${describeFilters(filters)} · ${items.length} matching sample item${items.length === 1 ? '' : 's'}`;
  items.forEach(item => {
    const card = document.createElement('article');
    card.className = 'item diet-item';
    const heading = document.createElement('h4');
    heading.textContent = item.name;
    card.append(heading);
    const details = [
      ['Dietary labels', item.diets ? (item.diets.join(', ') || 'None listed') + ' (fictional example)' : 'Unknown — confirm with staff'],
      ['Allergens', item.allergens ? (item.allergens.map(value => allergenNames[value]).join(', ') || 'None declared in this fictional recipe') : 'Unknown — confirm with staff'],
      ['Ingredients', item.ingredients],
      ['Calories', 'Not provided'],
      ['Availability', !venue.open || item.available === null ? 'Unconfirmed — venue closed' : item.available ? 'In stock (example)' : 'Out of stock (example)'],
    ];
    details.forEach(([label, value]) => {
      const line = document.createElement('p');
      const title = document.createElement('strong');
      title.textContent = label + ': ';
      line.append(title, document.createTextNode(value));
      card.append(line);
    });
    const note = document.createElement('p');
    note.className = 'small';
    note.textContent = 'Example only. Cross-contact is not assessed. Confirm ingredients and preparation with dining staff.';
    card.append(note);
    menu.append(card);
  });
}

function refreshDietaryResults() {
  const filters = readFilters();
  document.querySelector('#diet-summary').textContent = describeFilters(filters);
  document.querySelectorAll('[data-match-count]').forEach(count => {
    const id = count.dataset.matchCount;
    const number = dietary.menus[id].filter(item => dietary.matches(item, filters, venues[id].open)).length;
    count.textContent = `${number} matching sample item${number === 1 ? '' : 's'}`;
  });
  renderMenu(filters);
}

dietForm.addEventListener('submit', event => event.preventDefault());
dietForm.addEventListener('change', refreshDietaryResults);
dietForm.addEventListener('reset', () => requestAnimationFrame(refreshDietaryResults));

document.querySelectorAll('[data-venue]').forEach(link => {
  link.addEventListener('click', () => {
    selectedVenue = link.dataset.venue;
    const venue = venues[selectedVenue];
    document.querySelector('#venue-title').textContent = `${venue.name} at University of Texas at El Paso`;
    document.querySelector('#venue-status').textContent = `${venue.open ? 'OPEN' : 'CLOSED'} · [opening] to [closing]`;
    document.querySelector('#closed-note').hidden = venue.open;
    renderMenu(readFilters());
  });
});
refreshDietaryResults();

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
    if (target.tagName === 'DETAILS') target.open = true;
    const heading = target.querySelector('h2') || target;
    heading.setAttribute('tabindex', '-1');
    heading.focus({ preventScroll: true });
  });
});

