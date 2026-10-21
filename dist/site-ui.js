(() => {
  const button = document.querySelector('.back-to-top');
  if (!button) return;
  const update = () => button.classList.toggle('is-visible', window.scrollY > 450);
  window.addEventListener('scroll', update, {passive: true});
  window.addEventListener('pageshow', update);
  update();
  button.addEventListener('click', () => {
    window.scrollTo({top: 0, behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth'});
    const home = document.querySelector('header .brand');
    if (home) home.focus({preventScroll: true});
  });
})();
