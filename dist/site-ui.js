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

// Translation starts only when a visitor chooses the language link.
(() => {
 const link=document.querySelector('[data-translate]');
 if(!link)return;
 const update=()=>{
  let page=new URL(location.href);
  if(page.hash.startsWith('#lesen-')){
   const path=window.CONTENT_PATHS?.[page.hash.slice(7)];
   if(path)page=new URL(path,location.origin);
  }
  page.hash='';
  const translated=new URL('https://translate.google.com/translate');
  translated.search=new URLSearchParams({sl:'de',tl:'es',u:page.href}).toString();
  link.href=translated.href;
 };
 update();link.addEventListener('click',update);link.addEventListener('contextmenu',update);
 window.addEventListener('hashchange',update);
})();
