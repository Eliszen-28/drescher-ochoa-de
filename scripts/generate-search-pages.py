from pathlib import Path
from html import escape,unescape
import json,re,unicodedata,xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[1];dist=root/'dist';d=json.loads((dist/'data.js').read_text()[15:-1]);origin='https://drescher-ochoa-lesewelten.elisaaguilar10524.chatgpt.site';author='Heidrun Drescher-Ochoa'
def text(s):return re.sub(r'\s+',' ',unescape(re.sub('<[^>]*>',' ',s))).strip()
def slug(s):return re.sub('[^a-z0-9]+','-',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()).strip('-')
def js(d):return json.dumps(d,ensure_ascii=False).replace('<','\\u003c')
def head(title,desc,path,schema,img=None):
 url=origin+path
 return '<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+escape(title)+' · Drescher Ochoa</title><meta name="description" content="'+escape(desc,quote=True)+'"><meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"><link rel="canonical" href="'+url+'"><meta property="og:type" content="'+('article' if '/artikel/' in path else 'website')+'"><meta property="og:title" content="'+escape(title,quote=True)+'"><meta property="og:description" content="'+escape(desc,quote=True)+'"><meta property="og:url" content="'+url+'"><meta property="og:locale" content="de_DE">'+('<meta property="og:image" content="'+origin+'/'+img+'">' if img else '')+'<link rel="stylesheet" href="/style.css"><script type="application/ld+json">'+js(schema)+'</script></head><body><header><a class="brand" href="/">drescher<img class="brand-flower" src="/assets/logo-schmetterling-sonnenblume.svg" alt="" aria-hidden="true" width="48" height="51"><br>ochoa<span class="brand-small">BILDUNG. MENSCH. POTENZIAL.</span></a><nav aria-label="Hauptnavigation"><a href="/blog/">Blog</a><a href="/bibliothek/">Bibliothek</a><a href="/#ueber">Über mich</a></nav><a class="contact" href="/#kontakt">Kontakt ↗</a></header>'
def footer():return (root/"content/site-footer.html").read_text()+"</body></html>"
urls=['/','/blog/','/bibliothek/','/impressum/','/datenschutzerklaerung/'];mapping={};listing={}
for items,folder,index in [(d['posts'],'artikel','blog'),(d['books'],'buecher','bibliothek')]:
 listing[index]=[]
 for p in items:
  path='/'+folder+'/'+slug(p['title'])+'-'+p['id']+'/';mapping[p['id']]=path;urls.append(path);desc=text(p['excerpt'])[:170];url=origin+path
  schema={'@context':'https://schema.org','@type':'BlogPosting' if folder=='artikel' else 'Book','@id':url,'url':url,'name':p['title'],'headline':p['title'],'description':desc,'inLanguage':'de','author':{'@type':'Person','name':author},'image':origin+'/'+p['image']}
  if p.get('date'):schema['datePublished']=p['date']+'+02:00';schema['mainEntityOfPage']=url
  content=re.sub(r'((?:src|href)=")assets/',r'\1/assets/',p['content'])
  body=head(p['title'],desc,path,schema,p['image'])+'<main class="search-page"><a class="text-link" href="/'+index+'/">← '+('Zum Blog' if index=='blog' else 'Zur Bibliothek')+'</a><article id="reader-content"><p class="eyebrow">'+escape(p['topic'])+'</p><h1>'+escape(p['title'])+'</h1><p>'+author+(' · '+p['date'][:10] if p.get('date') else '')+'</p><img class="reader-cover" src="/'+p['image']+'" alt="'+escape(p['title'],quote=True)+'"><div class="article-body">'+content+'</div><p class="reader-source"><a href="'+p['source']+'" rel="noopener">Veröffentlichung auf der Originalwebsite ↗</a></p></article></main>'+footer()
  out=dist/path.strip('/');out.mkdir(parents=True,exist_ok=True);(out/'index.html').write_text(body);listing[index].append((p,path))
