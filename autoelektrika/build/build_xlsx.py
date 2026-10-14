#!/usr/bin/env python3
"""Generuje autoelektrika/Pomucka_autoelektrika.xlsx (živé vzorce). Spuštění: python3 build_xlsx.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xlhelp import *            # noqa: F401,F403  (Sheet, table, wb, styly)
from data import CAB, FUSES, SOC12

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Pomucka_autoelektrika.xlsx')
E24 = [1, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2, 2.2, 2.4, 2.7, 3, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]
# --- rozsahy na listu Data ---
SZ = 'Data!$A$3:$A$16'
AM = 'Data!$B$3:$B$16'
FU = 'Data!$D$3:$D$29'
SV = 'Data!$F$3:$F$7'     # SOC: napětí
SS = 'Data!$G$3:$G$7'     # SOC: %
EE = 'Data!$I$3:$I$26'    # E24
ST = 'Data!$K$3:$K$12'    # startér: standardní průřezy
START = [10, 16, 25, 35, 50, 70, 95, 120, 150, 185]
RHO = lambda t: f'(1/56*(1+0.00393*({t}-20)))'

# ------------------------------------------------------------ NÁVOD
s = Sheet('Návod', widths=(110,))
for line in [
    'Žlutá buňka = vstup (měň), modrá buňka = výsledek (vzorec). Listy odpovídají záložkám webové pomůcky.',
    '',
    'Kabely a jištění: Úbytek a průřez | Pojistka a kabel | Výkon a proud (srovnání 12/24/48 V) | Startér',
    'Baterie: Baterie (výdrž, stav nabití, nabíjení, sestavení)',
    'Zdroje a měniče: DC-DC střídač solár',
    'Energetická bilance a LED rezistor.',
    'Tabulky a Checklisty.',
    '',
    'Pomůcka je orientační a nenahrazuje údaje výrobce vozidla, baterie ani měniče. Výpočty vždy ověřte.',
    'Tabulka trvalých proudů kabelů (list Data) je konzervativní pro měděné vodiče ve svazku. Pro 48 V používejte pojistky a vypínače s DC napětím ≥ 58 V.',
    'List Data obsahuje pomocné tabulky (průřezy, pojistky, E24), na které se odkazují ostatní listy. Neodstraňujte je.',
]:
    s.ws.cell(s.r, 1, line)
    s.r += 1

# ------------------------------------------------------------ ÚBYTEK A PRŮŘEZ
s = Sheet('Úbytek a průřez', 'ΔU = I · ρ · L · k / S; doporučený průřez = max(podle úbytku, podle proudu)', widths=(44, 16, 14, 3, 12, 12, 12, 8))
ws = s.ws
s.head('Vstupy')
U = s.inp('Napětí soustavy', 12, 'V', [12, 24, 48])
mode = s.inp('Zadání (I = proud, P = výkon)', 'I', '', ['I', 'P'])
val = s.inp('Proud (A) / výkon (W)', 30)
L = s.inp('Délka kabelu (jednosměrně)', 5, 'm')
ret = s.inp('Zpětný vodič (2 = vlastní kabel, 1 = kostra)', 2, '', [1, 2])
S = s.inp('Průřez', 6, 'mm²', [c[0] for c in CAB])
T = s.inp('Teplota vodiče', 50, '°C')
lim = s.inp('Povolený úbytek', 3, '%', [1, 2, 3, 5])
s.gap()
s.head('Výsledky')
I = s.calc('Proud', f'=IF({mode}="I",{val},{val}/{U})', 'A', '0.0')
r = s.calc('Odpor smyčky (L · k · ρ / mm²)', f'={RHO(T)}*{L}*{ret}', 'Ω·mm²', '0.0000')
dU = s.calc('Úbytek napětí', f'={I}*{r}/{S}', 'V', '0.00')
pct = s.calc('Úbytek v %', f'={dU}/{U}*100', '%', '0.00', True)
s.calc('Hodnocení úbytku', f'=IF({pct}<={lim},"OK – vyhovuje","CHYBA – překročeno")', '', '@')
s.status_cf(f'B{s.r-1}:B{s.r-1}')
ampS = s.calc('Trvalý proud zvoleného kabelu', f'=VLOOKUP({S},Data!$A$3:$B$16,2,FALSE)', 'A', '0')
s.calc('Hodnocení proudu', f'=IF({I}<={ampS},"OK – vyhovuje","CHYBA – přetíženo")', '', '@')
s.status_cf(f'B{s.r-1}:B{s.r-1}')
sD = s.calc('Min. průřez podle úbytku', f'=IFERROR(INDEX({SZ},MATCH(TRUE,INDEX($F$5:$F$18<={lim},0),0)),"> 95")', 'mm²', '0.00')
sA = s.calc('Min. průřez podle proudu', f'=IFERROR(INDEX({SZ},MATCH(TRUE,INDEX({AM}>={I},0),0)),"> 95")', 'mm²', '0.00')
s.calc('Doporučený průřez', f'=IF(AND(ISNUMBER({sD}),ISNUMBER({sA})),MAX({sD},{sA}),"mimo tabulku")', 'mm²', '0.00', True)
s.calc('Ztráty v kabelu', f'={I}^2*{r}/{S}', 'W', '0.0')
table(ws, 4, 5, ['mm²', 'ΔU %', 'I max A', 'OK?'],
      [[f'=Data!A{3+i}', f'={I}*{r}/E{5+i}/{U}*100', f'=Data!B{3+i}', f'=IF(AND(F{5+i}<={lim},{I}<=G{5+i}),"ano","ne")'] for i in range(len(CAB))],
      numfmt={1: '0.00'})
# sloupec F (ΔU %) je odkazován výše jako $F$5:$F$18

# ------------------------------------------------------------ POJISTKA A KABEL
s = Sheet('Pojistka a kabel', 'Pojistka ≥ rezerva × trvalý proud a ≤ zatížitelnost kabelu')
U = s.inp('Napětí soustavy', 12, 'V', [12, 24, 48])
I = s.inp('Trvalý proud zátěže', 30, 'A')
f = s.inp('Rezerva (×)', 1.25)
L = s.inp('Délka kabelu (jednosměrně)', 3, 'm')
Rint = s.inp('Vnitřní odpor baterie', 5, 'mΩ')
s.note('Orientačně: olovo 100 Ah ≈ 5 mΩ na 12 V; LiFePO₄ 100 Ah ≈ 10–20 mΩ na 12 V (násobek pro 24/48 V).')
s.gap()
s.head('Výsledky')
mn = s.calc('Min. pojistka (I × rezerva)', f'={I}*{f}', 'A', '0.0')
Ifu = s.calc('Doporučená pojistka', f'=IFERROR(INDEX({FU},MATCH(TRUE,INDEX({FU}>={mn},0),0)),"> 500")', 'A', '0.0', True)
cab = s.calc('Kabel pod pojistkou', f'=IFERROR(INDEX({SZ},MATCH(TRUE,INDEX({AM}>={Ifu},0),0)),"mimo tabulku")', 'mm²', '0.00', True)
s.calc('Typ pojistky', f'=IF(NOT(ISNUMBER({Ifu})),"Class T / jistič",IF({Ifu}<=40,"plochá (ISO 8820)",IF({Ifu}<=200,"MIDI / MEGA / ANL","MEGA / ANL / Class T")))', '', '@')
s.calc('Min. DC napětí pojistky', f'=IF({U}<=24,"32 V DC – standardní","58 V DC – speciální")', '', '@')
Rc = s.calc('Odpor kabelu (tam a zpět)', f'=IFERROR({RHO(20)}*{L}*2/{cab},0)', 'Ω', '0.0000')
Isc = s.calc('Odhad zkratového proudu', f'={U}/({Rint}/1000+{Rc})', 'A', '0')
s.calc('Pojistka vs. zkrat', f'=IF({Isc}>=5*{Ifu},"OK – rychlé vypnutí","POZOR – zkrat vypne pomalu")', '', '@')
s.status_cf(f'B{s.r-1}:B{s.r-1}')
s.note('Při Isc > 1000 A použij pojistku s dostatečnou vypínací schopností (MEGA, ANL, Class T).')

# ------------------------------------------------------------ VÝKON A PROUD
s = Sheet('Výkon a proud', 'P = U·I; R = U²/P; srovnání 12/24/48 V', widths=(44, 16, 14, 12, 12))
ws = s.ws
s.head('Výkon ↔ proud ↔ odpor')
U = s.inp('Napětí', 12, 'V', [12, 24, 48])
P = s.inp('Výkon (vyplň P nebo I)', 600, 'W')
Iv = s.inp('Proud (volitelně, přepíše P)', None, 'A')
eff = s.inp('Účinnost zařízení', 100, '%')
Pw = s.calc('Výkon', f'=IF({Iv}<>"",{Iv}*{U},{P})', 'W', '0.0')
s.calc('Proud z baterie', f'={Pw}/({U}*{eff}/100)', 'A', '0.00', True)
s.calc('Odpor zátěže R = U²/P', f'={U}^2/{Pw}', 'Ω', '0.000')
s.calc('Energie za 1 hodinu', f'={Pw}/({eff}/100)/1000', 'kWh', '0.000')
s.gap()
s.head('Stejný výkon při 12 / 24 / 48 V')
cp = s.inp('Výkon zátěže', 2000, 'W')
cl = s.inp('Délka kabelu (jednosměrně)', 5, 'm')
cm = s.inp('Povolený úbytek', 3, '%')
s.r += 1
hdr = s.r
for j, h in enumerate(['Systém V', 'I (A)', 'Kabel mm²', 'Pojistka A']):
    c = ws.cell(hdr, 1 + j, h); c.font = Font(bold=True); c.fill = SUB; c.border = BOX
for i, v in enumerate((12, 24, 48)):
    rr = hdr + 1 + i
    ws.cell(rr, 1, v).border = BOX
    ws.cell(rr, 2, f'={cp}/A{rr}').number_format = '0.0'
    # kabel = max(podle úbytku při 50 °C, smyčka 2L; podle proudu)
    sd = f'IFERROR(INDEX({SZ},MATCH(TRUE,INDEX(B{rr}*{RHO(50)}*{cl}*2/{SZ}/A{rr}*100<={cm},0),0)),"> 95")'
    sa = f'IFERROR(INDEX({SZ},MATCH(TRUE,INDEX({AM}>=B{rr},0),0)),"> 95")'
    ws.cell(rr, 3, f'=IF(AND(ISNUMBER({sd}),ISNUMBER({sa})),MAX({sd},{sa}),"> 95")').number_format = '0.0'
    ws.cell(rr, 4, f'=IFERROR(INDEX({FU},MATCH(TRUE,INDEX({FU}>=B{rr}*1.25,0),0)),"–")')
    for cc in (2, 3, 4):
        ws.cell(rr, cc).border = BOX

# ------------------------------------------------------------ STARTÉR
s = Sheet('Startér', 'Špičkový proud při startu; celkový úbytek na + i − kabelu', widths=(44, 16, 14, 3, 10, 10, 10, 10, 10, 10, 10))
ws = s.ws
s.head('Vstupy')
su = s.inp('Napětí soustavy', 12, 'V', [12, 24, 48])
si = s.inp('Startovací proud (špička)', 250, 'A')
slp = s.inp('Délka kladného kabelu', 1.5, 'm')
sln = s.inp('Délka záporného kabelu / kostry', 0.5, 'm')
slim = s.inp('Povolený úbytek celkem (12 V: 0,5; 24 V: 1)', 0.5, 'V')
sth = s.inp('Teplota kabelu', 40, '°C')
s.note('Typicky: benzín 150–250 A, diesel 250–450 A, nákladní 24 V 400–800 A. Rozhoduje údaj výrobce motoru.')
s.gap()
s.head('Výsledky')
rr_ = s.calc('Odpor smyčky (délka · ρ)', f'={RHO(sth)}*({slp}+{sln})', 'Ω·mm²', '0.00000')
smin = s.calc('Vypočtený min. průřez', f'={si}*{rr_}/{slim}', 'mm²', '0.0')
sstd = s.calc('Doporučený průřez (+ i −)', f'=IFERROR(INDEX({ST},MATCH(TRUE,INDEX({ST}>={smin},0),0)),"> 185 – paralelní kabely")', 'mm²', '0', True)
sdu = s.calc('Úbytek při startu', f'=IF(ISNUMBER({sstd}),{si}*{rr_}/{sstd},"–")', 'V', '0.00')
s.calc('Hodnocení', f'=IF(ISNUMBER({sdu}),IF({sdu}<={slim},"OK","CHYBA – překročeno"),"–")', '', '@')
s.status_cf(f'B{s.r-1}:B{s.r-1}')
s.calc('Výkon při startu', f'={si}*{su}/1000', 'kW', '0.0')
s.calc('Ztráty v kabelu při startu', f'=IF(ISNUMBER({sstd}),{si}^2*{rr_}/{sstd},"–")', 'W', '0')
s.calc('Zbývá napětí na startéru (bez poklesu baterie)', f'=IF(ISNUMBER({sdu}),{su}-{sdu},"–")', 'V', '0.00')
ws.cell(4, 5, 'Min. průřez [mm²], 12 V, 0,5 V, 40 °C: řádky = A, sloupce = m (+ i −)').font = Font(bold=True)
for j, Lm in enumerate([1, 1.5, 2, 3, 4, 6]):
    c = ws.cell(5, 6 + j, Lm); c.font = Font(bold=True); c.fill = SUB; c.border = BOX
for i, Im in enumerate([100, 150, 200, 300, 400, 600]):
    c = ws.cell(6 + i, 5, Im); c.font = Font(bold=True); c.fill = SUB; c.border = BOX
    for j in range(6):
        col = chr(70 + j)
        c = ws.cell(6 + i, 6 + j, f'=IFERROR(INDEX({ST},MATCH(TRUE,INDEX({ST}>=$E{6+i}*{RHO(40)}*{col}$5/0.5,0),0)),">185")')
        c.border = BOX

# ------------------------------------------------------------ BATERIE
s = Sheet('Baterie', 'Výdrž, stav nabití, nabíjení, sestavení')
s.head('Výdrž a kapacita')
U = s.inp('Napětí baterie', 12, 'V', [12, 24, 48])
Ah = s.inp('Kapacita', 100, 'Ah')
dod = s.inp('Využitelná hloubka vybití (olovo 50, LiFePO₄ 80–90)', 50, '%')
load = s.inp('Zátěž', 200, 'W')
eff = s.inp('Účinnost (měnič, ztráty)', 90, '%')
hh = s.inp('Požadovaná výdrž', 10, 'h')
Wh = s.calc('Energie baterie', f'={U}*{Ah}', 'Wh', '#,##0')
use = s.calc('Využitelná energie', f'={Wh}*{dod}/100', 'Wh', '#,##0')
s.calc('Proud z baterie', f'={load}/({U}*{eff}/100)', 'A', '0.0')
s.calc('Výdrž', f'={use}*{eff}/100/{load}', 'h', '0.0', True)
s.calc('Potřebná kapacita pro požadovanou výdrž', f'={load}*{hh}/({U}*{dod}/100*{eff}/100)', 'Ah', '#,##0', True)
s.note('Peukertův efekt (u olova) není započítán.')
s.gap()
s.head('Stav nabití olověné baterie z napětí (v klidu ≥ 4 h)')
su = s.inp('Napětí soustavy', 12, 'V', [12, 24, 48])
sv = s.inp('Naměřené napětí v klidu', 12.3, 'V')
v12 = s.calc('Přepočet na 12 V', f'={sv}/({su}/12)', 'V', '0.000')
idx = s.calc('Pomocný index', f'=IF({v12}<=11.8,1,IF({v12}>=12.7,4,MATCH({v12},{SV},1)))', '', '0')
s.calc('Stav nabití (odhad)', f'=IF({v12}<=11.8,0,IF({v12}>=12.7,100,INDEX({SS},{idx})+({v12}-INDEX({SV},{idx}))/(INDEX({SV},{idx}+1)-INDEX({SV},{idx}))*(INDEX({SS},{idx}+1)-INDEX({SS},{idx}))))', '%', '0', True)
s.calc('Plně nabitá v klidu', f'=12.7*{su}/12', 'V', '0.0')
s.calc('Doporučené odpojení zátěže', f'=10.5*{su}/12', 'V', '0.0')
s.gap()
s.head('Doba nabíjení')
cu = s.inp('Napětí baterie', 12, 'V', [12, 24, 48])
cah = s.inp('Kapacita', 100, 'Ah')
cf = s.inp('Stav nabití z', 50, '%')
ct = s.inp('Stav nabití na', 100, '%')
ci = s.inp('Nabíjecí proud', 20, 'A')
ce = s.inp('Účinnost nabíjení (olovo 85, LiFePO₄ 95)', 85, '%')
cv = s.inp('Nabíjecí napětí', 14.4, 'V')
dAh = s.calc('Dodat do baterie', f'={cah}*({ct}-{cf})/100', 'Ah', '0.0')
s.calc('Doba nabíjení (orientačně)', f'={dAh}/({ce}/100*{ci})', 'h', '0.0', True)
s.calc('Příkon nabíječe', f'={ci}*{cv}', 'W', '0')
s.calc('C-rate', f'={ci}/{cah}', 'C', '0.00')
s.note('Olovo: poslední ≈ 20 % (absorpce) trvá o hodiny déle.')
s.gap()
s.head('Sestavení baterie (sériově / paralelně)')
tu = s.inp('Cílové napětí soustavy', 12, 'V', [12, 24, 48])
cell = s.inp('Jmenovité napětí článku / bloku', 12, 'V', [2, 3.2, 3.7, 6, 12])
cap = s.inp('Kapacita jednoho článku / bloku', 100, 'Ah')
par = s.inp('Paralelních větví', 2)
nS = s.calc('Počet v sérii', f'=ROUND({tu}/{cell},0)', 'ks', '0', True)
s.calc('Napětí sestavy', f'={nS}*{cell}', 'V', '0.0')
s.calc('Celková kapacita', f'={cap}*{par}', 'Ah', '0')
s.calc('Celkem článků / bloků', f'={nS}*{par}', 'ks', '0')
s.calc('Energie', f'={nS}*{cell}*{cap}*{par}/1000', 'kWh', '0.00')

# ------------------------------------------------------------ ZDROJE A MĚNIČE
s = Sheet('Zdroje a měniče', 'DC-DC měnič, střídač 230 V, solární regulátor')
s.head('DC-DC měnič / nabíječ')
vi = s.inp('Vstupní napětí', 12, 'V')
vo = s.inp('Výstupní napětí', 24, 'V')
io = s.inp('Výstupní proud', 20, 'A')
ef = s.inp('Účinnost', 92, '%')
po = s.calc('Výstupní výkon', f'={vo}*{io}', 'W', '0')
ii = s.calc('Vstupní proud', f'={po}/({vi}*{ef}/100)', 'A', '0.0', True)
s.calc('Ztráty měniče', f'={po}/({ef}/100)-{po}', 'W', '0')
fz = s.calc('Vstupní pojistka (≥ 1,25 × I)', f'=IFERROR(INDEX({FU},MATCH(TRUE,INDEX({FU}>={ii}*1.25,0),0)),"> 500")', 'A', '0.0')
s.calc('Vstupní kabel (podle pojistky)', f'=IFERROR(INDEX({SZ},MATCH(TRUE,INDEX({AM}>={fz},0),0)),"mimo tabulku")', 'mm²', '0.00')
s.gap()
s.head('Střídač 12/24/48 V → 230 V')
iu = s.inp('Napětí baterie', 12, 'V', [12, 24, 48])
ip = s.inp('Trvalý výkon AC', 1500, 'W')
ik = s.inp('Špičkový výkon AC', 3000, 'W')
ie = s.inp('Účinnost střídače', 90, '%')
il = s.inp('Délka DC kabelu (jednosměrně)', 1.5, 'm')
im = s.inp('Povolený úbytek', 2, '%')
Ic = s.calc('Trvalý DC proud', f'={ip}/({iu}*{ie}/100)', 'A', '0.0', True)
s.calc('Špičkový DC proud', f'={ik}/({iu}*{ie}/100)', 'A', '0')
Ifz = s.calc('DC pojistka (≥ 1,25 × I)', f'=IFERROR(INDEX({FU},MATCH(TRUE,INDEX({FU}>={Ic}*1.25,0),0)),"> 500")', 'A', '0.0')
sdd = f'IFERROR(INDEX({SZ},MATCH(TRUE,INDEX({Ic}*{RHO(50)}*{il}*2/{SZ}/{iu}*100<={im},0),0)),"> 95")'
saa = f'IFERROR(INDEX({SZ},MATCH(TRUE,INDEX({AM}>={Ifz},0),0)),"> 95")'
s.calc('DC kabel (úbytek a pojistka)', f'=IF(AND(ISNUMBER({sdd}),ISNUMBER({saa})),MAX({sdd},{saa}),"mimo tabulku")', 'mm²', '0.00', True)
s.calc('Min. kapacita baterie – LiFePO₄ (1 C)', f'={Ic}', 'Ah', '0')
s.calc('Min. kapacita baterie – olovo (0,2 C)', f'={Ic}/0.2', 'Ah', '0')
s.gap()
s.head('Solár — MPPT regulátor a výnos')
su2 = s.inp('Napětí baterie', 12, 'V', [12, 24, 48])
wp = s.inp('Výkon panelů', 400, 'Wp')
et = s.inp('Účinnost regulátoru (MPPT 0,95 / PWM 0,78)', 0.95)
vc = s.inp('Nabíjecí napětí', 14.4, 'V')
sun = s.inp('Plné sluneční hodiny / den', 3.5, 'h')
voc = s.inp('Voc panelu', 22.5, 'V')
nn = s.inp('Panelů v sérii', 2)
tk = s.inp('TK Voc', -0.27, '%/°C')
tm = s.inp('Min. teplota', -15, '°C')
vpv = s.inp('Max. PV napětí regulátoru', 100, 'V')
Ich = s.calc('Nabíjecí proud při špičce', f'={wp}*{et}/{vc}', 'A', '0.0', True)
s.calc('Regulátor (≥ 1,25 × I)', f'=IFERROR(INDEX({{10,15,20,30,40,50,60,70,80,100,120}},MATCH(TRUE,INDEX({{10,15,20,30,40,50,60,70,80,100,120}}>={Ich}*1.25,0),0)),"> 120")', 'A', '0')
Whd = s.calc('Denní výnos (odhad, ztráty 25 %)', f'={wp}*{sun}*0.75', 'Wh', '#,##0')
s.calc('Denní výnos v Ah', f'={Whd}/{su2}', 'Ah', '0')
vcold = s.calc('Voc za mrazu v sérii', f'={voc}*(1+{tk}/100*({tm}-25))*{nn}', 'V', '0.0')
s.calc('Limit regulátoru', f'=IF({vcold}<={vpv},"OK","CHYBA – překračuje limit")', '', '@')
s.status_cf(f'B{s.r-1}:B{s.r-1}')
s.calc('Voc ≥ napětí baterie + rezerva', f'=IF({voc}*{nn}>={vc}+2,"OK","POZOR – málo panelů v sérii")', '', '@')
s.status_cf(f'B{s.r-1}:B{s.r-1}')

# ------------------------------------------------------------ ENERGETICKÁ BILANCE + LED
s = Sheet('Energetická bilance', 'Spotřebič × počet × hodiny za den', widths=(36, 12, 12, 8, 16, 16))
ws = s.ws
table(ws, 4, 1, ['Spotřebič', 'W', 'h/den', 'ks', 'Wh/den', 'W (zapnuto)'], [])
loads = [('LED osvětlení', 24, 5, 1), ('Kompresorová chladnička', 45, 8, 1), ('Vodní čerpadlo', 60, 0.3, 1), ('Notebook + telefony', 60, 4, 1), ('Ventilátor', 20, 4, 1)] + [('', None, None, None)] * 7
for i, (n_, w_, h_, k_) in enumerate(loads):
    rr = 5 + i
    for j, v in enumerate((n_, w_, h_, k_)):
        c = ws.cell(rr, 1 + j, v); c.fill = INP; c.border = BOX
    ws.cell(rr, 5, f'=IF(B{rr}="","",B{rr}*C{rr}*D{rr})').border = BOX
    ws.cell(rr, 6, f'=IF(B{rr}="","",B{rr}*D{rr})').border = BOX
last = 4 + len(loads)
s.r = last + 2
U = s.inp('Napětí soustavy', 12, 'V', [12, 24, 48])
d = s.inp('Dní autonomie', 2)
dd_ = s.inp('Využitelná hloubka vybití (olovo 50, LiFePO₄ 80–90)', 50, '%')
ee = s.inp('Účinnost (měnič, ztráty)', 90, '%')
sn = s.inp('Plné sluneční hodiny / den', 3.5, 'h')
Wd = s.calc('Spotřeba za den', f'=SUM(E5:E{last})', 'Wh', '#,##0')
s.calc('Spotřeba za den', f'={Wd}/{U}', 'Ah', '0')
Wt = s.calc('Součet příkonů (vše zapnuto)', f'=SUM(F5:F{last})', 'W', '0')
s.calc('Součet příkonů (vše zapnuto)', f'={Wt}/{U}', 'A', '0.0')
s.calc('Kapacita baterie pro zadané dny', f'={Wd}*{d}/({U}*{dd_}/100*{ee}/100)', 'Ah', '#,##0', True)
s.calc('Kapacita baterie pro zadané dny', f'={Wd}*{d}/({dd_}/100*{ee}/100)/1000', 'kWh', '0.00')
s.calc('Solár pro pokrytí denní spotřeby', f'={Wd}/({sn}*0.75*{ee}/100)', 'Wp', '#,##0', True)
s.note('Počítej s rezervou 20–30 %. V zimě je výnos solárů několikrát nižší.')
s.gap()
s.head('LED a předřadný rezistor')
vs = s.inp('Napětí zdroje (max., při nabíjení)', 14.4, 'V')
vf = s.inp('Úbytek na 1 LED (Vf)', 2.0, 'V')
nl = s.inp('LED v sérii', 3)
lif = s.inp('Proud LED', 20, 'mA')
dr = s.calc('Přebytečné napětí', f'={vs}-{nl}*{vf}', 'V', '0.00')
Rr = s.calc('Vypočtený rezistor', f'=IF({dr}>0.5,{dr}/({lif}/1000),"málo napětí")', 'Ω', '0', True)
dec = s.calc('Pomocné: dekáda', f'=IF(ISNUMBER({Rr}),10^INT(LOG10({Rr})),"")', '', '0.0')
Re = s.calc('Nejbližší vyšší z řady E24', f'=IF(ISNUMBER({Rr}),IFERROR({dec}*INDEX({EE},MATCH(TRUE,INDEX({EE}*{dec}>={Rr}-0.000000001,0),0)),{dec}*10),"")', 'Ω', '0')
Ia = s.calc('Skutečný proud LED', f'=IF(ISNUMBER({Re}),{dr}/{Re}*1000,"")', 'mA', '0.0')
s.calc('Ztráta na rezistoru', f'=IF(ISNUMBER({Re}),({Ia}/1000)^2*{Re}*1000,"")', 'mW', '0')
s.note('Min. výkon rezistoru = 2 × ztráta. U 24/48 V zapoj více LED do série nebo použij proudový zdroj.')

# ------------------------------------------------------------ TABULKY
s = Sheet('Tabulky', widths=(34, 12, 12, 12, 3, 30, 14))
ws = s.ws
ws.cell(3, 1, 'Typická napětí podle soustavy (násobek pro 12/24/48 V)').font = Font(bold=True)
table(ws, 4, 1, ['', '12 V', '24 V', '48 V'], [
    ['Olovo: plně nabité v klidu'] + [f'={12.7}*{k}' for k in (1, 2, 4)],
    ['Olovo: absorpce (typ. min)'] + [f'={14.4}*{k}' for k in (1, 2, 4)],
    ['Olovo: absorpce (typ. max)'] + [f'={14.8}*{k}' for k in (1, 2, 4)],
    ['Olovo: float (typ.)'] + [f'={13.6}*{k}' for k in (1, 2, 4)],
    ['Olovo: odpojení zátěže'] + [f'={10.5}*{k}' for k in (1, 2, 4)],
    ['LiFePO₄: jmenovité (4S/8S/16S)'] + [f'={12.8}*{k}' for k in (1, 2, 4)],
    ['LiFePO₄: nabíjení (min)'] + [f'={14.2}*{k}' for k in (1, 2, 4)],
    ['LiFePO₄: nabíjení (max)'] + [f'={14.6}*{k}' for k in (1, 2, 4)],
    ['LiFePO₄: odpojení (min)'] + [f'={10}*{k}' for k in (1, 2, 4)],
    ['LiFePO₄: odpojení (max)'] + [f'={11}*{k}' for k in (1, 2, 4)]], numfmt={1: '0.0', 2: '0.0', 3: '0.0'})
ws.cell(16, 1, 'Průřez → trvalý proud → max. pojistka').font = Font(bold=True)
table(ws, 17, 1, ['mm²', 'I trvalý A', 'max pojistka A'],
      [[f'=Data!A{3+i}', f'=Data!B{3+i}', f'=IFERROR(LOOKUP(B{18+i},{FU}),"–")'] for i in range(len(CAB))])
table(ws, 3, 6, ['Barva pojistky (ISO 8820)', 'A'], [['černá', 1], ['šedá', 2], ['fialová', 3], ['růžová', 4], ['béžová', 5], ['hnědá', 7.5],
                                                      ['červená', 10], ['světle modrá', 15], ['žlutá', 20], ['bílá / čirá', 25], ['zelená', 30], ['oranžová', 40]])
ws.cell(17, 6, 'Značení svorek (DIN 72552)').font = Font(bold=True)
table(ws, 18, 6, ['Svorka', 'Význam'], [['30', 'trvalé + z baterie'], ['31', 'kostra (−)'], ['15', '+ po zapalování'], ['50', 'startér'], ['56 / 58', 'hlavní / obrysová světla'],
                                          ['49 / 49a', 'vstup / výstup směrovek'], ['61', 'kontrolka nabíjení'], ['85 / 86', 'relé: cívka'], ['30', 'relé: společný'], ['87 / 87a', 'relé: NO / NC']])
ws.column_dimensions['F'].width = 28
ws.column_dimensions['G'].width = 24
ws.cell(34, 1, 'AWG → mm²').font = Font(bold=True)
table(ws, 35, 1, ['AWG', 'Ø mm', 'mm²'], [])
for i, n in enumerate([24, 22, 20, 18, 16, 14, 12, 10, 8, 6, 4, 2, 1, 0, -1, -2, -3]):
    rr = 36 + i
    ws.cell(rr, 1, n if n > 0 else ('1/0' if n == 0 else f'{1-n}/0')).border = BOX
    ws.cell(rr, 2, f'=0.127*92^((36-{n})/39)').number_format = '0.00'
    ws.cell(rr, 3, f'=PI()/4*B{rr}^2').number_format = '0.00'

# ------------------------------------------------------------ CHECKLISTY
CHECKS = [
 ('Check nový okruh', 'Instalace nového spotřebiče / okruhu', [
  'Určen trvalý a špičkový proud spotřebiče',
  'Pojistka nebo jistič co nejblíž ke zdroji (baterii), dimenzovaná na kabel',
  'Průřez zkontrolován na úbytek napětí i na trvalý proud',
  'Kabel odolný teplu a oděru, ochranný vlnovec, průchodky v plechu',
  'Kvalitní lisované koncovky a spoje, správná velikost oka',
  'Velké zátěže spínány přes relé / stykač',
  'Kostrový spoj čistý, kov na kov, zajištěn proti uvolnění',
  'Spoje utaženy předepsaným momentem, svorky zakryty proti zkratu',
  'Změřen úbytek napětí na plus i mínus pod zátěží',
  'Zákres do schématu, kabely označeny']),
 ('Check diagnostika', 'Diagnostika baterie a nabíjení (12 V, u 24/48 V násobky)', [
  'Vizuálně: svorky, koroze, uchycení, oleje, zápach',
  'Napětí v klidu (po ≥ 4 h): ≥ 12,4 V (24 V: 24,8 V)',
  'Při startu napětí nesmí klesnout pod ≈ 9,6 V (24 V: 19,2 V)',
  'Napětí při běžícím motoru: 13,8–14,8 V (24 V: 27,6–29,6 V)',
  'Úbytek napětí na kladném kabelu při startu: < 0,5 V',
  'Úbytek napětí na kostře při startu: < 0,3 V',
  'Klidový odběr po uspání vozidla: typicky < 50 mA (dle výrobce)',
  'Zvlnění alternátoru (AC) při chodu: < 0,5 V',
  'Alternátor, řemen a pojistky nabíjecího okruhu OK']),
 ('Check ostrovní systém', 'Ostrovní systém 12/24/48 V (karavan, loď, dodávka)', [
  'Baterie s vhodným BMS / ochranami, ventilace u olova',
  'Hlavní pojistka (MEGA / Class T) a hlavní vypínač u baterie',
  'Pro 48 V: pojistky, vypínače a relé s jmenovitým DC napětím ≥ 58 V',
  'Samostatná pojistka na každou větev paralelních baterií',
  'Měření (shunt, BMS) zapojeno, nastavena kapacita a napětí',
  'Solární regulátor nastaven na typ baterie, kontrola Voc za mrazu',
  'Střídač: DC kabel krátký a dostatečný, pojistka u baterie',
  'AC strana: RCD/jistič, ochrana a uzemnění dle typu aplikace',
  'Společná kostra / záporná sběrnice, jedno místo spojení s kostrou',
  'Polarita a štítky na všech vodičích, zkušební zapnutí po částech',
  'Zátěžový test: výdrž, úbytky, teploty spojů'])]
for name, title, items in CHECKS:
    s = Sheet(name, title, widths=(100, 12, 18))
    ws = s.ws
    dv = DataValidation(type='list', formula1='"x,"', allow_blank=True)
    ws.add_data_validation(dv)
    for j, h in enumerate(('Bod', 'Splněno (x)', 'Poznámka')):
        ws.cell(s.r, 1 + j, h).font = Font(bold=True)
    first = s.r + 1
    for it in items:
        s.r += 1
        ws.cell(s.r, 1, it).alignment = Alignment(wrap_text=True, vertical='top')
        c = ws.cell(s.r, 2); c.fill = INP; c.border = BOX; c.alignment = Alignment(horizontal='center'); dv.add(c)
        ws.cell(s.r, 3).border = BOX
    s.r += 2
    ws.cell(s.r, 1, f'="Splněno "&COUNTIF(B{first}:B{s.r-2},"x")&" z {len(items)}"').font = Font(bold=True)
    ws.conditional_formatting.add(f'A{first}:B{s.r-2}', FormulaRule(formula=[f'$B{first}="x"'], fill=GOOD))

# ------------------------------------------------------------ DATA
s = Sheet('Data', 'Pomocné tabulky (neodstraňovat)', widths=(10, 12, 3, 12, 3, 12, 8, 3, 10, 3, 12))
ws = s.ws
table(ws, 2, 1, ['mm²', 'I trvalý A'], [list(c) for c in CAB])
table(ws, 2, 4, ['Pojistky A'], [[f] for f in FUSES])
table(ws, 2, 6, ['SOC V (12 V)', 'SOC %'], [list(p) for p in SOC12])
table(ws, 2, 9, ['E24'], [[e] for e in E24])
table(ws, 2, 11, ['Startér mm²'], [[x] for x in START])

for w in wb.worksheets:
    w.sheet_view.showGridLines = False
wb.save(OUT)
print('uloženo', os.path.abspath(OUT))
