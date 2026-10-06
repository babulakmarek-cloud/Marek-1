# mh-BIM 8 – Bauteilberechnung (mh-Bauteil), shrnutí manuálu (64 s.)
Čísla stran = tištěná čísla v manuálu (shodují se s PDF). Manuál je německy, vydání 2026. Text je převážně obecný (správa projektů); vlastní výpočet skladeb zabírá jen s. 5-6 a 42-48, 53-54.

## 1. Účel modulu a datový model
- mh-Bauteil eviduje stavební prvky (stěny, stropy, okna); jiné moduly (mh-EN12831 tepelné ztráty, mh-VDI2078 chladicí zátěž, mh-VDI2067/10 simulace, mh-FbCalc) na ně odkazují. Odkaz místo přímého zadání U-hodnot umožňuje centrální změny (s. 5).
- Umí: správa katalogů Baustoffe/Bauteile, data oken/dveří, výpočet U (DIN EN ISO 6946), U z více ploch (Fachwerk), difuze vodní páry, průběh teploty a Glaserův diagram (s. 5). Lze použít i samostatně (s. 5).
- Skupiny prvků: Aussenwand, Innenwand, Fußboden/Decke, Dach, Fenster/Türen, Mehrflächen (s. 5-6, 42).
- Dva katalogy: "verwendete Bauteile" (prvky skutečně použité v Heizlast/Kühllast) a "Katalog". Výpočty vždy běží nad "verwendete Bauteile" (s. 6, 42, 47). Použití prvku z Katalogu ho automaticky zkopíruje do "verwendete" (s. 46-47). Existuje i katalog napříč projekty (Lokale/Globale Kataloge) (s. 6, 42) – podrobnosti v tomto PDF nejsou.
- Hierarchie: Projekt (= budova/komplex) obsahuje Anlagen (moduly). Bauteil, Heizlast, Kühllast, RaumGEO jsou v projektu jen jednou a jmenují se jako projekt (s. 17, 21).
- Kopie Vorgabe-Katalogů se při první Anlage modulu uloží do projektu; každý projekt má vlastní nezávislé katalogy. Kód "BT" = Baustoff-Katalog + Bauteil-Katalog (s. 12, 21).
- Textury: každému prvku (kromě oken) lze přiřadit texturu pro objemové zobrazení v RaumGEO; po změně je nutný přepočet v RaumGEO (s. 42).

## 2. Postup práce (s. 6, 43-46)
1. Zapnout tlačítka "Aufbau" a "Editieren"; vybrat typ prvku vlevo nahoře; vpravo nahoře záložku "verwendete Bauteile" nebo "Katalog".
2. Zadat zkratku (max. 4 znaky) a název prvku.
3. Bez vrstev lze ručně zadat tloušťku, plošnou hmotnost a U-hodnotu. Pro Kühllast u Außenwand/Dach navíc absorpci a a emisivitu ε (s. 43).
4. Vrstvy zadávat zevnitř ven: dvojklik/F2 ve sloupci Wandschichten otevře Baustoffkatalog, dalším dvojklikem se přenese materiál s λ; pak se zadá tloušťka. Teplotní průběh, ps a p i U se počítají automaticky (s. 43).
5. Záložka R-Wert: odpory přestupu tepla R-Innen/R-Außen (návrh dle směru toku tepla, dvojklik = tabulka); RT = celkové R, R-Wert = R bez přestupů. Pro Fußboden/Decke volba "Auto" – v Heizlast se R volí podle teploty sousední místnosti, zadávají se R pro směr nahoru i dolů; Kühllast používá hodnoty "dolů" (s. 43).
6. Záložka Feuchte: teploty a relativní vlhkosti (zima/léto), doba období; výsledek množství kondenzátu (zima) a odpařené vody (léto). Teplotní průběh a Glaser jen pro zimu (s. 43-44).
7. Fenster/Türen: šířka, výška (pokud se mají předat do volajícího modulu), U-hodnota; pro Kühllast ε, "Vorschlagswerte" zasklení a stínění (podíl rámu, g, TL, akon, počet skel; poloha stínění Kein/Außen/Zwischen/Innen, gtot,dir/diff, TL tot,dir/diff, akon,tot) nebo "Manuelle Dateneingabe" (s. 44-45).
8. Mehrflächenelement: vybrat definované stěny, zadat délku×šířku, plochu nebo % (součet 100 %); U se spočte z plošných podílů; zobrazí se horní a dolní R (ISO 6946, kap. 6.2), R = jejich aritmetický průměr (s. 45). Nesmí se použít v Kühllast – nutný Ersatz-Bauteil (s. 45-46).
9. Assistent Flächenberechnung (dvojklik v poli plochy; analogicky objem): základní tvary, Teilflächen se sčítají, Abzugsflächen odečítají, vlastní vzorce (+ - * /, sin, cos, tan, arcsin, arccos, arctan, log, ln, PI, závorky); zadání se uchová (s. 46).
10. Ersatz-Bauteil pro Kühllast (záložka Kühlfläche): pro podhledy, chladicí stropy, vícedílné prvky; originál zůstává beze změny. U prvku s chladicí plochou nastavit R-Innen = 0,1 m²K/W (volba "Kühlfläche auf Innenseite setzen") (s. 47-48).
11. Kühllast a pořadí vrstev: Fußboden/Decke má pořadí podlahy, při použití jako strop se interně otočí; Innenwände jen symetrické, jinak zadat dvakrát s obráceným pořadím (s. 48).
- Kontrola: stavové zprávy vlevo (Hinweis = lze opravit, Fehler = nutno opravit; dvojklik na zprávu skočí na místo) (s. 62-64). Výsledky ověřovat vlastní přibližnou kalkulací (s. 31).

