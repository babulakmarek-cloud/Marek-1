#!/usr/bin/env python3
"""Generuje autoelektrika/Tahak_autoelektrika.pdf (A4). Vyžaduje Chromium (--headless --print-to-pdf)."""
import os, subprocess, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import CAB, FUSES, SOC12

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, '..', 'Tahak_autoelektrika.pdf'))
HTML = os.path.join(HERE, 'tahak.html')


def fmt(x, d=2):
    s = f'{x:.{d}f}'
    if '.' in s:
        s = s.rstrip('0').rstrip('.')
    return s.replace('.', ',')


def tbl(head, rows, cls=''):
    h = ''.join(f'<th>{x}</th>' for x in head)
    b = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<table class="{cls}"><tr>{h}</tr>{b}</table>'


RHO50 = 1 / 56 * (1 + 0.00393 * 30)


def cable_table():
    rows = []
    for s, a in CAB:
        mx = [f for f in FUSES if f <= a]
        rows.append([fmt(s), str(a), str(mx[-1]) if mx else '–'])
    return tbl(['mm² (Cu)', 'I trvalý (A)', 'max pojistka (A)'], rows, 'small')


def len_table():
    cur = [5, 10, 20, 30, 50, 100, 150, 200]
    rows = []
    for s, a in CAB:
        r = [fmt(s)]
        for i in cur:
            if i > a * 1.0:
                r.append('<span class="x">×</span>')
            else:
                L = 0.03 * 12 * s / (i * 2 * RHO50)
                r.append(fmt(L, 1) if L < 10 else fmt(L, 0))
        rows.append(r)
    return tbl(['mm² \\ A'] + [str(i) for i in cur], rows, 'small')


def soc_table():
    rows = []
    for v, p in reversed(SOC12):
        rows.append([f'{p} %'] + [fmt(v * k, 2) for k in (1, 2, 4)])
    return tbl(['Stav nabití (olovo, klid)', '12 V', '24 V', '48 V'], rows, 'small')


def volt_table():
    k = (1, 2, 4)
    def c(b): return [fmt(b * x, 1) for x in k]
    def rg(a, b): return [f'{fmt(a * x, 1)}–{fmt(b * x, 1)}' for x in k]
    rows = [['Olovo: plně nabité v klidu'] + c(12.7), ['Olovo: absorpce (typ.)'] + rg(14.4, 14.8), ['Olovo: float'] + rg(13.5, 13.8),
            ['Olovo: odpojení zátěže'] + c(10.5), ['LiFePO₄ jmenovité (4S / 8S / 16S)'] + c(12.8),
            ['LiFePO₄ nabíjení'] + rg(14.2, 14.6), ['LiFePO₄ odpojení zátěže'] + rg(10, 11), ['Alternátor při chodu', '13,8–14,8', '27,6–29,6', '–']]
    return tbl(['', '12 V', '24 V', '48 V'], rows, 'small')


FUSEC = [('1', '#222', 'černá'), ('2', '#9a9a9a', 'šedá'), ('3', '#7b4fa6', 'fialová'), ('4', '#e58fb4', 'růžová'), ('5', '#c8a86a', 'béžová'),
         ('7,5', '#8b5a2b', 'hnědá'), ('10', '#d62828', 'červená'), ('15', '#6fb7e8', 'sv. modrá'), ('20', '#f2c200', 'žlutá'),
         ('25', '#f2f2f2', 'bílá/čirá'), ('30', '#3fa34d', 'zelená'), ('40', '#f08a24', 'oranžová')]


def fuse_table():
    cells = ''.join(f'<tr><td><span class="sw" style="background:{c}"></span>{n}</td><td>{a} A</td></tr>' for a, c, n in FUSEC)
    return f'<table class="small">{cells}</table>'


CHECK = {
 'Instalace nového spotřebiče / okruhu': [
  'Určen trvalý a špičkový proud spotřebiče', 'Pojistka co nejblíž ke zdroji (baterii), dimenzovaná na kabel',
  'Průřez zkontrolován na úbytek napětí i na trvalý proud', 'Kabel odolný teplu a oděru, vlnovec, průchodky v plechu',
  'Kvalitní lisované koncovky a spoje, správná velikost oka', 'Velké zátěže spínány přes relé / stykač',
  'Kostrový spoj čistý, kov na kov, zajištěn proti uvolnění', 'Spoje utaženy předepsaným momentem, svorky zakryty',
  'Změřen úbytek napětí na plus i mínus pod zátěží', 'Zákres do schématu, kabely označeny'],
 'Diagnostika baterie a nabíjení (12 V; u 24/48 V násobky)': [
  'Vizuálně: svorky, koroze, uchycení, oleje, zápach', 'Napětí v klidu (po ≥ 4 h): ≥ 12,4 V (24 V: 24,8 V)',
  'Při startu napětí nesmí klesnout pod ≈ 9,6 V (24 V: 19,2 V)', 'Napětí při běžícím motoru: 13,8–14,8 V (24 V: 27,6–29,6 V)',
  'Úbytek na kladném kabelu při startu: < 0,5 V', 'Úbytek na kostře při startu: < 0,3 V',
  'Klidový odběr po uspání: typicky < 50 mA (dle výrobce)', 'Zvlnění alternátoru (AC) při chodu: < 0,5 V',
  'Alternátor, řemen a pojistky nabíjecího okruhu OK'],
 'Ostrovní systém 12/24/48 V (karavan, loď, dodávka)': [
  'Baterie s vhodným BMS / ochranami, ventilace u olova', 'Hlavní pojistka (MEGA / Class T) a hlavní vypínač u baterie',
  'Pro 48 V: pojistky, vypínače a relé s DC napětím ≥ 58 V', 'Samostatná pojistka na každou větev paralelních baterií',
  'Měření (shunt, BMS) zapojeno, nastavena kapacita a napětí', 'Solární regulátor nastaven na typ baterie, kontrola Voc za mrazu',
  'Střídač: DC kabel krátký a dostatečný, pojistka u baterie', 'AC strana: RCD/jistič, ochrana a uzemnění dle typu aplikace',
  'Společná kostra / záporná sběrnice, jedno místo spojení s kostrou', 'Polarita a štítky na všech vodičích, zkušební zapnutí po částech',
  'Zátěžový test: výdrž, úbytky, teploty spojů'],
}


