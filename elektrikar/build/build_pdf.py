#!/usr/bin/env python3
"""Generuje elektrikar/Tahak_elektrikare.pdf (A4). Vyžaduje Chromium (--headless --print-to-pdf)."""
import os, subprocess, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import AMP, KT, KG, SIZES, STD

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, '..', 'Tahak_elektrikare.pdf'))
HTML = os.path.join(HERE, 'tahak.html')


def fmt(x, d=2):
    return f'{x:.{d}f}'.replace('.', ',')


def pt(r0, t):
    A, B, C = 3.9083e-3, -5.775e-7, -4.183e-12
    return r0 * (1 + A * t + B * t * t) if t >= 0 else r0 * (1 + A * t + B * t * t + C * (t - 100) * t ** 3)


def ni(t):
    return 1000 * (1 + 5.485e-3 * t + 6.65e-6 * t * t + 2.805e-11 * t ** 4 - 2e-17 * t ** 6)


def tbl(head, rows, cls=''):
    h = ''.join(f'<th>{x}</th>' for x in head)
    b = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<table class="{cls}"><tr>{h}</tr>{b}</table>'


def amp_table():
    rows = []
    for s_i, s in enumerate(SIZES):
        r = [str(s).replace('.', ',')]
        for ins in ('PVC', 'XLPE'):
            for m in ('B2', 'C'):
                r.append(fmt(AMP[ins][m][3][s_i], 1).rstrip('0').rstrip(',') if AMP[ins][m][3][s_i] % 1 else str(int(AMP[ins][m][3][s_i])))
        mx = [x for x in STD if x <= AMP['PVC']['C'][3][s_i]]
        r.append(str(mx[-1]) if mx else '–')
        rows.append(r)
    return tbl(['mm² (Cu)', 'PVC B2', 'PVC C', 'XLPE B2', 'XLPE C', 'max In (PVC C)'], rows)


def amp_full():
    rows = []
    for ins in ('PVC', 'XLPE'):
        for m in ('A1', 'B1', 'B2', 'C'):
            for n in (2, 3):
                rows.append([f'{ins} {m}, {n} zat.'] + [str(v).replace('.', ',') for v in AMP[ins][m][n]])
    return tbl(['A (Cu, 30 °C)'] + [str(s).replace('.', ',') for s in SIZES], rows, 'small')


def temp_table():
    return tbl(['Teplota okolí °C'] + [str(k) for k in KT], [['PVC'] + [fmt(v[0]) for v in KT.values()], ['XLPE'] + [fmt(v[1]) for v in KT.values()]], 'small')


def kg_table():
    return tbl(['Obvodů'] + [str(k) for k in KG], [['Součinitel'] + [fmt(v) for v in KG.values()]], 'small')


def temp_sensor_table():
    rows = []
    for t in range(-50, 201, 10):
        rows.append([t, fmt(pt(100, t)), fmt(pt(1000, t), 1), fmt(ni(t), 1) if t <= 200 else ''])
    return tbl(['°C', 'Pt100 Ω', 'Pt1000 Ω', 'Ni1000 Ω'], rows, 'small')


def ma_table():
    rows = []
    for p in (0, 10, 25, 50, 75, 100):
        rows.append([f'{p} %', fmt(4 + 16 * p / 100, 2), fmt(20 * p / 100, 2), fmt(10 * p / 100, 1), str(round((4 + 16 * p / 100) / 20 * 27648))])
    return tbl(['% rozsahu', '4–20 mA', '0–20 mA', '0–10 V', 'Siemens (4–20 mA)'], rows, 'small')


