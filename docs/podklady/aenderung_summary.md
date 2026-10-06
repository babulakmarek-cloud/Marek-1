# Änderungsliste – Konzept Netztrennung Bau 2, Rev. 1 → Rev. 2 (shrnutí CZ)
Projekt BE-2025-MON-001, Mondelez Werk Lörrach, Bau 2 · datový stav 04.10.2026 · autor BE SYSTEMS – Marek Babuľák · bez komentářů ve Wordu.
**Pozor:** jde o koncept **otopné sítě (teplovod KH2/KH4, BHKW, kotle LOOS)**, ne o elektro rozvody. Číslované změny po elektrických okruzích/stoupačkách dokument neobsahuje – změny jsou řazeny po tématech/kapitolách konceptu.

## Účel
Seznam všech míst konceptu, která se mění na základě nově vyhodnocených dat (Analyse Wärmedaten Rev. 1, Effizienzrechner v4 – měsíční bilance), s náhradními čísly a textovými bloky. **Technické řešení se nemění** (2 stoupací zóny, rozdělovač na každé podlaží a stranu, vypínání přes SCADA, výstup 70 °C). Mění se zdůvodnění a ekonomika.

## Nová datová základna (kap. 2)
EnMS 2025 (547 měřidel, měsíční hodnoty); Wärmedaten 2024 (denní, KH2, víkend bez útlumu); počasí EnMPRO 2024–25 (15 min, oprava dubna/května 2025); ceny energií Mondelez 2024–26; e-mail D. Brehm 09.09.2026 (špičky 6 769–7 814 kW = celková el. zátěž).

## Změny v textu konceptu (kap. 3, bez číslování v originále)
1. **Energetická signatura** – Rev.1: 82 % základní zátěž, P0 ≈ 1,13 MW → Rev.2: 83 %, P0 ≈ 1,15 MW, 17 % (≈ 2 010 MWh/a) závislé na počasí; denní data 2024: P0 1,17 MW, 15 %. Důvod: duben/květen 2025 se správnými teplotami zpět v regresi.
2. **Podíl závislý na počasí Bau 2** – ≈ 1 200 → 1 100–1 430 MWh/a (rozpětí dle metody).
3. **Úspora sítě A** – 120–300 → fyzikálně 120–430 MWh/a; plyn šetří jen v měsících s kotli (led–bře, pro, revize BHKW). Důvod: BHKW kryje dub–lis prakticky samo.
4. **Mezní zdroj** – úspora zasahuje kotlové teplo jen ve stejném měsíci; dostupné kotlové teplo ≈ 1 170 MWh/a sdílí všechna opatření.
5. **Argument BHKW** – škrtnout „vyšší doba chodu“; ponechat nižší stabilní teplotu zpátečky; doplnit: hodnota roste při výpadku/náhradě BHKW.
6. **Špičky zatížení** – vyjasněno: el. celková zátěž = odběr EVU max ≈ 5,4 MW + BHKW ≈ 2,4 MW; nejde o teplo KH2; cena za výkon se vztahuje k odběru EVU.
7. **Zdůvodnění M3/M4 (oddělení, paralelní síť)** – místo úspor technicky: předpoklad pro 70 °C, SCADA vypínání po podlaží/straně, odstranění kolísání tlaku a **úzkého místa 6.OG**, bezpečnost dodávky. Energeticky samo 15–30 let návratnost.
8. **Seznam opatření** – nově M7 (rekuperace tepla z kompresorů KH2), M9 (vypínání podlaží/stran přes SCADA), opce M8 (TČ na zpětném chlazení C4 po konci BHKW).
9. **Dimenzování** – WT-A 0,79 MW, WT-P 1,08 MW, odbočka KH4 1,09 MW, primární rozdělovač 2,58 MW (měřená špička 2024: 2,6 MW); **DN beze změny**.
10. **Měřicí koncept / fáze 0** – doplnit detekci směru propojení KH4, opravu měřičů tepla LOOS B/C, podružné měření el. proudu čerpadel KH2, KPI jen z měřiče KH2 (EnMS „Plant Heating Total“ počítá BHKW dvakrát).
11. **Ochranné klauzule § 8** – stále otevřeno (rozpor s dokumentací hydraulického vyvážení).

## Ekonomika (kap. 4, nahrazuje tab. kap. 9)
Ceny 2026: plyn 59,8 €/MWh + CO₂ 60 €/t, el. 166,7 €/MWh, výkon 120 €/kW·a; 6 %, 15 let. Investice: M1 60k, M2 15k, M3 180k, M4 350k, M5 45k, M6 60k, M7 150k, M8 450k (opce), M9 40k €.
Varianty: v4 balík M1–M7+M9 základ 136 882 €/a, 900 k€, 6,6 let, NPV 590 580 €, IRR 15,5 %; konzervativně 9,8 let; bez BHKW 302 768 €/a, 3,0 let. (v3 M1–M6: 5,2 let → v4 korigováno 7,7 let.)

## Stav / revize
Platí pro Rev. 1 → Rev. 2. Otevřené body pro D. Brehm (kap. 6): bilanční mezera KH2 ≈ 710 MWh/a, pomocný proud čerpadel (odhad 250 MWh/a), typ/chlazení kompresorů KH2, výhřevnost plynu, provoz a zbytková životnost BHKW, zda el. sazba obsahuje cenu za výkon, okna vypnutí pro M9.

## Vstup pro model v MH BIM (odvozeno z dokumentu)
- Topologie beze změny: 2 stoupací zóny, rozdělovač na každé podlaží a stranu, výstup 70 °C (síť P), síť A 60/45 °C.
- Výkony: WT-A 0,79 MW, WT-P 1,08 MW, odbočka KH4 1,09 MW, primární rozdělovač 2,58 MW; DN se nemění.
- Úzké místo 6.OG (řeší paralelní rozvod M3/M4).
- Nová měřidla: směr toku propojení KH4, měřiče tepla LOOS B/C, podružný elektroměr čerpadel KH2.
- Nová/opční zařízení: M7 rekuperace z kompresorů KH2 (napojení do zpátečky KH2, ~70 °C – před tím ověřit typ chlazení), M9 SCADA vypínání po podlaží/straně, M8 TČ u C4 (opce).
- Konkrétní podlaží, čísla okruhů ani stoupaček kromě 6.OG dokument neuvádí.
