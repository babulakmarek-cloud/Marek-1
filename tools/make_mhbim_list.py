"""Sestaví vystupy/MHBIM_zadavaci_list.xlsx ze soupisů podlaží a System_Uebersicht_Werk2.xlsx."""
import glob, os, re, openpyxl
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

V = "vystupy"
PODLAZI = [  # (soubor soupisu, podlaží, označení v Abgleich_Raumheizung)
    ("1UG_soupis.xlsx", "1.UG", "KG"), (None, "EG", "EG"), (None, "1.OG", "1.OG"), (None, "2.OG", "2.OG"),
    ("3OG_soupis.xlsx", "3.OG", "3.OG"), ("4OG_soupis.xlsx", "4.OG", "4.OG"), ("5OG_soupis.xlsx", "5.OG", "5.OG"),
    ("6OG_soupis.xlsx", "6.OG", "6.OG"), ("Dachbereich_Aussentank_soupis.xlsx", "Dachbereich / Außentank", None),
    ("Versorgungsgang_soupis.xlsx", "Versorgungsgang", None), ("Sozialgebaeude_soupis.xlsx", "Sozialgebäude", None),
]
DXF_STAV = {"1.UG": "Drive, >10 MB – číst lokálně", "EG": "jen DWG (107 MB)", "1.OG": "DXF 904 MB – PURGE/WBLOCK",
            "2.OG": "DXF 791 MB – PURGE/WBLOCK", "3.OG": "Drive, >10 MB – číst lokálně", "4.OG": "Drive, >10 MB – číst lokálně",
            "5.OG": "Drive, >10 MB – číst lokálně"}
SYSTEMY = [  # hladina (regex) -> systém v MH BIM
    (r"\+60 -Heizkörper Vorlauf|\+50 -Heizkörper R", "Raumheizung", "60/50", "Statická otopná tělesa (Gussheizkörper, Plattenheizkörper)"),
    (r"\+90 Klima V|\+70 Klima R", "Klimaheizung / Lüftung", "90/70 dle hladin; topologie uvádí 70/55", "Ohřívače VZT – ROZPOR teplot, ověřit"),
    (r"\+90 Prozess V|\+70 Prozess R", "Prozessheizung", "90/70", "Technologie (tanky, Conchen, W+D)"),
    (r"\+60 Prozess V|\+50 Prozess R", "Prozessheizung NT", "60/50", "Procesní okruhy 60/50"),
    (r"\+45 Prozess V|\+35 Prozess R", "Prozessheizung 45/35", "45/35", "pravděpodobně OPM1 (KH4 45/35) – ověřit"),
    (r"blind", "—", "—", "slepé/odpojené potrubí – nemodelovat, jen poznámka"),
    (r"^HEIZUNG|^Heizung", "nezařazeno", "?", "hladina bez teploty (6.OG, Versorggang, Dach) – zařadit podle výkresu"),
]

wb = openpyxl.Workbook(); wb.remove(wb.active)
B = Font(bold=True); FILL = PatternFill("solid", fgColor="FFF2CC")

def sheet(name, head, rows, widths=None):
    ws = wb.create_sheet(name); ws.append(head)
    for c in ws[1]: c.font = B
    for r in rows: ws.append(r)
    for i, _ in enumerate(head, 1):
        ws.column_dimensions[get_column_letter(i)].width = (widths or {}).get(i, 22)
    ws.freeze_panes = "A2"; ws.auto_filter.ref = ws.dimensions
    return ws

sys_wb = openpyxl.load_workbook(os.path.join(V, "System_Uebersicht_Werk2.xlsx"), read_only=True)
abg = list(sys_wb["Abgleich_Raumheizung"].iter_rows(values_only=True))
q_abg = {r[3]: r[8] for r in abg[1:] if r[2] == "KH2(1.OG).5.13.0"}

# 1) Podlaží
rows, tel, hladiny = [], [], {}
for f, pod, kod in PODLAZI:
    n = s = 0
    if f:
        x = openpyxl.load_workbook(os.path.join(V, f), read_only=True)
        for r in list(x["Otopná tělesa"].iter_rows(values_only=True))[1:]:
            cnt = r[1] or 1; n += cnt; s += (r[2] or 0)
            tel.append([pod, r[0], cnt, r[2], r[4], r[5], r[6], "", "", ""])
        for r in list(x["Potrubí dle hladin"].iter_rows(values_only=True))[1:]:
            hladiny.setdefault(r[0], {})[pod] = r[4]
    hotovo = pod == "6.OG"
    rows.append([pod, "ano" if f else "NE", DXF_STAV.get(pod, "DXF čitelné (příloha)"), n if f else None, s if f else None,
                 q_abg.get(kod), "", "24331,68325 (osa 39 × E)" if hotovo else "",
                 "podklad hotov: vystupy/podklady_mhbim/6OG_*.dxf" if hotovo else "", ""])
ws = sheet("Podlaží", ["Podlaží", "Soupis hotov", "Podklad DXF/DWG", "Počet těles (výkres)", "Σ výkon těles W (výkres, nejbližší popisek)",
                       "Q Hochbau BA.A dle Abgleich W (jen Vt 01, odhad)", "Výška podlaží / kóta (doplnit)", "Vztažný bod X,Y (doplnit)",
                       "Čistý podklad / vložen v MH BIM", "Poznámka"], rows, {1: 24, 3: 30, 5: 26, 6: 26})
