import sys, math, collections, ezdxf
from ezdxf import path as ezpath
T = collections.Counter()
d = ezdxf.readfile(sys.argv[1]); m = d.modelspace()
L = collections.defaultdict(float); N = collections.Counter()
for e in m:
    ly = e.dxf.layer
    if not ly.lower().startswith("heiz"): continue
    t = e.dxftype()
    try:
        if t == "LINE": l = e.dxf.start.distance(e.dxf.end)
        elif t in ("LWPOLYLINE","POLYLINE","ARC","SPLINE"):
            if t in ("LWPOLYLINE","POLYLINE") and e.is_closed: continue  # uzavřené = symboly těles, ne trubky
            pts = list(ezpath.make_path(e).flattening(distance=1.0))
            l = sum(a.distance(b) for a, b in zip(pts, pts[1:]))
        else: continue
    except Exception: continue
    L[ly] += l; N[ly] += 1; T[t] += 1
print(f"{'layer':45s} {'entities':>8s} {'length_m':>10s}")
for k in sorted(L): print(f"{k:45s} {N[k]:8d} {L[k]/1000:10.1f}")
