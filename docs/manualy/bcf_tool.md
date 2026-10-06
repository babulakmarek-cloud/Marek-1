# BCF-Tool (mh-software, MH BIM) - shrnutí manuálu (originál německy, čísla stran = PDF = tištěné)

## 1. Účel
- BCF (Open BIM Collaboration Format) = zjednodušená výměna informací mezi různými SW nad IFC; modelová komunikace, nese stav, místo, směr pohledu, prvek, poznámku, uživatele a čas v IFC modelu (s. 4).
- Nový standardní BCF-Tool má rozhraní pro cloud externího poskytovatele; podporuje BCF 2.0, 2.1 a 3.0 (s. 4).
- Projekt = témata (Themen), doplňovaná komentáři, snapshoty a obrázky (s. 4). Spuštění: menu Projekt nebo ikona v otevřené anlage mh-BIM (s. 4, 15).

## 2. Postup práce
- Spustit nástroj -> zvolit osobní / týmový / cloudový projekt -> otevřít nebo založit téma -> napsat či upravit komentář (s. 4).
- Projekty (s. 13, 15-17): nový panel "+"; Persönlich/Team = lokální, Cloud = připojení k účtům. Více projektů současně, každý ve vlastním panelu.
- Lokální projekt (s. 19-20): název, cesta, u osobního i verze BCF; vybrat šablonu (výchozí / z jiného projektu / prázdná).
- Téma (s. 22-23): název -> Stav, Typ, Priorita, Řešitel, Fáze, Label, termín, popis; vpravo Snapshoty a obrázky, Přílohy (odkazy, dokumenty), Související témata.
- Komentář (s. 24-26): povinně text, volitelně snapshot a/nebo obrázek (PNG, JPG, JPEG); odeslání ikonou. Snapshot se bere z aktuálně zobrazených anlagen v mh-BIM; chyba, pokud mh-BIM neběží. Před odesláním lze snapshot/obrázek upravit (otevře se MS Paint) nebo smazat. Komentář lze později upravit/smazat přes "...".
- Snapshot zpět do projektu (s. 26): otevřít potřebné anlagen v mh-BIM, ikona nastaví pohled na snapshotem zachycený výřez; více/neortogonální řezy se sloučí do jednoho obdélníkového výřezu.
- Filtr a historie posledních témat (s. 26-27). Nastavení: jazyk DE/EN, světlé/tmavé schéma, proxy, lokální uživatel (jméno, ID/mail), výchozí šablona; změny platí po restartu (s. 27-28).
- Šablony (s. 28-29): projektově specifické slovníky hodnot polí; výchozí šablona se kopíruje do nových projektů, pozdější změny na existující projekty nepůsobí.

## 3. Formáty a vazba na IFC/DWG
- .bcf (osobní, single-user): oficiální formát, čitelný externími BCF viewery; nejrozšířenější je verze 2.1 (s. 19).
- .mhbcf (týmový, multi-user): interní formát mh, externí viewery jej nezpracují; jen pro komunikaci uvnitř firmy (s. 19). Pro komunikaci mezi více firmami doporučují cloudové projekty (s. 19).
- Cloud (s. 18): poskytovatelé s API dle BCF standardu; uvedeni BIMcollab Cloud a Bimsync Arena (Catenda); vlastního poskytovatele lze přidat (API URL, Client ID, Client Secret, Scope); potřeba účet u poskytovatele a volba verze BCF. Šablony a omezení (např. mazání témat, přílohy) se u cloudu řídí webovou aplikací poskytovatele (s. 22, 23, 25).
- Přílohy: u osobních/týmových projektů od BCF 3.0, u cloudu jen pokud to poskytovatel povolí (s. 23).
- IFC (s. 7-11, kap. 3.4 "Allgemeine IFC-Einstellungen"): export z mh-BIM do IFC 2x3 nebo IFC 4; jednotky Automaticky/mm/m; Autor, adresa, fáze stavby; kontrola jedinečnosti IFC-GUID; tři režimy souřadnic exportu (mh-souřadnice [výchozí] / souřadnice aktivního referenčního IFC / ruční souřadnice), včetně natočení k severu; volby rozsahu: značka počátku, IfcDistributionPorts (logické vazby potrubí/kanálů), IfcZip, mh PropertySets, uživatelské PropertySets, BaseQuantities/Qto pro AVA.
- Snapshoty a zobrazení se řídí globálními souřadnicemi z těchto IFC nastavení; platí pro všechny IFC exporty všech anlagen aktivního projektu, změny je nutné odsouhlasit s celým týmem (s. 17, 25, 26).
- DWG: v manuálu se nevyskytuje (nic o DWG nenalezeno).

## 4. Důležité pro tvorbu modelu
- Sjednotit IFC nastavení (verze, jednotky, souřadnice, referenční IFC) v celém projektu před vytvářením BCF snapshotů, jinak nesedí výřezy při externím zpracování (s. 17, 25).
- Zkontrolovat IFC-GUID na duplicity (s. 8); GUID identifikují prvky, ke kterým se BCF vztahuje (IFC datový model, s. 4).
- Jednotky: některé viewery ignorují jednotku v IFC a hodnoty nepřepočtou; mh proto píše jednotku i do popisu (s. 10).
- Export Durchbrüche z DpSYS: doporučeno zapnout "Ursprung der Liegenschaft" (VDI 2552 list 11.2, s. 10). KanSYS: kabelové trasy lze přepnout entitu z Kanal na Kabelträger (s. 11).
- Pro vlastnosti: využít mhDATA a uživatelské PropertySets k exportu jen vybraných dat (s. 10).
- Nezapomenout: verze starších projektů (výběr Liegenschaft od v7.0.300, červen 2023) může dát nekompatibilní export (s. 8).
- Požadavky: Windows 10 64bit, 8 GB RAM doporučeno (s. 4-5).

## 5. Otevřené otázky (v manuálu nezodpovězeno)
- Nic o DWG ani o tom, jak BCF zachází s 2D/DWG výkresy.
- Jak přesně BCF téma odkazuje na konkrétní prvek/GUID (výběr prvků, viewpointy) - manuál popisuje jen snapshot a výřez, ne vazbu na komponenty.
- Nepopsán import/export .bcf souboru z cloudu, ani převod .mhbcf -> .bcf.
- Chybí obsah kapitol "veraltetes BCF-Tool" (odkazy na s. 17, 18, 21, 22 bez popisu) a práva/role uživatelů.
- Které verze BCF jsou v cloudu preferované a jak se řeší konflikty v Team-projektech (jen "Aktualisieren", s. 20, 24).
- Manuál je 29 stran, strana 1 je titulní, 2 obsah, 30 prázdná; obrázky (dialogy) nebyly čteny, jen text.
