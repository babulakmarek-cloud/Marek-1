# Referenzdaten 2025 + Wetterdaten – shrnutí

## 1) Referenzdaten_Energieverbraucher_2025.xlsx
- 1 list `Tabelle1`, transponovaný: sloupec B = popisky, řádek 3 = názvy měřičů, řádky 4–15 = měsíce leden–prosinec 2025 (měsíční součty). **547 pojmenovaných sloupců** (1 sloupec bez názvu) → údaj 547 sedí.
- Jednotky podle přípony názvu: kWh 212, MWh 36, m3/m³ 68, Nm3 15, l 13, tons 2, kW 1, ~200 bez jednotky (m_* KPI/vypočtené, ručně psané řádky). Sloupce ~492–546 (Kessel-Lieferung, Gas in kWh, Kosten…) jsou prázdné nebo `#REF!` – nepoužitelné.
- Pozor: duplicity – `d_OPM1_Process_Cooling/Heating_MWh` je 2× (sl. 9/10 kompletní; sl. 471/472 jen 03–12). `m_DE_Loe_Conchen_800/900` = konstanta 94,3/95,7 každý měsíc (není spotřeba).

| Měřič (název v souboru) | Σ 2025 | Jiná analýza | Výsledek |
|---|---|---|---|
| d_KH2_Total_Heating_MWh | 12 081,8 MWh | 12 082 | shoda |
| d_Verbund_KH4_Heating_MWh | 4 634,9 | 4 635 | shoda |
| d_BHKW_Heating_MWh | 10 214,7 | 10 215 | shoda |
| d_LOOS_B_Gas_Nm3 + d_LOOS_C_Gas_Nm3 | 12 596 + 117 876 = 130 472 Nm³ | kotle 1 174 MWh | v souboru není přímo v MWh; 1 174 MWh ≈ 130 472 Nm³ × 9,0 kWh/Nm³ (moje domněnka o přepočtu, neověřeno) |
| d_800_900_Heating_MWh (Conchen) | 573,1 | 573 | shoda |
| d_OPM1_Process_Heating_MWh (sl. 10) | 493,1 | 493 | shoda (duplicitní sl. 472 = 463,5, chybí 01–02) |
| d_Klima_2_Heating_MWh | 138,4 | 138 | shoda |
| d_Klima_1_Heating_MWh | 126,1 | 126 | shoda |
| d_Verteiler_13_Heating_MWh | 90,5 | 91 | shoda |
| d_Silberhalle_Heating_MWh | 58,0 | 58 | shoda |
| d_OPM1_KB_HVAC_Heating 20,0 + d_OPM1_WB_HVAC_Heating 37,2 | 57,2 | OPM1 HVAC 57 | shoda jen jako součet KB+WB |
| d_Space_Heating_Heating_MWh | 31,9 | 32 | shoda |
| d_Boiler_Water_Heating_MWh | 24,1 | 24 | shoda |

Další relevantní: d_LOOS_D_Gas_Nm3 105 492 Nm³ (jen 01–09); m_Wärmemenge LOOS B 33 959 335 / LOOS C 228 885 507 (bez jednotky; LOOS C má nuly v 06–07 přestože plyn byl – nekonzistentní); d_BHKW_Gas_Nm3 2 289 834; d_Werk2_Gas_Nm3 2 420 306; d_BHKW_Generated_Electricity_MWh 9 686; d_Ruehrwerke_Heating 0. Chlad: d_OPM1_Process_Cooling 1 313,4, OPM1_KB_HVAC_Cooling 741,8, OPM1_WB_HVAC_Cooling 99,4 (1 měsíc „-“), d_MH1_Cooling_freie_Kuehlung 2 280,1, d_MH7_Cooling 3 637,7, C1–C4 Cooling ±2 (C4 +2: 7 901,8; C4 −2: 11 475,8) MWh.
Profil KH2: max leden 1 329, min červen 803 MWh/měs → velká letní základní (procesní) zátěž, ne jen vytápění.

## 2) Wetterdaten_Hydraulischer_Abgleich_Marek_09.2026.xlsx
- Listy: `EnMPRO_d_Weather_Humidity_P (2)` (69 850 hodnot), `EnMPRO_d_Weather_Temperature_C ` (69 851), `Tabelle1` prázdný.
- Zdroj: export z EnMPRO (tag d_Weather_Temperature_C / Humidity), sloupec LOKAL_DATUM – stanice/poloha čidla v souboru **neuvedena**.
- Interval 15 min, období 2024-01-01 00:15 – 2026-01-01 00:00 (2 roky); místní čas (DST skoky), 34 mezer 30 min + pár delších; 3 (2024) / 5 (2025) neúplných dnů.

| | 2024 | 2025 |
|---|---|---|
| Průměr (15min) | 12,84 °C | 12,23 °C |
| Min | −6,5 °C (20.1. 08:45) | −7,5 °C (31.12. 07:15) |
| Max | 36,5 °C | 37,6 °C |
| Nejchladnější denní průměr | −3,2 °C | −3,4 °C |
| Hodin < −10 °C / < −12 °C | 0 / 0 | 0 / 0 |
| Topné dny (Tm < 15 °C) | 223 | 230 |
| GTZ 20/15 | 2 638 Kd | 2 853 Kd |
| HGT 15 | 1 523 Kd | 1 703 Kd |

Metoda: denní průměr z 15min hodnot (posun −15 min, aby 00:00 patřila předchozímu dni); GTZ = Σ(20 − Tm) pro dny s Tm < 15 °C (VDI 2067/4710 styl), HGT = Σ(15 − Tm). Vlhkost: 13–100 %, průměr 75,3 %.

- **NAT −10 / −12 °C: data nepodporují ani nepopírají** – dva mírné roky, nejnižší 15min hodnota −7,5 °C, žádná hodina pod −10 °C. Normová NAT (DIN/TS 12831-1, příloha podle lokality/PLZ) se z 2 let měření neurčuje; jde o extrém s dlouhou dobou návratu.
- **GTZ: měřené 2 638 / 2 853 Kd (průměr ≈ 2 745)** – blíže 2 700 Kd; 3 064 Kd neodpovídá ani jednomu roku (může to být dlouhodobý/normový průměr – v souboru nedoloženo).

## 3) Vstup pro MH BIM / EN 12831?
- **Ne jako normová klimatická data.** Pro EN 12831 je třeba NAT a roční střední teplotu z národní přílohy/DWD podle lokality, ne 2 roky čidla bez určení polohy.
- Použitelné jako **podpůrná/validační data**: kontrola GTZ/HGT, korelace spotřeby KH2/KH4 s teplotou (signatura), roční průměr ~12,2–12,8 °C pro plausibilitu θm,e. Referenzdaten jsou měsíční bilance měřičů – vstup pro bilanci/ověření zátěže, ne pro výpočet tepelné ztráty v BIM.