CHECK = {
 'Výchozí revize / kontrola elektroinstalace': [
  'Dokumentace (projekt, schémata, určení vnějších vlivů) k dispozici', 'Rozváděč a jističe označeny, obvody odpovídají schématu',
  'Barvy a označení vodičů správně, PE nepřerušený', 'Utažení svorek, zaslepení volných otvorů',
  'Průřezy a jištění odpovídají zatížení (Ib ≤ In ≤ Iz)', 'Hlavní a doplňující ochranné pospojování',
  'Odpor uzemnění / připojení na uzemňovací soustavu', 'Izolační odpor 500 V DC (≥ 1 MΩ) změřen',
  'Impedance smyčky Zs změřena a porovnána s limity', 'RCD: vybavovací proud a doba, tlačítko TEST',
  'Sled fází a funkce zásuvek / spotřebičů', 'Krytí, štítky a označení rozváděče', 'Protokol o revizi vyhotoven a předán'],
 'FVE — uvedení do provozu (ČSN EN 62446-1)': [
  'Mechanická kontrola: uchycení, utažení, poškození panelů', 'Polarita každého řetězce před připojením ke střídači',
  'Voc každého řetězce změřeno a porovnáno s výpočtem', 'Isc / provozní proud řetězců změřen při stabilním ozáření',
  'Izolační odpor DC polí (Voc: <120 V → 250 V, 120–500 V → 500 V, >500 V → 1000 V)', 'Pospojování a uzemnění rámů, kontinuita PE',
  'SPD typ dle projektu (DC i AC), hromosvod', 'DC odpínač, pojistky, AC jistič a RCD správně osazeny',
  'Výstražné štítky DC, schéma, označení pro hasiče', 'Nastavení střídače: síťový kód, limity U, f, cos φ, omezení exportu',
  'Anti-islanding, přepnutí při výpadku sítě (hybridy: záloha)', 'Komunikace a monitoring, přístupy předány', 'Měřič / CT správně orientováno',
  'Fotodokumentace, protokol a revizní zpráva (ČSN 33 2000-6, 7-712)'],
 'MaR — oživení smyček a regulace': [
  'Zapojení dle schématu, svorky popsány, stínění uzemněno', 'Napájení 24 V ověřeno (pod zátěží, polarita, jištění)',
  'Analogové vstupy: simulace 4 / 12 / 20 mA, škálování v PLC', 'Poruchové stavy (< 3,8 mA, přerušení vodiče) vyvolávají alarm',
  'Teplotní čidla porovnána s referenčním teploměrem', 'Aktory: směr, doba chodu, 0–100 %, koncové polohy, poloha při poruše',
  'Binární vstupy / výstupy: I/O check každého bodu', 'Komunikace: adresy, rychlost, parita, zakončení RS-485 120 Ω',
  'Regulátory: PID, stabilita, omezení výstupu, anti-windup', 'Alarmy a limity nastaveny, signál ověřen',
  'Bezpečnostní funkce (protimrazová ochrana, havarijní vypnutí) otestovány', 'Program zálohován, verze zaznamenána, dokumentace aktualizována'],
}


def checks():
    out = []
    for t, items in CHECK.items():
        out.append(f'<section class="chk"><h3>{t}</h3>' + ''.join(f'<div class="ci"><span class="box"></span>{i}</div>' for i in items) +
                   '<div class="sig">Datum: ____________ &nbsp;&nbsp; Provedl: ____________________ &nbsp;&nbsp; Podpis: ____________</div></section>')
    return ''.join(out)


