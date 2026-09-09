import re,device as d,sys,time
nodes=[n for n in d.dump().iter('node') if n.get('checkable')=='true' and n.get('class')=='android.view.View']
assert len(nodes)==1
n=nodes[0]; desired='true' if sys.argv[1]=='on' else 'false'
if n.get('checked')!=desired:
    x1,y1,x2,y2=map(int,re.findall(r'\d+',n.get('bounds'))); d.adb('shell','input','tap',str((x1+x2)//2),str((y1+y2)//2));time.sleep(.5)
