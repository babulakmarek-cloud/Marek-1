# BE SYSTEMS – Koncepce stoupaček Bau 2 Mondelez (Rev. 3.1, 04.10.2026) – shrnutí
Zdroje: PDF 23 s. (citace „s. N“), XLSX 28 listů (citace „list …“; obsah dle listu Přehled shodný s PDF, navíc výpočetní listy 6.2a a 14.2 se vzorci). Domněnky = **[D]**.

## 1 Účel a rozsah
- Nový rozvod vytápění Bau 2: 2 stoupačky (S1, S2) na koncích výškové části, na každém podlaží rozdělovač L a R + příčné propojení (bypass, NC); vzorový rozdělovač 14× (s. 1, kap. 1–2).
- Cíle: redundance (n-1), dálkové odpojení každé zóny ze SCADA, měření (WMZ na okruh/zónu/stoupačku/bypass, EnMPRO 15 min), LOTO, oddělení tepla budova/proces (s. 1).
- Rozsah: KG + EG–5.OG = 14 zón (×L/R), 6.OG = technické podlaží s hlavami stoupaček (s. 1, 3). Status: návrh k odsouhlasení, ne realizační dokumentace (s. 1).

## 2 Stoupačky
| Stoupačka | Umístění | Podlaží | Napojení z KH2 (KG osa 5–9, řada A–C) | DN (A / B) | Průtok normál / A / B |
|---|---|---|---|---|---|
| S1 (strana L = strana KH2) | osa 0–1′, schodiště/stoupací šachta (stáv. potrubí „pro výrobu“, „pro klima 2.OG/5.OG“) | KG–6.OG | cca 37 m (s. 3) | DN125 / DN100 | 25,8 / 51,6 / 30,9 m³/h |
| S2 (strana R) | osa 38–39, trubní šachta B/39-38; hlava 6.OG u kotelny osa 35–37 | KG–6.OG | cca 151 m, trasa řada C/D, dilatace ~105 mm | DN125 / DN100 | 25,8 / 51,6 / 30,9 m³/h |
- Médium: otopná voda, návrh 70/50 °C; každá stoupačka vlastní čerpadlo P S1/P S2 (EC, zdvojené, Δp regulace dle PDT S na hlavě), WMZ S, XV+HV v patě, TK min. oběh v hlavě (s. 3–4, s. 7; list 11.2 Datové body stoup.).
- Odbočky zón: 14×, normál 3,7 m³/h (85 kW průměr), A DN65 7,4 m³/h, B DN50 4,4 m³/h; příčná propojení 7×: A DN50, B DN32 (s. 5, tab. 6.2; list 6.2a – vzorce, rychlosti 0,46–1,05 m/s „OK“).
- Celkem 1 200 kW (budova ~620 kW z modelu mh při 90/70 + proces ~580 kW, k potvrzení), ΔT 20 K → 51,6 m³/h (s. 5, tab. 6.1). TV bojlery 6.OG nově z hlavy S2; kotle Viessmann I–III mimo provoz (s. 3–4).
- Stávající: hlavní stoupačky 1–4 ve 4.OG u osy 36/37; KH2→KH4 DN150 (s. 4, s. 21).

