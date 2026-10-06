# mh-AufCALC (MH BIM, "Aufmaßberechnung") - shrnutí manuálu (83 s., ©2026 mh-software GmbH)
Čísla stran = tištěná čísla v manuálu (s. N). Vše z textu manuálu; co tam není, je výslovně uvedeno jako "manuál neuvádí".

## DŮLEŽITÉ ZJIŠTĚNÍ
Modul NENÍ výměra místností/ploch z výkresu. mh-AufCALC je kalkulace povrchů vzduchotechnických kanálů (VZT) a izolací, délek spojovacích prvků a časů, podle DIN 18379:2016-09 (s. 6). Neexistuje zde datový model budova/podlaží/místnost. Manuál NEOBSAHUJE import DWG/DXF do tohoto modulu (viz bod 3).

## 1. K čemu slouží + datový model
- Funkce: zadání tvarovek/kanálů/rour, správa tvarovek (kopírovat/mazat), povrch kanálu a izolace pro hranaté kanály, kusovníky, rámové a řezné seznamy spojovacích prvků (s. 6). Kulaté roury jen se zvláštním modulem ACrund (s. 6, 48).
- Hierarchie: Projekt > Anlage (zařízení/systém) > Anlagenteil (část zařízení) > tvarovka (řádek tabulky). Min. 1 Anlage a 1 Anlagenteil nutné pro zadání (s. 7, 45).
- Na úrovni Projekt není žádný vstup; Anlage má jen volitelný popis; data se zadávají v Anlagenteil (s. 45).
- Projekt v mh-BIM = budova/komplex; Anlage = modul/výpočet (AufCALC, KanSYS, RohrSYS, RaumGEO...). "Sys" Anlagen jich může být v projektu víc se svobodným názvem (s. 19-20).
- Anlagenteil: záložky Allgemeine Daten (LV-Position, Zeichnungs-Nr., Druckstufe, Dichtheitsklasse - volitelné, bez vlivu na výpočet; s. 46), Abmessungen, Material/Dämmung (s. 45-48).
- Řádek tvarovky: Position, n (počet), KB (zkratka typu), rozměry, V1/V2/V3 (spojovací prvky), materiál (Herst/Prod/síla), izolace (Art: Ungedämmt/Außen/Innen + Herst/Prod/síla), text/Hinweis; výstup Fläche, Grp, Kl (s. 47-48).
- Pole KanSYS: Element-ID přiřazená exportem z mh-KanSYS; neměnit/nemazat (s. 46). Bez Element-ID jsou rozměry editovatelné (s. 46, 47).
- Katalogy (v projektu kopie Vorgabe-katalogů): Kanal-Material, Dämmungs-Material, Verbindungsteile, Komponenten (s. 13, 69-73).

## 2. Postup práce (s. 6-7, 47-48, 63)
1. V mh-Projektverwaltung vytvořit projekt (název; Vorgabe-Projekt; Plus/Basis) a Anlage pro modul AufCALC (s. 22-24).
2. V AufCALC: tlačítko "Neu" > zadat Anlage + Anlagenteil, OK; lze opakovat (s. 7, 63).
3. Volitelně popis Anlage; allgemeine Daten Anlagenteilu (s. 7).
4. Záložka Abmessungen: Position, n, KB (F2/dvojklik = výběr typu), rozměry (nepoužitá pole jsou šedá), V1-V3; "3D-Grafik" pro kontrolu (s. 47).
5. Materiál a izolace (hlavička nebo záložka Material/Dämmung; F6 přepíná záložky) (s. 47-48).
6. Kontrola chyb/hlášení v levém panelu (s. 81), Daten > Globale Änderung pro hromadné změny (s. 68-69).
7. Projekt > Drucken (náhled, tisk, export PDF/TXT) (s. 65-66).
- Uložení: vše se ukládá automaticky, žádné "Uložit" (s. 6).
- Vorschlagswerte: pozice se automaticky číslují; rozměry/materiál/V z předchozího řádku (s. 49).
- Schusslängen (Optionen): při délce nad definovanou délku "dílce" se součást sama rozdělí na n dílů + zbytek; zvlášť pro hranaté a kulaté (s. 73).
- Formteile < 1 m2 se podle DIN 18379 5.2 počítají jako 1 m2 (výjimka SR 100-500 mm a L); lze přepnout na přesný výpočet, ale to je v rozporu s normou (s. 45).

