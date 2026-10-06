# Hydraulický Abgleich Mondelez Lörrach Bau 2 – shrnutí (PDF 37 s. + Leitfaden 3 s.)
Text: scratchpad/docs_abgleich2/{mondelez,leitfaden,paged}.txt. Excel: /home/user/Marek-1/vystupy/Hydraulicky_abgleich_2026-09-08.xlsx

## 1) Kdo, kdy, metoda
- Objednatel Mondelez International, Bau 2, Brombacher Str. 37, Lörrach; zhotovitel Cool Technology (IČO 07544961), podpis Marek Babuľák (s. 1–2). Schutzklauseln: datum 07.07.2026, v1.0 (s. 1), podpis 08.09.2026 (s. 2). Vorberechnungstool: 08.09.2026, „v1.0 – Vorberechnung“ (s. 4). Projektplan „Stand: Mai 2026“ (s. 25), na s. 26 je zhotovitel uveden jako „BE SYSTEMS / Marek Ba…“.
- Metoda: „Verfahren B (BEG EM-konform)“ (s. 4). Jde o VÝPOČET: ṁ = Q/(1,163·ΔT), n = 1,3, DIN/TS 12831-1:2020-04 + EN 442, NAT −12 °C (s. 1, 5). Data pocházejí výhradně z vlastního zaměření na místě, podklady od AG chyběly (§1–§3, s. 1). Měření není doložené: legenda „q_v Ist = Messwert vor Ort eintragen“ (s. 7) a §6 doporučuje měření průtoků AŽ PO zaregulování (s. 2).
- Rozpory v teplotách: 90/70 °C (s. 4 a hlavičky podlaží s. 6–17, s. 32) proti 70/50 °C (s. 5 Systemparameter, s. 19). ΔT je všude 20 K.

## 2) Rozsah
- Pouze Bau 2: 1.UG, EG, 1.–6.OG (s. 6–17); s. 37 přitom uvádí „7 Geschosse (1.UG + EG + 1.–6.OG)“, ale vyjmenovaných podlaží je 8. Sozialgebäude/Versorgungsgang zde nejsou.
- 170 řádků místností, 346 HK, Σ Q_ges 575 993 W (s. 18). Sloupec má v hlavičce [kW], hodnoty jsou ale ve W. Σ Anz×Q_N = 613 575 W.
- Po podlažích (řádky / HK / Q_ges W): 1.UG 28/53/115 450; EG 36/64/90 000; 1.OG 24/55/131 350; 2.OG 44/85/145 875; 3.OG 15/42/12 416; 4.OG 6/6/5 352; 5.OG 14/38/70 550; 6.OG 3/3/5 000. Všechny počty řádků i součty sedí na řádky SUMME v PDF (list Kontrolle).
- Okruhy/stoupačky: PDF NEOBSAHUJE seznam okruhů ani stoupaček. Uvádí jen „Einrohr / Zweirohr“ (s. 4), u 2.OG „50 – Einrohr“ (s. 12) a 6 zón s vlastními DDR jako návrh (s. 34). Mimo topení: 47 VZT jednotek + 12 stropních chladičů (s. 27–31), 56+ Massetanků (s. 34–35).

## 3) Tabulky
- Tabulky těles+ventilů jsou na s. 6–17. V Excelu je 8 listů HK_* (170 řádků, hlavičky DE, sloupec Strana PDF) a k nim listy Gesamtuebersicht (s. 18), Kontrolle, Vergleich_Soupis, Vergleich_Typen a Vergleich_SystemUebersicht.
- Ventily: obsahují jen číslo kv, bez typu a výrobce. „Danfoss RA“ a PICV se objevují jen jako plán v AP 2.5 (s. 25). Sloupec „Pos.“ obsahuje rastr os (např. „J–K / 35–39“), přestože legenda ho definuje jako Voreinstellwert (s. 7). Skutečné přednastavení tedy v PDF chybí. Sloupec Status je prázdný.
- Tabulky stoupaček ani čerpadel v PDF nejsou. Jsou tam jen doporučení: Grundfos MAGNA3 / Wilo Stratos (B1, s. 20) a „Pumpenauslegung … nach Angaben von Mondelez“ (AP 2.6, s. 25).
- Chyby v datech PDF:
  - q_v Soll je počítáno na 1 HK (167 ze 170 řádků = Q_N/23,26).
  - V EG/1.OG/2.OG platí q_v Ist = Anz×q_v Soll (35 řádků), z toho vznikají „Abw.“ −100 až −500 %. Nejde o měření.
  - kv = q_v Ist[m³/h]/√Δp[kPa] (sedí u 160 ze 170 řádků). Δp je dosazeno v kPa místo bar, takže kv vychází 10× menší.
  - 3.OG a 4.OG: Q_ges ≈ Q_N×(1−Abw), bez násobení počtem kusů.
  - 4.OG: řádky dávají Σ q_v Ist 230,0, SUMME uvádí 197,9.
  - EG: čísla řádků mají mezery (1–4, 35–44, 47–50 chybí, jeden řádek je bez čísla). V 1.OG je Nr. 15 dvakrát.