## 3 Okruhy a teplotní úrovně
- Koncepce: dnes přívod 90 °C → cíl 70 °C (70/50); K1 budova stat. plochy 60/45 ekvitermně, K2 VZT 70/50 + protimraz, K3 proces nádrže a K4 doprovodný ohřev „T dle procesu (otevřené)“ (s. 3, s. 8). Stávající ohřev hmoty/plášťů 80/70, nádrže 38–60 °C, Massenbegleitheizung VL 80–90 / RL 38–70 (s. 3, s. 21). Procesní větev (TV bojler 1/2, Silberhalle 10, KH4 15/16, konše 17, venk. nádrže) zůstává na HR KH2 (s. 22, tab. 17.3).
- Porovnání s hladinami výkresů:
  - +90/+70 Prozess – odpovídá „dnes 90 °C“ a procesním okruhům 90 °C (s. 3); cíl: posoudit (70 °C / VT vývod / dohřev).
  - +90/+70 Klima – odpovídá dnešnímu stavu; koncepce cílí K2 na 70/50 (s. 8).
  - +60/+50 Heizkörper – **rozpor**: koncepce hodnotí tělesa proti 90/70 (s. 3, s. 5), ale výkresy už vedou okruhy těles 60/50; cíl K1 60/45 je tedy blízko stávající hladině **[D: hladina = návrh. teploty okruhu, ne primáru]**.
  - +45/+35 Prozess – v koncepci **není zmíněna** (nejbližší: nádrže 38–60 °C). Nutno přiřadit ke K3/K4.

## 4 Navržené změny a etapy
- Změny proti Rev. 2 (s. 3, list 2.1 Změny): poloha KH2 na konci výškové části, oddělená potrubí S1/S2, přiřazení UG=KG, E1–E6=EG–5.OG, 70 °C potvrzeno, kotle 6.OG mimo provoz, procesní větev, rozdělení X1/X2, náklady A 3 044 100 € / B 2 831 700 € bez DPH ±30 % (s. 18–19; list 14.2).
- Nové: rozdělení smíšeného okruhu X1/X2 (35 k€), přepojení 56 stáv. okruhů (140 k€), demontáže (60 k€), napojení TV bojlerů 6.OG (18 k€) (s. 18).
- Odpadne: přímé okruhy 5/6, 8/9, 3/4, 19/20 jako vývody KH2, staré stoupačky v šachtě, podružné rozdělovače (s. 22, 17.5).
- Doporučení BE SYSTEMS: varianta A (+212 400 €), případně mezistupeň (KG+stoupačky dle A, odbočky/bypassy dle B); při 1,5 MW DN150 (+59 500 €) (s. 6).
- **Etapy výstavby dokument nedefinuje**; zmíněno jen: prohlídka na místě před LPH 3, projekt LPH 5–8, postupný náběh zón (s. 4, 18, 21).

## 5 Vstupy pro model MH BIM (RohrSYS)
- Dimenze, kvs a čerpadla mají vzejít z RohrSYS (s. 3, otevřený bod 8, s. 20); koncepční DN jsou jen hrubé (s. 5).
- Zadání: 1 200 kW / 70/50 / 51,6 m³/h; 14 zón á ~85 kW (KG–2.OG větší – halová část do řady K, osa 13); délky KG 37 m a 151 m (+přídavek → 410 m VL+RL), stoupačky 2×38 m, odbočky 14×37 m, bypassy 7×74 m (s. 18, list 14.1); mezní rychlosti ≤DN50 0,7 / DN65–80 1,0 / ≥DN100 1,3 m/s (s. 5; list 6.2a vnitřní průměry).
- Scénáře: normál, n-1 A (100 %) a B (60 %), rozdělovače ≤0,5 m/s pro oba směry (s. 9).
- Ověření těles při 70/50 po místnostech (DIN EN 12831/HkCALC, bod 20) – zde vstupem soupisy těles z výkresů.
- Materiál: ≤DN100 C-ocel lisovaná, ≥DN125 P235GH svař./drážkové; izolace GEG příl. 8 100 % (s. 17).

