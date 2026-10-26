#!/usr/bin/env python3
"""Idempotent metadata, entity graph and crawl files for the production domain."""
from pathlib import Path
from html import escape,unescape
from urllib.parse import urlsplit
import json,re,xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[1];dist=root/'dist'
origin='https://drescher-ochoa.net';previous='https://drescher-ochoa-lesewelten.elisaaguilar10524.chatgpt.site'
data=json.loads((dist/'data.js').read_text()[15:-1]);paths=json.loads((dist/'paths.js').read_text().removeprefix('window.CONTENT_PATHS=').removesuffix(';'))
def plain(s):return ' '.join(unescape(re.sub('<[^>]+>',' ',s)).split())
def brief(s,n=160):
 s=re.sub(r'https?://\S+', '', plain(s)).strip()
 return s if len(s)<=n else s[:n-1].rsplit(' ',1)[0]+'…'
def js(o):return json.dumps(o,ensure_ascii=False).replace('</','<\\/')
author={'@type':'Person','@id':origin+'/#heidrun','name':'Heidrun Drescher-Ochoa','honorificPrefix':'Dr. phil.','honorificSuffix':'M.A.','url':origin+'/#heidrun-intro','image':origin+'/assets/heidrun-fondo-blanco.png','jobTitle':'Pädagogin, Autorin und Mentorin','description':'Pädagogin und Autorin mit Unterrichtserfahrung in Deutschland, Argentinien und Spanien; Mentorin für Logotherapie und Existenzanalyse, akkreditiert vom Viktor Frankl Institut Wien.','knowsAbout':['Holistische Pädagogik','Logotherapie','Existenzanalyse','Enneagramm','Biografiearbeit','Selbsterkenntnis','Potenzialentfaltung'],'knowsLanguage':['de','es'],'address':{'@type':'PostalAddress','addressLocality':'Segovia','addressCountry':'ES'},'sameAs':['https://www.facebook.com/HeidrunDrescherOchoa/','https://www.youtube.com/@heidrundrescher8364/featured']}
website={'@type':'WebSite','@id':origin+'/#website','url':origin+'/','name':'Drescher Ochoa – Holistische Pädagogik','inLanguage':'de','publisher':{'@id':origin+'/#heidrun'}}
items={paths[p['id']]:p for p in data['posts']+data['books']}
# Clarify the existing biography without adding a duplicate paragraph.
p=dist/'index.html';s=p.read_text()
s=re.sub(r'<p class="heidrun-international">.*?</p>','',s)
s=s.replace('in Deutschland, Argentinien und Spanien und ist Mentorin für Logotherapie und Existenzanalyse.', 'in Deutschland, Argentinien (Lateinamerika) und Spanien und ist Mentorin für Logotherapie und Existenzanalyse, akkreditiert vom Viktor Frankl Institut Wien.')
p.write_text(s)
urls=[]
for p in sorted(dist.rglob('index.html')):
 path='/'+p.parent.relative_to(dist).as_posix().strip('.')+'/'
 path=re.sub('/+','/',path);url=origin+path;urls.append(path)
 s=p.read_text().replace(previous,origin)
 head=re.search(r'<head>(.*?)</head>',s,re.S).group(1)
 title=plain(re.search(r'<title>(.*?)</title>',head,re.S).group(1))
 desc_match=re.search(r'<meta name="description" content="([^"]*)"',head)
 desc=brief(desc_match.group(1) if desc_match else title)
 image=origin+'/assets/heidrun-fondo-blanco.png'
 graph=[];item=items.get(path)
 if path=='/':
  title='Heidrun Drescher-Ochoa | Holistische Pädagogik & HOLLA'
  desc='Holistische Pädagogik, Logotherapie und Enneagramm: Bücher, Biografiearbeit und das HOLLA-Netzwerk von Dr. Heidrun Drescher-Ochoa in Spanien.'
  graph=[website,author,{'@type':'WebPage','@id':url+'#webpage','url':url,'name':title,'description':desc,'inLanguage':'de','isPartOf':{'@id':website['@id']},'about':{'@id':author['@id']},'mainEntity':{'@id':author['@id']}}]
 elif item:
  desc=brief(item['excerpt']);image=origin+'/'+item['image']
  entity={'@type':'BlogPosting' if item['type']=='Artikel' else 'Book','@id':url+'#'+('article' if item['type']=='Artikel' else 'book'),'url':url,'name':item['title'],'description':desc,'inLanguage':'de','author':{'@id':author['@id']},'image':image,'mainEntityOfPage':{'@id':url+'#webpage'}}
  if item['type']=='Artikel':
   entity.update(headline=item['title'],articleSection=item['topic'],publisher={'@id':author['@id']})
   if item.get('date'):entity['datePublished']=item['date']+'+02:00' if 'T' in item['date'] and not re.search(r'(Z|[+-]\d\d:\d\d)$',item['date']) else item['date']
  graph=[entity,{'@type':'WebPage','@id':url+'#webpage','url':url,'name':item['title'],'inLanguage':'de','isPartOf':{'@id':website['@id']},'mainEntity':{'@id':entity['@id']}},author,website]
 else:
  page={'@type':'CollectionPage' if path in ('/blog/','/bibliothek/') else 'WebPage','@id':url+'#webpage','url':url,'name':title,'description':desc,'inLanguage':'de','isPartOf':{'@id':website['@id']},'about':{'@id':author['@id']}}
  if path in ('/blog/','/bibliothek/'):
   rows=data['posts'] if path=='/blog/' else data['books']
   page['mainEntity']={'@type':'ItemList','itemListElement':[{'@type':'ListItem','position':i+1,'name':x['title'],'url':origin+paths[x['id']]} for i,x in enumerate(rows)]}
  graph=[page,website,author]
 if path!='/':graph.append({'@type':'BreadcrumbList','@id':url+'#breadcrumbs','itemListElement':[{'@type':'ListItem','position':1,'name':'Startseite','item':origin+'/'},{'@type':'ListItem','position':2,'name':item['title'] if item else title,'item':url}]})
 head=re.sub(r'<title>.*?</title>','',head,flags=re.S)
 head=re.sub(r'<meta\b[^>]*(?:name="(?:description|robots|author|twitter:[^"]+)"|property="og:[^"]+")[^>]*>','',head)
 head=re.sub(r'<link\b[^>]*(?:rel="canonical"|rel="alternate"[^>]*hreflang=)[^>]*>','',head)
 head=re.sub(r'<script type="application/ld\+json">.*?</script>','',head,flags=re.S)
 metadata='<title>'+escape(title)+'</title><meta name="description" content="'+escape(desc,quote=True)+'"><meta name="author" content="Dr. Heidrun Drescher-Ochoa"><meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"><link rel="canonical" href="'+url+'"><link rel="alternate" hreflang="de" href="'+url+'">'
 for key,value in {'title':title,'description':desc,'url':url,'type':'article' if item and item['type']=='Artikel' else 'website','locale':'de_DE','site_name':'Drescher Ochoa','image':image,'image:alt':item['title'] if item else 'Dr. Heidrun Drescher-Ochoa'}.items():metadata+='<meta property="og:'+key+'" content="'+escape(value,quote=True)+'">'
 for key,value in {'card':'summary_large_image','title':title,'description':desc,'image':image}.items():metadata+='<meta name="twitter:'+key+'" content="'+escape(value,quote=True)+'">'
 metadata+='<script type="application/ld+json">'+js({'@context':'https://schema.org','@graph':graph})+'</script>'
 s=re.sub(r'<head>.*?</head>',lambda m:'<head>'+head+metadata+'</head>',s,count=1,flags=re.S);p.write_text(s)
