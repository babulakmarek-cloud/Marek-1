# Mondelez Lörrach, Werk 2 / Bau 2 – souhrnná zpráva k podkladům pro MH BIM

Stav 2026-10-06. Zpracováno z výkresů (DXF/DWG/PDF) a projektových dokumentů dodaných uživatelem.
Podrobnosti ke každému dokumentu: `docs/podklady/*.md`. Tabulky: `vystupy/`.

## 1. Co je hotové

| Výstup | Obsah | Soubor |
|---|---|---|
| Soupisy podlaží | otopná tělesa (typ, počet, výkon/ks, celkem), DN popisky, popisy, délky potrubí podle hladin (jen z DXF) | `vystupy/*_soupis*.xlsx` (11 souborů) |
| Podkladové DXF | půdorys + topné hladiny, bez strojní dispozice, 2–9 MB | `vystupy/podklady_dxf/` (7 souborů) |
| Raumverzeichnis | 156 místností, UG–6.OG, Dach, Versorgungsgang | `vystupy/Raumverzeichnis_Werk2.xlsx` |
| Rozdělovače | 43 rozdělovačů, 228 vývodů, DN/PN, ventily, čerpadla | `vystupy/Verteiler_Liste_Werk2.xlsx` |
| Systémový přehled | topologie KH2/KH4/KH6, registr 51 čerpadel, Abgleich Raumheizung | `vystupy/System_Uebersicht_Werk2.xlsx` |
| Hydraulický Abgleich 08.09.26 | 170 řádků / 346 těles po podlažích + porovnání | `vystupy/Hydraulicky_abgleich_2026-09-08.xlsx` |
| Klimatizace / VZT | 52 jednotek + 12 stropních chladičů, rozpory zdrojů | `vystupy/Klimaanlagen_Werk2.xlsx` |

## 2. Co se vzájemně potvrdilo

- **Výkon otopných těles Bau 2 ≈ 615–620 kW** – tři nezávislé zdroje:
  výkresy 622 kW (bez Sozialgebäude) · Abgleich 613,6 kW (počet × Q_N) · koncepce stoupaček „~620 kW“ (s. 5).
  Hodnota **576 kW** (analýza tepelných dat) = řádek SUMME z Abgleichu, který obsahuje chybu (3.OG/4.OG nenásobí počet kusů) → **platí ~614 kW**.
- Výkon v popiscích „3x … P ≈ X W“ = **na 1 kus** (potvrzeno uživatelem; odpovídá i Abgleichu).
- 3.OG–6.OG: výkresy a Abgleich se shodují v počtu i výkonu na watt.
- Měřiče 2025 (Referenzdaten) = analýza tepelných dat (12 hlavních měřičů, ±1 MWh).
- Výměník **GEA VT40 B-16**, 10 bar / 110 °C, v. č. 171/22070 – štítek (foto) = doplněk Rev3.2.
- Klimakarte (PSČ 79539): **NAT −10 °C, 3 064 Kd** (topná hranice 15 °C) = doplněk Rev3.2.
- Všech 43 ID rozdělovačů: seznam rozdělovačů = registr v System-Übersicht.

## 3. Rozpory k vyjasnění

