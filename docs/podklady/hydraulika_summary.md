# BE SYSTEMS – Hydraulická analýza Bau 2 Mondelez (HA-01 Rev. 0, 04.10.2026) – shrnutí
Zdroj: CZ PDF (5 str.) + CZ XLSX (13 listů); DE PDF (6 str.) + DE XLSX jen porovnány. Texty: scratchpad/docs_hydraulika/cz.txt, de.txt.

## 1 Účel a metoda
- Účel: vysvětlit kolísání tlaku a přívod 90 °C, porovnat stávající stav s přestavbou dle koncepce stoupaček MV-01 Rev. 3.1, odhadnout účinek, navrhnout okamžitá opatření a měření (CZ s.1).
- Metoda: **není to měření ani síťový výpočet.** Je to kvalitativní analýza z prohlídky, rozhovorů s provozovatelem, DWG KG–6.OG, schématu a referenčních dat 2025. „Stávající světlosti a průtoky nejsou změřeny… spolehlivé hodnoty dá měření (kap. 9) a hydraulický výpočet (mh-BIM)“ (s.1, list Přehled).
- Čísla jsou ilustrační příklady (s.2, listy Výpočet tlakové ztráty/průtoku/energie mají editovatelné vstupy).

## 2 Okruhy, větve, stoupačky – co dokument obsahuje
- Zdroj KH2 (KG, osa 5–9): KGJ + kotle LOOS B+C, hlavní rozdělovač s okruhy 1–22 a X1–X4 (s.1). Ty okruhy nejsou dál rozepsané (žádné průtoky, výkony ani DN pro jednotlivé okruhy).
- Bývalá kotelna 6.OG (osa 35–37): kotle Viessmann I–III mimo provoz, rozdělovač „Industriewärme“, v provozu zůstaly jen TV bojlery (s.1).
- Trasa k nejnepříznivějšímu spotřebiči (jedna cesta, list 2.2 Trasa, s.1): 37 m KH2→stoupací trasa (osa 0–1′) + 36 m stoupačka KG→6.OG + 140 m přechod v 6.OG (osa 1→36/37) + 36 m spádové potrubí šachtou B/39-38 = **cca 250 m + x** (katakomby→sociální budova x m, trasa není ve výkresu). Po přestavbě cca 151 m + x.
- Na spádové větvi jsou podle schématu Bindler 3 (2.OG), OPM1 (1.OG), KH6/sociální budova, sklad plnicí hmoty a Rework (KG) (s.1).
- Průtok a Δp: jen **příklad** DN 100, 500 m VL+RL: 25 m³/h, 0,80 m/s, 55 Pa/m, 0,36 bar → 50 m³/h, 1,59 m/s, 207 Pa/m, 1,35 bar (×3,8). Výpočet je Colebrook/Swamee-Jain s di 105,3 mm, k 0,045 mm, voda 70 °C a přirážkou 30 % na místní odpory (s.2; list Výpočet tlakové ztráty). DN 100 i průtoky jsou předpoklady.
- ΔT: příklad pro 100 kW: ΔT 10/20/30 K → 8,6/4,3/2,9 m³/h; při RL 55 °C potřebný přívod 65/75/85 °C (s.2, list 3.5). Provoz dnes: přívod celoročně až 90 °C; cíl 70/50, RL ≤ 50 °C (s.4).
- Výkony: jen KH2 12 082 MWh/rok tepla, z toho cca 20 % závislé na počasí. Ztráty rozvodu 300–600 MWh/rok a pomocná energie čerpadel cca 250 MWh/rok jsou předpoklady (s.4).
- Čerpadla: hlavní v KH2, okruhová a přečerpávací v podružných rozdělovačích, dvojice čerpadel v 6.OG, regulační stanice 1.OG/2.OG. Typy ani výtlačné výšky uvedené nejsou (s.2).
- Udržování tlaku: ve výkresu KG jsou expanzní nádoby s předtlakem 6,0 a 2,5 bar; nejvyšší bod je cca 36 m nad KH2 (s.2).
- Po přestavbě: stoupačky S1/S2 (varianta A DN125), 14 zón (KG…5.OG, strana L/R) s regulací Δp, příčná propojení NC (s.3–4).

## 3 Zjištěné problémy (s.1–2, schéma s.3, body 1–5)
1. Úzké hrdlo v 6.OG: dva okruhy spojené do starých DN (odhad: 2× průtok ≈ 4× Δp).
2. Sériové zapojení: sociální budova a katakomby visí na konci za celou výškovou částí, nemají vlastní regulovaný přívod.
3. Čerpadla bez hydraulického oddělení (chybí vyrovnávač i regulace Δp), staré čerpadla 6.OG mohou pracovat proti KH2.
4. Nejvyšší bod 6.OG: podtlak, vzduch, možná dvě udržování tlaku pracující proti sobě.
5. 90 °C jako náhrada chybějícího průtoku. Důsledky: vysoká zpátečka, přezásobení blízkých spotřebičů (= nevyvážení), ventily pracují v nejnižším zdvihu, horší využití KGJ, nelze tlumit (s.2).
- Nízké ΔT ani předimenzování nejsou měřením doložené. Vysoká zpátečka je uvedena kvalitativně.

