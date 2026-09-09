import device as d,sys,time,re
lang,target=sys.argv[1:3]
names={'ko':['허리와 다리 · 일상 기록','목·어깨 · 책상 작업','무릎 · 활동 후 기록'],'en':['Lower back & leg · daily life','Neck & shoulders · desk work','Knee · after activity']}[lang]
want={'back':0,'neck':1,'knee':2}[target]
def current():
 root=d.dump();texts={n.get('text') for n in root.iter('node')};found=[i for i,name in enumerate(names) if name in texts];assert len(found)==1,found;return found[0]
for _ in range(3):
 now=current()
 if now==want:break
 x1,x2=('900','180') if now<want else ('180','900')
 d.adb('shell','input','swipe',x1,'1200',x2,'1200','500');time.sleep(1)
 assert current()!=now,'Pager did not move; inspect UI before retry'
assert current()==want
print('Selected',names[want]);d.snap(f'{lang}-scene-{target}')
