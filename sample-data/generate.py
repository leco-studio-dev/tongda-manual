#!/usr/bin/env python3
"""Rebase bilingual synthetic DrawingPath fixtures and generate native encrypted TNGD."""
import argparse, datetime as dt, hashlib, json, math, os, pathlib, uuid
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
ROOT=pathlib.Path(__file__).resolve().parent
TZ=dt.timezone(dt.timedelta(hours=9))
def js(x): return json.dumps(x,ensure_ascii=False,separators=(',',':'))
def encrypt(data):
    salt,iv=os.urandom(16),os.urandom(12)
    key=hashlib.pbkdf2_hmac('sha256',b'TongdaApp_2026_bk',salt,100000,32)
    return b'TNGD\x01'+salt+iv+AESGCM(key).encrypt(iv,data,None)
def decrypt(data):
    assert data[:5]==b'TNGD\x01'
    return AESGCM(hashlib.pbkdf2_hmac('sha256',b'TongdaApp_2026_bk',data[5:21],100000,32)).decrypt(data[21:33],data[33:],None)
def stroke(coords,level,size=8):
    return dict(points=[dict(x=round(x,5),y=round(y,5)) for x,y in coords],size=size,intensity=level)
def patch(cx,cy,rx,ry,level):
    # Three gently curved parallel brush gestures; no dots or exterior marks.
    return [stroke([(cx+rx*t,cy+off*ry+0.003*math.sin(t*math.pi)) for t in [-1,-.75,-.5,-.25,0,.25,.5,.75,1]],level,7) for off in [-1,0,1]]
def drawing(scenario,day,level,morning):
    age=-day; broad=age>28; wave=0.003*math.sin(age*.7)
    f=[]; b=[]
    if scenario==0:
        b+=patch(.49+wave,.407,.075 if broad else .046,.012 if broad else .007,level)
        # Earlier left posterior thigh; recent right posterior thigh. Waist persists.
        x=.375 if broad else .622
        length=.125 if broad else .065
        b += [stroke([(x+.007*math.sin(t*math.pi),.553+t*length) for t in [0,.15,.3,.45,.6,.75,.9,1]],max(1,level-2),9 if broad else 7)]
        if 29<age<56: b+=patch(.60,.455,.027,.01,max(1,level-1))
    elif scenario==1:
        b+=patch(.493,.151,.030,.008, max(1,level-1))
        b+=patch(.36 if broad else .64,.185,.058 if broad else .043,.009,level)
        if age%12<5: b+=patch(.64 if broad else .36,.194,.033,.006,max(1,level-2))
    else:
        f+=patch(.614,.705,.034 if broad else .021,.014 if broad else .008,level)
        if age%14<7: f += [stroke([(.625,.65),(.635,.662),(.635,.675)],max(1,level-2),7)]
    for path in f+b:
        path["size"] = round(path["size"] * (.76 + age/180 + .14*math.sin(age*.45) + (.18 if morning else 0)), 2)
    return dict(front=f,back=b)
