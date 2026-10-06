# Mondelez Werk 2 – digitalizace v MH BIM: přehled

Stav 2026-10-06. **Hlavní dokument: [`ZPRAVA.md`](ZPRAVA.md)** – co je hotové, co se potvrdilo, rozpory, co chybí a postup v MH BIM.

## Struktura repozitáře
| Složka | Obsah |
|---|---|
| `vystupy/` | Excel soupisy a tabulky pro MH BIM (podlaží, místnosti, rozdělovače, systém, Abgleich, VZT) |
| `vystupy/podklady_dxf/` | očištěné podkladové DXF k importu do MH BIM + seznam ponechaných/odstraněných hladin |
| `docs/podklady/` | shrnutí projektových dokumentů (koncepce stoupaček, hydraulika, Abgleich, tepelná data, LOOS, klima, energie…) |
| `docs/manualy/` | shrnutí manuálů MH BIM (AufCALC, Bauteil, FbCALC, BCF-Tool) |
| `docs/web/` | poznatky z webu mh-software (jen ze snippetů vyhledávání, neověřené) |
| `tools/` | skripty: DXF → soupis, PDF → texty, čištění DXF, převod PDF → DXF |

## Zdrojová data (jen u uživatele, nejsou v repozitáři)
`J:\M - work\Práce\DE\Angebote\2026\System Aufnahme 2. Teil - 25_336\Für Mondelez\Mondelez Konzept\Gebäudeaufnahme\Werk 2\Plene`

## Technické poznámky
- DXF výkresů: AC1024, jednotky mm. Topné okruhy jsou rozlišené hladinami `Heiz Wasser +TT …` (teplota, V = přívod, R = zpátečka).
- DWG (AC1032) se v relaci převádí přes LibreDWG 0.13.3 (`dwg2dxf`), ověřeno shodou počtu prvků s DXF.
- PDF výkresy jsou vektorové, ale měřítko nebylo spolehlivě ověřeno → z PDF se neberou délky.
- Konektor Google Drive stahuje jen soubory do 10 MB; přílohy v chatu do 30 MB.
