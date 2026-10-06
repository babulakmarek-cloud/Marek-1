# System Übersicht – shrnutí (PDF „Aktualisierung läuft“)

**Typ dokumentu:** Tabulka, ne výkres. Je to tisk z Excelu `Hydraulischer_Abgleich_Mondelez_Loerrach.xlsx` (Microsoft Print to PDF, autor Marek Babulak), 6 stran A4 na šířku, vytvořeno 17.06.2026. Zpracovatel Cool Technology s.r.o. Lokalita je **Mondelez Werk Lörrach, Brembocher Str. 37 (pravopis jako v PDF)**. Slovo „Werk 2“ v PDF není. Podklad: Systemaufnahme 2025 (43 PDF rozdělovačů). Postup: Verfahren B (NWG), DIN EN 12831-1 / VDMA 24198. Řeší jen **VYTÁPĚNÍ**. Chlazení v dokumentu není.
Strany: 1 projektová data, 2 topologie + tabulka KH4, 3 hydraulické vyvážení okruhu Raumheizung 60/50, 4 registr rozdělovačů (43), 5–6 registr čerpadel (51).

## Strom systému (podle s. 1, 2 a 4)
- **Zdroje:** LOOS kotel B + C (KH2) a BHKW (rezerva, čerpadlo P-KH2.2 KSB Etaline DN80 PN16, „Abgang X3.VL“).
- **KH2 Hauptverteiler** Q.1.08.1 (1.OG KH2), 22 odboček, DN80-150. Má to tyto větve:
  - 5.VL Raumheizung DN80 (P-KH2.1 KSB UD1104, Belimo NV230A-TPC) → Vt 01 (EG) → Hochbau BA.A KG–6.OG (litinová otopná tělesa) a Straßenseite BA.B → Vt Milchpulverlager (MP) → kanceláře BA.D 1.+2.OG
  - 3.RL/4.VL DN100 → **Klimaverteiler 04** (6 odboček DN65-80). Strang 1: Vt 31/32 + větrání. Strang 2: Vt 14/14.1 Walzensaal. Strang 3: Vt 30 Lecithin. Strang 4: Vt 10 RBH 19er Massetanks. Strang 5: Walzensaal Süd, Jensen 1-4, Labor. Strang 6: Vt 40 Nusslager. Dále Vt 41 (HK1a/2a/3a/4a) a LN.
  - 8.VL (Prozess, „Strang 2“) → Vt 05/06/06.1/07/08/09 EG Seitengang, Vt 12/22 KG Conchensaal
  - 12.RL → Vt 03 → WT Rührwerke KG
  - 19.VL → Vt 13 Robertson-Decke 2.OG → Vt 17/18/19 (Jensen 5); Vt 36/37 Aussentanks (napájení „KH2 Robertson-Decke“)
  - Verbundleitung DN150 → **KH4 Unterverteiler** KH2(1.OG).15.02.6 (6.OG). Podle s. 1 má 9 odboček, tabulka uvádí 7:
    - 4.VL Rohrschacht B DN80 (KSB Rio 80-70D): KH6, OPM1, Rework, Fülltanklager
    - 5.VL Produktionsheizung I DN125, bez čerpadla (přímé připojení)
    - 6.VL Klimaheizung I DN80 a 10.VL Klimaheizung II DN80 (rezerva), obě Wilo Stratos 65/1-12
    - 7.VL Raumheizung KH4-Kreis DN125 (Grundfos MAGNA 3, směšování ventilem Sauter)
    - 8.VL Produktionsheizung II DN100 (KSB Supreme 2,2 kW)
    - 9.VL Rohrschacht 2 DN65
    - Mimo tabulku: podle registru čerpadel „Abgang 3“ Boiler-Kreispumpe KSB RIO 65-100D
    - Dále navazuje: Rohrkanal RK (tranzitní, DN50-125) → **KH6 Sozialgebäude** (DN125; WW I/II, radiátory, VZT, Pförtnerhaus), RW, RT, JB, FT, Vt 26 W+D3, Vt 45 W+D1 (14 okruhů), Vt 47, OPM1 (17 linek) a R-32

## Okruhy a teploty (jen tak, jak je uvádí PDF)
| Okruh | VL/RL | Údaje |
|---|---|---|
| Raumheizung | 60/50, ΔT 10 K | Hauptstrang 364 kW, 31 304 l/h, DN80. Součet 21 řádků je na s. 3. |
| Klimaheizung/Lüftung | 70/55, ΔT ~15 K | Vt 04, DN65-100. Výkony v PDF nejsou. |
| Prozessheizung | 90/70, ΔT 20 K | Výkony v PDF nejsou, jen DN a čerpadla v registru. |
| OPM1 | „45/35 + 60/50°C“ | Jediná zmínka 45/35. |

Raumheizung (s. 3): uvedený SUM 358 kW / 30 788 l/h „ohne WW“ jsem ověřil, sedí na součet řádků 1–20 bez řádků 15 a 16. Včetně WW vychází 413 kW. Řádky mají Rohr-DN 25–65, čerpadlo, ventil, Kv_soll (Δp 150 mbar) a SRV.

## Vstup pro mh-BIM RohrSYS
- Topologie: rozdělovač → odbočka → podřízený rozdělovač. Ke každému rozdělovači je ID (např. KH2(1.OG).8.19.0), podlaží, primární napájení, počet okruhů, rozsah DN, čerpadlo, regulační ventil a typ okruhu.
- Pro 21 okruhů Raumheizung: Q [W], θVL/θRL, q_V, DN potrubí, DN ventilu, Kv_soll.
- Registr 51 čerpadel: DN, PN, regulace Fix/VFD.
- **V PDF chybí:** délky tras, tvarovky, stoupačky (jen „Rohrschacht“), výkony Klima a Prozess, měřiče tepla. Nejsou tam ani zdroje LOOS A, KH4 jako zdroj, GEA VT40 B-16, 90/70 Klima ani +45/+35 Prozess.

## Nejasnosti
1. Dokument je o Werk Lörrach. Shodu s „Werk 2“ je potřeba potvrdit.
2. Prvky ze zadání v PDF chybí: LOOS A, výměník GEA VT40 B-16, měřiče a chlazení. Teploty Klima jsou v PDF 70/55, ne 90/70.
3. KH4 má mít 9 odboček, tabulka jich obsahuje 7. Odbočka 3 (boiler) je uvedená jen v registru čerpadel.
4. KH2 má 22 odboček, ale chybí k nim tabulka.
5. Hauptstrang 364 kW nesedí se SUM 358 kW.
6. WW boilery KH6 jsou v tabulce Raumheizung. HK3a (klima) je vedený jako okruh 60/50.
7. Vt 10/14/14.1/15/30/32/40/LN mají typ „Prozessheizung“, ale napájí je Klimaverteiler 04, takže teplotní úroveň je nejasná.
8. Počty okruhů „3+“ a „7+“ jsou neúplné. Vt 17.1 je mimo provoz.
9. Všechny Q jsou odhady (Hinweis 1). V PDF jsou chybné přehlásky („LÖrrach“), převzal jsem je beze změny.

Výstupy:
- `/home/user/Marek-1/vystupy/System_Uebersicht_Werk2.xlsx`. Listy: Projektdaten 12, Topologie 30, KH4_Abgaenge 7, Abgleich_Raumheizung 21, Verteiler_Register 43, Pumpenregister 51, Hinweise 7, Kontrolle 15. Počty sedí s PDF.
- Text: `scratchpad/docs_system/`
