# Kotle LOOS – Mondelez (Jacobs Suchard) Lörrach, Bau/Kesselhaus 2, 1.UG
Zdroje: B = `LOOS-B_technische_Daten.pdf` (sken RICOH, 6 listů, Sulzer, protokol DIN 4751 T4, 1988) – čteno vizuálně;
C = `LOOS-C_technische_Daten.pdf` (3 str., výpočet komína DIN 4705, kominík Vogel, 29.03.1996; digitalizovaný přepis z 07.05.2026). Text: `docs_loos/*.txt`.

| Parametr | LOOS B (Blatt) | LOOS C (str.) |
|---|---|---|
| Výrobce | Eisenwerke Theodor Loos GmbH, Gunzenhausen (B1) | Loos (C1) |
| Typ | „Typ NH“ (ručně psáno, B1) | Loos Unimat NH 4750 (C1, C2) |
| Výr. číslo | 50306 **a** 50307 – list platí pro 2 kotle (B1) | neuvedeno |
| Rok výroby | 1988 (B1) | neuvedeno (výpočet 1996) |
| Bauart-Zul.-Nr. / materiál | 02-226-122; RSt 37-2 nebo H II (B1) | – |
| Druh | horkovodní/teplovodní: zul. Vorlauf 120 °C, provoz 105 °C (B1) | neuvedeno (jen „Wärmeerzeuger“) |
| Palivo/hořák | přímé Gas/Öl (B1); typ hořáku neuveden | Öl-Gebläse für Heizöl (C1) |
| Výkon | Wärmeleistung 1500 kW, ručně připsáno „1700 kW“; Beheizungsleistung 2 kotle à 1648 kW (B1) | Nennwärmeleistung 4750 kW; Feuerungswärmeleistung 5397,7 kW (C1, C2) |
| Tlak | zul. Betriebsüberdruck 6,0 bar; max. provoz 5,0 bar; stat. tlak 0,5 bar; PV 6,0 bar (B1) | neuvedeno |
| Teploty | primár 105 °C, sekundár 92 °C, zul. VL 120 °C (B1); TR 105 / TW 115 / STB 120 °C (B2) | spaliny 190 °C (C2) |
| Účinnost | neuvedena | 88 % (C2) |
| Spaliny/odkouření | neuvedeno | hrdlo kruh. Ø636; Verbindungsstück 600×800 mm, 10 m, šamot; komín Plewa čtverc. 600, účinná výška 34 m; CO2 13,5 %, 2215,5 g/s (C1–C2) |
| Objem vody, rozměry, hmotnost | neuvedeno | neuvedeno |
| DN přívod/zpátečka | neuvedeno (jen PV DN 40/65, B3) | neuvedeno |
| Další | PV ARI, TÜV.SV.85-688.36, 1500 kW (B3); presostat max Sauter DFC 27 B43W 5,5 bar (B3), min DFC 17B58 2,0 bar (B4); Wassermangel Sasserath 933.1 (B4); expanzní nádoba Winkelmann+Pannhoff 800 l, 6 bar, č. 8/3469 a 8/3471 STW, 1988 (B5); regulátor L&G QAE 21 (B2) | konvenční komín v budově, výpočet splňuje DIN 4705 (C1, C3); kotel v kotelně, NLV skup. 4 v kouřovodu (C1, C3) |

## Vstupy pro MH BIM / RohrSYS (zdroj tepla)
- **Použitelné:** výkon B 1500 kW (resp. 1700 kW ručně – ověřit), C 4750 kW; teploty B 105/92 °C (pozn.: „primär/sekundär“ = provozní teploty prim./sek. strany, NE spád VL/RL – zpátečka neuvedena), max. VL 120 °C, tlak 5/6 bar; C: Ø odkouření 636 mm a kouřovod 600×800 pro 3D trasu spalin; DN 40/65 PV (B).
- **Chybí:** celý LOOS A (pravděpodobně druhý kotel z listu B – výr. č. 50306/50307 – ale přiřazení A/B z dokumentu nelze určit); u C výr. číslo, rok, tlak, teploty vody; u obou: DN VL/RL, objem vody, rozměry, hmotnost, poloha hrdel (nutné pro 3D a hydrauliku), teplota zpátečky/spád, průtok, typ hořáku; u B účinnost a odkouření.
- Nejasnost: B1 uvádí Wärmeleistung 1500 kW tištěně vs. 1700 kW ručně; „NH“ je ručně dopsané.