def checks():
    out = []
    for t, items in CHECK.items():
        out.append(f'<section class="chk"><h3>{t}</h3>' + ''.join(f'<div class="ci"><span class="box"></span>{i}</div>' for i in items) +
                   '<div class="sig">Datum: ____________ &nbsp;&nbsp; Provedl: ____________________ &nbsp;&nbsp; Podpis: ____________</div></section>')
    return ''.join(out)


html = f'''<!doctype html><html lang="cs"><head><meta charset="utf-8"><title>Tahák autoelektrika</title>
<style>
@page{{size:A4;margin:11mm 10mm}}
*{{box-sizing:border-box}}
body{{font:8.6pt/1.32 "DejaVu Sans",Arial,sans-serif;color:#16202c;margin:0}}
h1{{font-size:17pt;margin:0 0 1mm;color:#d8590b}}
h2{{font-size:11pt;margin:4mm 0 1.5mm;padding:1mm 2mm;background:#d8590b;color:#fff;border-radius:2px;break-after:avoid}}
h3{{font-size:9.2pt;margin:2.5mm 0 1mm;color:#d8590b;break-after:avoid}}
.sub{{color:#5b6877;margin:0 0 2mm}}
.cols{{column-count:2;column-gap:6mm}}
.box2{{width:100%;border:.3mm solid #c9d3de;border-radius:2px;padding:1.5mm 2.5mm;margin:0 0 2.2mm;break-inside:avoid}}
.f{{font-family:"DejaVu Sans Mono",monospace;background:#fdf0e6;padding:.6mm 1.4mm;border-radius:2px;display:block;margin:.7mm 0}}
table{{border-collapse:collapse;width:100%;margin:1mm 0 2mm;break-inside:avoid}}
th,td{{border:.25mm solid #c9d3de;padding:.5mm 1.4mm;text-align:left}}
th{{background:#fdeee3}}
table.small{{font-size:7.6pt}}
td:not(:first-child){{text-align:right}}
.l td{{text-align:left}}
.x{{color:#b3261e;font-weight:bold}}
.sw{{display:inline-block;width:3mm;height:3mm;border:.25mm solid #888;margin-right:1.5mm;vertical-align:-.5mm}}
.note{{color:#5b6877;font-size:7.5pt}}
.pg{{break-before:page}}
.chk{{margin-bottom:6mm;break-inside:avoid}}
.ci{{display:flex;gap:2mm;padding:1.1mm 0;border-bottom:.2mm solid #dde3ea;font-size:9pt}}
.box{{flex:0 0 3.4mm;height:3.4mm;border:.35mm solid #16202c;margin-top:.4mm}}
.sig{{margin-top:3mm;font-size:8.5pt;color:#5b6877}}
footer{{margin-top:4mm;color:#5b6877;font-size:7.3pt}}
</style></head><body>
<h1>🚗 Tahák autoelektrika 12 / 24 / 48 V</h1>
<p class="sub">Kabely, pojistky, baterie, měniče, solár. Orientační pomůcka, rozhodují údaje výrobce a platné předpisy.</p>

<h2>1. Vzorce</h2>
<div class="cols">
<div class="box2"><h3>Kabel a úbytek napětí</h3>
<span class="f">I = P / U</span>
<span class="f">ΔU = I · ρ · L · k / S</span>
<span class="f">k = 2 (vlastní zpětný vodič), 1 (kostra)</span>
<span class="f">ρ(θ) = 1/56 · (1 + 0,00393·(θ − 20)) Ω·mm²/m</span>
<span class="f">Pztrát = I² · ρ · L · k / S</span>
<p class="note">Limit úbytku: 1 % citlivé obvody, 3 % běžné, 5 % nekritické. Startér: úbytek do 0,5 V. Při stejném výkonu je proud při 24 V poloviční a při 48 V čtvrtinový, ztráty v kabelu ¼ resp. 1⁄16.</p></div>
<div class="box2"><h3>Pojistka a zkrat</h3>
<span class="f">In,pojistky ≥ 1,25 · Itrvalý</span>
<span class="f">In,pojistky ≤ Itrvalý,kabelu</span>
<span class="f">Isc ≈ U / (Rint + Rkabelu)</span>
<p class="note">Pojistku dej co nejblíž ke zdroji. Plochá autopojistka je na 32 V DC, pro 48 V potřebuješ ≥ 58 V (MRBF, MIDI/MEGA 58 V, Class T). Při Isc &gt; 1000 A použij MEGA / ANL / Class T.</p></div>
<div class="box2"><h3>Baterie</h3>
<span class="f">E [Wh] = U · Ah</span>
<span class="f">Výdrž [h] = U·Ah·DoD·η / P</span>
<span class="f">Ah potřebná = P·t / (U·DoD·η)</span>
<span class="f">t nabíjení = Ah·Δ% / (η · Inab)</span>
<p class="note">DoD: olovo 50 %, LiFePO₄ 80–90 %. Účinnost nabíjení: olovo ≈ 85 %, LiFePO₄ ≈ 95 %. Olovo: poslední ≈ 20 % trvá o hodiny déle.</p></div>
<div class="box2"><h3>Měnič, střídač, solár, LED</h3>
<span class="f">DC-DC: Iin = Uout·Iout / (Uin·η)</span>
<span class="f">Střídač: IDC = PAC / (U·η), pojistka ≥ 1,25·IDC</span>
<span class="f">Solár: Inab = Wp·η / Unab (MPPT 0,95; PWM 0,78)</span>
<span class="f">Voc,min = Voc·(1 + TK·(Tmin − 25))·N ≤ Vpv,max</span>
<span class="f">LED: R = (Uzdroj − n·Vf) / If</span>
<p class="note">Použij UZDROJ při nabíjení (14,4 / 28,8 / 57,6 V). Výnos solárů: léto ≈ 4–5 h, jaro/podzim 2–3 h, zima 0,5–1 h plného výkonu za den.</p></div>
</div>

<h2>2. Kabely</h2>
<div class="cols">
<div class="box2"><h3>Trvalý proud a max. pojistka</h3>{cable_table()}
<p class="note">Konzervativní hodnoty pro měděné vodiče ve svazku.</p></div>
<div class="box2"><h3>Max. délka kabelu pro úbytek 3 % (12 V)</h3>{len_table()}
<p class="note">Délka jednosměrně [m], vlastní zpětný vodič, 50 °C. Pro 24 V × 2, pro 48 V × 4. × = proud přesahuje trvalou zatížitelnost kabelu.</p></div>
</div>

<h2 class="pg">3. Napětí, baterie, pojistky</h2>
<div class="cols">
<div class="box2"><h3>Typická napětí podle soustavy</h3>{volt_table()}
<p class="note">Orientační. Nabíjecí a odpojovací napětí řiď údaji výrobce baterie / BMS.</p></div>
<div class="box2"><h3>Stav nabití olova z napětí v klidu</h3>{soc_table()}
<p class="note">Měř po min. 4 h klidu. LiFePO₄ nelze (plochá křivka), čti BMS / shunt.</p></div>
<div class="box2"><h3>Barvy plochých pojistek (ISO 8820)</h3>{fuse_table()}</div>
<div class="box2"><h3>Značení svorek a relé</h3>{tbl(['Svorka','Význam'],[['30','trvalé + z baterie'],['31','kostra (−)'],['15','+ po zapnutí zapalování'],['50','startér'],['56 / 58','hlavní / obrysová světla'],['49 / 49a','směrovky vstup / výstup'],['61','kontrolka nabíjení'],['85 / 86','relé: cívka'],['30','relé: společný kontakt'],['87 / 87a','relé: NO / NC']],'l')}</div>
<div class="box2"><h3>Orientační příkony</h3>{tbl(['Spotřebič','W'],[['Halogen H4/H7','55–60'],['LED hlavní světlo','20–40'],['Brzdové světlo','21'],['Stěrače','60–90'],['Ventilátor topení','100–250'],['Kompresorová chladnička','40–60'],['Vodní čerpadlo','30–80'],['LED pásek 5050 (60/m)','14 W/m'],['Startér (špička)','1–3 kW']],'l')}</div>
<div class="box2"><h3>12 V vs. 24 V vs. 48 V</h3>{tbl(['','12 V','24 V','48 V'],[['Proud při 1 kW','83 A','42 A','21 A'],['Ztráty v kabelu','1×','¼','1⁄16'],['Použití','osobní, karavan','nákladní, lodě','mild-hybrid, ostrov']],'l')}
<p class="note">48 V je pod mezí 60 V DC, ale zkratový proud baterie je nebezpečný. Sundej svorku −, používej izolované nářadí.</p></div>
</div>

<h2 class="pg">4. Checklisty (k vytištění)</h2>
{checks()}
<footer>Pomůcka je orientační a nenahrazuje údaje výrobce vozidla, baterie ani měniče ani platné předpisy. Interaktivní verze: index.html, výpočty v Excelu: Pomucka_autoelektrika.xlsx.</footer>
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
