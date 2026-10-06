# Analyse Wärmedaten 2025 – Mondelez Lörrach Bau 2, Rev. 1 (BE SYSTEMS, BE-2025-MON-001, 04.10.2026)

## Listy (12, všechny malé, 12–30 řádků, max. 18 sloupců)
- **Folgerungen** (A:D, 15 bodů): Nr. / Thema / Befund 2025 / Konsequenz pro koncept.
- **Wirtschaftlichkeit v4** (A:I): moduly M1–M9 (podíly úspor A/P, invest., €/a) + 10 variant (úspora, NPV 15 let/6 %, IRR, plyn, CO₂).
- **Monatsbilanz Kessel** (A:J): měsíčně KH2 total, BHKW teplo, plyn kotlů LOOS B+C, teplo kotlů, bilanční mezera.
- **Parameter** (A:D): vstupy výpočtu (žluté).
- **Daten 2025** (A:R): měsíční data 2025 – T venk., KH2, KH4, BHKW, plyn LOOS B/C, průměrné výkony.
- **Energiesignatur**: regrese P = P0 + k·max(0; Tb − T) přes 12 měsíčních průměrů.
- **Abnehmer KH2** (A:G): podružné měřiče, podíl, Jan/Jul, přiřazení k síti A/P.
- **Dimensionierung** (A:H): návrh VS (WT) a průtoků.
- **Abwärme**: kompresory, chlad C4. **Bilanz Werk 2025**: elektřina/plyn/chlad celého závodu. **Wärmedaten 2024**: kontrola s denními daty 2024.

## Co se měří
- Měsíční hodnoty 2025 (Jan–Dez, MWh) ze souboru „Referenzdaten Energieverbraucher 2025“ (547 měřičů, ≈170 prázdných/nevěrohodných); venkovní T z 15min dat EnMPRO.
- Hlavní měřič d_KH2_Total_Heating_MWh, Verbund KH4, BHKW teplo, plyn kotlů LOOS B/C (Nm³), podružné: Conchen 800/900, OPM1 Prozess, Klima 1/2, Verteiler 13, Silberhalle, Space Heating, OPM1 HVAC, Boiler Water.
- **Teploty přívod/zpátečka se neměří – v souboru nejsou.** Jen návrhové ΔT: síť A 15 K (cíl 60/45 °C), síť P 20 K (70 °C dle M2).

## Roční spotřeby 2025 [MWh]
KH2 celkem 12 082 · Verbund KH4 4 635 (38 %) · KH2 bez KH4 (≈ Bau 2) 7 447 · BHKW teplo 10 215 (84,5 %) · teplo kotlů 1 174 · bilanční mezera 713.
Podružné: Conchen 573, OPM1 Prozess 493, Klima 2 138, Klima 1 126, Verteiler 13 91, Silberhalle 58, OPM1 HVAC 57, Space Heating 32, Boiler Water 24; Rest neměřeno 5 855 (48,5 %).
2024 pro srovnání: KH2 12 099, KH4 5 099.

## Měsíční KH2 total [MWh] (KH2 bez KH4 / T venk. °C)
Jan 1 329 (808 / 3,4) · Feb 1 139 (727 / 4,5) · Mär 1 147 (721 / 8,7) · Apr 926 (607 / 11,9) · Mai 932 (560 / 14,7) · Jun 803 (481 / 22,2) · Jul 822 (491 / 20,6) · Aug 835 (496 / 21,2) · Sep 814 (470 / 16,2) · Okt 1 030 (831 / 11,4, KH4 měřič podezřelý) · Nov 1 117 (618 / 6,2) · Dez 1 187 (637 / 4,4).
Teplo kotlů jen Jan 377, Feb 230, Mär 220, Jun 149, Jul 119 (revize BHKW), Dez 56; ostatní ≈ 0–9.

## Výkony
- Průměrné měsíční výkony KH2: 1,11–1,79 MW (max Jan 1,79); KH2 bez KH4 0,65–1,12 MW; KH4 0,27–0,74 MW.
- Energetická signatura (Tb 15 °C, NAT −12 °C): KH2 P0 1,15 MW, k 0,0506 MW/K, R² 0,95; bez KH4 P0 0,72 MW, k 0,028, R² 0,56; KH4 P0 0,43 MW, R² 0,61.
- Výkon při NAT (měs. model): KH2 2,52 MW (vč. špičkového faktoru 2,58); bez KH4 1,48 (1,52); KH4 1,04 (1,07). Vytápěcí podíl při NAT: 1,37 / 0,76 / 0,61 MW.
- Naměřená 15min špička KH2: 2,64 MW (2024, Parameter) resp. 2,6 MW 11.01.2024; pro 2025 jen měsíční hodnoty.
- Podíl závislý na počasí: KH2 17 % (2 012 MWh), bez KH4 15 % (1 113 MWh; metodou denostupňů 1 425 → rozpětí 1 100–1 430).
- Špičky 7,4–7,8 MW (D. Brehm) = elektřina, ne teplo KH2.

## Závěry analýzy (Folgerungen, výběr)
1. 83 % tepla KH2 je základní zatížení → síť P hlavní spotřebitel, úspory sítě A držet nízko.
2. KH4 jako samostatná větev na primárním rozdělovači (doplnit schéma Blatt 01 + výkaz).
3. WT-A ≈ 0,8 MW potvrzeno; WT-P spíš ≈ 1,1 MW místo 1,5 MW (ověřit 15min daty).
4. Úspory plynu jen v měsících s kotli; v4 M1–M6 ≈ 92 T€/a místo 136 T€/a (v3); balík M1–M7+M9 základ 137 T€/a, invest. 900 T€, návratnost 6,6 let.
5. Nejsilnější páka M7 rekuperace kompresorů (≈ 1 900 MWh/a při 70 °C); M3/M4 energeticky 15–30 let → zdůvodnit jako technický předpoklad.
6. Rozpor s §8 dokumentace hydraul. vyvážení („dělení okruhů nedoporučeno“); bilanční mezera ≈ 710 MWh/a vyjasnit s D. Brehmem; vyžádat 15min data KH2, KH4, BHKW.

## Vstupy pro MH BIM (model/dimenzování)
| Větev | Návrhový výkon | ΔT | Průtok | DN orient. |
|---|---|---|---|---|
| WT-A síť A (Bau 2) | 0,794 MW | 15 K | 45,5 m³/h | DN 125 |
| WT-P síť P (Bau 2) | 1,085 MW | 20 K | 46,6 m³/h | DN 125 |
| Větev Verbund KH4 | 1,088 MW | 20 K | 46,8 m³/h | DN 125 |
| Primární rozdělovač celkem | 2,584 MW | 20 K | 111,1 m³/h | DN 200 |
- DN jen hrubě (ocel, 1,0–1,5 m/s); závazně dle výpočtu sítě „mh-BIM RohrSYS“.
- Kontrola tepelných ztrát: instalovaný výkon otopných těles dle Erfassung 576 kW + Luftheizer (vs. WT-A 0,79 MW) – vlastní výpočet ztrát dle DIN/TS 12831-1 v souboru není.
- Předpoklady k ověření: špičkový faktor procesu 1,5 (ANNAHME), vytápění 1,05; výhřevnost 10 kWh/Nm³, η kotlů 0,9.
- Pozn.: Daten 2025 řádek 20 je zastaralá poznámka z Rev. 0 (Apr/Mai vyřazeny), v Rev. 1 jsou zahrnuty (ř. 19).
