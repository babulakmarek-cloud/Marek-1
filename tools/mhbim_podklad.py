"""Příprava čistého podkladového DXF pro vložení do MH BIM.

Použití (lokálně na PC, potřeba: pip install ezdxf):
  python mhbim_podklad.py VSTUP.dxf --seznam
      vypíše hladiny s počtem prvků a navrženou skupinou (arch / heiz / -)
  python mhbim_podklad.py VSTUP.dxf VYSTUP.dxf [--profil arch|heiz|vse]
        [--hladiny REGEX] [--oblast XMIN,YMIN,XMAX,YMAX] [--posun X,Y] [--bez-kot] [--bez-srafy]

Co dělá:
  - v modelovém prostoru ponechá jen prvky na vybraných hladinách,
  - volitelně ponechá jen prvky v obdélníku --oblast (např. bez situace/Lageplanu a rohového razítka),
  - volitelně smaže kóty (DIMENSION) a šrafy (HATCH),
  - vyprázdní výkresové listy (paperspace),
  - odstraní nepoužité bloky a hladiny (purge),
  - volitelně posune celý výkres o -X,-Y (společný vztažný bod pro všechna podlaží),
  - nastaví jednotky mm a uloží DXF ve stejné verzi jako vstup (Werk 2: AC1024 = AutoCAD 2010).
Záporné hodnoty zapisuj se rovnítkem, jinak je argparse vezme jako přepínač:
  --oblast=-7000,15000,80000,102000   --posun=-1530000,-1960000
Výchozí skupiny hladin vycházejí z názvů ve výkresech Werk 2
(A0… + Nord-Pfeil = stavba/kóty/osy/text, Heiz…/HEIZUNG… = topení). U jiných výkresů nejdřív --seznam.
"""
import argparse, collections, re, sys
import ezdxf
from ezdxf import bbox

PROFILY = {
    "arch": r"^(A0|0$|Nord-Pfeil)",
    "heiz": r"^(heiz|heizung)",
    "vse":  r"^(A0|0$|Nord-Pfeil|heiz|heizung)",
}


def skupina(layer):
    for k in ("arch", "heiz"):
        if re.search(PROFILY[k], layer, re.I):
            return k
    return "-"


def pouzite_bloky(doc):
    """Názvy bloků použitých v modelu (rekurzivně přes vnořené bloky)."""
    used, fronta = set(), [doc.modelspace()]
    while fronta:
        for e in fronta.pop():
            if e.dxftype() == "INSERT" and e.dxf.name not in used:
                used.add(e.dxf.name)
                if e.dxf.name in doc.blocks:
                    fronta.append(doc.blocks[e.dxf.name])
            if e.dxftype() == "DIMENSION" and e.dxf.hasattr("geometry"):
                used.add(e.dxf.geometry)
    return used


def purge(doc):
    used = pouzite_bloky(doc)
    # bloky šipek ve stylech kót a odkazovaných objektech nesmí zmizet
    for ds in doc.dimstyles:
        for atr in ("dimblk", "dimblk1", "dimblk2", "dimldrblk"):
            if ds.dxf.hasattr(atr):
                used.add(ds.dxf.get(atr))
    used |= {doc.header.get(k) for k in ("$DIMBLK", "$DIMBLK1", "$DIMBLK2", "$DIMLDRBLK")} - {None, ""}
    smazano_b = 0
    for b in list(doc.blocks):
        n = b.name
        if n.startswith("*") and n.upper().startswith(("*MODEL_SPACE", "*PAPER_SPACE")):
            continue
        if n not in used:
            try:
                doc.blocks.delete_block(n, safe=True)
                smazano_b += 1
            except Exception:
                pass
    pouzite_h = {"0", "Defpoints"}
    for e in doc.modelspace():
        pouzite_h.add(e.dxf.layer)
    for b in doc.blocks:
        for e in b:
            pouzite_h.add(e.dxf.layer)
    smazano_h = 0
    for ly in list(doc.layers):
        if ly.dxf.name not in pouzite_h:
            try:
                doc.layers.remove(ly.dxf.name)
                smazano_h += 1
            except Exception:
                pass
    for nazev, skup in list(doc.groups):
        if not any(True for _ in skup):  # iterace vrací jen živé prvky
            doc.groups.delete(nazev)
    return smazano_b, smazano_h


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("vstup")
    ap.add_argument("vystup", nargs="?")
    ap.add_argument("--seznam", action="store_true", help="jen vypsat hladiny")
    ap.add_argument("--profil", choices=PROFILY, default="vse")
    ap.add_argument("--hladiny", help="vlastní regex hladin (přepíše --profil)")
    ap.add_argument("--oblast", help="XMIN,YMIN,XMAX,YMAX v mm (původní souřadnice); prvky, jejichž střed leží mimo, se smažou")
    ap.add_argument("--posun", help="vztažný bod X,Y v mm; výkres se posune o -X,-Y")
    ap.add_argument("--bez-kot", action="store_true")
    ap.add_argument("--bez-srafy", action="store_true")
    a = ap.parse_args()

    doc = ezdxf.readfile(a.vstup)
    msp = doc.modelspace()

    if a.seznam or not a.vystup:
        c = collections.Counter(e.dxf.layer for e in msp)
        print(f"{'prvků':>8}  skupina  hladina")
        for ly, n in sorted(c.items(), key=lambda x: (skupina(x[0]), -x[1])):
            print(f"{n:8d}  {skupina(ly):7s}  {ly}")
        return

    rx = re.compile(a.hladiny or PROFILY[a.profil], re.I)
    typy_pryc = set()
    if a.bez_kot:
        typy_pryc.add("DIMENSION")
    if a.bez_srafy:
        typy_pryc.add("HATCH")

    oblast = [float(v) for v in a.oblast.split(",")] if a.oblast else None

    def mimo(e):
        try:
            bb = bbox.extents([e], fast=True)
        except Exception:
            return False
        if not bb.has_data:
            return False
        c = bb.center
        return not (oblast[0] <= c.x <= oblast[2] and oblast[1] <= c.y <= oblast[3])

    pred = len(msp)
    for e in list(msp):
        if not rx.search(e.dxf.layer) or e.dxftype() in typy_pryc or (oblast and mimo(e)):
            msp.delete_entity(e)
    for lay in doc.layouts:
        if lay.name != "Model":
            for e in list(lay):
                lay.delete_entity(e)

    if a.posun:
        x, y = (float(v) for v in a.posun.split(","))
        for e in msp:
            try:
                e.translate(-x, -y, 0)
            except Exception as ex:  # nepodporovaný typ prvku
                print(f"posun neproveden: {e.dxftype()} ({ex})", file=sys.stderr)

    b, h = purge(doc)
    doc.units = ezdxf.units.MM
    doc.header["$INSUNITS"] = 4
    doc.saveas(a.vystup)
    print(f"prvků: {pred} -> {len(msp)}; smazáno bloků {b}, hladin {h}; uloženo {a.vystup}")


if __name__ == "__main__":
    main()
