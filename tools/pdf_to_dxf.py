import sys, json, math, pymupdf, ezdxf
src, out_dxf, out_json, scale = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
K0 = 25.4/72*scale           # nominal pt -> real mm
doc = pymupdf.open(src); p = doc[0]; H = p.rect.height
import statistics
def calibrate():
    hs=[];vs=[]
    for d in p.get_drawings():
        for it in d["items"]:
            if it[0]!="l": continue
            a,b=it[1],it[2]
            if abs(a.y-b.y)<0.01 and abs(a.x-b.x)>20: hs.append(((a.x+b.x)/2,a.y,abs(a.x-b.x)))
            elif abs(a.x-b.x)<0.01 and abs(a.y-b.y)>20: vs.append((a.x,(a.y+b.y)/2,abs(a.y-b.y)))
    rs=[]
    for b in p.get_text("dict")["blocks"]:
        for l in b.get("lines",[]):
            for s in l["spans"]:
                t=s["text"].strip().replace(",",".")
                try: v=float(t)
                except: continue
                if not 1500<=v<=60000: continue
                x0,y0,x1,y1=s["bbox"]; cx=(x0+x1)/2; cy=(y0+y1)/2
                dx,dy=l["dir"]
                pool = [(sx,sy,L) for sx,sy,L in hs if abs(sx-cx)<4 and abs(sy-cy)<14] if abs(dy)<0.1 else [(sx,sy,L) for sx,sy,L in vs if abs(sy-cy)<4 and abs(sx-cx)<14]
                for _,_,L in pool:
                    r=L*K0/v
                    if 0.9<r<1.1: rs.append(r)
    if len(rs)<5: return 1.0,len(rs),None
    m=statistics.median(rs); good=[r for r in rs if abs(r-m)<0.004]
    return (statistics.median(good) if len(good)>=5 else 1.0), len(good), len(rs)
CAL,ncal,nall=calibrate()
K=K0/CAL
print("calibration factor",round(CAL,4),"matches",ncal,"of",nall,"=> effective scale 1:%.1f"%(scale/CAL))
def P(pt): return (pt.x*K, (H-pt.y)*K)
names = {(0,0,0):"BLACK",(1,0,0):"RED",(1,.5,0):"ORANGE",(1,0,1):"MAGENTA",(0,0,1):"BLUE",(0,1,0):"GREEN",(1,1,0):"YELLOW"}
def lay(col):
    if not col: return "NOCOLOR"
    k = tuple(round(v,2) for v in col)
    if k in names: return names[k]
    return "C%02X%02X%02X" % tuple(int(round(v*255)) for v in col)
dxf = ezdxf.new("R2010"); dxf.units = 4; msp = dxf.modelspace()
def ensure(l):
    if l not in dxf.layers: dxf.layers.add(l)
n=0
for d in p.get_drawings():
    col = d.get("color") or d.get("fill"); L = lay(col); ensure(L)
    for it in d["items"]:
        t = it[0]
        if t=="l":
            msp.add_line(P(it[1]),P(it[2]),dxfattribs={"layer":L}); n+=1
        elif t=="re":
            r=it[1]; pts=[P(pymupdf.Point(r.x0,r.y0)),P(pymupdf.Point(r.x1,r.y0)),P(pymupdf.Point(r.x1,r.y1)),P(pymupdf.Point(r.x0,r.y1))]
            msp.add_lwpolyline(pts,close=True,dxfattribs={"layer":L}); n+=1
        elif t=="qu":
            q=it[1]; msp.add_lwpolyline([P(q.ul),P(q.ur),P(q.lr),P(q.ll)],close=True,dxfattribs={"layer":L}); n+=1
        elif t=="c":
            pts=[P(x) for x in it[1:5]]
            msp.add_spline(fit_points=None, control_points=pts, degree=3, dxfattribs={"layer":L}) if False else None
            # approximate bezier by 6 segments
            p0,p1,p2,p3=it[1:5]
            prev=P(p0)
            for i in range(1,7):
                u=i/6; a=(1-u)**3;b=3*u*(1-u)**2;c=3*u*u*(1-u);e=u**3
                x=a*p0.x+b*p1.x+c*p2.x+e*p3.x; y=a*p0.y+b*p1.y+c*p2.y+e*p3.y
                cur=P(pymupdf.Point(x,y)); msp.add_line(prev,cur,dxfattribs={"layer":L}); prev=cur
            n+=1
ensure("TEXT"); texts=[]
for b in p.get_text("dict")["blocks"]:
    for l in b.get("lines",[]):
        for s in l["spans"]:
            t=s["text"].strip()
            if not t: continue
            x0,y0,x1,y1=s["bbox"]; dx,dy=l["dir"]; ang=math.degrees(math.atan2(-dy,dx))
            o=P(pymupdf.Point(*s["origin"])); h=s["size"]*K*0.7
            msp.add_text(t,height=max(h,1),rotation=ang,dxfattribs={"layer":"TEXT","insert":o})
            texts.append({"t":t,"x":round((x0+x1)/2*K,1),"y":round((H-(y0+y1)/2)*K,1),"ang":round(ang),"size":round(s["size"],1),"color":"%06X"%s["color"]})
dxf.saveas(out_dxf); json.dump(texts,open(out_json,"w"),ensure_ascii=False)
print(src.split('/')[-1], "entities",n,"texts",len(texts))