ws.append([]); ws.append(["Pozn.: Σ výkon z výkresu ≠ Q z Abgleich – Abgleich uvádí jen BA.A přes Verteiler 01 a jde o odhady; "
                          "výkres obsahuje všechna tělesa podlaží. Slouží jen jako hrubá kontrola. U '3x …' není ověřeno, zda výkon platí na kus. 1.UG je přiřazeno ke KG z Abgleich (předpoklad)."])

# 2) Systémy (hladiny -> okruhy)
rows = []
for ly in sorted(hladiny):
    m = next((s for s in SYSTEMY if re.search(s[0], ly, re.I)), (None, "?", "?", ""))
    rows.append([ly, m[1], m[2], m[3]] + [hladiny[ly].get(p[1]) for p in PODLAZI if p[0]])
sheet("Systémy z hladin", ["Hladina DXF", "Systém v MH BIM", "Teploty VL/RL °C", "Poznámka"] + [f"{p[1]} m" for p in PODLAZI if p[0]],
      rows, {1: 40, 2: 24, 3: 26, 4: 48})

# 3) Otopná tělesa
sheet("Otopná tělesa", ["Podlaží", "Popisek z výkresu", "Počet", "Výkon W (popisek P≈)", "X mm", "Y mm", "Hladina",
                        "Místnost (RaumGEO)", "Zadáno v MH BIM", "Poznámka"], tel, {2: 40, 7: 36, 8: 22})

# 4) Rozdělovače a 5) okruhy – převzato
for src, dst in (("Verteiler_Register", "Rozdělovače"), ("Abgleich_Raumheizung", "Okruhy Raumheizung"), ("Pumpenregister", "Čerpadla")):
    r = list(sys_wb[src].iter_rows(values_only=True))
    ws = sheet(dst, list(r[0]) + ["Zadáno v MH BIM"], [list(x) + [""] for x in r[1:]], {2: 40})

# 6) Kontrolní seznam
kroky = [
    ("0", "Projekt", "Založit projekt v mh-Projektverwaltung (lokální disk s písmenem, ne UNC/cloud)."),
    ("0", "Projekt", "Zadat Liegenschaft: Brembocher Str. 37 (pravopis dle PDF – ověřit), 79589 Lörrach; klimadata dle lokality (DWD TRY)."),
    ("1", "Podklady", "Pro každé podlaží: tools/mhbim_podklad.py --seznam, pak export čistého DXF se SPOLEČNÝM vztažným bodem."),
    ("1", "Podklady", "Vztažný bod = průsečík osy 39 a osy E (v 6.OG X=24331, Y=68325). Ověřit, že ostatní podlaží mají stejnou osovou síť a souřadnice. Sozialgebäude má jiný souřadný systém (X≈-1,5 mil.) – posun nutný."),
    ("1", "Podklady", "1.OG, 2.OG: v AutoCADu nejdřív PURGE/AUDIT/WBLOCK (DXF 790–900 MB). EG: DWG→DXF v AutoCADu / ODA."),
    ("2", "Budova", "Založit podlaží a kóty/výšky (list Podlaží – sloupec G)."),
    ("2", "Budova", "Vložit podkladové DXF do každého podlaží, zkontrolovat jednotky mm a překryv podlaží."),
    ("3", "RaumGEO", "Obkreslit zdi a místnosti nad podkladem (automatické rozpoznání zdí z DWG nenalezeno)."),
    ("4", "Topení", "Zdroj LOOS B+C v KH2 (1.OG), hlavní rozdělovač KH2 Q.1.08.1, podružné KH4 (6.OG), KH6 (SG) – list Rozdělovače."),
    ("4", "Topení", "Okruhy podle teplot: 60/50 Raumheizung, 90/70 Prozess, 70/55 Klima (ROZPOR s hladinami +90/+70 – rozhodnout)."),
    ("4", "Topení", "Otopná tělesa umístit podle X/Y z listu Otopná tělesa (po odečtení vztažného bodu), výkon jako kontrolní hodnota."),
    ("4", "Topení", "Potrubí kreslit jako Systemlinien po trasách z podkladu; DN z výkresu jen pro kontrolu automatického dimenzování."),
    ("5", "Výpočet", "Dimenzování + hydraulické vyvážení v RohrSYS; porovnat průtoky s listem Okruhy Raumheizung (q_V_soll)."),
    ("6", "Výstup", "Export IFC 4 s mh-Data, DWG/PDF plány."),
]
sheet("Postup – checklist", ["Krok", "Oblast", "Úkol", "Hotovo", "Poznámka"], [list(k) + ["", ""] for k in kroky], {3: 110})

for ws in wb:
    for c in ws[1]: c.fill = FILL
wb.move_sheet("Postup – checklist", offset=-len(wb.sheetnames) + 1)
wb.save(os.path.join(V, "MHBIM_zadavaci_list.xlsx"))
print("ok", wb.sheetnames, len(tel), "těles")