## 3. Import / export formáty
- DWG/DXF import do AufCALC: manuál NEUVÁDÍ. Zmínky o DXF/DWG jsou jen obecné: importované půdorysy se v projektu ukládají do formátu "dxb" (nejsou to originální DXF/DWG) a lze je při komprimaci zahrnout (s. 30); Darstellungs-Set obsahuje barvy/styly čar a Layer pro export PDF/DWG (s. 12); katalogy symbolů lze rozšířit externími DWG (s. 16-18, jiné moduly). Požadované hladiny/bloky/jednotky/měřítko: manuál neuvádí.
- Vstup z jiného modulu: export z mh-KanSYS do AufCALC (Element-ID); po opakovaném exportu se ručně zadané tvarovky přesunou na konec seznamu (s. 41, 46).
- Výstupy: tisk, PDF (kvalita 0-100), TXT s tabulátory, vhodný pro Excel (Datei > Öffnen) - doporučeno vypnout záhlaví/zápatí v "Seite einrichten" (s. 65-67).
- Projekty: komprimace do .mhz8 (s. 29-30), e-mail (s. 31); složky projektu .mh8 (plný) / .mhb8 (Basis) (s. 10, 20); starší mh6/mh7 se konvertují kopií (s. 27); mh3-5 ne (s. 21).
- Zadávání přes schránku: kopírování řádků mezi tabulkami/dokumenty jen při shodné struktuře (s. 36-37). Zda lze vložit text z Excelu: manuál neuvádí.

## 4. Konvence názvů, kódů, atributů
- Názvy projektu/Anlage: krátké, bez speciálních znaků (s. 10). Přejmenování/kopie jen přes Projektverwaltung, nikdy přes souborový systém (s. 10, 20).
- Cesta přes písmeno disku; UNC cesta nelze; cloud/synchronizace (OneDrive, SharePoint) při práci nepřípustná (s. 10).
- KB kódy tvarovek (s. 49-63). Hranaté: L, LT, TL, FL, LG (zařízení), SO (speciál), BS, BA, WS, WA, LB, US, UA, UP, RS, RA, ES, EA, TG, TA, HS, KS, KSA, BO, TR, SU, SR (hrdlo). Kulaté: R, FR, DF, NP, MF, RG, DR, RBG, RBS, RUS, RUA, RUP, RE, REB, S, SA, TS, TSA, TSU, TSAU, XS, XSA, XSU, XSAU, RHS, RHA, SZ, SZA, TZ, TZA, TZU, TZAU, XZ, XZA, XZU, XZAU.
- Rozměry: a, b (otvory), e, f (přesazení) se u US, UA, RS, RA, ES, EA, TA, HS zadávají záporně dle obrázku (DIN 18379 s. 17, pozn. 4) (s. 46-47). Přesné významy písmen rozměrů jsou v obrázcích (nečteno z textu).
- SO: zadává se celková plocha (plocha x počet) (s. 49).
- Katalogy: Herst/Prod = krátké kódy + dlouhý název; síla (a hustota); Abrechnungsgruppen: "Gerade Kanäle L" a "Formstücke F", každá 6 tříd po hranici "bis" (mm), poslední třída 9999; cena a čas volitelné (s. 70). Verbindungsteile: KB + Zuschlag (b/d/h) a (a/c), záporný = srážka (s. 71). Komponenty (např. tlumiče, klapky) pro LG/RG (s. 72).
- Hodnoty zadání/výstup: bílá pole = vstup, šedá = výstup (s. 33). Plus-projekt nelze vrátit na Basis (s. 19).

## 5. Co lze automatizovat / připravit mimo software
- Manuál NEUVÁDÍ žádné API, skriptování, makra ani import CSV/Excel/XML.
- Zdokumentované cesty: (a) naplnění přes mh-KanSYS > export do AufCALC (s. 46); (b) kopírování řádků mezi tabulkami schránkou (s. 35-37), (c) globální změna materiálu/spojů/izolace (s. 68-69), (d) předvolby ve Vorgabe-Projektu (katalogy, hlavička tisku) (s. 11-14, 67), (e) výstup TXT (TAB) do Excelu k dalšímu zpracování (s. 66).
- Mimo software lze (odvozeně, v manuálu to není popsáno) připravit tabulku sloupců Position/n/KB/rozměry/materiál/izolace/V1-V3 podle struktury řádku (s. 47-48) a katalogy (s. 70-72); nelze potvrdit, že je lze importovat hromadně.
- Interní soubory projektu nejsou určeny k ručním zásahům (s. 10, 20).

## 6. Otevřené otázky
- Má Marek na mysli jiný modul (RaumGEO/Raumbuch, Bauteil) nebo jiný manuál pro výměry místností z DWG? Tento manuál to nepokrývá.
- Existuje v mh-BIM import DWG/DXF (půdorysy, "dxb") a jeho požadavky (hladiny, bloky, jednotky, měřítko)? Zdokumentováno jinde (manuál Projektverwaltung/KanSYS?), zde ne.
- Lze do AufCALC hromadně importovat řádky (CSV/Excel/schránka z Excelu)? Neuvedeno.
- Formát/obsah exportu KanSYS > AufCALC a jeho případné předpřipravení mimo software: neuvedeno.
- Význam rozměrů tvarovek (obrázky s. 49-63) nebyl vyčten z textu; je potřeba prohlédnout obrázky přes Read.
- Zda lze licenčně využívat ACrund a Plus u zákazníka (s. 6, 16-19).
