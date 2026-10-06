# mh-BIM / mh-RohrSYS - shrnutí (omezený zdroj)
OMEZENÍ: WebFetch na mh-software.de, www.mh-software.de, media.mh-software.de (i allplan.com, auxalia.com) selhal:
`EGRESS_BLOCKED: Access to <domain> is blocked by the network egress proxy.`
Veškerá fakta níže pochází jen ze SNIPPETŮ WebSearch (shrnutí vyhledávače, ne z plného čtení stránek). Atributy tělesa/potrubí a detaily importu NEJSOU ověřeny.

## Ověřeno (snippet WebSearch, zdroj uveden)
1. Kreslení potrubí: základem jsou "Systemlinien" - kreslí se jen trasa bez výrobce, DN a konkrétních tvarovek; následně automatické dimenzování. 3D model celé sítě v jednom modelu, ne po podlažích.
   https://www.mh-software.de/heizung/rohrnetzplanung-heizung.html
   Katalogy trubek/izolace/komponent jsou volně editovatelné, známí výrobci předkonfigurováni (snippet, tytéž zdroje).
2. Armatury: z VDI 3805 (Danfoss, Honeywell, Kermi, Oventrop aj.), jejich parametry vstupují do vyvážení a tlakových ztrát. (tamtéž)
3. Hydraulické vyvážení: jedním kliknutím pro celou síť i dimenzování; jednotrubní, dvoutrubní, Tichelmann, asymetrické i vnořené kombinace. Analýza/filtry ukážou největší tlakovou ztrátu a nastavení ventilů (Voreinstellung). (tamtéž)
4. Otopná tělesa (mh-HkCALC): dimenzování z tepelné ztráty podle dat výrobců VDI 3805; mh-EN12831 není povinný, ale umožní téměř automatický návrh. Délka tělesa se navrhuje z oken/zástupných prvků RaumGEO, těleso se automaticky umístí před okno; program sestaví seřazený seznam vhodných těles a vybere optimální; výstup: seznam těles a místností; změna geometrie místnosti ovlivní ztrátu i návrh.
   https://www.mh-software.de/heizung/heizkoerperauslegung.html ; https://media.mh-software.de/downloads/heizkoerperauslegung.pdf
   => Těleso je vázáno na místnost (RaumGEO) - to je inference z popisu, přesné datové pole neověřeno.
5. Výměnné formáty: export IFC, PDF, 2D a 3D DWG, DXF; spolupráce klasicky přes DWG/IFC import a export. DWG/DXF lze načíst jako podkladové výkresy. Originální 3D objekty výrobců lze načíst přes IFC nebo 3D-DWG.
   https://www.mh-software.de/sylt/collaboration/dwg-pdf-ifc-plaene-generieren.html ; https://mh-software.de/images/download/Artikel/Service_Support/Programmeinfuehrung/mh-bim_datenaustauschformate.pdf (jen v seznamu výsledků)
6. Excel: import/export atributů rozpisek (Plankopf/plan header) více plánů; vlastní sady vlastností (Property-Sets) lze vyexportovat, doplnit v Excelu a znovu importovat. (snippet; zdroj: https://www.mh-software.de/haeufige-fragen.html a stránky o filtrech https://www.mh-software.de/loesungen/filterlisten.html - přiřazení konkrétní stránce nejisté)
7. Související stránky existují (nenačteny): Flächenheizung https://www.mh-software.de/heizung/flaechenheizungsauslegung.html a https://media.mh-software.de/downloads/flaechenheizung.pdf ; RohrSYS PDF https://media.mh-software.de/downloads/rohrnetz-planung.pdf ; Heizlast https://media.mh-software.de/downloads/heizlastberechnung2020.pdf ; RaumGEO https://www.mh-software.de/zentrales-modul-raum-geo.html ; IFC-Viewer https://media.mh-software.de/downloads/ifc-viewer.pdf ; Starter https://www.mh-software.de/service-support/freeware/tga-tools.html

## Neověřeno / nenalezeno
- Konkrétní seznam atributů tělesa a potrubí (výkon, typ, rozměry, DN, materiál, průtok, nastavení...) - nezjištěno.
- Import otopných těles jako DWG bloků s atributy nebo hromadný import těles z Excelu - žádný důkaz; snippety zmiňují jen Excel pro rozpisky/Property-Sets a IFC/3D-DWG pro 3D objekty výrobců. Neuvádět jako fakt.
- Rohrbegleitheizung, Verteiler (rozdělovač) detaily, export do Excelu (výkazy) - nezjištěno.
- Doporučení: otevřít PDF (rohrnetz-planung.pdf, heizkoerperauslegung.pdf, mh-bim_datenaustauschformate.pdf) mimo tento sandbox nebo povolit doménu mh-software.de v egress proxy.