| Téma | Hodnoty | Kde |
|---|---|---|
| Výpočtová venkovní teplota | −10 °C ↔ −12 °C | Klimakarte, Rev3.2 ↔ Abgleich, energetická signatura |
| Teploty Raumheizung | 60/50 ↔ 60/45 ↔ 70/50 ↔ 90/70 | výkresy + System-Übersicht ↔ Rev3.2 ↔ Abgleich s. 5 ↔ Abgleich hlavičky |
| Abgleich – chyby výpočtu | kv 10× menší (Δp v kPa místo bar); q_v Ist = počet × Soll (není měření); Q_ges 3./4.OG | Abgleich 08.09.26 |
| Raumheizung v System-Übersicht | okruhy 1–8: 140 kW ↔ 614 kW; Hauptstrang 364 ↔ Σ 358/413 kW | System-Übersicht ↔ Abgleich |
| Počty odboček | KH4 9 ↔ 7; KH2 22 ↔ 16 | System-Übersicht ↔ seznam rozdělovačů |
| DN rozdělovačů | 19 ze 43 se liší (např. Vert. 17 DN25–50 ↔ DN15) | seznam rozdělovačů ↔ registr |
| LOOS B výkon | 1 500 kW tištěně ↔ 1 700 kW rukou | protokol 1988 |
| LOOS D | měřič plynu `LOOS_D_Gas` (105 492 Nm³) – kotel D v žádném dokumentu | Referenzdaten 2025 |
| Měřič LOOS C | 0 MWh v 06–07, přitom spotřeba plynu | Referenzdaten 2025 |
| Klima Excely | posunuté křížky funkcí u 33/38 jednotek; originál = KlimaanlagenPlan-DM.pdf | Übersicht/Engineering ↔ DM |
| Oddělení okruhů | § 8 Abgleich „wirtschaftlich nicht vertretbar“ ↔ koncepce stoupaček jej navrhuje | Abgleich ↔ MV-01 |
| Denostupně | měření 2024/25: 2 638 / 2 853 Kd ↔ 3 064 Kd (norma) ↔ 2 700 Kd (SD-01) | meteo ↔ Klimakarte ↔ SD-01 |
| Ekonomika | cena za výkon 120 €/kW·a bez zdroje; CO₂ 60 €/t pod EU-ETS 2024–26 (66–78 €/t) | Änderungsliste Rev2 |
| Délky potrubí | výkresy ↔ koncepce tab. 17.4 sedí jen ve 3.OG | soupisy ↔ MV-01 |

## 4. Co chybí pro model v MH BIM

1. **Výkresy EG, 1.OG, 2.OG v DWG/DXF** (soupisy jsou jen z PDF, bez délek; podklad pro import chybí).
2. **Plochy, výšky a teploty místností** – v Raumverzeichnis prázdné; výpočet tepelných ztrát (EN 12831) neexistuje.
3. **VZT**: výkony registrů (kW), médium, teplotní spád, napojení na rozdělovače, poloha jednotek.
4. **Kotle a zdroje**: DN přípojek, rozměry, hmotnost, objem vody (LOOS B/C; LOOS A chybí úplně); rozměry pláště GEA.
5. **Ventily a čerpadla**: typy a přednastavení ventilů; výkony/nastavení čerpadel.
6. **Topologie okruhů**: přiřazení těles → okruh → rozdělovač → stoupačka (okruhy 1–22 / X1–X4 nejsou nikde rozepsané).
7. Teploty u 208 z 228 vývodů rozdělovačů.

## 5. Doporučený postup v MH BIM

1. **Projektverwaltung**: projekt „Mondelez Werk 2“, budova Bau 2 (+ Sozialgebäude), podlaží UG, EG, 1.–6.OG podle Raumverzeichnis.
2. **Podklady**: vložit `vystupy/podklady_dxf/*_podklad.dxf` (jednotky mm) jako půdorysy podlaží.
3. **RaumGEO**: místnosti podle Raumverzeichnis (156; čísla Raum-KID) – plochy a výšky vzniknou z modelu.
4. **Zdroje (KH2)**: BHKW 1 600 kW th, LOOS B 1 500 kW, LOOS C 4 750 kW, výměník GEA VT40 B-16 (10 bar / 110 °C).
5. **RohrSYS**: rozdělovače a vývody ze seznamu rozdělovačů; trasy po topných hladinách podkladu (V/R podle teplot v názvu hladiny); otopná tělesa z `Hydraulicky_abgleich_2026-09-08.xlsx` / soupisů (typ, počet, Q_N/ks, Raum-ID, rastr os).
6. **Výpočet**: NAT podle Klimakarte (−10 °C), dimenzování a hydraulické vyvážení přímo v RohrSYS – nahradí chybné kv z Abgleichu.
7. **Kontrola**: součet těles ≈ 614 kW (Bau 2); větve WT-A 0,79 MW, WT-P 1,08 MW, KH4 1,09 MW, primár 2,58 MW.