## 6 Rozpory a nejasnosti v dokumentu
- Délka výškové části 146 m (s. 3, 21) vs. „148 m potvrzena“ (s. 21) a „105 mm na 148 m“ (s. 17); s. 4 uvádí 105 mm pro S2 151 m.
- Tab. 6.4 (s. 6, list 6.4): řádek „Vícenáklady A celkem“ = 3 044 100 / 2 831 700 €, ale uvedené podíly dávají 1 893 400 / 1 680 900 € (zbytek nerozepsán); rozdíly 212 500 vs. 212 400 € (zaokrouhlení). „≈ +8 %“ (s. 6) vs. 7,5 % (list 14.2).
- Stoupačky 2×38 m vs. „8 podlaží × 4,5 m“ = 36 m (s. 18) – přídavek nevysvětlen.
- Expanze 2,5 bar vs. hlava 6.OG ~36 m nad KH2 – sám dokument jako otevřený bod 16 **[D: 2,5 bar na statickou výšku 36 m nestačí]**.
- Budova 620 kW „model mh, 90/70“ vs. cíl 70/50 – výkon při 70/50 nedoložen (s. 5).
- Nejisté: zda halová část osa 5–13 patří k Bau 2, trasa C/D, přiřazení okruhů 17.3 (body 2, 15).

## 7 Porovnání se soupisy z výkresů (vystupy/*_soupis.xlsx)
Soupisy: 1UG, 3OG, 4OG, 5OG, 6OG, Sozialgebaeude, Versorgungsgang, Dachbereich_Aussentank. **Chybí EG, 1.OG, 2.OG** (koncepce má 7 úrovní zón).
- Teploty: hladiny ve všech soupisech (+90/+70 Prozess, +90/+70 Klima, +60/+50 HK, +45/+35 Prozess v 1UG/3OG/5OG) – viz bod 3; +45/+35 i +60/+50 v koncepci chybí.
- DN (list DN popisky): DN150 opakovaně na stejném místě X≈165 m/Y≈86 m (3OG, 4OG, 5OG; 1UG X≈170 m), DN125 X≈46–49 m a X≈62–67 m/Y≈77–79 m, DN100 X≈28 m/Y≈84 m – vše +90/+70 Prozess/Klima **[D: stávající svislé hlavní stoupačky]**. Shoda s koncepcí „stávající DN150/125/100“ (s. 21); nové S1/S2 DN125 (A) / DN100 (B) jsou ≤ stávajícím → podporuje otevřený bod 1a (zatížení možná >1 200 kW). Přiřazení X-souřadnic k osám 0–1′ / 38–39 neověřeno.
- Otopná tělesa (list Otopná tělesa; výkon „P≈“ z popisku, u „Nx“ nejasné na kus/celkem): 1UG 56 ks 78,6–118,8 kW; 3OG 42 ks 48,4 kW; 4OG 6 ks 7,0 kW; 5OG 38 ks 29,6–70,5 kW; 6OG 3 ks 5,0 kW; Sozialgebaeude 75 ks 34,0–52,4 kW; Versorgungsgang 1 ks 2,7 kW. Součet ≈ 206–305 kW vs. koncepce „budova ~620 kW“ (s. 5) – rozdíl může krýt VZT/klima a chybějící podlaží **[D]**. Teplota, ke které se P≈ vztahuje, ve výkresu neuvedena.
- Délky (list Potrubí dle hladin vs. tab. 17.4, s. 22; VL+RL, m): 3OG HK 517 vs. 503 ✓, Klima 51 vs. 53 ✓, Proces 677 vs. 1 104 ✗; 4OG 163/10/55 vs. 449/151/531 ✗ (soupis 4OG zjevně neúplný nebo jiný výkres); 5OG 626/153/1 241 vs. 439/382/416 ✗; 6OG 59/20/153 vs. 72/238/105 (+348 kotelna) ✗. Metody se liší (soupis vyřazuje uzavřené polylinie) – shoda jen ve 3OG.
- 1UG: soupis má oddělené hladiny dle druhu tepla (4 190 m proces, 2 416 m HK, 281 m klima), koncepce tvrdí, že v KG–1.OG nejsou sítě kresleny odděleně (s. 22) → **rozpor** – buď jiná verze DWG, nebo 1UG ≠ KG **[D: 1UG = KG, rozsah X do ~190 m odpovídá 196 m s halovou částí]**.
- Počty: koncepce 14 zón × 4 okruhy = 56 přepojených okruhů (s. 18) – ze soupisů nelze ověřit (okruhy nejsou v soupisech identifikovány).
