#!/usr/bin/env python3
"""Prepare dist/ for a GitHub project Pages URL without changing production files."""
import argparse,json,re,shutil
from pathlib import Path
parser=argparse.ArgumentParser();parser.add_argument('--base',required=True);parser.add_argument('--output',default='_site');args=parser.parse_args()
base='/'+args.base.strip('/');root=Path(__file__).resolve().parents[1];source=root/'dist';output=root/args.output
if output.exists():raise SystemExit('Output directory must not already exist')
shutil.copytree(source,output)
for page in output.rglob('*.html'):
 s=page.read_text();s=re.sub(r'\b(href|src|action)="/(?!/)([^"]*)"',lambda m:m[1]+'="'+base+'/'+m[2]+'"',s);page.write_text(s)
paths=output/'paths.js';s=paths.read_text();data=json.loads(s.removeprefix('window.CONTENT_PATHS=').removesuffix(';'));paths.write_text('window.CONTENT_PATHS='+json.dumps({k:base+v for k,v in data.items()},ensure_ascii=False)+';')
(output/'.nojekyll').write_text('')
print('GitHub Pages artifact prepared at',output,'with base',base)
