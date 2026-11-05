// Small-screen navigation
const toggle = document.querySelector('.nav-toggle');
const nav = document.querySelector('.nav-links');
toggle.addEventListener('click', () => {
  const open = nav.classList.toggle('is-open');
  toggle.setAttribute('aria-expanded', String(open));
  toggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
});

// Figure viewer: links marked data-figure open their image in a dialog
const dialog = document.querySelector('.figure-dialog');
const dialogImage = dialog.querySelector('img');
document.querySelectorAll('[data-figure]').forEach(link => {
  link.addEventListener('click', event => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || typeof dialog.showModal !== 'function') return;
    event.preventDefault();
    dialogImage.src = link.href;
    dialogImage.alt = link.querySelector('img')?.alt || '';
    dialog.showModal();
  });
});
dialog.querySelector('button').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', event => {
  const r = dialog.getBoundingClientRect();
  if (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom) dialog.close();
});

// Research-figure carousel: previous/next buttons and arrow keys
document.querySelectorAll('.figure-carousel').forEach(carousel => {
  const slides = [...carousel.querySelectorAll('.carousel-slide')];
  const count = carousel.querySelector('.carousel-count');
  let index = 0;
  const show = i => {
    index = (i + slides.length) % slides.length;
    slides.forEach((slide, k) => {
      slide.classList.toggle('active', k === index);
      slide.setAttribute('aria-hidden', String(k !== index));
    });
    count.textContent = `${index + 1} / ${slides.length}`;
  };
  carousel.querySelector('.carousel-prev').addEventListener('click', () => show(index - 1));
  carousel.querySelector('.carousel-next').addEventListener('click', () => show(index + 1));
  carousel.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft') show(index - 1);
    if (event.key === 'ArrowRight') show(index + 1);
  });
  show(0);
});
