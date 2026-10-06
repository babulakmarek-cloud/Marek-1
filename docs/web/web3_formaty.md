# mh-BIM (mh-software GmbH) - výměnné formáty a automatizace
Metodika: WebFetch na všechny domény (mh-software.de, media.mh-software.de, community.graphisoft.com, newforma.com) selhal:
`EGRESS_BLOCKED ... Access to <domain> is blocked by the network egress proxy.`
Veškerá fakta tedy pocházejí jen ze souhrnů WebSearch (AI shrnutí výsledků), ne z přímého čtení stránek. Nutno ověřit na zdrojích.

## (1) IFC
- Čtení IFC 2x3 a IFC 4 (IFC-Viewer, zobrazení spolu s plánem mh-BIM) - https://media.mh-software.de/downloads/ifc-viewer.pdf
- Pro koordinaci lze importovat 3D-DWG nebo IFC (2x3 / 4); export IFC 4, volitelně s atributy / bez - https://media.mh-software.de/downloads/mh-bim_datenaustauschformate.pdf (dokument pro verzi 6.0)
- Synchronizace s referenčním IFC; Liegenschaft (pozemek) zadatelný, volitelně s natočeným geografickým severem - tamtéž
- v8: "mh-Data" = centrální skupinování/pojmenování/přiřazení modelových a výpočetních hodnot objektům; použitelné jako PropertySets při IFC exportu. U 3D-MiniCAD a geometrických objektů lze explicitně nastavit IFC třídu - https://www.mh-software.de/mh-8.html
- Integrovaný BCF manager (BIMcollab, Bimsync), BCF-Tool - https://media.mh-software.de/downloads/bcf-tool.pdf
- Export IFC z mh-BIM fungoval v Solibri, BIMcollab, BIM-Vision (příspěvek uživatele ve fóru; výrobce přiznal omezené zkušenosti s některými CAD) - https://community.graphisoft.com/t5/TGA/mh-software-Hotlink-Bug-bitte-um-Erfahrungswerte/td-p/544724
- NEOVĚŘENO: zda v8 exportuje i IFC 2x3 (zdroje uvádějí jen IFC 4 export); konkrétní seznam PropertySetů; Hotlink-chyba s ArchiCADem existuje (ve vlákně).

## (2) Import z CAD / Excel / CSV
- Import pro podklady: DWG/DXF půdorysy; gbXML z architektonických CAD (geometrie + termofyzikální data pro energetiku); 3D-DWG, IFC - datenaustauschformate.pdf výše
- Revit/ArchiCAD: nenalezen žádný přímý nativní import; cesta je IFC / DWG / gbXML (domněnka z uvedených formátů).
- Excel: v8 import/export atributů popisových polí (Plankopf) všech plánů přes Excel - mh-8.html. Materiálové seznamy export do XLS (datenaustauschformate.pdf).
- NEOVĚŘENO: import Raumbuch / Bauteile / Heizkörper z Excelu/CSV (vyhledávání nic konkrétního nevrátilo). Export AVA: ORCA AVA - https://www.mh-software.de/sylt/collaboration/datenaustausch-orca.html
- Exporty: IFC, PDF, 2D/3D-DWG, DXF - https://www.mh-software.de/sylt/collaboration/dwg-pdf-ifc-plaene-generieren.html

## (3) API / skriptování / makra / COM / hromadný import
- Ve výsledcích nenalezena žádná zmínka o veřejném API, makrech, skriptování ani COM. Neprokázáno = neexistuje; nutno dotaz na podporu.
- Jediná nalezená "automatizace": Excel round-trip popisových polí, IFC/BCF, DWG export. Newforma app-market má záznam mh software (https://www.newforma.com/app-market/mh-software/mh-software/), obsah nenačten.

## (4) Formáty projektů (.mh8, .mhb8, .mhz8, .dxb)
- Žádný zdroj nenalezen o struktuře těchto formátů. Nelze říct, zda jsou čitelné/otevřené. Domněnka (neověřeno): proprietární; interoperabilita jen přes IFC/DWG/DXF. Zkontrolovat FAQ https://www.mh-software.de/haeufige-fragen.html (nenačteno).

## (5) Novinky v8 a workflow 2D DWG -> BIM
- v8 (https://www.mh-software.de/mh-8.html): generátor schémat, 2D & 3D MiniCAD, návrhy prostupů jedním klikem, legendy, mh-Data (PropertySets), Excel plankopf, nové ikony, tmavý režim.
- Workflow (https://www.mh-software.de/planerstellung-abgabe.html, https://mh-software.de/produkte/gebaeude/durchbruchsplanung.html): DWG půdorys se vloží jako podklad; při návrhu prostupů se chytají čáry zdí z DWG; model je 3D celkový model (stockwerke, výpočty, plány provázané); kolize přes RaumGEO (tepelný model budovy - https://media.mh-software.de/downloads/raumgeometrie.pdf); výstup DWG/PDF/IFC.
- Automatické rozpoznání zdí z 2D DWG: nenalezeno. Doporučení je domněnka: DWG podklad -> ručně modelovat zdi/místnosti v RaumGEO -> TZB v 3D -> IFC 4 export s mh-Data.
