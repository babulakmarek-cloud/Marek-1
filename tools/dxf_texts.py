import sys, json, re, collections, ezdxf
d = ezdxf.readfile(sys.argv[1]); m = d.modelspace(); out=[]
for e in m:
    t=e.dxftype()
    if t=="TEXT": s=e.dxf.text; p=e.dxf.insert
    elif t=="MTEXT": s=e.plain_text(); p=e.dxf.insert
    else: continue
    s=re.sub(r"\s+"," ",s).strip()
    if s: out.append({"t":s,"x":round(p.x),"y":round(p.y),"layer":e.dxf.layer})
json.dump(out,open(sys.argv[2],"w"),ensure_ascii=False)
print(len(out),"texts")
c=collections.Counter(o["layer"] for o in out); print(c.most_common(12))
hk=[o for o in out if re.search(r"heizk|radiator|P\s*[=≈]",o["t"],re.I)]
print("heating-body labels:",len(hk))
for o in hk[:12]: print("  ",o["t"],"|",o["layer"])
dn=collections.Counter(o["t"] for o in out if re.fullmatch(r"DN\s?\d+",o["t"]))
print("DN labels:",sum(dn.values()),dict(sorted(dn.items(),key=lambda kv:int(re.sub(r'\D','',kv[0])))))