# No language variants are invented: all pages currently have German content.
(dist/'robots.txt').write_text('User-agent: *\nAllow: /\n\n# Search retrieval is permitted, including ChatGPT Search.\nUser-agent: OAI-SearchBot\nAllow: /\n\nSitemap: '+origin+'/sitemap.xml\n')
ns='http://www.sitemaps.org/schemas/sitemap/0.9';ET.register_namespace('',ns);tree=ET.Element('{'+ns+'}urlset')
for path in sorted(urls):ET.SubElement(ET.SubElement(tree,'{'+ns+'}url'),'{'+ns+'}loc').text=origin+path
ET.ElementTree(tree).write(dist/'sitemap.xml',encoding='utf-8',xml_declaration=True)
llms=(dist/'llms.txt').read_text().replace(previous,origin)
intro='''\n## Autorin und internationaler Kontext\nDr. phil. Heidrun Drescher-Ochoa M.A. ist Pädagogin, Autorin und Mentorin. Ihre Themen sind holistische Pädagogik, Logotherapie, Existenzanalyse, Enneagramm und Biografiearbeit. Sie lebt in Segovia, Spanien, und unterrichtete in Deutschland, Spanien und Argentinien (Lateinamerika). Ihre persönliche Akkreditierung stammt vom Viktor Frankl Institut Wien. Dies bezeichnet keine Niederlassung in Wien oder in anderen Ländern. Das HOLLA-Netzwerk ist unter https://www.holistischepaedagogik.de/ erreichbar.\n\nDie Inhalte dieser Website sind deutschsprachig und international zugänglich. Es gibt auf dieser Website derzeit keine eigenständige spanische Sprachversion.\n'''
if '## Autorin und internationaler Kontext' not in llms:llms=llms.replace('## Übersichten',intro+'\n## Übersichten')
(dist/'llms.txt').write_text(llms)
# Apache migration rules activate only on the final domain, never on Sites or Pages.
redirects={'/de/drescherochoawillkommen/':'/','/de/impressum/':'/impressum/','/de/datenschutzerklaerung/':'/datenschutzerklaerung/','/de/rezension/':paths['book0']+'#rezension'}
for item in data['posts']:
 old=urlsplit(item['source'])
 if old.hostname in ('drescher-ochoa.net','www.drescher-ochoa.net') and old.path not in redirects and old.path!=paths[item['id']]:redirects[old.path]=paths[item['id']]