## 4) Zjištění a doporučení
- §7 (s. 2): okruhy Heizung a Industrieheizung jsou v „weiten Teilen“ hydraulicky propojené. Úplné vyregulování podle VDI 2073 / EN 14336 proto není možné a výsledek je jen „bestmögliche Annäherung“.
- §8 (s. 2), „dělení okruhů nedoporučeno“. Tvrdí, že úplné oddělení Heizung od Industrieheizung bylo „geprüft“ a vyhodnoceno jako wirtschaftlich nicht vertretbar. Důvody:
  - stáří zařízení,
  - nejasné vedení potrubí v nepřístupných místech,
  - zásah do výroby.
  Investice podle §8 „in erheblichem Maße“ převyšují energetický přínos. Žádná čísla (náklady ani úspory) tam nejsou. Oddělení navíc nebylo součástí rozsahu zakázky.
- §9 (s. 2) přitom doporučuje oddělení zařadit do střednědobého investičního plánu při plánované obnově, jako předpoklad pro normový Abgleich a pro napojení TČ.
- §6: ověřit průtoky měřením, odchylky upraví odborná firma (s. 2). Opatření A1–A5, B1–B5, C1–C5 a varianty D1–D5 (s. 19–24):
  - Abgleich Verfahren B (A1),
  - snížení VL 70→60 °C (A2),
  - DDR po skupinách stoupaček (B3),
  - PICV pro Klima 1+2 (B2),
  - izolace 1.UG (B5),
  - 60/45 °C (C1),
  - TČ 200 kW (D1).
  Úspory a ceny (s. 33–36) jsou v textu prázdné.

## 5) Leitfaden (postup/standard, 3 s.)
- Normy: DIN EN 12831-1 / VDI 2073 / EN 12828 / EN 14336 / EN 442 (s. 1).
- Postup:
  - sběr dat (systém, DN, armatury, Δp regulátory, čerpadla),
  - ΔT: radiátory 20 K, VZT 10–15 K, podlahovka 5–10 K,
  - tlakové ztráty a Bezugsstrang,
  - VDI 2073 Verfahren B: kv = V̇/√Δp, přednastavení z tabulky výrobce, DDR/PICV, ±10 % Soll,
  - čerpadlo: H = ΣΔp krit. větve + rezerva 10–20 %,
  - EN 14336 protokol (s. 1–2).
- Rychlosti: připojky k HK ≤ 0,9 m/s, stoupačky ≤ 1,5, hlavní větve ≤ 2,0 m/s (s. 2). Workflow v 7 krocích (s. 2–3).
- Červeně je u mnoha bodů poznámka „Keine Informationen seitens des Mondelez“ (provozní režimy, výpočet tepelných ztrát, jemné doladění, čerpadla, proplach/VDI 2035/měření/předávací protokol, zóny, VZT, GLT; s. 1–2).
- Pozor: vzorec na s. 1 „Q[kW] = 0,86·V̇[m³/h]·ΔT“ má prohozený koeficient (správně 1,163, resp. V̇ = 0,86·Q/ΔT). Na s. 2 je uvedeno správně V̇ = Q/(0,86·ΔT).

## 6) Srovnání se soupisy a System_Uebersicht
- Soupisy (výkon na 1 ks):
  - 3.OG–6.OG se shodují v počtu i W (48 400 / 6 950 / 70 550 / 5 000; u 3.OG a 4.OG se počítá Anz×Q_N z PDF).
  - Rozdíly soupis−PDF: 1.UG +3 HK / +3 400 W, EG −2 / −2 900, 1.OG +10 / +2 825, 2.OG +2 / +2 800.
  - Σ 8 podlaží: PDF 613 575 W, soupisy 619 700 W (+ Versorgungsgang 2 700 = 622 400 W bez Sozialgebäude, Sozial 52 400 W, celkem 674 800 W).
  - Typové rozdíly: 35 řádků v listu Vergleich_Typen (jiné Q_N na kus, např. 1.OG 50/680/135 3 850 vs 1 925 W; 1.UG 27/500/100 1 200 vs 1 500 W).
- System_Uebersicht (Abgleich_Raumheizung): okruhy 1–8 (KG–6.OG) dávají 140 kW při 60/50/10 K. PDF má pro stejná podlaží 613,6 kW (Anz×Q_N), takže hodnoty nejsou srovnatelné; největší rozdíl je 1.UG 115 vs 25 kW a 2.OG 146 vs 20 kW. Okruhy 1–21 dávají dohromady 413 kW, Hauptstrang je 364 kW. ΔT 10 K (Übersicht) proti 20 K (PDF) dává dvojnásobné průtoky.

## 7) Přímý vstup pro mh-BIM RohrSYS / HkCALC
- Použitelné:
  - Raum-ID, typ HK (rozměry), počet, Q_N na 1 HK, θint 18/20 °C, DN připojky (část řádků), rastr os (sloupec Pos.) pro umístění,
  - NAT −12 °C, ΔT 20 K, n = 1,3, ṁ-vzorec (s. 1, 5).
- Nepoužitelné bez opravy/doplnění:
  - q_v Ist, Abw., kv (chyba kPa/bar), Q_ges ve 3.OG/4.OG,
  - nejednoznačné VL/RL (90/70 vs 70/50 vs 60/50 v System_Uebersicht),
  - chybí typy ventilů a přednastavení, topologie stoupaček/okruhů, délky potrubí, čerpadla, Bezugsstrang a výpočet tepelných ztrát místností (podle s. 1 byl mimo rozsah).
