#!/usr/bin/env python3
"""Verify fixtures, native app exports, and optional copied synthetic Room databases."""
import collections, datetime as dt, json, pathlib, sqlite3
from PIL import Image
from generate import ROOT, decrypt, TZ
ASSETS=ROOT.parent.parent/'Dev/app/src/main/assets'
def bodymask(side):
    im=Image.open(ASSETS/f'body_{side}.png').convert('RGBA');w,h=im.size
    if w>512:im=im.resize((512,int(h*512/w)));w,h=im.size
    pix=im.load();bg=set();q=collections.deque()
    def add(x,y):
        if (x,y) in bg:return
        r,g,b,a=pix[x,y]
        if a<128 or min(r,g,b)>200:bg.add((x,y));q.append((x,y))
    for x in range(w):add(x,0);add(x,h-1)
    for y in range(h):add(0,y);add(w-1,y)
    while q:
        x,y=q.popleft()
        for a,b in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if 0<=a<w and 0<=b<h:add(a,b)
    return w,h,bg
masks={s:bodymask(s) for s in ['front','back']}
def canonical(p):
    names={i['id']:i['name'] for i in p['issues']}
    return {'issues':sorted((i['name'],i['startDate'],i['lastUpdated'],i['status']) for i in p['issues']), 'records':sorted((names[r['painIssueId']],r['timestamp'],r['intensity'],json.dumps(json.loads(r['drawingDataJson']),sort_keys=True),r['side'],r['note'],r['symptoms']) for r in p['records']), 'treatments':sorted((names[t['painIssueId']],t['timestamp'],t['type'],t['notes']) for t in p['treatments'])}
report={}
for lang in ['ko','en']:
    p=json.loads((ROOT/f'tongda-sample-{lang}.json').read_text());assert json.loads(decrypt((ROOT/f'tongda-sample-{lang}.tngd').read_bytes()))==p
    cases=[]
    for issue in p['issues']:
        rows=[r for r in p['records'] if r['painIssueId']==issue['id']];days=collections.Counter(dt.datetime.fromtimestamp(r['timestamp']/1000,TZ).date().isoformat() for r in rows)
        strokes=0
        for r in rows:
            drawing=json.loads(r['drawingDataJson']);levels=[]
            for side,paths in drawing.items():
                w,h,bg=masks[side]
                for path in paths:
                    assert len(path['points'])>=2
                    assert 1<=path['intensity']<=10 and path['size']>0
                    levels.append(path['intensity']);strokes+=1
                    for pt in path['points']:
                        assert (int(pt['x']*w),int(pt['y']*h)) not in bg,(issue['name'],side,pt)
            assert max(levels)==r['intensity']
        cases.append(dict(name=issue['name'],records=len(rows),drawingDays=len(days),multiRecordDays=sum(n>1 for n in days.values()),strokes=strokes,start=min(days),end=max(days),distinctBrushSizes=len({path['size'] for r in rows for paths in json.loads(r['drawingDataJson']).values() for path in paths})))
    export=ROOT/f'app-export-{lang}.tngd'
    ok=None
    if export.exists():ok=canonical(json.loads(decrypt(export.read_bytes())))==canonical(p);assert ok
    report[lang]=dict(counts=p['counts'],scenarios=cases,allStrokePointsInsideBodyMask=True,appExportMatchesFixture=ok)
(ROOT/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
