#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
import json,re,subprocess,hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parent.parent
class Page(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.images=[];self.links=[];self.headings=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id'in a:self.ids.append(a['id'])
  if tag=='img':self.images.append(a)
  if tag=='a':self.links.append(a.get('href',''))
  if tag in ['h1','h2','h3']:self.headings.append(tag)
report={};manifest=[]
for lang in ['ko','en']:
 p=ROOT/lang/'index.html';s=p.read_text()
 def dimensions(m):
  tag=m.group();src=re.search(r'src="([^"]+)"',tag).group(1);f=p.parent/src
  w,h=Image.open(f).size;tag=re.sub(r' (width|height)="[^"]*"','',tag)
  return tag[:-1]+f' width="{w}" height="{h}">'
 s=re.sub(r'<img\b[^>]*>',dimensions,s);p.write_text(s)
 c=Page();c.feed(s)
 baseline=Page();baseline.feed(subprocess.check_output(['git','show',f'HEAD:{lang}/index.html'],cwd=ROOT).decode())
 assert c.ids==baseline.ids, 'Existing anchors must remain unchanged'
 assert len(c.ids)==len(set(c.ids))
 assert set(baseline.links)<=set(c.links),(lang,set(baseline.links)-set(c.links))
 for a in c.images:
  f=p.parent/a['src'];assert f.exists();w,h=Image.open(f).size;assert (int(a['width']),int(a['height']))==(w,h)
 for href in c.links:
  if href.startswith('#'):assert href[1:] in c.ids
  elif href and not re.match(r'[a-z]+:',href):assert (p.parent/href.split('#')[0]).exists(),href
 for f in sorted((ROOT/'capture-record'/lang).glob('*.png')):
  asset=ROOT/'assets/img'/lang/f.name
  assert Image.open(f).size==(1080,2400)
  assert Image.open(asset).size==(648,1440)
  manifest.append(dict(language=lang,file=str(asset.relative_to(ROOT)),raw=str(f.relative_to(ROOT)),rawSize=[1080,2400],webSize=[648,1440],sha256=hashlib.sha256(asset.read_bytes()).hexdigest()))
 report[lang]=dict(anchors=c.ids,imageReferences=len(c.images),allImagesExist=True,allImageDimensionsMatch=True,existingLinksPreserved=True,headings=c.headings)
assert report['ko']['anchors']==report['en']['anchors']
assert report['ko']['headings']==report['en']['headings']
assert len(set(hashlib.sha256((ROOT/'assets/img'/lang/f).read_bytes()).hexdigest() for lang in ['ko','en'] for f in ['07_stats_month.png','08_stats_trend.png','09_stats_day.png']))==6
(ROOT/'capture-record/html-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
(ROOT/'capture-record/manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print('PASS: anchors, headings, existing links, image dimensions, distinct stats screens; captures',len(manifest))
