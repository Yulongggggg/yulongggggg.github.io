const toggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('.nav-links');
function closeMenu() {
  nav.classList.remove('is-open');
  toggle.setAttribute('aria-expanded', 'false');
  toggle.setAttribute('aria-label', 'Open navigation');
}
toggle.addEventListener('click', () => {
  const open = nav.classList.toggle('is-open');
  toggle.setAttribute('aria-expanded', String(open));
  toggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
});
nav.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && nav.classList.contains('is-open')) { closeMenu(); toggle.focus(); }
});
document.addEventListener('click', event => { if (!event.target.closest('.navbar')) closeMenu(); });
const dialog = document.querySelector('.figure-dialog');
const figure = dialog.querySelector('img');
document.querySelectorAll('[data-figure]').forEach(link => {
  link.addEventListener('click', event => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    if (typeof dialog.showModal !== 'function') return;
    event.preventDefault();
    figure.src = link.href;
    figure.alt = link.querySelector('img').alt;
    dialog.showModal();
  });
});
dialog.querySelector('button').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', event => {
  const rect = dialog.getBoundingClientRect();
  if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
});

// Decorative pixel companion. Clicking empty space tosses a toy; links stay untouched.
const cat = document.querySelector('.corner-cat');
const toy = document.querySelector('.cat-toy');
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
let catX = 0, catY = 0, catFrame = 0;
function placeCat(x, y, facing = 1) {
  catX = x; catY = y;
  cat.style.transform = `translate(${x}px, ${y}px)`;
  cat.firstElementChild.style.transform = `scaleX(${facing})`;
}
function resetCat() {
  cancelAnimationFrame(catFrame);
  cat.classList.remove('running');
  toy.hidden = true;
  placeCat(Math.max(0, innerWidth - 260), Math.max(0, innerHeight - 210));
  cat.classList.toggle('ready', !reducedMotion.matches);
}
resetCat();
window.addEventListener('resize', resetCat);
reducedMotion.addEventListener('change', resetCat);
document.addEventListener('click', event => {
  if (reducedMotion.matches || event.target.closest('a, button, dialog, .navbar') || getSelection()?.toString()) return;
  cancelAnimationFrame(catFrame);
  const x = Math.max(-65, Math.min(innerWidth - 175, event.clientX - 120));
  const y = Math.max(-55, Math.min(innerHeight - 155, event.clientY - 130));
  const startX = catX, startY = catY;
  const facing = x < startX ? -1 : 1;
  const duration = Math.max(250, Math.hypot(x - startX, y - startY) / .55);
  const start = performance.now();
  toy.style.left = `${event.clientX - 14}px`;
  toy.style.top = `${event.clientY - 14}px`;
  toy.hidden = false;
  cat.classList.add('running');
  function move(now) {
    const progress = Math.min(1, (now - start) / duration);
    placeCat(startX + (x - startX) * progress, startY + (y - startY) * progress, facing);
    if (progress < 1) catFrame = requestAnimationFrame(move);
    else { cat.classList.remove('running'); toy.hidden = true; }
  }
  catFrame = requestAnimationFrame(move);
});

// News carousels: swipe, arrows, dots or arrow keys move between items; they advance slowly unless hovered, focused or reduced motion is set.
document.querySelectorAll('.news-carousel').forEach(carousel => {
  const track = carousel.querySelector('.carousel-track');
  const slides = [...track.querySelectorAll('.carousel-slide')];
  let index = 0, paused = false;
  const show = i => {
    index = (i + slides.length) % slides.length;
    track.scrollTo({ left: index * track.clientWidth, behavior: reducedMotion.matches ? 'auto' : 'smooth' });
  };
  const dots = slides.map((_, i) => {
    const dot = document.createElement('button');
    dot.type = 'button';
    dot.setAttribute('aria-label', `Show item ${i + 1} of ${slides.length}`);
    dot.addEventListener('click', () => show(i));
    carousel.querySelector('.carousel-dots').append(dot);
    return dot;
  });
  const mark = () => dots.forEach((dot, i) => dot.setAttribute('aria-current', String(i === index)));
  track.addEventListener('scroll', () => { index = Math.round(track.scrollLeft / Math.max(1, track.clientWidth)); mark(); }, { passive: true });
  carousel.querySelector('.carousel-prev').addEventListener('click', () => show(index - 1));
  carousel.querySelector('.carousel-next').addEventListener('click', () => show(index + 1));
  track.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft') { event.preventDefault(); show(index - 1); }
    if (event.key === 'ArrowRight') { event.preventDefault(); show(index + 1); }
  });
  carousel.addEventListener('pointerenter', () => { paused = true; });
  carousel.addEventListener('pointerleave', () => { paused = false; });
  carousel.addEventListener('focusin', () => { paused = true; });
  carousel.addEventListener('focusout', () => { paused = false; });
  window.addEventListener('resize', () => track.scrollTo({ left: index * track.clientWidth }));
  setInterval(() => { if (!paused && !reducedMotion.matches && !document.hidden) show(index + 1); }, 7000);
  mark();
});
