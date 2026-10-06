# MV-01 Rev. 3.2: doplněk ke koncepci stoupaček Bau 2 (shrnutí)
Zdroj: BE-2025-MON-001 · MV-01 · Rev. 3.2, 05.10.2026, 4 strany, „návrh k odsouhlasení, ne realizační dokumentace“ (s. 1). Platí spolu s Rev. 3.1, mění jen body v kap. 2 a přidává kap. 18–21 (s. 1).

## Změny proti Rev. 3.1 (kap. 2, s. 1–2)
- Č. 1 (kap. 2/3): oddělení budova/proces je **hydraulické**: zóny na S1/S2, procesní větev na HV KH2. WT-A/WT-P jsou větvová zatížení, ne výměníky. Výměníky jen pro glykolové okruhy (s. 1).
- Č. 2 (kap. 3): 70/50 °C jen pro zónovou síť, okruhy budovy ekvitermně 60/45 °C, RL ≤ 50 °C, proces 80–90 °C (bod T3) (s. 1).
- Č. 3 (kap. 3): NAT **−10 °C** místo −12 °C (DIN/TS 12831-1, PSČ 79539), podíl závislý na počasí 17 % (s. 1).
- Č. 4 (kap. 6.1): zatížení 1 200 kW porovnat s měřením: primár 2,58 MW, budova 0,79 MW, proces 1,08 MW, KH4 1,09 MW. **Citlivost 1,5 MW → DN150.** Potvrdit 15min daty (E7) (s. 1).
- Č. 5 (kap. 14.2): nová pol. 19, samostatný vývod KG → katakomby → sociální budova (cena po zaměření) (s. 1).
- Č. 6–9: nové kap. 18–21; č. 10: otevřené body 21–27 (s. 1–2).

## Okrajové podmínky (kap. 3, s. 2)
NAT −10 °C (282 m n. m.) · průměr 10,8 °C / otopné období 2,2 °C · GTZ 3 064 Kd (241 dnů) vs. SD-01 2 700 Kd, sjednotit (bod 23) · teploty: zóny 70/50, budova 60/45, proces 80–90, zásobníky 38–60 °C · KH2 12 082 MWh/a, špička 2,6 MW (2024) · Bau 2 závislé na počasí 1 425 MWh/a.

## Kap. 18 Hospodárnost (s. 2)
Stufe 1 (M1, M5–M7): 315 tis. €, 115,2 tis. €/a, 2,7 roku, NPV +932 tis. €. Stufe 2 (dvě stoupačky, **14 zón** řízených ze SCADA, přívod 70 °C): 2 847–3 059 tis. € (±30 %), s BHKW návratnost 131–141 let, bez BHKW 40–43 let. Celý balík bez BHKW: 10,4–11,1 roku. Stufe 2 je investice do infrastruktury (úzké místo 6.OG, kolísání tlaku, n-1).

## Kap. 19 Zdroje a tlak KH2 (s. 2–3)
BHKW MWM TCG 2020 V16 1 600 kW th (2011); LOOS B 1 500 kW (1988, primár 105 / sekundár 92 °C, max. 5,0 bar, PV 6,0 bar); LOOS C Unimat 4 750 kW (1989). Kotlový okruh oddělen deskovým výměníkem **GEA VT40 B-16** (10 bar / 110 °C, ≈ 2008, 1 420 kg). Expanze 2,5 bar = kotlový okruh, 6,0 bar = otopná síť. Hlava stoupaček v 6.OG ≈ 36 m nad KH2 (≈ 3,6 bar) (s. 3).
Důsledky: S1/S2 a procesní větev napojit na **sekundární (síťovou) stranu** výměníku. Udržování tlaku sítě navrhnout samostatně pro 6,0 bar. Výměník je jediný (úzké místo n-1), návrh: **druhý výměník paralelně 2 × 50–60 % špičky** nebo nouzový bypass. Ověřit výkon vůči 2,6 MW, desky a ΔT. Instalováno 7,85 MW vs. špička 2,6 MW (s. 3).
Pozn.: na s. 3 se v PDF překrývá text s tabulkou. Text uvádí „přiřazení ověřit na místě“, tabulka „potvrzeno 05.10.2026“.

## Kap. 20 Zásobníky hmoty, 56 ks (s. 3)
Conchen Süd 16, Nord 16, venkovní 12, 1.OG BA „A“ 5, KG Weiße Zone/máslo/QI 7. Z toho 29 přes výměník, 26 přímo, 1 neuvedeno. Tlaky 0,6–3,5 bar podle rozdělovačů 03/06/11/12/14/22/36/37. Všechny zůstávají na procesní větvi HV KH2, odpojování zón se jich netýká. Přímo ohřívané potřebují až 80–90 °C.

## Kap. 21 Po konci BHKW (s. 3–4)
BHKW má ≈ 105 000 Bh. Odpadní teplo C4 ≈ 24 GWh/a při 30–35 °C slouží jako zdroj pro TČ M8 (≈ 450 tis. €). WRG stlačeného vzduchu ≈ 2 200 MWh/a při 60–70 °C, vývod KH2 13/14 „Reserve“. Obojí vyžaduje RL ≤ 50 °C a zónovou síť 70/50 °C (s. 4).

## Otevřené body 21–27 (s. 4)
21 životnost BHKW/EnBW · 22 výměník GEA (výkon, desky, ΔT, BHKW primár/sekundár, n-1) · 23 NAT a GTZ · 24 přímo ohřívané zásobníky · 25 teplo C4 pro M8 · 26 trasa k sociální budově · 27 výměna oken (Ug 0,6), vliv na dimenze zón.

## Vstupy pro model v MH BIM (odvozeno z textu, ne výslovně uvedeno v doplňku)
- Topologie: KH2 → GEA VT40 B-16 → sekundár → S1/S2 (zóny, 14 zón) + procesní větev HV KH2 (56 zásobníků). Výměníky jen u glykolových okruhů (s. 1, 3).
- Systémy a teploty: zóny 70/50, budova 60/45 (RL ≤ 50), proces 80–90 °C (s. 1–2).
- Tlakový stupeň sítě 6,0 bar, statická výška ≈ 36 m (s. 3).
- DN: doplněk uvádí jen citlivost 1,5 MW → DN150. Jiné DN neuvádí, platí Rev. 3.1 (s. 1).
- Rezerva pro 2. výměník (paralelně) / bypass, vývod KH2 13/14 Reserve (WRG), nový vývod KG → sociální budova (pol. 19, trasa nezaměřena) (s. 1, 3, 4).
- Doplněk neuvádí žádné nové údaje o polohách stoupaček, podlažích (kromě 6.OG) ani o etapách nad rámec Stufe 1/2.
