#!/usr/bin/env python3
"""Generuje elektrikar/Pomucka_elektrikare.xlsx (živé vzorce). Spuštění: python3 build_xlsx.py"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import AMP, KT, KG
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Pomucka_elektrikare.xlsx')
INP = PatternFill('solid', fgColor='FFF2CC')
OUTF = PatternFill('solid', fgColor='E8F0FC')
HEAD = PatternFill('solid', fgColor='0B63D1')
SUB = PatternFill('solid', fgColor='D9E0E8')
thin = Side(style='thin', color='B8C2CE')
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
GOOD = PatternFill('solid', fgColor='C6EFCE')
BADF = PatternFill('solid', fgColor='FFC7CE')

wb = Workbook()
wb.remove(wb.active)


class Sheet:
    def __init__(self, title, intro='', widths=(42, 16, 16)):
        self.ws = wb.create_sheet(title)
        self.r = 1
        ws = self.ws
        for i, w in enumerate(widths):
            ws.column_dimensions[chr(65 + i)].width = w
        ws['A1'] = title
        ws['A1'].font = Font(size=15, bold=True, color='0B63D1')
        self.r = 2
        if intro:
            ws.cell(self.r, 1, intro).font = Font(italic=True, color='5B6877')
            ws.cell(self.r, 1).alignment = Alignment(wrap_text=False)
            self.r += 1
        self.r += 1

    def head(self, text):
        c = self.ws.cell(self.r, 1, text)
        for col in (1, 2, 3):
            self.ws.cell(self.r, col).fill = HEAD
        c.font = Font(bold=True, color='FFFFFF')
        self.r += 1

    def inp(self, label, val, unit='', options=None, fmt=None):
        ws = self.ws
        ws.cell(self.r, 1, label)
        c = ws.cell(self.r, 2, val)
        c.fill = INP
        c.border = BOX
        c.font = Font(color='0000FF', bold=True)
        if fmt:
            c.number_format = fmt
        ws.cell(self.r, 3, unit).font = Font(color='5B6877')
        if options:
            dv = DataValidation(type='list', formula1='"' + ','.join(str(o) for o in options) + '"', allow_blank=False)
            ws.add_data_validation(dv)
            dv.add(c)
        addr = f'$B${self.r}'
        self.r += 1
        return addr

    def calc(self, label, formula, unit='', fmt='0.00', bold=False):
        ws = self.ws
        ws.cell(self.r, 1, label)
        c = ws.cell(self.r, 2, formula)
        c.fill = OUTF
        c.border = BOX
        c.number_format = fmt
        c.font = Font(bold=bold)
        c.alignment = Alignment(horizontal='right')
        ws.cell(self.r, 3, unit).font = Font(color='5B6877')
        addr = f'$B${self.r}'
        self.r += 1
        return addr

    def note(self, text):
        c = self.ws.cell(self.r, 1, text)
        c.font = Font(italic=True, size=9, color='5B6877')
        self.r += 1

    def gap(self, n=1):
        self.r += n

    def status_cf(self, rng):
        self.ws.conditional_formatting.add(rng, FormulaRule(formula=[f'ISNUMBER(SEARCH("OK",{rng.split(":")[0]}))'], fill=GOOD))
        self.ws.conditional_formatting.add(rng, FormulaRule(formula=[f'ISNUMBER(SEARCH("CHYBA",{rng.split(":")[0]}))'], fill=BADF))
        self.ws.conditional_formatting.add(rng, FormulaRule(formula=[f'ISNUMBER(SEARCH("POZOR",{rng.split(":")[0]}))'], fill=PatternFill('solid', fgColor='FFEB9C')))


def table(ws, r0, c0, header, rows, widths=None, numfmt=None):
    for j, h in enumerate(header):
        c = ws.cell(r0, c0 + j, h)
        c.font = Font(bold=True)
        c.fill = SUB
        c.border = BOX
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            c = ws.cell(r0 + 1 + i, c0 + j, v)
            c.border = BOX
            if numfmt and j in numfmt:
                c.number_format = numfmt[j]


RHO = lambda mat, th: f'IF({mat}="Cu",1/56,1/35)*(1+IF({mat}="Cu",0.00393,0.00403)*({th}-20))'
SIZES = [1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120]
SIZES_ALL = SIZES + [150, 185, 240]
STD = [6, 10, 13, 16, 20, 25, 32, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630]

# ------------------------------------------------------------------ NÁVOD
s = Sheet('Návod', widths=(110,))
ws = s.ws
for line in [
    'Žlutá buňka = vstup (měň), modrá buňka = výsledek (vzorec). Listy odpovídají záložkám webové pomůcky.',
    '',
    'Elektroinstalace: Úbytek napětí | Zatížitelnost | Smyčka | Výkon a kompenzace | Bilance příkonu',
    'FVE: FVE string | FVE kabel a jištění | FVE výnos | FVE baterie a řady',
    'MaR: MaR škálování | MaR čidla | MaR regulace a hydraulika',
    'Tabulky a Checklisty.',
    '',
    'Výpočty jsou orientační. Rozhoduje projekt, platné normy a odpovědnost oprávněné osoby.',
    'Tabulky zatížitelnosti: IEC 60364-5-52 / ČSN 33 2000-5-52 (Cu, 30 °C). Před použitím v projektu ověřte proti aktuálnímu vydání normy.',
    'List Zatížitelnost obsahuje i pomocné tabulky (korekce, typizované In), na které se odkazují ostatní listy. Neodstraňujte je.',
]:
    ws.cell(s.r, 1, line)
    s.r += 1

# ------------------------------------------------------------------ ÚBYTEK NAPĚTÍ
s = Sheet('Úbytek napětí', 'ΔU = k·I·L·(R′cosφ + X′sinφ), X′ = 0,08 mΩ/m', widths=(44, 16, 14, 3, 12, 14, 16))
ws = s.ws
s.head('Vstupy')
sys_ = s.inp('Soustava (1 = 1f 230 V, 3 = 3f 400 V)', 3, '', [1, 3])
P = s.inp('Výkon', 11, 'kW')
Iin = s.inp('Proud (volitelně, přepíše výkon)', None, 'A')
cos = s.inp('cos φ', 0.95)
L = s.inp('Délka vedení (jednosměrně)', 40, 'm')
mat = s.inp('Materiál', 'Cu', '', ['Cu', 'Al'])
th = s.inp('Teplota vodiče', 70, '°C')
S = s.inp('Průřez', 6, 'mm²', SIZES_ALL)
lim = s.inp('Povolený úbytek', 3, '%')
s.gap()
s.head('Výsledky')
U = s.calc('Napětí', f'=IF({sys_}=1,230,400)', 'V', '0')
I = s.calc('Proud', f'=IF({Iin}<>"",{Iin},{P}*1000/(IF({sys_}=1,1,SQRT(3))*{U}*{cos}))', 'A')
rho = s.calc('Rezistivita při provozní teplotě', '=' + RHO(mat, th), 'Ω·mm²/m', '0.00000')
kU = f'IF({sys_}=1,2,SQRT(3))'
dU = s.calc('Úbytek napětí', f'={kU}*{I}*{L}*({rho}/{S}*{cos}+0.00008*SQRT(1-{cos}^2))', 'V')
pct = s.calc('Úbytek v %', f'={dU}/{U}*100', '%', '0.00', True)
s.calc('Hodnocení', f'=IF({pct}<={lim},"OK – vyhovuje","CHYBA – překročeno")', '', '@')
r_first = 5
minS = s.calc('Min. průřez pro daný limit', f'=IFERROR(INDEX($E$5:$E$19,MATCH(TRUE,INDEX($F$5:$F$19<={lim},0),0)),"> 240 mm²")', 'mm²', '0.0', True)
s.calc('Ztráty ve vedení', f'=IF({sys_}=1,2,3)*{I}^2*{rho}/{S}*{L}', 'W', '0')
s.status_cf(f'B{s.r-3}:B{s.r-3}')
table(ws, 4, 5, ['Průřez mm²', 'ΔU %', 'Stav'],
      [[sz, f'={kU}*{I}*{L}*({rho}/E{5+i}*{cos}+0.00008*SQRT(1-{cos}^2))/{U}*100',
        f'=IF(F{5+i}<={lim},"OK","CHYBA")'] for i, sz in enumerate(SIZES_ALL)], numfmt={1: '0.00'})
s.status_cf('G5:G19')

# ------------------------------------------------------------------ ZATÍŽITELNOST

s = Sheet('Zatížitelnost', 'Podmínka Ib ≤ In ≤ Iz. Cu, 2 resp. 3 zatížené vodiče, IEC 60364-5-52', widths=(40, 14, 14, 3, 12, 14, 12))
ws = s.ws
s.head('Vstupy')
Ib = s.inp('Návrhový proud Ib', 32, 'A')
ins = s.inp('Izolace', 'PVC', '', ['PVC', 'XLPE'])
meth = s.inp('Způsob uložení', 'C', '', ['A1', 'B1', 'B2', 'C'])
nn = s.inp('Zatížené vodiče', 3, '', [2, 3])
cm = s.inp('Materiál', 'Cu', '', ['Cu', 'Al'])
ta = s.inp('Teplota okolí', 30, '°C', [10,15,20,25,30,35,40,45,50,55,60])
ng = s.inp('Seskupené obvody', 1, '', [1,2,3,4,5,6,7,8,9,12,16,20])
s.gap()
s.head('Výsledky')
kt = s.calc('Součinitel teploty', f'=VLOOKUP({ta},$A$50:$C$60,IF({ins}="PVC",2,3),FALSE)', '', '0.00')
kg = s.calc('Součinitel seskupení', f'=VLOOKUP({ng},$E$50:$F$61,2,FALSE)', '', '0.00')
f = s.calc('Celkový součinitel (× 0,78 pro Al)', f'={kt}*{kg}*IF({cm}="Al",0.78,1)', '', '0.000')
In = s.calc('Jistič In (nejbližší ≥ Ib)', f'=IFERROR(INDEX($H$50:$H$69,MATCH(TRUE,INDEX($H$50:$H$69>={Ib},0),0)),"> 630")', 'A', '0', True)
row = s.calc('Pomocný index řádku dat', f'=MATCH({ins}&"|"&{meth}&"|"&{nn},$B$30:$B$45,0)', '', '0')
s.calc('Min. průřez', f'=IFERROR(INDEX($E$5:$E$16,MATCH(TRUE,INDEX($F$5:$F$16>={In},0),0)),"mimo tabulku")', 'mm²', '0.0', True)
table(ws, 4, 5, ['mm²', 'Iz (A)', 'max In (A)'],
      [[sz, f'=IF(AND({cm}="Al",E{5+i}<16),0,INDEX($C$30:$N$45,{row},MATCH(E{5+i},$C$29:$N$29,0))*{f})',
        f'=IFERROR(LOOKUP(F{5+i},$H$50:$H$69),"–")'] for i, sz in enumerate(SIZES)], numfmt={1: '0.0'})
ws.cell(28, 1, 'Pomocná data: zatížitelnost při 30 °C [A], Cu').font = Font(bold=True)
table(ws, 29, 2, ['Klíč (izolace|metoda|vodiče)'] + SIZES, [])
ws.cell(29, 2).value = 'Klíč'
r = 30
for insk in ('PVC', 'XLPE'):
    for m in ('A1', 'B1', 'B2', 'C'):
        for n in (2, 3):
            ws.cell(r, 2, f'{insk}|{m}|{n}').border = BOX
            for j, v in enumerate(AMP[insk][m][n]):
                ws.cell(r, 3 + j, v).border = BOX
            r += 1
for j, sz in enumerate(SIZES):
    ws.cell(29, 3 + j, sz).font = Font(bold=True)
table(ws, 49, 1, ['Teplota °C', 'PVC', 'XLPE'], [[k, v[0], v[1]] for k, v in KT.items()])
table(ws, 49, 5, ['Obvodů', 'k'], [[k, v] for k, v in KG.items()])
table(ws, 49, 8, ['Typiz. In'], [[v] for v in STD])
ws.column_dimensions['B'].width = 16

# ------------------------------------------------------------------ SMYČKA
s = Sheet('Smyčka', 'Podmínka odpojení: Zs ≤ U₀/Ia, Ia = k·In (B 5×, C 10×, D 20×)')
U0 = s.inp('Fázové napětí U₀', 230, 'V')
ch = s.inp('Charakteristika', 'B', '', ['B', 'C', 'D'])
Inl = s.inp('Jmenovitý proud In', 16, 'A')
z0 = s.inp('Impedance před obvodem Zs₀', 0.3, 'Ω')
Ll = s.inp('Délka vedení', 60, 'm')
sf = s.inp('Průřez fáze', 2.5, 'mm²')
spe = s.inp('Průřez PE', 2.5, 'mm²')
ml = s.inp('Materiál', 'Cu', '', ['Cu', 'Al'])
tl = s.inp('Teplota vodiče', 70, '°C')
s.gap()
s.head('Výsledky')
a = s.calc('Činný odpor R′ smyčky (fáze + PE)', f'={RHO(ml, tl)}*(1/{sf}+1/{spe})', 'Ω/m', '0.00000')
Zc = s.calc('Impedance vedení', f'=SQRT(({a}*{Ll})^2+(0.00016*{Ll})^2)', 'Ω', '0.000')
Zs = s.calc('Zs celkem', f'={z0}+{Zc}', 'Ω', '0.000', True)
Ia = s.calc('Ia (vybavovací proud)', f'=IF({ch}="B",5,IF({ch}="C",10,20))*{Inl}', 'A', '0')
Zm = s.calc('Zs,max = U₀/Ia', f'={U0}/{Ia}', 'Ω', '0.000')
s.calc('Zs,max pro měření (× 2/3)', f'={Zm}*2/3', 'Ω', '0.000')
s.calc('Hodnocení', f'=IF({Zs}<={Zm},"OK – vyhovuje","CHYBA – nevyhovuje")', '', '@')
s.status_cf(f'B{s.r-1}:B{s.r-1}')
s.calc('Zkratový proud na konci', f'={U0}/{Zs}', 'A', '0')
s.calc('Max. délka při těchto průřezech', f'=IF({Zm}>{z0},({Zm}-{z0})/SQRT({a}^2+0.00016^2),"–")', 'm', '0')
s.note('Doplňující ochrana RCD 30 mA se vyžaduje nezávisle. Skutečnou hodnotu ověřte měřením při revizi.')

# ------------------------------------------------------------------ VÝKON A KOMPENZACE
s = Sheet('Výkon a kompenzace')
s.head('Výkon ↔ proud')
ps = s.inp('Soustava (1 / 3)', 3, '', [1, 3])
pu = s.inp('Napětí (sdružené u 3f)', 400, 'V')
pc = s.inp('cos φ', 0.9)
pP = s.inp('Činný výkon P (vyplň P nebo I)', 11, 'kW')
pI = s.inp('Proud I (volitelně, přepíše P)', None, 'A')
k = f'IF({ps}=1,1,SQRT(3))'
cI = s.calc('Proud', f'=IF({pI}<>"",{pI},{pP}*1000/({k}*{pu}*{pc}))', 'A', '0.00', True)
cP = s.calc('Činný výkon P', f'={k}*{pu}*{cI}*{pc}/1000', 'kW')
cS = s.calc('Zdánlivý výkon S', f'={k}*{pu}*{cI}/1000', 'kVA')
s.calc('Jalový výkon Q', f'=SQRT(MAX({cS}^2-{cP}^2,0))', 'kvar')
s.gap()
s.head('Kompenzace účiníku')
kp = s.inp('Činný výkon P', 50, 'kW')
c1 = s.inp('Stávající cos φ', 0.8)
c2 = s.inp('Cílový cos φ', 0.98)
s.calc('Potřebný kompenzační výkon Qc', f'={kp}*(TAN(ACOS({c1}))-TAN(ACOS({c2})))', 'kvar', '0.00', True)

# ------------------------------------------------------------------ BILANCE
s = Sheet('Bilance příkonu', 'Instalovaný výkon × počet × soudobost. Proud pro 3f 400 V.', widths=(36, 14, 10, 12, 16, 16))
ws = s.ws
table(ws, 4, 1, ['Spotřebič', 'P (kW)', 'ks', 'β', 'Instalovaný', 'Soudobý'], [])
loads = [('Osvětlení', 3, 1, .8), ('Zásuvky', 6, 1, .5), ('Tepelné čerpadlo', 5, 1, 1), ('Indukční varná deska', 7, 1, .5), ('Wallbox', 11, 1, .6)] + [('', None, None, None)] * 7
for i, (n_, p_, k_, b_) in enumerate(loads):
    rr = 5 + i
    for j, v in enumerate((n_, p_, k_, b_)):
        c = ws.cell(rr, 1 + j, v)
        c.fill = INP
        c.border = BOX
    ws.cell(rr, 5, f'=IF(B{rr}="","",B{rr}*C{rr})').border = BOX
    ws.cell(rr, 6, f'=IF(B{rr}="","",B{rr}*C{rr}*D{rr})').border = BOX
last = 4 + len(loads)
s.r = last + 2
bc = s.inp('cos φ (průměr)', 0.95)
br = s.inp('Rezerva', 20, '%')
ei = s.calc('Instalovaný příkon', f'=SUM(E5:E{last})', 'kW')
es = s.calc('Soudobý příkon', f'=SUM(F5:F{last})', 'kW')
eI = s.calc('Soudobý proud (3f 400 V)', f'={es}*1000/(SQRT(3)*400*{bc})', 'A')
eR = s.calc('Proud s rezervou', f'={eI}*(1+{br}/100)', 'A')
s.calc('Hlavní jistič (min.)', f"=IFERROR(INDEX('Zatížitelnost'!$H$50:$H$69,MATCH(TRUE,INDEX('Zatížitelnost'!$H$50:$H$69>={eR},0),0)),\"> 630\")", 'A', '0', True)

# ------------------------------------------------------------------ FVE STRING
s = Sheet('FVE string', 'Voc za mrazu ≤ max. DC napětí; Vmpp za tepla ≥ dolní mez MPPT', widths=(44, 14, 14))
s.head('Panel (STC)')
pm = s.inp('Pmax', 440, 'Wp')
voc = s.inp('Voc', 40.3, 'V')
vmp = s.inp('Vmpp', 33.9, 'V')
isc = s.inp('Isc', 13.9, 'A')
imp = s.inp('Impp', 13.0, 'A')
tkv = s.inp('TK Voc', -0.27, '%/°C')
tkm = s.inp('TK Vmpp', -0.30, '%/°C')
s.head('Střídač')
vdc = s.inp('Max. DC napětí', 1000, 'V')
vlo = s.inp('MPPT od', 160, 'V')
vhi = s.inp('MPPT do', 850, 'V')
imx = s.inp('Max. proud / MPPT', 16, 'A')
iscx = s.inp('Max. Isc / MPPT', 22, 'A')
nM = s.inp('Počet MPPT', 2)
pac = s.inp('Jmenovitý AC výkon', 10, 'kW')
s.head('Podmínky a konfigurace')
tmin = s.inp('Min. teplota okolí', -15, '°C')
tcell = s.inp('Max. teplota článků', 70, '°C')
N = s.inp('Panelů v řetězci', 14)
par = s.inp('Paralelních řetězců / MPPT', 1)
used = s.inp('Využitých MPPT', 2)
s.gap()
s.head('Výsledky')
vocC = s.calc('Voc při min. teplotě', f'={voc}*(1+{tkv}/100*({tmin}-25))', 'V', '0.0')
vmpH = s.calc('Vmpp při max. teplotě článků', f'={vmp}*(1+{tkm}/100*({tcell}-25))', 'V', '0.0')
vmpC = s.calc('Vmpp při min. teplotě', f'={vmp}*(1+{tkm}/100*({tmin}-25))', 'V', '0.0')
nS = s.calc('Max. panelů (z hlediska max. DC napětí)', f'=ROUNDDOWN({vdc}/{vocC},0)', '', '0')
nH = s.calc('Max. panelů (horní mez MPPT)', f'=ROUNDDOWN({vhi}/{vmpC},0)', '', '0')
nL = s.calc('Min. panelů (dolní mez MPPT)', f'=ROUNDUP({vlo}/{vmpH},0)', '', '0')
s.calc('Doporučený rozsah panelů v řetězci', f'=IF({nL}<=MIN({nS},{nH}),{nL}&" až "&MIN({nS},{nH}),"žádná vyhovující délka")', '', '@', True)
s.calc('Voc za mrazu (řetězec)', f'={N}*{vocC}', 'V', '0')
s.calc('1) Voc za mrazu ≤ max. DC napětí', f'=IF({N}*{vocC}<={vdc},"OK","CHYBA")', '', '@')
s.calc('2) Vmpp za tepla ≥ dolní mez MPPT', f'=IF({N}*{vmpH}>={vlo},"OK","CHYBA")', '', '@')
s.calc('3) Vmpp za mrazu ≤ horní mez MPPT', f'=IF({N}*{vmpC}<={vhi},"OK","POZOR")', '', '@')
s.calc('4) Impp × řetězce ≤ max. proud MPPT', f'=IF({imp}*{par}<={imx},"OK","POZOR")', '', '@')
s.calc('5) Isc × řetězce ≤ max. Isc MPPT', f'=IF({isc}*{par}<={iscx},"OK","CHYBA")', '', '@')
s.calc('6) Využité MPPT ≤ počet MPPT', f'=IF({used}<={nM},"OK","CHYBA")', '', '@')
s.status_cf(f'B{s.r-6}:B{s.r-1}')
mod = s.calc('Panelů celkem', f'={N}*{par}*{used}', 'ks', '0')
pdc = s.calc('DC výkon', f'={mod}*{pm}/1000', 'kWp')
rat = s.calc('Poměr DC/AC', f'={pdc}/{pac}', '', '0.00', True)
s.calc('Hodnocení poměru', f'=IF({rat}<0.9,"POZOR – nízký",IF({rat}<=1.3,"OK",IF({rat}<=1.5,"POZOR – ořezávání špiček","CHYBA – příliš vysoký")))', '', '@')
s.status_cf(f'B{s.r-1}:B{s.r-1}')

# ------------------------------------------------------------------ FVE KABEL A JIŠTĚNÍ
s = Sheet('FVE kabel a jištění')
STDR = "'Zatížitelnost'!$H$50:$H$69"
s.head('DC kabel — úbytek a ztráty')
di = s.inp('Proud řetězce', 13, 'A')
du = s.inp('Napětí řetězce (Vmpp)', 475, 'V')
dl = s.inp('Délka (jednosměrně)', 35, 'm')
ds = s.inp('Průřez', 6, 'mm²', [2.5, 4, 6, 10, 16, 25])
dt = s.inp('Teplota kabelu', 70, '°C')
rr_ = f'(1/56*(1+0.00393*({dt}-20)))'
dU_ = s.calc('Úbytek napětí', f'={di}*{rr_}*2*{dl}/{ds}', 'V')
dp = s.calc('Úbytek', f'={dU_}/{du}*100', '%', '0.00', True)
s.calc('Hodnocení', f'=IF({dp}<=1,"OK – dobré",IF({dp}<=2,"POZOR – hraniční","CHYBA – vysoké"))', '', '@')
s.status_cf(f'B{s.r-1}:B{s.r-1}')
s.calc('Ztráty výkonu', f'={di}^2*{rr_}*2*{dl}/{ds}', 'W', '0')
s.calc('Ztráty z výkonu řetězce', f'={di}^2*{rr_}*2*{dl}/{ds}/({du}*{di})*100', '%')
s.note('Proudové dimenzování DC kabelu min. 1,25·Isc (IEC 62548), solární kabel dle ČSN EN 50618.')
s.gap()
s.head('DC pojistky řetězců')
fi = s.inp('Isc panelu', 13.9, 'A')
fm = s.inp('Max. pojistka modulu', 25, 'A')
fn = s.inp('Paralelních řetězců', 3)
lo = s.calc('Min. pojistka řetězce (1,56·Isc)', f'=1.56*{fi}', 'A', '0.0')
fz = s.calc('Doporučená gPV pojistka', f'=IFERROR(INDEX({{10,12,15,16,20,25,30,32,40}},MATCH(TRUE,INDEX({{10,12,15,16,20,25,30,32,40}}>={lo},0),0)),"–")', 'A', '0', True)
s.calc('Pojistka ≤ max. pojistka modulu', f'=IF(ISNUMBER({fz}),IF({fz}<={fm},"OK","CHYBA"),"CHYBA")', '', '@')
s.calc('Pojistky řetězců nutné?', f'=IF(({fn}-1)*{fi}>{fm},"ANO – (n−1)·Isc > max. pojistka","NE")', '', '@')
s.status_cf(f'B{s.r-2}:B{s.r-2}')
s.gap()
s.head('AC strana střídače')
ap = s.inp('AC výkon střídače', 10, 'kW')
aph = s.inp('Výstup (1 / 3)', 3, '', [1, 3])
iac = s.calc('Jmenovitý AC proud', f'={ap}*1000/IF({aph}=3,SQRT(3)*400,230)', 'A', '0.0')
ib = s.calc('Jistič AC (≥ 1,1·In)', f'=IFERROR(INDEX({STDR},MATCH(TRUE,INDEX({STDR}>=1.1*{iac},0),0)),"> 630")', 'A', '0', True)
s.calc('Min. průřez Cu (XLPE, uložení C, 30 °C)',
       f"=IFERROR(INDEX('Zatížitelnost'!$C$29:$N$29,MATCH(TRUE,INDEX(INDEX('Zatížitelnost'!$C$30:$N$45,MATCH(\"XLPE|C|\"&IF({aph}=3,3,2),'Zatížitelnost'!$B$30:$B$45,0),0)>={ib},0),0)),\"> 120\")",
       'mm²', '0.0')
s.note('Orientační. Rozhoduje max. výstupní proud a doporučení výrobce. Úbytek na AC přívodu ověřte zvlášť (≤ 1–2 %).')

# ------------------------------------------------------------------ FVE VÝNOS
s = Sheet('FVE výnos', 'Hrubý odhad (±10–15 %). Pro nabídku použijte PVGIS.', widths=(44, 16, 14, 3, 8, 16, 16, 16))
ws = s.ws
s.head('Vstupy')
kwp = s.inp('Instalovaný výkon', 8.8, 'kWp')
ref = s.inp('Referenční výnos (optimum)', 1000, 'kWh/kWp')
orf = s.inp('Orientační součinitel orientace/sklonu', 1.0, '', [1, 0.96, 0.93, 0.88, 0.86, 0.72, 0.6])
s.note('1 = J 30–35°, 0,96 = JV/JZ 30°, 0,93 = J plochá 10°, 0,88 = V–Z plochá, 0,86 = V/Z 30°, 0,72 = J fasáda, 0,6 = S 30°')
deg = s.inp('Degradace / rok', 0.5, '%')
inv = s.inp('Investice', 320000, 'Kč/€')
sc = s.inp('Vlastní spotřeba', 40, '%')
buy = s.inp('Cena nákupu', 6.5, '/kWh')
ex = s.inp('Výkupní cena', 1.5, '/kWh')
g = s.inp('Růst ceny energie / rok', 3, '%')
s.gap()
s.head('Výsledky')
Y = s.calc('Roční výroba (1. rok)', f'={kwp}*{ref}*{orf}', 'kWh', '#,##0', True)
s.calc('Měrný výnos', f'={ref}*{orf}', 'kWh/kWp', '#,##0')
s1 = s.calc('Úspora / příjem 1. rok', f'=F5', '', '#,##0')
s.calc('Prostá návratnost', f'=IF({s1}>0,{inv}/{s1},"–")', 'let', '0.0')
s.calc('Návratnost s růstem cen a degradací', '=IFERROR(INDEX(H5:H44,MATCH(TRUE,INDEX(G5:G44>=' + inv + ',0),0))-1+(' + inv + '-IFERROR(INDEX(G5:G44,MATCH(TRUE,INDEX(G5:G44>=' + inv + ',0),0)-1),0))/INDEX(F5:F44,MATCH(TRUE,INDEX(G5:G44>=' + inv + ',0),0)),"> 40")', 'let', '0.0', True)
s.calc('Celkem za 25 let', '=SUM(F5:F29)', '', '#,##0')
table(ws, 4, 5, ['Rok', 'Úspora', 'Kumulativně', 'Rok (pom.)'],
      [[y, f'={Y}*(1-{deg}/100)^({y}-1)*({sc}/100*{buy}*(1+{g}/100)^({y}-1)+(1-{sc}/100)*{ex})',
        (f'=F{5+y-1}' if y == 1 else f'=G{5+y-2}+F{5+y-1}'), y] for y in range(1, 41)], numfmt={1: '#,##0', 2: '#,##0'})
# sloupec E = rok, F = úspora, G = kumulativně, H = pomocný (rok)
ws.column_dimensions['H'].width = 10

# ------------------------------------------------------------------ BATERIE A ŘADY
s = Sheet('FVE baterie a řady')
s.head('Velikost baterie')
be = s.inp('Energie z baterie / den', 8, 'kWh')
bd = s.inp('Dnů autonomie', 1)
bdod = s.inp('Využitelná hloubka vybití', 90, '%')
beta = s.inp('Účinnost cyklu', 92, '%')
bp = s.inp('Špičkový odběr z baterie', 5, 'kW')
bv = s.inp('Napětí baterie', 51.2, 'V')
s.calc('Využitelná kapacita', f'={be}*{bd}', 'kWh')
nom = s.calc('Jmenovitá kapacita baterie', f'={be}*{bd}/({bdod}/100*{beta}/100)', 'kWh', '0.00', True)
s.calc('Proud při špičce', f'={bp}*1000/{bv}', 'A', '0')
s.calc('C-rate při špičce', f'={bp}/{nom}', 'C', '0.00')
s.note('Pravidlo palce: 1–1,5 kWh na 1 kWp pro rodinný dům (zvýšení vlastní spotřeby).')
s.gap()
s.head('Rozestup řad (plochá střecha)')
lat = s.inp('Zeměpisná šířka φ', 49.5, '°')
pl = s.inp('Délka panelu ve spádu', 1.76, 'm')
sk = s.inp('Sklon β', 15, '°')
h = s.calc('Výška Slunce 21. 12. v poledne', f'=90-{lat}-23.44', '°', '0.0')
hh = s.calc('Výška hrany panelu', f'={pl}*SIN(RADIANS({sk}))', 'm')
s.calc('Rozteč řad (hrana–hrana)', f'=IF({h}>0,{pl}*COS(RADIANS({sk}))+{hh}/TAN(RADIANS({h})),"nelze")', 'm', '0.00', True)
s.calc('Mezera mezi řadami', f'=IF({h}>0,{hh}/TAN(RADIANS({h})),"nelze")', 'm')

# ------------------------------------------------------------------ MaR ŠKÁLOVÁNÍ
s = Sheet('MaR škálování', 'Signál ↔ fyzikální hodnota (lineární)')
slo = s.inp('Signál od', 4, 'mA / V')
shi = s.inp('Signál do', 20, 'mA / V')
rlo = s.inp('Rozsah veličiny od', 0)
rhi = s.inp('Rozsah veličiny do', 10, 'bar')
s.gap()
s.head('Signál → hodnota')
sg = s.inp('Signál', 12, 'mA / V')
vv = s.calc('Hodnota', f'={rlo}+({sg}-{slo})/({shi}-{slo})*({rhi}-{rlo})', '', '0.000', True)
s.calc('% rozsahu', f'=({sg}-{slo})/({shi}-{slo})*100', '%', '0.0')
s.calc('Siemens normalizované (0–27648)', f'=ROUND({sg}/{shi}*27648,0)', '', '0')
s.calc('12bit ADC (0–4095)', f'=ROUND({sg}/{shi}*4095,0)', '', '0')
s.calc('Stav 4–20 mA (NE43)', f'=IF({slo}<>4,"–",IF({sg}<3.8,"CHYBA – porucha / přerušení",IF({sg}>20.5,"CHYBA – přetížení","OK")))', '', '@')
s.status_cf(f'B{s.r-1}:B{s.r-1}')
s.gap()
s.head('Hodnota → signál')
hv = s.inp('Hodnota', 5)
s.calc('Signál', f'={slo}+({hv}-{rlo})/({rhi}-{rlo})*({shi}-{slo})', 'mA / V', '0.000', True)

# ------------------------------------------------------------------ MaR ČIDLA
s = Sheet('MaR čidla', 'Pt100/Pt1000: EN 60751 (Callendar–Van Dusen). Ni1000 DIN 43760. NTC: rovnice β.', widths=(44, 16, 14, 3, 10, 12, 12, 12))
ws = s.ws
A_, B_, C_ = 3.9083e-3, -5.775e-7, -4.183e-12
s.head('Pt100 / Pt1000')
r0 = s.inp('R0 (100 = Pt100, 1000 = Pt1000)', 1000, 'Ω', [100, 1000])
tt = s.inp('Teplota', 20, '°C')
Rt = s.calc('Odpor R(T)', f'=IF({tt}>=0,{r0}*(1+{A_}*{tt}+{B_}*{tt}^2),{r0}*(1+{A_}*{tt}+{B_}*{tt}^2+{C_}*({tt}-100)*{tt}^3))', 'Ω', '0.000', True)
s.calc('Citlivost', f'={r0}*({A_}+2*{B_}*{tt})', 'Ω/K', '0.000')
s.calc('Tolerance třída A', f'=0.15+0.002*ABS({tt})', '± K', '0.00')
s.calc('Tolerance třída B', f'=0.3+0.005*ABS({tt})', '± K', '0.00')
s.gap()
s.head('Odpor → teplota (Newtonova metoda, 4 kroky)')
rin = s.inp('Naměřený odpor', 1077.935, 'Ω')
T0 = s.calc('Krok 0', f'=({rin}/{r0}-1)/{A_}', '°C', '0.000')
def newton(Tp):
    fx = f'IF({Tp}>=0,{r0}*(1+{A_}*{Tp}+{B_}*{Tp}^2),{r0}*(1+{A_}*{Tp}+{B_}*{Tp}^2+{C_}*({Tp}-100)*{Tp}^3))'
    dfx = f'{r0}*({A_}+2*{B_}*{Tp}+IF({Tp}<0,{C_}*(4*{Tp}^3-300*{Tp}^2),0))'
    return f'={Tp}-({fx}-{rin})/({dfx})'
T1 = s.calc('Krok 1', newton(T0), '°C', '0.000')
T2 = s.calc('Krok 2', newton(T1), '°C', '0.000')
T3 = s.calc('Krok 3', newton(T2), '°C', '0.000')
s.calc('Teplota', newton(T3), '°C', '0.00', True)
s.gap()
s.head('NTC (β)')
nb = s.inp('β', 3950, 'K')
nr = s.inp('R25', 10000, 'Ω')
nt = s.inp('Teplota', 25, '°C')
s.calc('Odpor', f'={nr}*EXP({nb}*(1/({nt}+273.15)-1/298.15))', 'Ω', '0.0', True)
nrr = s.inp('Naměřený odpor NTC', 10000, 'Ω')
s.calc('Teplota z odporu', f'=1/(1/298.15+LN({nrr}/{nr})/{nb})-273.15', '°C', '0.00', True)
s.gap()
s.head('Chyba dvouvodičového čidla')
wl = s.inp('Délka kabelu', 30, 'm')
wsx = s.inp('Průřez vodiče', 0.5, 'mm²')
wr0 = s.inp('R0 čidla (100 / 1000)', 100, 'Ω', [100, 1000])
wt = s.inp('Teplota měření', 20, '°C')
rl = s.calc('Odpor smyčky kabelu', f'=2*(1/56)*{wl}/{wsx}', 'Ω', '0.000')
s.calc('Chyba měření', f'={rl}/({wr0}*({A_}+2*{B_}*{wt}))', 'K', '0.00', True)
s.note('Chyba je kladná. Řešení: 3/4-vodič nebo kompenzace R kabelu v PLC. Pt1000 má 10× menší chybu.')
ts = list(range(-50, 251, 10))
def ni(T): return 1000 * (1 + 5.485e-3 * T + 6.65e-6 * T * T + 2.805e-11 * T ** 4 - 2e-17 * T ** 6)
table(ws, 4, 5, ['°C', 'Pt100 Ω', 'Pt1000 Ω', 'Ni1000 Ω'],
      [[t, f'=IF(E{5+i}>=0,100*(1+{A_}*E{5+i}+{B_}*E{5+i}^2),100*(1+{A_}*E{5+i}+{B_}*E{5+i}^2+{C_}*(E{5+i}-100)*E{5+i}^3))',
        f'=F{5+i}*10', f'=1000*(1+5.485E-3*E{5+i}+6.65E-6*E{5+i}^2+2.805E-11*E{5+i}^4-2E-17*E{5+i}^6)'] for i, t in enumerate(ts)],
      numfmt={1: '0.00', 2: '0.0', 3: '0.0'})

# ------------------------------------------------------------------ MaR REGULACE A HYDRAULIKA
s = Sheet('MaR regulace a hydraulika')
s.head('Proudová smyčka 4–20 mA — rozpočet napětí')
vs = s.inp('Napájení smyčky', 24, 'V')
vm = s.inp('Min. napětí vysílače', 12, 'V')
rlo_ = s.inp('Zátěž (vstup PLC, indikátory)', 250, 'Ω')
cl = s.inp('Délka kabelu (jednosměrně)', 200, 'm')
cs = s.inp('Průřez vodiče', 0.5, 'mm²')
rc = s.calc('Odpor kabelu (tam a zpět)', f'=2*(1/56)*{cl}/{cs}', 'Ω', '0.0')
rmax = s.calc('Max. celkový odpor smyčky (22 mA)', f'=({vs}-{vm})/0.022', 'Ω', '0')
s.calc('Rezerva', f'={rmax}-{rlo_}-{rc}', 'Ω', '0', True)
s.calc('Napětí na vysílači při 22 mA', f'={vs}-0.022*({rlo_}+{rc})', 'V', '0.00')
s.calc('Hodnocení', f'=IF({vs}-0.022*({rlo_}+{rc})>={vm},"OK","CHYBA – nedostatečné napájení")', '', '@')
s.status_cf(f'B{s.r-1}:B{s.r-1}')
s.gap()
s.head('PID — Ziegler–Nichols (metoda kmitů)')
ku = s.inp('Ku (kritické zesílení)', 2.4)
tu = s.inp('Tu (perioda kmitů)', 60, 's')
s.calc('P: Kp', f'=0.5*{ku}', '', '0.000')
s.calc('PI: Kp', f'=0.45*{ku}', '', '0.000')
s.calc('PI: Ti', f'={tu}/1.2', 's', '0.0')
s.calc('PID: Kp', f'=0.6*{ku}', '', '0.000', True)
s.calc('PID: Ti', f'=0.5*{tu}', 's', '0.0', True)
s.calc('PID: Td', f'=0.125*{tu}', 's', '0.0', True)
s.gap()
s.head('PID — Ziegler–Nichols (přechodová charakteristika)')
K = s.inp('K (zisk soustavy)', 2.4)
Ld = s.inp('L (dopravní zpoždění)', 60, 's')
Tc = s.inp('T (časová konstanta)', 300, 's')
s.calc('P: Kp', f'={Tc}/({K}*{Ld})', '', '0.000')
s.calc('PI: Kp', f'=0.9*{Tc}/({K}*{Ld})', '', '0.000')
s.calc('PI: Ti', f'=3.33*{Ld}', 's', '0.0')
s.calc('PID: Kp', f'=1.2*{Tc}/({K}*{Ld})', '', '0.000', True)
s.calc('PID: Ti', f'=2*{Ld}', 's', '0.0', True)
s.calc('PID: Td', f'=0.5*{Ld}', 's', '0.0', True)
s.note('U pomalých soustav (VZT, topení) začněte s Kp o 30–50 % nižším.')
s.gap()
s.head('Výkon ↔ průtok (voda)')
qp = s.inp('Výkon', 20, 'kW')
qdt = s.inp('Rozdíl teplot ΔT', 10, 'K')
qd = s.inp('Vnitřní průměr trubky', 26, 'mm')
q = s.calc('Průtok', f'={qp}/(1.163*{qdt})', 'm³/h', '0.000', True)
s.calc('Průtok', f'={q}*1000', 'l/h', '#,##0')
s.calc('Rychlost v potrubí', f'=({q}/3600)/(PI()/4*({qd}/1000)^2)', 'm/s', '0.00')
s.calc('Hodnocení rychlosti', f'=IF({q}/3600/(PI()/4*({qd}/1000)^2)<=1,"OK",IF({q}/3600/(PI()/4*({qd}/1000)^2)<=1.5,"POZOR – vyšší","CHYBA – příliš vysoká"))', '', '@')
s.status_cf(f'B{s.r-1}:B{s.r-1}')
s.gap()
s.head('Ventil — Kv a autorita')
kq = s.inp('Průtok Q', 1.72, 'm³/h')
kdp = s.inp('Tlaková ztráta ventilu Δp', 10, 'kPa')
krest = s.inp('Tlaková ztráta zbytku okruhu', 20, 'kPa')
s.calc('Potřebné Kv', f'={kq}/SQRT({kdp}/100)', 'm³/h', '0.00', True)
beta_ = s.calc('Autorita β', f'={kdp}/({kdp}+{krest})', '', '0.00')
s.calc('Hodnocení', f'=IF({beta_}>=0.3,"OK","POZOR – nízká autorita (< 0,3)")', '', '@')
s.status_cf(f'B{s.r-1}:B{s.r-1}')

# ------------------------------------------------------------------ TABULKY
s = Sheet('Tabulky', widths=(26, 24, 18, 44, 14, 14))
ws = s.ws
table(ws, 3, 1, ['Vodič', 'Barva'], [['PE', 'zeleno-žlutá'], ['N', 'světle modrá'], ['PEN', 'zeleno-žlutá, konce světle modré'],
                                       ['L1 / L2 / L3', 'hnědá / černá / šedá']])
table(ws, 9, 1, ['Char. jističe', 'Okamžité vybavení', 'Použití'], [['B', '3–5 × In', 'světla, zásuvky, dlouhá vedení'], ['C', '5–10 × In', 'běžné spotřebiče'],
                                                                     ['D', '10–20 × In', 'transformátory, motory'], ['K', '8–14 × In', 'motory'], ['Z', '2–3 × In', 'polovodiče']])
table(ws, 16, 1, ['RCD typ', 'Detekuje'], [['AC', 'sinusový AC'], ['A', '+ pulzní DC'], ['F', '+ smíšené frekvence'], ['B', '+ hladký DC (FVE, wallbox, měniče) dle výrobce']])
table(ws, 22, 1, ['IP číslice', '1. (pevná tělesa)', '2. (voda)'],
      [[0, '–', '–'], [2, '≥ 12,5 mm', 'kapky, sklon 15°'], [3, '≥ 2,5 mm', 'déšť'], [4, '≥ 1 mm', 'stříkání'], [5, 'prach', 'tryskající voda'],
       [6, 'prachotěsné', 'silné proudy'], [7, '', 'ponoření dočasné'], [8, '', 'ponoření trvalé']])
ws.cell(33, 1, 'AWG → mm²').font = Font(bold=True)
table(ws, 34, 1, ['AWG (číslo)', 'Ø mm', 'mm²'], [])
for i, n in enumerate([24, 22, 20, 18, 16, 14, 12, 10, 8, 6, 4, 2, 1, 0, -1, -2, -3]):
    r = 35 + i
    ws.cell(r, 1, n if n > 0 else ('1/0' if n == 0 else f'{1-n}/0')).border = BOX
    ws.cell(r, 5, n)  # pomocný sloupec
    ws.cell(r, 2, f'=0.127*92^((36-E{r})/39)').number_format = '0.00'
    ws.cell(r, 3, f'=PI()/4*B{r}^2').number_format = '0.00'
ws.cell(34, 5, 'n (pom.)')
table(ws, 3, 4, ['Norma', 'Název'], [
    ['ČSN 33 2000-4-41', 'Ochrana před úrazem elektrickým proudem'], ['ČSN 33 2000-4-43', 'Ochrana proti nadproudům'],
    ['ČSN 33 2000-5-52', 'Elektrická vedení'], ['ČSN 33 2000-6', 'Revize'], ['ČSN 33 2000-7-712', 'Fotovoltaické (PV) soustavy'],
    ['ČSN EN IEC 62548-1', 'Návrh PV polí'], ['ČSN EN 62446-1', 'PV: dokumentace, uvedení do provozu, kontroly'],
    ['ČSN EN 62305', 'Ochrana před bleskem'], ['ČSN EN 61439', 'Rozváděče nn'], ['ČSN 33 1500', 'Revize elektrických zařízení'],
    ['ČSN EN 50110-1', 'Obsluha a práce na elektrických zařízeních'], ['ČSN EN 61131-3', 'Programovací jazyky PLC']])
ws.column_dimensions['D'].width = 24
ws.column_dimensions['E'].width = 44
# přeuspořádání: sloupec D = norma, E = název; pomocné n přesun
for i in range(17):
    ws.cell(35 + i, 5).value = None
ws.cell(34, 5).value = None
for i, n in enumerate([24, 22, 20, 18, 16, 14, 12, 10, 8, 6, 4, 2, 1, 0, -1, -2, -3]):
    r = 35 + i
    ws.cell(r, 2, f'=0.127*92^((36-{n})/39)').number_format = '0.00'

# ------------------------------------------------------------------ CHECKLISTY
CHECKS = [
 ('Výchozí revize / kontrola elektroinstalace', [
  'Dokumentace (projekt, schémata, protokol o určení vnějších vlivů) je k dispozici',
  'Rozváděč a jističe jsou označeny, obvody odpovídají schématu',
  'Barvy a označení vodičů (PE, N, L) jsou správně, PE je nepřerušený',
  'Utažení svorek, kontrola vodičů ve svorkách, zaslepení volných otvorů',
  'Průřezy vodičů a jištění odpovídají zatížení (Ib ≤ In ≤ Iz)',
  'Hlavní ochranné pospojování a doplňující pospojování (koupelny aj.)',
  'Odpor uzemnění / ověření připojení na uzemňovací soustavu',
  'Izolační odpor 500 V DC (≥ 1 MΩ) změřen a zapsán',
  'Impedance smyčky Zs změřena a porovnána s limity jističů',
  'RCD: vybavovací proud a doba změřeny, tlačítko TEST funguje',
  'Sled fází a funkce zásuvek / spotřebičů ověřena',
  'Krytí a označení rozváděče (výstražné štítky, štítek s údaji)',
  'Protokol o revizi vyhotoven a předán']),
 ('FVE — uvedení do provozu (ČSN EN 62446-1)', [
  'Mechanická kontrola: uchycení, utažení, rozestupy, poškození panelů',
  'Polarita každého řetězce ověřena před připojením ke střídači',
  'Napětí Voc každého řetězce změřeno a porovnáno s výpočtem',
  'Isc (nebo provozní proud) řetězců změřen při stabilním ozáření',
  'Izolační odpor DC polí (zkušební napětí dle Voc: <120 V → 250 V, 120–500 V → 500 V, >500 V → 1000 V)',
  'Pospojování a uzemnění rámů a konstrukce, kontinuita PE',
  'Hromosvod / SPD typ dle projektu (DC i AC), vzdálenosti dodrženy',
  'DC odpínač, pojistky, AC jistič a RCD správně osazeny',
  'Označení: výstražné štítky DC, schéma, kontakt, označení pro hasiče',
  'Nastavení střídače: země / síťový kód, limity U, f, cos φ, omezení exportu',
  'Funkce anti-islanding, přepnutí při výpadku sítě (u hybridů záloha)',
  'Komunikace a monitoring, přístupy předány zákazníkovi',
  'Měřič / měření toků (elektroměr, CT) správně orientováno',
  'Fotodokumentace, protokol, revizní zpráva dle ČSN 33 2000-6 a 7-712']),
 ('MaR — oživení smyček a regulace', [
  'Zapojení zkontrolováno dle schématu, svorky popsány, stínění uzemněno',
  'Napájení 24 V ověřeno (napětí pod zátěží, polarita, jištění)',
  'Analogové vstupy: simulace 4 / 12 / 20 mA, kontrola škálování v PLC',
  'Poruchové stavy (< 3,8 mA, přerušení vodiče) vyvolávají alarm',
  'Teplotní čidla porovnána s referenčním teploměrem',
  'Aktory: směr, doba chodu, 0–100 %, koncové polohy, poloha při poruše',
  'Binární vstupy / výstupy: test každého bodu (I/O check)',
  'Komunikace: adresy, rychlost, parita, zakončení RS-485 120 Ω',
  'Regulátory: PID nastaveny, kontrola stability, omezení výstupu a anti-windup',
  'Alarmy a limity nastaveny, ověřen jejich signál',
  'Bezpečnostní funkce (protimrazová ochrana, havarijní vypnutí) otestovány',
  'Program zálohován, verze zaznamenána, dokumentace aktualizována'])]
for title, items in CHECKS:
    s = Sheet('Check ' + {'Výchozí': 'revize', 'FVE —': 'FVE', 'MaR —': 'MaR'}[next(k for k in ('Výchozí', 'FVE —', 'MaR —') if title.startswith(k))],
              title, widths=(100, 10, 18))
    ws = s.ws
    dv = DataValidation(type='list', formula1='"x,"', allow_blank=True)
    ws.add_data_validation(dv)
    ws.cell(s.r, 1, 'Bod').font = Font(bold=True)
    ws.cell(s.r, 2, 'Splněno (x)').font = Font(bold=True)
    ws.cell(s.r, 3, 'Poznámka').font = Font(bold=True)
    first = s.r + 1
    for it in items:
        s.r += 1
        ws.cell(s.r, 1, it).alignment = Alignment(wrap_text=True, vertical='top')
        c = ws.cell(s.r, 2)
        c.fill = INP
        c.border = BOX
        c.alignment = Alignment(horizontal='center')
        dv.add(c)
        ws.cell(s.r, 3).border = BOX
    s.r += 2
    ws.cell(s.r, 1, f'=\"Splněno \"&COUNTIF(B{first}:B{s.r-2},\"x\")&\" z {len(items)}\"').font = Font(bold=True)
    ws.conditional_formatting.add(f'A{first}:B{s.r-2}', FormulaRule(formula=[f'$B{first}="x"'], fill=GOOD))

for w in wb.worksheets:
    w.sheet_view.showGridLines = False
    w.freeze_panes = None
wb.save(OUT)
print('uloženo', os.path.abspath(OUT))
