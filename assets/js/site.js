document.documentElement.classList.add('js');

const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const narrowScreen = window.matchMedia('(max-width: 760px)');

requestAnimationFrame(() => document.documentElement.classList.add('is-ready'));

const menuButton = document.querySelector('.menu-button');
const siteNav = document.querySelector('.site-nav');

if (menuButton && siteNav) {
  menuButton.addEventListener('click', () => {
    const willOpen = menuButton.getAttribute('aria-expanded') !== 'true';
    menuButton.setAttribute('aria-expanded', String(willOpen));
    siteNav.classList.toggle('is-open', willOpen);
  });

  siteNav.addEventListener('click', (event) => {
    if (!event.target.closest('a')) return;
    menuButton.setAttribute('aria-expanded', 'false');
    siteNav.classList.remove('is-open');
  });
}

const revealItems = document.querySelectorAll('.reveal');

if ('IntersectionObserver' in window && revealItems.length && !reducedMotion.matches) {
  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.12 });

  revealItems.forEach((item) => revealObserver.observe(item));
} else {
  revealItems.forEach((item) => item.classList.add('is-visible'));
}

const sprintAccordion = document.querySelector('[data-sprint-accordion]');

if (sprintAccordion) {
  const slices = [...sprintAccordion.querySelectorAll('[data-sprint-slice]')];
  const buttons = slices.map((slice) => slice.querySelector('button'));

  const openSprint = (selectedIndex) => {
    slices.forEach((slice, index) => {
      const isOpen = index === selectedIndex;
      slice.classList.toggle('is-open', isOpen);
      buttons[index].setAttribute('aria-expanded', String(isOpen));
    });
  };

  buttons.forEach((button, index) => {
    button.addEventListener('click', () => openSprint(index));
    button.addEventListener('keydown', (event) => {
      if (!['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home', 'End'].includes(event.key)) return;
      event.preventDefault();
      let targetIndex = index;
      if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') targetIndex = (index - 1 + buttons.length) % buttons.length;
      if (event.key === 'ArrowRight' || event.key === 'ArrowDown') targetIndex = (index + 1) % buttons.length;
      if (event.key === 'Home') targetIndex = 0;
      if (event.key === 'End') targetIndex = buttons.length - 1;
      buttons[targetIndex].focus();
      openSprint(targetIndex);
    });
  });
}

let gsapContexts = [];

function initializeScrollMotion() {
  if (reducedMotion.matches || narrowScreen.matches || !window.gsap || !window.ScrollTrigger) return;

  window.gsap.registerPlugin(window.ScrollTrigger);

  document.querySelectorAll('.method-story').forEach((story) => {
    const heading = story.querySelector('.method-story__heading');
    const cards = [...story.querySelectorAll('.method-card')];
    if (!heading || cards.length < 2) return;

    const context = window.gsap.context(() => {
      cards.slice(0, -1).forEach((card, index) => {
        window.gsap.to(card, {
          scale: 0.96,
          autoAlpha: 0,
          ease: 'none',
          scrollTrigger: {
            trigger: cards[index + 1],
            start: 'top 70%',
            end: 'top 18%',
            scrub: true,
            invalidateOnRefresh: true
          }
        });

        window.ScrollTrigger.create({
          trigger: card,
          start: 'top 12%',
          endTrigger: cards[cards.length - 1],
          end: 'top 12%',
          pin: true,
          pinSpacing: false,
          invalidateOnRefresh: true
        });
      });
    }, story);

    gsapContexts.push(context);
  });
}

initializeScrollMotion();

function resetScrollMotion() {
  gsapContexts.forEach((context) => context.revert());
  gsapContexts = [];
  initializeScrollMotion();
}

reducedMotion.addEventListener('change', resetScrollMotion);
narrowScreen.addEventListener('change', resetScrollMotion);

window.addEventListener('pagehide', () => {
  gsapContexts.forEach((context) => context.revert());
  gsapContexts = [];
});
