# Energetické podklady Mondelez – shrnutí (texty v scratchpad/docs_energie/)

## 1) Interní ceny Mondelez – „Energiekosten Hydraulischer Abgleich" (xlsx→PDF, 2 str.)
| €/kWh (Druckluft €/m³) | Druckluft | Strom | Warmwasser | Kaltwasser | Gas | Öl |
|---|---|---|---|---|---|---|
| 2024 | 0,06 | 0,17 | 0,17 | 0,04 | 0,07 | 0,10 |
| 2025 | 0,05 | 0,20 | 0,17 | 0,07 | 0,07 | 0,10 |
| 2026 | 0,05 | 0,17 | 0,13 | 0,06 | 0,06 | 0,10 |
- Jen 2 desetinná místa, bez rozpadu (CO₂, síť, daně) a bez ceny za výkon (Leistungspreis). Neuvádí, zda je Gas vč. CO₂.

## 2) BDEW Gaspreisanalyse 08/2026 (obecná, DE) – klíčová čísla pro průmysl
- Malý průmysl 5–50 GWh/a (VEA, ct/kWh, vč. sítě a neodpočitatelných daní): 2024 **6,49** | 2025 **6,85** | 2026 **6,80**
  (z toho CO₂-Preis 0,80 / 0,97 / 1,15; Gasspeicherumlage 0,22 / 0,29 / –; Erdgassteuer 0,41). Měsíčně 2026: 5,7–7,7 ct (08/26 7,7; nárůst od 03/2026 – „Iran-Krieg").
- Střední průmysl 28–278 GWh/a (Eurostat): 2024 a 2025 **5,7** ct/kWh; velký 278–1 111 GWh/a: 2025 4,7 ct. Údaje 2026 nejsou.
- Burza THE spot Ø: 2024 34,63 | 2025 37,24 | 2026 (do 20.8.) 46,70 €/MWh; 20.8.2026 65,9 €/MWh. Termín Cal-27: 48,63 €/MWh (20.8.).
- EU-ETS CO₂ (EUA) Ø: 2024 66,45 | 2025 74,42 | 2026 78,14 €/t; 20.8.2026 82,45 €/t.
- Elektřina: BDEW (plynová analýza) žádnou cenu elektřiny neuvádí, jen index Destatis (graf).

## 3) Výkonové špičky – e-mail D. Brehm (Energymanager, Werk Lörrach), 09.09.2026 „Lastspitzen"
| Rok | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|
| kW | 7 481 | 7 406 | 7 814 | 7 811 | 6 769 | 7 781 | 7 608 |
- **Jen roční hodnoty – měsíční špičky v podkladu NEJSOU.** Název souboru „KW-Verbrauch" je zavádějící: jde o max. výkon (kW), ne spotřebu (kWh).
- Elektřina vs. teplo: **e-mail to výslovně neuvádí.** Rozsah 6 769–7 814 kW sedí přesně na tvrzení jiného dokumentu „elektřina"; „Lastspitzen" od energetika obvykle = elektrický odběr ze sítě (základ Leistungspreis) – ale jde o úsudek, potvrdit u D. Brehma. Neuvádí se ani, zda jde o celý závod Lörrach nebo jen Werk 2.

## 4) Relevance pro hydraulické vyvážení / ekonomiku
- Přímo relevantní jsou interní ceny Warmwasser (0,17→0,13 €/kWh), Kaltwasser (0,04–0,07) a Strom pro čerpadla (0,17–0,20) – hodnocení úspor tepla/chladu a el. práce čerpadel.
- Špičky: úspora příkonu čerpadel (desítky kW) by snížila Leistungspreis jen pokud se trefí do roční špičky; cena za kW v podkladech chybí.
- BDEW je jen kontext (trend: plyn 2026 roste, CO₂ roste) – pro výpočet ROI použít interní ceny Mondelez.

## 5) Rozpory s Änderungsliste Rev2
- **Plyn 59,8 €/MWh:** ≈ interní 2026 (0,06 €/kWh); proti 2024/25 (0,07 = 70 €/MWh) nižší; BDEW malý průmysl 2026 = 68 €/MWh vč. CO₂. Pokud je 59,8 bez CO₂ a CO₂ se přičítá zvlášť, hrozí dvojí započtení (interní cena rozpad neuvádí).
- **CO₂ 60 €/t:** pod EU-ETS Ø 2024–2026 (66–78 €/t, aktuálně 82,45). BDEW uvádí národní CO₂ v plynu jen v ct/kWh (1,15 ct 2026; při ~0,2 t/MWh ≈ 57 €/t – můj přepočet, ne údaj z dokumentu). Nutno ujasnit, který systém (BEHG vs. EU-ETS) Rev2 myslí.
- **Elektřina 166,7 €/MWh:** odpovídá interním 0,17 (2024, 2026), ne 2025 (0,20). OK, pokud referenční rok 2026.
- **Cena za výkon 120 €/kW·a:** **v žádném ze tří podkladů není** – zdroj neověřitelný, vyžádat od Mondelez/síťového tarifu.

## 6) MH BIM
Nic z toho není vstupem pro model v MH BIM (ceny, CO₂ a roční špičky se do geometrie/hydrauliky modelu nezadávají). Je to vstup jen pro ekonomické vyhodnocení/zprávu.