## 3. Knihovny skladeb a materiálů (s. 12, 46-47, 53-54)
- Baustoff-Katalog: menu Katalog > Baustoffe (nebo dvojklik/F2 ve sloupci Wandschichten). Dvě záložky: "verwendete Baustoffe" a "Baustoff-Katalog"; použití z katalogu kopíruje materiál do "verwendete" (s. 53-54).
- Nový materiál: záložka -> skupina materiálů -> "Editieren" -> prázdný řádek -> název, hustota (Dichte), λ, difuzní odpor µ, měrná tepelná kapacita c -> "Übernehmen"/dvojklik (s. 53).
- Skladby (Bauteile) se vytvářejí ve skupinách výše; hromadná správa a "Lokale und Globale Baustoffe" jsou jen odkazem, obsah v PDF chybí.
- Vorgabe-Kataloge sdílené všemi Vorgabe-Projekty; doporučeno udržovat aktuální, ne držet více starých verzí výrobce; lze je upravit přes libovolný Vorgabe-Projekt (s. 12).

## 4. Import / export
- Bauteile samotné: DWG/DXF import/export manuál NEUVÁDÍ. V modulu není žádná funkce importu/exportu skladeb.
- Tisk/export výpisu (s. 49-52): PDF (kvalita 0-100) nebo TXT s TAB oddělovači pro Excel (doporučeno předem vypnout hlavičku a patičku v "Seite einrichten"). Logo bmp/jpg 1:1 (cca 2×2 cm), celá hlavička 1:10 (cca 2×20 cm).
- Související (jiné moduly, jen zmínky): importované půdorysy z DXF/DWG se ukládají jako *.dxb (s. 28); Layer a barvy pro PDF/DWG export jsou v Darstellungs-Sets (s. 11); externí DWG symboly (s. 15-16); IFC export (s. 14).
- Přenos dat mezi dokumenty: Kopírovat/Vložit řádků tabulky mezi stejně strukturovanými dokumenty; u tabulek bez čísel řádků je klíč zkratka (s. 32-34).
- Archiv: Projekt > Komprimovat do *.mhz8 (s. 27-30); konverze mh6/mh7 -> mh8 (s. 24-27).

## 5. Konvence názvů a atributů
- Zkratka prvku max. 4 znaky + název (s. 6, 43). U oken/dveří a ostatních typů stejně.
- Název projektu i Anlage: krátký, bez speciálních znaků. Složka projektu má příponu .mh8 (plná) nebo .mhb8 (Basis) (s. 9, 18).
- Přejmenování/kopírování/mazání jen přes mh Projektverwaltung, nikdy v průzkumníku (riziko zničení projektu) (s. 9, 18, 24).
- Cesta přes písmeno disku, UNC cesta není možná; cloud (OneDrive, SharePoint) a trvalé zrcadlení při práci nejsou povolené (s. 9).
- Pojmenování konkrétních atributů mimo výše uvedené (zkratka, název, λ, µ, c, ε, a, R, U) manuál nespecifikuje.

## 6. Co lze připravit mimo software
- Seznam Baustoffe: název, hustota, λ, µ, c (s. 53), rozdělený do skupin materiálů.
- Seznam skladeb zevnitř ven (materiál + tloušťka), zkratka (max. 4 znaky) a název; hodnoty R-Innen/R-Außen, směr toku tepla (s. 43).
- Pro okna: U, rozměry, ε, g, TL, podíl rámu, typ a poloha stínění (s. 44-45).
- Pro Kühllast: absorpce a, ε, Ersatz-Bauteile pro podhledy, chladicí stropy a Mehrflächen (s. 45-48).
- Klimatické okrajové podmínky pro difuzi (t, φ zima/léto, doba období) (s. 43).
- Organizace: logo/hlavička pro tisk (s. 50), Vorgabe-Projekt s firemními standardy (s. 10-13), logické názvy projektů. Software nemá deklarovaný import tabulek – zadání se dělá ručně nebo přes Zwischenablage/Vložit (s. 32-34, 52).

## 7. Otevřené otázky
- Existuje import skladeb/materiálů z Excelu/CSV či jiných zdrojů? Manuál uvádí jen tabulkové kopírování přes schránku (s. 32-35).
- DWG/DXF u Bauteilů: žádná zmínka; ověřit u výrobce (hotline@mh-software.de, s. 4).
- "Lokale und Globale Kataloge" / "Lokale und Globale Baustoffe" – odkazy bez obsahu v tomto PDF (s. 6, 42, 53).
- Jak se provádí Vorgabe-Katalog "BT" správa (editace přes Vorgabe-Projekt – kroky nejsou v tomto PDF) (s. 12).
- Přesné hodnoty Vorschlagswerte (R přestupu, podíly rámů) a vazba na normu nejsou v textu; pouze odkaz na tabulky (s. 47).
- Vzorce a okrajové podmínky Glaserovy metody (norma, výpočet) nejsou popsány, jen výstup (s. 5, 43-44).
- Obrázky (screenshoty masek) nebyly čteny; text obsahuje pouze popisy (nezkoumáno vizuálně).
