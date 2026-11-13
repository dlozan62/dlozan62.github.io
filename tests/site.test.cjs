'use strict';
const { test } = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, '../assets/js/site.js'), 'utf8');

function runSite({ hash = '', elements = {}, entries = [], search = null, groups = [] } = {}) {
  const events = new Map();
  const window = {
    location: { hash },
    addEventListener(name, callback) { events.set(name, callback); },
  };
  const document = {
    documentElement: { classList: { add() {} } },
    querySelector(selector) { return selector === '.document-search' ? search : null; },
    querySelectorAll(selector) {
      if (selector === '.document-group') return groups;
      return selector === 'details:not([open])' ? entries.filter(entry => !entry.open) : [];
    },
    getElementById(id) { return elements[id] || null; },
  };
  vm.runInNewContext(source, { window, document, requestAnimationFrame: callback => callback() });
  return { window, events };
}

test('a direct link opens both the member entry and its closed parent', () => {
  const parent = { tagName: 'DETAILS', open: false, parentElement: null };
  const member = { tagName: 'DETAILS', open: false, parentElement: parent };
  let scrolled = 0;
  const target = { tagName: 'H3', parentElement: member, scrollIntoView() { scrolled++; } };
  runSite({ hash: '#member%20notes', elements: { 'member notes': target } });
  assert.equal(parent.open, true);
  assert.equal(member.open, true);
  assert.equal(scrolled, 1);
});

test('hash navigation reveals a previously closed entry', () => {
  const target = { tagName: 'DETAILS', open: false, parentElement: null, scrollIntoView() {} };
  const { window, events } = runSite({ elements: { memo: target } });
  window.location.hash = '#memo';
  events.get('hashchange')();
  assert.equal(target.open, true);
});

test('missing and malformed anchors leave the page usable', () => {
  assert.doesNotThrow(() => runSite({ hash: '#missing' }));
  assert.doesNotThrow(() => runSite({ hash: '#%broken' }));
});

test('printing includes closed answers and restores the reader’s existing entries', () => {
  const open = { open: true };
  const closed = { open: false };
  const { events } = runSite({ entries: [open, closed] });
  events.get('beforeprint')();
  assert.equal(open.open, true);
  assert.equal(closed.open, true);
  events.get('afterprint')();
  assert.equal(open.open, true);
  assert.equal(closed.open, false);
});


test('document search matches sprint and title, handles no results, and clears', () => {
  const inputEvents = new Map();
  const clearEvents = new Map();
  let focused = false;
  const input = { value: '', addEventListener: (name, fn) => inputEvents.set(name, fn), focus: () => { focused = true; } };
  const clear = { addEventListener: (name, fn) => clearEvents.set(name, fn) };
  const count = { textContent: '' };
  const search = { hidden: true };
  const makeGroup = (sprint, titles) => ({
    hidden: false,
    rows: titles.map(textContent => ({ textContent, hidden: false })),
    querySelector() { return { textContent: sprint }; },
    querySelectorAll() { return this.rows; },
  });
  const groups = [makeGroup('Sprint 2', ['One-page budget', 'Business case']), makeGroup('Sprint 3', ['Interview notes'])];
  runSite({ search, groups, elements: { 'document-search': input, 'document-clear': clear, 'document-count': count } });
  assert.equal(search.hidden, false);
  assert.equal(count.textContent, '3 documents shown.');
  input.value = ' SPRINT 2 budget ';
  inputEvents.get('input')();
  assert.equal(groups[0].rows[0].hidden, false);
  assert.equal(groups[0].rows[1].hidden, true);
  assert.equal(groups[1].hidden, true);
  assert.equal(count.textContent, '1 document shown.');
  input.value = 'does not exist';
  inputEvents.get('input')();
  assert.ok(groups.every(group => group.hidden));
  assert.match(count.textContent, /No documents found/);
  clearEvents.get('click')();
  assert.equal(input.value, '');
  assert.ok(groups.every(group => !group.hidden && group.rows.every(row => !row.hidden)));
  assert.equal(focused, true);
});