html = f'''<!doctype html><html lang="cs"><head><meta charset="utf-8"><title>Tahák elektrikáře</title>
<style>
@page{{size:A4;margin:11mm 10mm}}
*{{box-sizing:border-box}}
body{{font:8.6pt/1.32 "DejaVu Sans",Arial,sans-serif;color:#16202c;margin:0}}
h1{{font-size:17pt;margin:0 0 1mm;color:#0b63d1}}
h2{{font-size:11pt;margin:4mm 0 1.5mm;padding:1mm 2mm;background:#0b63d1;color:#fff;border-radius:2px;break-after:avoid}}
h3{{font-size:9.2pt;margin:2.5mm 0 1mm;color:#0b63d1;break-after:avoid}}
.sub{{color:#5b6877;margin:0 0 2mm}}
.cols{{column-count:2;column-gap:6mm}}
.cols>*{{break-inside:avoid}}
.box2{{width:100%;border:.3mm solid #c9d3de;border-radius:2px;padding:1.5mm 2.5mm;margin:0 0 2.2mm;break-inside:avoid}}
.f{{font-family:"DejaVu Sans Mono",monospace;background:#f1f5fb;padding:.6mm 1.4mm;border-radius:2px;display:block;margin:.7mm 0}}
table{{border-collapse:collapse;width:100%;margin:1mm 0 2mm;break-inside:avoid}}
th,td{{border:.25mm solid #c9d3de;padding:.5mm 1.4mm;text-align:left}}
th{{background:#e8f0fc}}
table.small{{font-size:7.4pt}}
td:not(:first-child){{text-align:right}}
.txt td:not(:first-child),.l td{{text-align:left}}
.note{{color:#5b6877;font-size:7.5pt}}
.pg{{break-before:page}}
.chk{{margin-bottom:6mm;break-inside:avoid}}
.ci{{display:flex;gap:2mm;padding:1.1mm 0;border-bottom:.2mm solid #dde3ea;font-size:9pt}}
.box{{flex:0 0 3.4mm;height:3.4mm;border:.35mm solid #16202c;margin-top:.4mm}}
.sig{{margin-top:3mm;font-size:8.5pt;color:#5b6877}}
footer{{margin-top:4mm;color:#5b6877;font-size:7.3pt}}
</style></head><body>
<h1>⚡ Tahák elektrikáře</h1>
<p class="sub">Elektroinstalace · FVE · MaR — vzorce, tabulky, checklisty. Orientační pomůcka, rozhoduje projekt a platné normy.</p>

<h2>1. Elektroinstalace</h2>
<div class="cols">
<div class="box2"><h3>Proud, výkon, úbytek</h3>
<span class="f">1f: I = P / (U·cosφ) &nbsp; U = 230 V</span>
<span class="f">3f: I = P / (√3·U·cosφ) &nbsp; U = 400 V</span>
<span class="f">S = √3·U·I ; Q = √(S² − P²)</span>
<span class="f">ΔU = k·I·L·(R′cosφ + X′sinφ)</span>
<span class="f">k = 2 (1f), √3 (3f); R′ = ρ/S; X′ ≈ 0,08 mΩ/m</span>
<span class="f">ρ(θ) = ρ₂₀·(1 + α·(θ − 20)); Cu 1/56, Al 1/35 Ω·mm²/m; α = 0,00393 (Cu), 0,00403 (Al)</span>
<p class="note">Typické limity úbytku: 3 % světla, 5 % ostatní, 4 % celkem od zdroje (informativně).</p></div>

<div class="box2"><h3>Jištění a vodič</h3>
<span class="f">Ib ≤ In ≤ Iz &nbsp; (Iz = Iz,tab · kteplota · kseskupení)</span>
<span class="f">Zs ≤ U₀ / Ia ; Ia = k·In ; B: 5×, C: 10×, D: 20×</span>
<span class="f">Měření (studené): Zs ≤ ⅔·U₀/Ia</span>
<span class="f">Qc = P·(tg φ₁ − tg φ₂)</span>
<span class="f">Typizované In: {', '.join(str(x) for x in STD[:14])} A</span>
<p class="note">RCD 30 mA jako doplňující ochrana se vyžaduje nezávisle na výpočtu.</p></div>
</div>

<h3>Zatížitelnost Cu, 3 zatížené vodiče, 30 °C [A] (IEC 60364-5-52 / ČSN 33 2000-5-52)</h3>
{amp_table()}
<p class="note">B2 = kabel v trubce na zdi / liště, C = kabel přímo na zdi / pod omítkou. Hliník ≈ 0,78 × hodnota Cu (min. 16 mm²).</p>
<h3>Korekční součinitele</h3>
{temp_table()}
{kg_table()}

<div class="cols">
<div class="box2"><h3>Barvy vodičů</h3>{tbl(['Vodič','Barva'],[['PE','zeleno-žlutá'],['N','světle modrá'],['PEN','zeleno-žlutá, konce modré'],['L1/L2/L3','hnědá / černá / šedá']],'l')}</div>
<div class="box2"><h3>Charakteristiky jističů</h3>{tbl(['Char.','Vybavení','Použití'],[['B','3–5 × In','světla, zásuvky'],['C','5–10 × In','běžné spotřebiče'],['D','10–20 × In','trafa, motory'],['K','8–14 × In','motory'],['Z','2–3 × In','polovodiče']],'l')}</div>
<div class="box2"><h3>Typy RCD</h3>{tbl(['Typ','Detekuje'],[['AC','sinusový AC'],['A','+ pulzní DC'],['F','+ smíšené frekvence'],['B','+ hladký DC (FVE, wallbox, měniče) dle výrobce']],'l')}</div>
<div class="box2"><h3>Krytí IP</h3>{tbl(['Č.','1. číslice (tělesa)','2. číslice (voda)'],[['2','≥ 12,5 mm','kapky 15°'],['3','≥ 2,5 mm','déšť'],['4','≥ 1 mm','stříkání'],['5','prach','tryskající voda'],['6','prachotěsné','silné proudy'],['7/8','','ponoření dočasné/trvalé']],'l')}</div>
</div>

<h2>2. FVE</h2>
<div class="cols">
<div class="box2"><h3>Návrh řetězce</h3>
<span class="f">Voc,min = Voc·(1 + TKvoc·(Tmin − 25))</span>
<span class="f">Vmpp,hot = Vmpp·(1 + TKvmpp·(Tcell − 25))</span>
<span class="f">N,max = ⌊Vdc,max / Voc,min⌋</span>
<span class="f">N,min = ⌈Vmppt,od / Vmpp,hot⌉</span>
<span class="f">N,mppt = ⌊Vmppt,do / Vmpp,cold⌋</span>
<p class="note">Typicky Tmin −15 °C (ČR/SK), Tcell max 70 °C. Kontroluj i Isc·paralelní řetězce ≤ max. Isc MPPT a Impp·řetězce ≤ max. proud MPPT. Poměr DC/AC 1,0–1,3 je běžný.</p></div>
<div class="box2"><h3>Pojistky, kabely, jištění</h3>
<span class="f">gPV pojistka: 1,56·Isc ≤ In ≤ max. pojistka modulu</span>
<span class="f">Pojistky nutné, pokud (n − 1)·Isc &gt; max. zpětný proud modulu</span>
<span class="f">DC kabel: Iz ≥ 1,25·Isc ; ΔU ≤ 1–2 %</span>
<span class="f">ΔU_DC = I · 2·ρ·L / S</span>
<span class="f">AC jistič ≈ 1,1 · P / (√3·400)</span>
<p class="note">Solární kabel H1Z2Z2-K (ČSN EN 50618). DC odpínač, SPD DC/AC a RCD typ dle výrobce střídače.</p></div>
<div class="box2"><h3>Výnos (orientačně, ČR/SK)</h3>
{tbl(['Orientace / sklon','Koef.'],[['J 30–35° (optimum)','1,00'],['JV / JZ 30°','0,96'],['J plochá 10°','0,93'],['V–Z plochá 10°','0,88'],['V / Z 30°','0,86'],['J fasáda 90°','0,72'],['S 30°','0,60']],'l')}
<p class="note">Referenční výnos ≈ 1000 kWh/kWp·rok, degradace ≈ 0,5 %/rok. Pro nabídku použijte PVGIS.</p></div>
<div class="box2"><h3>Rozestup řad, baterie</h3>
<span class="f">h = 90° − φ − 23,44° (poledne 21. 12.)</span>
<span class="f">d = L·cosβ + L·sinβ / tg(h)</span>
<span class="f">Ebat,nom = E / (DoD · η)</span>
<p class="note">Pravidlo palce: 1–1,5 kWh baterie na 1 kWp pro zvýšení vlastní spotřeby.</p></div>
</div>

<h2>3. MaR</h2>
<div class="cols">
<div class="box2"><h3>Analogové signály</h3>
<span class="f">X = Xmin + (sig − sig,min)/(sig,max − sig,min) · (Xmax − Xmin)</span>
{ma_table()}
<p class="note">4–20 mA: porucha &lt; 3,8 mA, nadlimit &gt; 20,5 mA (NAMUR NE43). Siemens normalizované 0–27648.</p>
<span class="f">Smyčka: R,max = (Vnapájení − Vvysílač,min) / 22 mA</span></div>
<div class="box2"><h3>Čidla a hydraulika</h3>
<span class="f">Pt: R = R0·(1 + A·T + B·T²), T ≥ 0 °C</span>
<span class="f">A = 3,9083·10⁻³ ; B = −5,775·10⁻⁷ ; C = −4,183·10⁻¹²</span>
<span class="f">Chyba 2-vodič: ΔT = 2·ρ·L/S / (dR/dT)</span>
<span class="f">V̇ [m³/h] = P [kW] / (1,163 · ΔT [K])</span>
<span class="f">Kv = Q / √(Δp/100) [m³/h ; kPa]</span>
<span class="f">Autorita β = Δpventil / (Δpventil + Δpokruh) ≥ 0,3</span></div>
<div class="box2"><h3>PID — Ziegler–Nichols</h3>
{tbl(['Metoda kmitů (Ku, Tu)','Kp','Ti','Td'],[['P','0,5·Ku','–','–'],['PI','0,45·Ku','Tu/1,2','–'],['PID','0,6·Ku','0,5·Tu','0,125·Tu']],'l')}
{tbl(['Přechodová ch. (K, L, T)','Kp','Ti','Td'],[['P','T/(K·L)','–','–'],['PI','0,9·T/(K·L)','3,33·L','–'],['PID','1,2·T/(K·L)','2·L','0,5·L']],'l')}
<p class="note">U pomalých soustav (VZT, topení) začni s Kp o 30–50 % nižším.</p></div>
<div class="box2"><h3>Sběrnice a signály</h3>{tbl(['Typ','Poznámka'],[['Modbus RTU','RS-485, do 1200 m, zakončení 120 Ω, adresy 1–247'],['KNX TP','do 1000 m / linie, 9600 bit/s'],['Pt100/Pt1000','α = 0,00385; 3/4-vodič pro delší vedení'],['Ni1000','DIN: TK 6180 ppm; LG-Ni1000: 5000 ppm (jiná tabulka)'],['DI 24 V DC','log. 1 &gt; 15 V, log. 0 &lt; 5 V']],'l')}</div>
</div>
<h3>Odpory čidel</h3>
{temp_sensor_table()}

<h2 class="pg">4. Checklisty (k vytištění)</h2>
{checks()}

<h2 class="pg">5. Zatížitelnost — úplná tabulka a normy</h2>
{amp_full()}
<p class="note">Cu, 30 °C, 12 průřezů 1,5–120 mm². Zdroj: IEC 60364-5-52 / ČSN 33 2000-5-52; před použitím v projektu ověř proti aktuálnímu vydání.</p>
<h3>Normy a předpisy (ověř aktuální vydání)</h3>
{tbl(['Norma','Téma'],[['ČSN 33 2000-4-41','Ochrana před úrazem elektrickým proudem'],['ČSN 33 2000-4-43','Ochrana proti nadproudům'],['ČSN 33 2000-5-52','Elektrická vedení'],['ČSN 33 2000-6','Revize'],['ČSN 33 2000-7-712','Fotovoltaické (PV) soustavy'],['ČSN EN IEC 62548-1','Návrh PV polí'],['ČSN EN 62446-1','PV: dokumentace, uvedení do provozu, kontroly'],['ČSN EN 62305','Ochrana před bleskem'],['ČSN EN 61439','Rozváděče nn'],['ČSN 33 1500','Revize elektrických zařízení'],['ČSN EN 50110-1','Obsluha a práce na elektrických zařízeních'],['ČSN EN 61131-3','Programovací jazyky PLC']],'l')}
<footer>Pomůcka je orientační a nenahrazuje projekt, platné normy, předpisy distributora ani odpovědnost oprávněné osoby. Interaktivní verze: index.html, výpočty v Excelu: Pomucka_elektrikare.xlsx.</footer>
</body></html>'''

open(HTML, 'w', encoding='utf-8').write(html)
chrome = shutil.which('chromium') or shutil.which('google-chrome') or '/opt/pw-browsers/chromium'
cmd = [chrome, '--headless', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer', f'--print-to-pdf={OUT}', 'file://' + HTML]
r = subprocess.run(cmd, capture_output=True, text=True)
if not os.path.exists(OUT):
    print(r.stdout, r.stderr)
    sys.exit('PDF se nevytvořilo')
os.remove(HTML)
print('uloženo', OUT)