for index,title in [('blog','Blog – Gedanken für eine humane Bildung'),('bibliothek','Bibliothek – Bücher von Heidrun Drescher-Ochoa')]:
 rows=listing[index];schema={'@context':'https://schema.org','@type':'CollectionPage','name':title,'url':origin+'/'+index+'/','inLanguage':'de','mainEntity':{'@type':'ItemList','itemListElement':[{'@type':'ListItem','position':i+1,'url':origin+path,'name':p['title']} for i,(p,path) in enumerate(rows)]}}
 body=head(title,'Alle '+('28 Artikel über holistische Pädagogik, Selbsterkenntnis und Bildung.' if index=='blog' else '8 Bücher und wissenschaftlichen Publikationen der Autorin.'),'/' +index+'/',schema)+'<main class="section"><p class="eyebrow">'+('DER BLOG' if index=='blog' else 'DIE BIBLIOTHEK')+'</p><h1 class="archive-title">'+escape(title)+'</h1><p><a class="text-link" href="/#'+index+'">Mit Suche und Themenfiltern entdecken ↗</a></p><div class="catalog '+('blog-catalog' if index=='blog' else '')+'">'
 for p,path in rows:body+='<article class="catalog-card"><a href="'+path+'" class="cover '+('article' if index=='blog' else '')+'"><img src="/'+p['image']+'" alt="'+escape(p['title'],quote=True)+'" loading="lazy"></a><p class="meta">'+escape(p['topic'])+'</p><h2 class="archive-item-title"><a href="'+path+'">'+escape(p['title'])+'</a></h2><p>'+escape(text(p['excerpt'])[:220])+'</p><a class="text-link" href="'+path+'">'+('Artikel lesen' if index=='blog' else 'Buch entdecken')+' ↗</a></article>'
 out=dist/index;out.mkdir(exist_ok=True);(out/'index.html').write_text(body+'</div></main>'+footer())
(dist/'paths.js').write_text('window.CONTENT_PATHS='+js(mapping)+';')
s=(dist/'index.html').read_text();s=s.replace('<script defer src="app.js"></script>','<script defer src="paths.js"></script><script defer src="app.js"></script>')
metadata='<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"><link rel="canonical" href="'+origin+'/"><meta property="og:title" content="Drescher Ochoa – Bildung neu denken"><meta property="og:description" content="Holistische Pädagogik, Selbsterkenntnis und Potenzialentfaltung. Blog und Bücher von Heidrun Drescher-Ochoa."><meta property="og:url" content="'+origin+'/"><meta property="og:type" content="website"><meta property="og:locale" content="de_DE"><meta property="og:image" content="'+origin+'/'+d['portrait']+'"><script type="application/ld+json">'+js({'@context':'https://schema.org','@graph':[{'@type':'WebSite','@id':origin+'/#website','url':origin+'/','name':'Drescher Ochoa – Bildung neu denken','inLanguage':'de','author':{'@id':origin+'/#author'}},{'@type':'Person','@id':origin+'/#author','name':author,'url':origin+'/#ueber','image':origin+'/'+d['portrait'],'jobTitle':'Pädagogin und Autorin'}]})+'</script>'
s=s.replace('</head>',metadata+'</head>');(dist/'index.html').write_text(s)
(dist/'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: '+origin+'/sitemap.xml\n')
urlset=ET.Element('urlset',xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
for path in urls:ET.SubElement(ET.SubElement(urlset,'url'),'loc').text=origin+path
ET.ElementTree(urlset).write(dist/'sitemap.xml',encoding='utf-8',xml_declaration=True)
llms='# Drescher Ochoa\n\n> Deutschsprachige Website von Dr. Heidrun Drescher-Ochoa über holistische Pädagogik, Selbsterkenntnis, Achtsamkeit und Potenzialentfaltung.\n\n## Übersichten\n- [Blog]('+origin+'/blog/): Alle 28 Artikel.\n- [Bibliothek]('+origin+'/bibliothek/): Bücher und wissenschaftliche Publikationen.\n\n## Artikel und Bücher\n'
for index in listing:
 for p,path in listing[index]:llms+='- ['+p['title']+']('+origin+path+'): '+p['topic']+'\n'
(dist/'llms.txt').write_text(llms)
print('Generated',len(urls),'indexable URLs, sitemap, robots.txt, structured data and llms.txt.')
