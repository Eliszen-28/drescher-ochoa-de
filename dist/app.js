const {posts,books,portrait}=window.CONTENT;const all=[...books,...posts];const $=s=>document.querySelector(s);const esc=s=>String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));let saved;try{saved=JSON.parse(localStorage.getItem('do-reading')||'[]');if(!Array.isArray(saved))saved=[]}catch{saved=[]}
let readerSection='bibliothek';
const date=s=>new Date(s).toLocaleDateString('de-DE',{day:'numeric',month:'short',year:'numeric'});
const openButton=p=>`<button class="image-button" data-open="${p.id}" aria-label="${esc(p.title)} lesen"><img src="${esc(p.image)}" alt="${esc(p.title)}" loading="lazy"></button>`;

const bookActions=p=>p.type==='Buch'?`<div class="book-actions"><a class="book-buy" href="${esc(p.buyUrl)}" ${p.buyUrl.startsWith('https:')?'target="_blank" rel="noopener"':''}>Buch kaufen </a>${p.hasReview?`<a class="book-review" href="${esc(window.CONTENT_PATHS[p.id])}#rezension">Rezension </a>`:''}</div>${p.buyUrl.startsWith('mailto:')?'<p class="book-action-note">Kaufanfrage per E-Mail an die Autorin.</p>':''}`:'';
$('#portrait').src=portrait;
$('#hero-books').innerHTML=[books[1],books[0]].map(b=>`<img class="hero-book" src="${esc(b.image)}" alt="${esc(b.title)}">`).join('');
const sections=[{id:'bibliothek',prefix:'',items:books,type:'Alle',topic:'Alle Themen',limit:12},{id:'blog',prefix:'blog-',items:posts,type:'Alle',topic:'Alle Themen',limit:6}];
const field=(s,name)=>$('#'+s.prefix+name);
function render(s){
 const query=field(s,'search').value.trim().toLocaleLowerCase('de');
 let items=s.items.filter(p=>(s.type!=='Merkliste'||saved.includes(p.id))&&(s.topic==='Alle Themen'||p.topic===s.topic)&&(!query||`${p.title} ${p.excerpt} ${p.topic} ${p.content.replace(/<[^>]+>/g,' ')}`.toLocaleLowerCase('de').includes(query)));
 if(field(s,'sort').value==='az')items.sort((a,b)=>a.title.localeCompare(b.title,'de'));else items.sort((a,b)=>(b.date||'').localeCompare(a.date||''));
 field(s,'results').textContent=`${items.length} ${s.id==='blog'?'Artikel':items.length===1?'Buch':'Bücher'}${query?' für „'+field(s,'search').value+'“':''}`;
 field(s,'saved-count').textContent=s.items.filter(p=>saved.includes(p.id)).length;
 field(s,'catalog').innerHTML=items.slice(0,s.limit).map(p=>`<article class="catalog-card"><div class="cover ${p.type==='Artikel'?'article':''}">${openButton(p)}<button class="save" data-save="${p.id}" aria-pressed="${saved.includes(p.id)}" aria-label="${esc(p.title)} ${saved.includes(p.id)?'aus Merkliste entfernen':'merken'}">${saved.includes(p.id)?'♥':'♡'}</button></div><div class="meta"><span>${esc(p.topic)}</span>${p.date?`<span>${date(p.date)}</span>`:''}</div><h3>${esc(p.title)}</h3><p class="excerpt">${esc(p.excerpt)}</p><a class="read-link" href="${window.CONTENT_PATHS[p.id]}" data-open="${p.id}">${p.type==='Buch'?'Buch entdecken':'Artikel lesen'} </a></article>`).join('')||'<div class="empty"><h3>Noch nichts gefunden?</h3><p>Versuche einen anderen Suchbegriff oder wähle ein anderes Thema.</p><button class="button outline" data-reset>Filter zurücksetzen</button></div>';
 field(s,'more').hidden=items.length<=s.limit;
}
for(const s of sections){
 const topics=['Alle Themen',...new Set(s.items.map(p=>p.topic))];
 field(s,'topics').innerHTML=topics.map((t,i)=>`<button data-topic="${esc(t)}" class="${i?'':'active'}" aria-pressed="${!i}">${esc(t)}</button>`).join('');
 field(s,'search').addEventListener('input',()=>{s.limit=s.id==='blog'?6:12;render(s)});
 field(s,'sort').addEventListener('change',()=>render(s));
 field(s,'more').onclick=()=>{s.limit+=s.id==='blog'?6:12;render(s)};
 $('#'+s.id).addEventListener('click',e=>{
  const topic=e.target.closest('[data-topic]'),tab=e.target.closest('[data-type],[data-blog-type]');
  if(topic){s.topic=topic.dataset.topic;s.limit=s.id==='blog'?6:12;field(s,'topics').querySelectorAll('button').forEach(b=>{b.classList.toggle('active',b===topic);b.setAttribute('aria-pressed',b===topic)});render(s)}
  if(tab){s.type=tab.dataset.type||tab.dataset.blogType;s.limit=s.id==='blog'?6:12;$('#'+s.id).querySelectorAll('.tabs button').forEach(b=>{b.classList.toggle('active',b===tab);b.setAttribute('aria-pressed',b===tab)});render(s)}
  if(e.target.closest('[data-reset]')){field(s,'search').value='';field(s,'topics').querySelector('button').click();$('#'+s.id).querySelector('.tabs button').click()}
 });render(s);
}
function openReader(id){const p=all.find(x=>x.id===id);if(!p)return;readerSection=p.type==='Buch'?'bibliothek':'blog';$('#reader-back').textContent=p.type==='Buch'?' Zurück zur Bibliothek':' Zurück zum Blog';$('#reader-content').innerHTML=`<p class="eyebrow">${p.type} · ${esc(p.topic)}</p><h1>${esc(p.title)}</h1>${p.date?`<p>${date(p.date)} · Heidrun Drescher-Ochoa</p>`:''}<img class="reader-cover" src="${esc(p.image)}" alt="${esc(p.title)}">${bookActions(p)}<div class="article-body">${p.content}</div>${p.type==='Buch'?p.reviewContent.replace('id="rezension"','id="reader-rezension"'):''}<div class="reader-source"><a href="${window.CONTENT_PATHS[p.id]}">Eigene Artikelseite öffnen </a> · <a href="${esc(p.source)}" target="_blank" rel="noopener">${p.type==='Buch'?'Veröffentlichung auf der Originalwebsite ansehen':'Originalartikel ansehen'} </a> · <button class="read-link" data-save="${p.id}">${saved.includes(p.id)?'♥ Gemerkt':'♡ Für später merken'}</button></div>`;$('#reader').showModal();$('#reader').scrollTop=0;document.body.classList.add('modal-open');history.replaceState(null,'','#lesen-'+id)}
function closeReader(){$('#reader').close();$('#reader-content').innerHTML='';document.body.classList.remove('modal-open');history.replaceState(null,'','#'+readerSection)}

document.addEventListener('click',e=>{let b=e.target.closest('[data-open]');if(b){if(e.metaKey||e.ctrlKey||e.shiftKey||e.altKey)return;e.preventDefault();openReader(b.dataset.open);return}b=e.target.closest('[data-save]');if(b){const id=b.dataset.save;saved=saved.includes(id)?saved.filter(x=>x!==id):[...saved,id];try{localStorage.setItem('do-reading',JSON.stringify(saved))}catch{}sections.forEach(render);if(b.closest('#reader-content'))b.textContent=saved.includes(id)?'♥ Gemerkt':'♡ Für später merken'}});
$('#reader-close').onclick=closeReader;$('#reader-back').onclick=closeReader;
$('#reader').addEventListener('cancel',e=>{e.preventDefault();closeReader()});$('#reader').addEventListener('click',e=>{if(e.target===$('#reader'))closeReader()});
if(location.hash.startsWith('#lesen-'))openReader(location.hash.slice(7));
if(location.hash==='#impulse')location.hash='blog';