## 4 Doporučení
- Přestavba dle MV-01 (S1/S2, 14 zón, EC čerpadla s regulací Δp, centrální udržování tlaku v KH2, omezení zpátečky) (s.4).
- Nový vlastní vývod pro katakomby a sociální budovu přímo z KG: buď okruh na hlavním rozdělovači KH2, nebo u paty S2 (osa 38), vždy s regulátorem Δp, měřičem tepla a motorickým uzávěrem. Má jít jako položka do Rev. 3.2 (kap. 7, s.4).
- Okamžitá opatření S1–S6: odvzdušnit, zkontrolovat udržování tlaku (předtlak ≥ statická výška + 0,5 bar), zmapovat čerpadla, uzavřít zkraty VL↔RL v 6.OG, provizorní vyvážení, stupňový test přívodu 90→85→80 °C (s.5).
- Měření M1–M6 loggery v 1min rastru po 2–4 týdny (s.5). Odhad úspor: 100–200 MWh/rok tepla a 75–125 MWh/rok elektřiny (s.4).

## 5 Vstupy pro model a vyvážení v mh-BIM (RohrSYS)
- Použitelné z HA-01: topologie (KH2 → stoupačka → 6.OG → šachta B/39-38 → katakomby → sociální budova), délky úseků z osové sítě (list 2.2), výška 36 m, teplotní režimy stav 90/? → nově 70/50, cílová zpáteč ≤ 50 °C, DN125 pro S1/S2 (var. A), členění do 14 zón, umístění měřicích bodů.
- **Chybí** (open points s.5, č. 1–4, 6): skutečné DN spojeného potrubí v 6.OG, trasa/DN/délka v katakombách, zatížení sociální budovy/KH6, seznam čerpadel s křivkami, údaje o udržování tlaku, výkony okruhů 1–22/X1–X4, max. RL KGJ. Bez nich a bez měření M1–M6 nemá model stávajícího stavu podklad k kalibraci.
- Domněnka: pro mh-BIM bude výkonovým vstupem u otopných těles soupis z výkresů (viz 7) a procesní/VZT zátěž bude nutné doplnit z dat Mondelez.

## 6 CZ vs DE
- Obsah je shodný: kapitoly 1–10, všechny tabulky a čísla. XLSX mají shodné názvy listů (jen přeložené) a všech 63 číselných vstupů a vzorců ve třech výpočtových listech je identických (ověřeno skriptem).
- Rozdíly: DE PDF má 6 stran (jiné zalomení; kap. 2.2 začíná na s.2, schéma je na s.4), CZ má 5 stran. CZ má v poznámce navíc vysvětlení zkratek podlaží (KG/EG/x.OG). Terminologie: KGJ=BHKW, TV=TWW, spádové potrubí=Fallleitung. Jiné rozdíly v číslech jsem nenašel.

## 7 Porovnání se soupisy z výkresů (vystupy/*_soupis.xlsx)
- Pokrytí: soupisy jsou pro 1UG, 3OG–6OG, Sozialgebäude, Versorgungsgang a Dach. **EG, 1.OG a 2.OG chybí**, a právě tam jsou podle HA-01 Bindler 3, OPM1 a regulační stanice.
- Teploty: hladiny ve výkresech nesou návrhové režimy 90/70 Prozess, 90/70 Klima (VZT), 60/50 Heizkörper a 45/35 Prozess (list Potrubí dle hladin). HA-01 popisuje provoz 90 °C pro celý závod. Domněnka: 60/50 a 45/35 jsou sekundární okruhy za regulačními stanicemi. HA-01 je nerozlišuje, pro model je nutné je rozlišit.
- DN v 6.OG (6OG_soupis, DN popisky): na 90/70 Prozess jsou **DN 80, DN 100, DN 125, DN 150**, na Klima V DN 150, na 60 Heizkörper DN 125 a DN 15. Příklad DN 100 v HA-01 je tedy v rozsahu DN z výkresu, ale HA-01 uvádí, že jde o předpoklad. Přiřazení popisků k úsekům spojení (osa 35–37) soupis neprovádí, takže otevřený bod 1 zůstává.
- Sociální budova / katakomby (otevřený bod 2): v Sozialgebaeude_soupis jsou 4× DN 125 na 90/70 Prozess, ve Versorgungsgang_soupis DN 125 (90/70) a DN 50. Domněnka: Versorgungsgang může odpovídat „katakombám“, je potřeba ověřit. Délky kresby ve Versorgungsgang: 90 V 149 m a 70 R 150 m (jen délka kresby, ne ověřená trasa).
- Výkony těles (P≈ W, součet řádků / počet × výkon; u „2x/3x“ není ověřeno, zda jde o výkon na kus): 1UG 78,6/118,9 kW; 3OG 48,4 kW; 4OG 6,95 kW; 5OG 29,6/70,6 kW; 6OG 5,0 kW; Sozialgebäude 34,1/52,4 kW (75 ks); Versorgungsgang 2,7 kW. HA-01 výkony těles neuvádí, takže je není s čím porovnat. Soupis Sozialgebäude dává jen hrubý údaj k zatížení sociální budovy (bez VZT a procesu).
- DN125 pro nové S1/S2 se objevuje i ve stávajících popiscích (1UG 6×, 3OG 4×, 4OG 4×, 5OG 7×). Domněnka: jde o stávající páteř, nesouvisí s variantou A.
- Okruhy 1–22 / X1–X4 v soupisech identifikované nejsou, hladiny jsou členěné jen podle média a teploty.
