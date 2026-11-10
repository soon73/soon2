import json,re
files="l1a l1b l1c l2a l2b l2c l3a l3b l3c l4a l4b l5a l5b".split()
out=[];seen=set();cur=None;lv=0;dups=[];bad=[]
groups=[]  # (lv,header,[lines])
for f in files:
    for ln in open(f'data/{f}.txt',encoding='utf-8'):
        ln=ln.rstrip('\n')
        if not ln.strip(): continue
        if ln.startswith('@'): lv=int(ln[1]); continue
        if ln.startswith('#'):
            if len(ln[1:].split('|'))<5: bad.append(ln)
            cur=[lv,ln,[]]; groups.append(cur); continue
        p=ln.split('|')
        if len(p)<3 or not p[0] or not p[1] or not p[2]: bad.append(ln); continue
        w=p[0].lower()
        if w in seen: dups.append((w,cur[1][:20])); continue
        seen.add(w); cur[2].append(ln)
txt=[];counts={}
for lvl,h,ws in groups:
    if not ws: continue
    counts[lvl]=counts.get(lvl,0)+len(ws)
for L in range(1,6):
    txt.append(f'@{L}')
    for lvl,h,ws in groups:
        if lvl==L and ws:
            txt.append(h); txt+=ws
data='\n'.join(txt).replace('접력, 릴레이','교대 방식, 릴레이')
open('data.txt','w',encoding='utf-8').write(data)
print('counts',counts,'total',sum(counts.values()))
print('dups',dups); print('bad',bad)
t=open('template.html',encoding='utf-8').read()
assert '__DATA__' in t
open('index.html','w',encoding='utf-8').write(t.replace('__DATA__',json.dumps(data,ensure_ascii=False).replace('</','<\\/')))
