import sys, math, collections, ezdxf
from ezdxf import path as ezpath
d = ezdxf.readfile(sys.argv[1]); m = d.modelspace()
L = collections.defaultdict(float); N = collections.Counter()
for e in m:
    ly = e.dxf.layer
    if not ly.lower().startswith("heiz"): continue
    t = e.dxftype()
    try:
        if t == "LINE": l = e.dxf.start.distance(e.dxf.end)
        elif t in ("LWPOLYLINE","POLYLINE","ARC","SPLINE","ELLIPSE","CIRCLE"):
            p = ezpath.make_path(e); l = p.length() if hasattr(p,"length") else 0
        else: continue
    except Exception: continue
    L[ly] += l; N[ly] += 1
print(f"{'layer':45s} {'entities':>8s} {'length_m':>10s}")
for k in sorted(L): print(f"{k:45s} {N[k]:8d} {L[k]/1000:10.1f}")