ht='''DirectoryIndex index.html
<IfModule mod_rewrite.c>
RewriteEngine On
# Canonical host and HTTPS. Only affects the production hostname.
RewriteCond %{HTTP_HOST} ^www\\.drescher-ochoa\\.net$ [NC]
RewriteRule ^ https://drescher-ochoa.net%{REQUEST_URI} [R=301,L,NE]
RewriteCond %{HTTP_HOST} ^drescher-ochoa\\.net$ [NC]
RewriteCond %{HTTPS} !=on
RewriteCond %{HTTP:X-Forwarded-Proto} !https [NC]
RewriteRule ^ https://drescher-ochoa.net%{REQUEST_URI} [R=301,L,NE]
'''
for old,new in redirects.items():
 ht+='RewriteCond %{HTTP_HOST} ^(?:www\\.)?drescher-ochoa\\.net$ [NC]\nRewriteRule ^'+re.escape(old.strip('/'))+'/?$ '+origin+new+' [R=301,L,NE]\n'
ht+='''</IfModule>
<IfModule mod_mime.c>
AddType image/avif .avif
AddType image/webp .webp
AddType image/svg+xml .svg
</IfModule>
<IfModule mod_deflate.c>
AddOutputFilterByType DEFLATE text/html text/css text/plain application/javascript application/json image/svg+xml
</IfModule>
'''
(dist/'.htaccess').write_text(ht)
print('Updated',len(urls),'pages;',len(redirects),'legacy redirects; sitemap, robots, entity graph and llms.')
