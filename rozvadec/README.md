# Návrh rozváděče (NN) – pomůcka pro elektrikáře

Program v prohlížeči pro návrh nových a překreslení stávajících rozváděčů. **Bez instalace, bez internetu, bez serveru** – data zůstávají na vašem počítači.

## Spuštění na workstationu
Zkopírujte soubor **`dist/Rozvadec.html`** kamkoli (plocha, disk J:, USB) a otevřete ho dvojklikem (Edge / Chrome / Firefox).
Vývojová verze: `index.html` (potřebuje vedle sebe `app.css` a složku `js/`).

## Co umí
| Záložka | Obsah |
|---|---|
| 1 Rozváděč | soustava (TN-C-S, TN-S, TN-C, TT), Ze, Ik3, skříň (řady × moduly, Pde), údaje pro štítek, jazyk CZ/DE/EN |
| 2 Přístroje a vývody | hlavní vypínač, RCD, jističe 1f/3f, RCBO, pojistky, SPD, stykač, relé, elektroměr, zdroj, svorky, rezerva; vývody s kabelem, délkou, uložením; živý náhled skříně; vyvážení fází, přečíslování BMK, návrh průřezů |
| 3 Výpočty | Ib, Iz (tab. × teplota × seskupení), Ib ≤ In ≤ Iz, I2 ≤ 1,45·Iz, ΔU (vč. přívodu), Zs, Ik1 min, Ia, doba odpojení 0,4/5 s, RCD 30 mA u zásuvek, Icn vs. Ik3, zatížení chráničů, soudobost, RDF, ztrátový výkon vs. Pde, nesymetrie fází, obsazenost řad |
| 4 Pohled | optické znázornění reálného vzhledu (DIN lišty, přístroje, popisové pruhy) |
| 5 Jednopólové | přehledové schéma s tabulkou (BMK, přístroj, fáze, P, Ib, kabel, délka, ΔU, okruh) |
| 6 Vícepólové | L1/L2/L3/N/PE, každý pól, sběrnice za chrániči, svorky vývodů |
| 7 Štítky | popisové pruhy 1:1, typový štítek dle EN 61439-1 čl. 6.1, výstražný štítek, seznam okruhů (Stromkreisliste) |
| 8 Protokol | kusové ověření EN 61439-1 čl. 11, naměřené Zs/Riso/RCD vs. výpočet |

Exporty: **DXF** (AutoCAD/DraftSight/EPLAN, mm), SVG, PNG, tisk/PDF, projekt `.json`, seznam vývodů **CSV** (středník, Excel). Stávající rozváděč lze sepsat v Excelu a načíst přes *Import CSV*.

## Normy
ČSN EN IEC 61439-1/-2/-3 (DIN EN 61439 / VDE 0660-600), ČSN 33 2000-4-41 (VDE 0100-410), -4-43 (VDE 0100-430), -5-52 (VDE 0100-520, VDE 0298-4), ČSN 33 2000-6 (VDE 0100-600). Přehled v záložce **?**.

## Omezení – co je potřeba ověřit
- Zatížitelnost: IEC 60364-5-52 příl. B, Cu/PVC 70 °C. Hodnoty DIN VDE 0298-4 se mohou mírně lišit. Kabely XLPE/Al zatím nejsou.
- Ia pojistek gG je **orientační**; ztrátové výkony přístrojů jsou **typické** – pro oteplení použijte katalog výrobce.
- Selektivita se kontroluje jen podle jmenovitých proudů, ne podle charakteristik.
- Výpočet nenahrazuje měření při výchozí revizi.

## Testy
```
node test/calc.test.js     # výpočty
node test/ui.test.js       # prohlížeč (Playwright)
python3 build.py           # sestaví dist/Rozvadec.html
```
