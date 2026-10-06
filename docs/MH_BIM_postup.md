# Werk 2 v MH BIM – postup krok za krokem

Stav 2026-10-06. Nabídky a ovládání MH BIM jsem neověřoval (manuály RaumGEO, RohrSYS a Projektverwaltung chybí, web výrobce je z cloudu blokovaný). Názvy modulů jsou podle `docs/web/`, konkrétní tlačítka si dohledej v programu.

Pracovní soubor: **`vystupy/MHBIM_zadavaci_list.xlsx`**
- **Postup – checklist**: kroky níže, se sloupcem „Hotovo“.
- **Podlaží**: stav podkladů, počet a výkon těles z výkresu, kontrolní Q z Abgleich. Doplň sem výšky podlaží a vztažný bod.
- **Systémy z hladin**: přiřazení hladin DXF k okruhům a teplotám. Jsou tu i délky potrubí po podlažích.
- **Otopná tělesa**: 148 záznamů (typ, výkon, X/Y, hladina) a sloupce pro místnost a stav zadání.
- **Rozdělovače / Okruhy Raumheizung / Čerpadla**: převzato ze `System_Uebersicht_Werk2.xlsx`.

List se dá znovu vygenerovat příkazem `python tools/make_mhbim_list.py`.

## Hotovo
- **6.OG**: čisté podklady `vystupy/podklady_mhbim/6OG_arch.dxf` a `6OG_heiz.dxf`, posunuté na vztažný bod osa 39 × osa E. Podrobnosti v `vystupy/podklady_mhbim/README.md`.

## 1. Podklady (AutoCAD / Python, na PC)
1. **Vztažný bod**: průsečík osy 39 a osy E. V 6.OG leží na X = 24331, Y = 68325 (mm). U každého dalšího podlaží ověř, že je tam stejný průsečík, a jeho souřadnice zapiš do listu Podlaží.
2. Pro každé DXF podlaží spusť:
   ```
   pip install ezdxf
   python tools\mhbim_podklad.py 6OG.dxf --seznam
   ```
   Vypíše hladiny a navrženou skupinu (`arch` = A0…, `heiz` = Heiz…/HEIZUNG…). Hladiny mimo obě skupiny (Sprinkler, Elektro…) se do podkladu nedostanou. Když je potřeba, uprav výběr přes `--hladiny "REGEX"`.
3. Export čistých podkladů:
   ```
   python tools\mhbim_podklad.py 6OG.dxf 6OG_arch.dxf --profil arch --posun X,Y --bez-srafy
   python tools\mhbim_podklad.py 6OG.dxf 6OG_heiz.dxf --profil heiz --posun X,Y
   ```
   `--oblast XMIN,YMIN,XMAX,YMAX` ořízne situaci a razítko (v 6.OG: `15000,60000,178000,95000`).
   Pro celou složku najednou: `tools\priprav_podklady.bat X,Y` (výstup jde do `mhbim\`).
4. Pozor:
   - **Sozialgebäude** leží v jiném souřadném systému (tělesa mají X ≈ −1,5 mil. mm), takže potřebuje vlastní posun. Do dávky ho nedávej.
   - **1.OG / 2.OG** (790–900 MB): nejdřív v AutoCADu `AUDIT`, `PURGE` a `WBLOCK` jen modelu, teprve potom skript.
   - **EG** existuje jen jako DWG: v AutoCADu ho ulož jako DXF 2010.
   - Jestli MH BIM DXF nebere, ulož výstup v AutoCADu jako DWG.

## 2. Projekt a budova (MH BIM)
1. V mh-Projektverwaltung založ nový projekt. Cesta musí být na lokálním disku s písmenem, ne UNC ani synchronizovaná cloudová složka.
2. Zadej lokalitu Lörrach (Brembocher Str. 37, ulice napsaná podle PDF) a klimatická data.
3. Založ podlaží 1.UG, EG, 1.OG–6.OG, Dach a další budovy/části (Sozialgebäude, Versorgungsgang). Výšky v podkladech nejsou, doplň je z řezů nebo zaměření.
4. Do každého podlaží vlož odpovídající `*_arch.dxf` a `*_heiz.dxf` v jednotkách mm. Zkontroluj, že se podlaží kryjí, třeba podle schodiště nebo šachty.

## 3. Místnosti (RaumGEO)
- Zdi a místnosti obkresli nad podkladem `*_arch`. Automatické rozpoznání zdí z DWG jsem v dostupných zdrojích nenašel.
- Pokud se má počítat tepelná ztráta (EN 12831), zadej i skladby konstrukcí. Hodnoty Q v Abgleich jsou jen odhady.

## 4. Topení (RohrSYS)
1. **Zdroje a rozdělovače** (list Rozdělovače):
   - zdroj LOOS B+C v KH2 (1.OG),
   - hlavní rozdělovač KH2 `Q.1.08.1`,
   - podružné rozdělovače KH4 (6.OG) a KH6 (Sozialgebäude),
   - Verteiler 01, 04, 41 a další.
2. **Okruhy a teploty** (list Systémy z hladin):

   | Hladiny | Okruh | Teploty VL/RL |
   |---|---|---|
   | `+60 Heizkörper V` / `+50 … R` | Raumheizung | 60/50 |
   | `+90 Prozess V` / `+70 Prozess R` | Prozessheizung | 90/70 |
   | `+45` / `+35 Prozess` | pravděpodobně OPM1 | 45/35 |
   | `+90 Klima` / `+70 Klima` | Klimaheizung | **rozpor:** hladiny 90/70, topologie 70/55, nutno rozhodnout |
   | `HEIZUNG VORLAUF/RÜCKLAUF` (bez teploty) | dořadit podle výkresu | ? |
   | `blind` | nemodelovat | – |
3. **Otopná tělesa**: umísti je podle X/Y z listu Otopná tělesa. Od souřadnic odečti vztažný bod, tedy stejný posun jako u podkladu. Výkon z popisku `P ≈ … W` ber jako kontrolní hodnotu. U `3x …` není jasné, jestli je výkon na kus.
4. **Potrubí** kresli jako Systemlinien po trasách z `*_heiz`. DN z výkresu (listy „DN popisky“ v soupisech) slouží jen ke kontrole automatického dimenzování.

## 5. Výpočet a kontrola
- Spusť dimenzování a hydraulické vyvážení.
- Porovnej průtoky s `q_V_soll` v listu Okruhy Raumheizung a typy čerpadel s listem Čerpadla.

## 6. Výstup
- IFC 4 s mh-Data, DWG/PDF plány.

## Co ještě chybí (blokuje přesnost)
- DXF pro EG, 1.OG a 2.OG zatím nejsou zpracované (soupisy chybí).
- Výšky podlaží.
- Rozhodnutí o teplotách Klimaheizung (90/70 vs. 70/55).
- Manuály RaumGEO, RohrSYS a Projektverwaltung, které by potvrdily ovládání.