def make_fixture(lang):
    names={'ko':['허리와 다리 · 일상 기록','목·어깨 · 책상 작업','무릎 · 활동 후 기록'],'en':['Lower back & leg · daily life','Neck & shoulders · desk work','Knee · after activity']}[lang]
    notes={'ko':[['오래 앉아 작업한 날. 허리와 왼쪽 허벅지 뒤쪽을 표시했어요.','최근에는 허리 표시가 작아지고 오른쪽 허벅지 뒤쪽 느낌을 따로 남겼어요.'],['책상 작업 뒤 목과 어깨가 뻐근했어요.','작업 중 쉬는 시간이 있었어요. 오늘은 반대쪽 어깨 느낌도 표시했어요.'],['계단과 산책이 많았던 날. 무릎 앞쪽을 표시했어요.','활동량이 적었던 날. 무릎 주변의 좁은 부위를 표시했어요.']], 'en':[['After prolonged sitting, I marked my lower back and the back of my left thigh.','The lower-back marking is smaller recently; I also marked a sensation in the back of my right thigh.'],['My neck and shoulder felt stiff after desk work.','I took breaks from desk work and also marked the opposite shoulder today.'],['A day with stairs and walking. I marked the front of my knee.','A quieter day with a smaller marking around my knee.']]}[lang]
    symptoms={'ko':[['뻐근해요','오래 앉아 있으면 아파요'],['뻐근해요','자세 바꾸면 달라져요'],['욱신거려요','움직일 때만 아파요']], 'en':[['Stiff','Hurts after sitting a while'],['Stiff','Changes when I shift position'],['Throbbing','Only hurts when moving']]}[lang]
    items={'ko':['걷기','스트레칭','휴식'],'en':['Walking','Stretching','Rest']}[lang]
    result={'sampleOnly':True,'language':lang,'durationDays':84,'timezone':'Asia/Seoul','scenarios':[]}
    for s in range(3):
        records=[]; treatments=[]
        for day in range(-83,1):
            if day%2 and day<-3: continue
            if day in [-70,-56,-42,-28,-14,-6]: continue
            if s>0 and day==0: continue
            age=-day; base=(7 if age>56 else 6 if age>28 else 4)+(1 if age%10<3 else 0)
            if s==1: base=max(2,base-1)
            if s==2: base=max(2,base-2+(2 if age%8==0 else 0))
            for morning in ([True,False] if day%6==0 else [False]):
                level=min(9,base+(1 if morning else 0))
                records.append({'dayOffset':day,'time':('08:10' if morning else ['19:20','18:30','18:00'][s]),'intensity':level,'drawing':drawing(s,day,level,morning),'side':'front' if s==2 else 'back','symptoms':symptoms[s], 'note':('합성 예시. ' if lang=='ko' else 'Synthetic example. ')+notes[s][int(age<=28)]+((' 아침 기록.' if morning else ' 저녁 기록.') if lang=='ko' else (' Morning entry.' if morning else ' Evening entry.'))})
            if day%4==0:
                treatments.append({'dayOffset':day,'time':'12:30','type':'other' if s==2 else 'exercise','items':[items[s]],'note':'합성 활동 기록 · 효과를 뜻하지 않아요' if lang=='ko' else 'Synthetic activity log; no causal effect implied'})
        result['scenarios'].append(dict(name=names[s],records=records,treatments=treatments))
    return result

def generate(fixture,today):
    def ts(offset,time): return int(dt.datetime.combine(today+dt.timedelta(days=offset),dt.time.fromisoformat(time),TZ).timestamp()*1000)
    # Catalog labels are persisted Korean identifiers in the native app.
    # Keep readable EN fixtures in English; serialize canonical IDs so edit chips stay selected.
    canonical={'Stiff':'뻐근해요','Hurts after sitting a while':'오래 앉아 있으면 아파요','Changes when I shift position':'자세 바꾸면 달라져요','Throbbing':'욱신거려요','Only hurts when moving':'움직일 때만 아파요','Walking':'걷기','Stretching':'스트레칭','Rest':'휴식'}
    labels=lambda xs: [canonical.get(x,x) for x in xs]
    issues=[]; records=[]; treatments=[]
    for i,s in enumerate(fixture['scenarios'],1):
        for r in s['records']:
            records.append(dict(id=len(records)+1,painIssueId=i,timestamp=ts(r['dayOffset'],r['time']),intensity=r['intensity'],drawingDataJson=js(r['drawing']),side=r['side'],symptoms=js(labels(r['symptoms'])),note=r['note']))
        for t in s['treatments']:
            # Native TreatmentLog.notes is a JSON array of selected item labels.
            treatments.append(dict(id=str(uuid.uuid5(uuid.NAMESPACE_URL,f'tongda-sample/{i}/{t["dayOffset"]}')),painIssueId=i,timestamp=ts(t['dayOffset'],t['time']),type=t['type'],notes=js(labels(t['items']))))
        own=[r['timestamp'] for r in records if r['painIssueId']==i]
        issues.append(dict(id=i,name=s['name'],startDate=min(own),lastUpdated=max(own),status='Active'))
    return dict(app='Tongda',schema='native-v2',version=2,exportedAt=dt.datetime.now(TZ).isoformat(),counts=dict(issues=len(issues),records=len(records),treatments=len(treatments)),issues=issues,records=records,treatments=treatments)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--date',default=dt.datetime.now(TZ).date().isoformat());p.add_argument('--init',action='store_true');a=p.parse_args()
    for lang in ['ko','en']:
        source=ROOT/f'fixture-{lang}.json'
        if a.init or not source.exists(): source.write_text(json.dumps(make_fixture(lang),ensure_ascii=False,indent=2)+'\n')
        payload=generate(json.loads(source.read_text()),dt.date.fromisoformat(a.date))
        raw=json.dumps(payload,ensure_ascii=False,indent=2).encode()
        (ROOT/f'tongda-sample-{lang}.json').write_bytes(raw)
        (ROOT/f'tongda-sample-{lang}.tngd').write_bytes(encrypt(raw))
        print(lang,payload['counts'],a.date)
