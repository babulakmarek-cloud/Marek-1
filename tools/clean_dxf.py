import sys, re, collections, ezdxf
src, dst, report = sys.argv[1], sys.argv[2], sys.argv[3]
KEEP = re.compile(r"^(A0_Grundri|A0_Grundriß|A03_T|A04_Treppen|A05_Bema|A06_Text|A07_Achs|Heiz|HEIZUNG|Armaturen|Geometrie$|Geometrie_Bestand|Nord-Pfeil|Maßstab|Defpoints)", re.I)
d = ezdxf.readfile(src); m = d.modelspace()
kept = collections.Counter(); dropped = collections.Counter()
for e in list(m):
    ly = e.dxf.layer
    if KEEP.match(ly): kept[ly] += 1
    else: dropped[ly] += 1; m.delete_entity(e)
d.saveas(dst)
with open(report,"w") as f:
    f.write("ponecháno\tprvků\n"); [f.write(f"{k}\t{v}\n") for k,v in kept.most_common()]
    f.write("\nodstraněno\tprvků\n"); [f.write(f"{k}\t{v}\n") for k,v in dropped.most_common()]
print(src.split("/")[-1], "kept", sum(kept.values()), "dropped", sum(dropped.values()))
