import subprocess, pathlib, xml.etree.ElementTree as ET, re, sys, time, io
from PIL import Image
ROOT=pathlib.Path(__file__).resolve().parent
ADB='/Users/choi3/Library/Android/sdk/platform-tools/adb'
def adb(*args):return subprocess.check_output([ADB,'-s','emulator-5554',*args])
def dump():
    adb('shell','uiautomator','dump','/sdcard/window.xml')
    raw=adb('exec-out','cat','/sdcard/window.xml');(ROOT/'window.xml').write_bytes(raw)
    return ET.fromstring(raw)
def show():
    for n in dump().iter('node'):
        t=n.get('text') or n.get('content-desc')
        if t: print(t, n.get('bounds'), 'click='+str(n.get('clickable')))
def tap(label,long=False):
    nodes=[n for n in dump().iter('node') if label in [n.get('text'),n.get('content-desc')]]
    assert len(nodes)==1,(label,len(nodes))
    x1,y1,x2,y2=map(int,re.findall(r'\d+',nodes[0].get('bounds')));x,y=(x1+x2)//2,(y1+y2)//2
    adb('shell','input',*(['swipe',str(x),str(y),str(x),str(y),'900'] if long else ['tap',str(x),str(y)]));time.sleep(.6)
def snap(name):
    time.sleep(1.2)
    raw=adb('exec-out','screencap','-p');p=ROOT/(name+'.png');p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
    print(p)
def scroll(up=True):adb('shell','input','swipe','530','1850' if up else '600','530','650' if up else '1850','450');time.sleep(.5)
if __name__=='__main__':
    c=sys.argv[1]
    if c=='show':show()
    elif c=='tap':tap(sys.argv[2],len(sys.argv)>3)
    elif c=='snap':snap(sys.argv[2])
    elif c=='scroll':scroll(len(sys.argv)==2)
    elif c=='back':adb('shell','input','keyevent','4')
