'use strict';
const { test } = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, '../assets/js/site.js'), 'utf8');

function runSite({ hash = '', elements = {}, entries = [] } = {}) {
  const events = new Map();
  const window = {
    location: { hash },
    addEventListener(name, callback) { events.set(name, callback); },
  };
  const document = {
    documentElement: { classList: { add() {} } },
    querySelector() { return null; },
    querySelectorAll(selector) {
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
