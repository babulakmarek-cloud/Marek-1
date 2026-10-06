import sys, ezdxf
src = sys.argv[1]; d = ezdxf.readfile(src); m = d.modelspace()
n_before = len(m)
keep = set()
def walk(layout):
    for e in layout:
        if e.dxftype() == "INSERT": keep.add(e.dxf.name)
        if e.dxftype() == "DIMENSION" and e.dxf.hasattr("geometry"): keep.add(e.dxf.geometry)
for lay in d.layouts: walk(lay)
# šipky a bloky z kótovacích stylů
for ds in d.dimstyles:
    for a in ("dimblk","dimblk1","dimblk2","dimldrblk"):
        if ds.dxf.hasattr(a) and ds.dxf.get(a): keep.add(ds.dxf.get(a))
changed = True
while changed:
    changed = False
    for name in list(keep):
        if name in d.blocks:
            for e in d.blocks[name]:
                if e.dxftype()=="INSERT" and e.dxf.name not in keep: keep.add(e.dxf.name); changed = True
removed = 0
for blk in list(d.blocks):
    nm = blk.name
    if nm.startswith("*") or nm.startswith("_") or nm in keep: continue
    d.blocks.delete_block(nm, safe=False); removed += 1
d.saveas(src)
d2 = ezdxf.readfile(src)
print(src.split("/")[-1], "bloků smazáno", removed, "| prvků před/po", n_before, len(d2.modelspace()), "| OK" if n_before==len(d2.modelspace()) else "| CHYBA")
