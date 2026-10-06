# Mondelez Werk 2 – digitalizace v MH BIM: přehled stavu

Stav k 2026-10-06. Zdroj: cloudová relace Claude Code; k disku J: ani k MH BIM na ploše přístup neměla.

## Cíl
Digitalizovat závod Mondelez (Werk 2, Lörrach) v softwaru **MH BIM** (mh-software GmbH). Vstupní formát softwaru: **DWG** (potvrzeno uživatelem). Zakázka: `System Aufnahme 2. Teil – 25_336`.
Složka s podklady (pouze na PC uživatele): `J:\M - work\Práce\DE\Angebote\2026\System Aufnahme 2. Teil - 25_336\Für Mondelez\Mondelez Konzept\Gebäudeaufnahme\Werk 2\Plene`

## Co obsahují výkresy (ověřeno)
- 1.UG (1. Untergeschoss, Bau 2, 1:200): topný systém – potrubí s DN, otopná tělesa s výkony (např. „Gussheizkörper 42/900/100, P ≈ 3000 W“), Rohrbegleitheizung, Kältezentrale, Maschinenhaus, BHKW, Trafo, Sprinkler.
- PDF z AutoCADu jsou **vektorové** (A0, 120–460 tis. cest, stovky textů) – geometrii i popisky lze z nich vyčíst.
- DXF (AC1024, jednotky mm) a DWG (AC1032 = AutoCAD 2018) existují pro podlaží 1.UG, EG, 1.OG–6.OG, Dachbereich, Versorgungsgang, Sozialgebäude, Verteiler, Heizungs-Schema, OPM1, Außentankanlage.

## Dostupnost souborů
| Soubor | Stav |
|---|---|
| 6.OG DXF, Versorggang DXF, Dachbereich/Außentank DXF, Sozialgebäude DXF | přílohou v relaci (čitelné) |
| 1.UG, 3.OG, 4.OG, 5.OG DXF | na Google Drive, ale konektor Drive má limit stažení **10 MB** → nutno číst lokálně |
| 1.OG (904 MB), 2.OG (791 MB) DXF | extrémně velké; před použitím PURGE/WBLOCK |
| EG | na Drive jen DWG (107 MB) |
| DWG | bez konvertoru (ODA/LibreDWG) nečitelné; v cloudu se LibreDWG nekompilovalo (uživatel přerušil) |

## Měřítko PDF → DXF: NEOVĚŘENO
Ruční shoda 6 kót na 1.UG dala poměr skutečná/nominální délka ≈ 0,985 (tj. PDF zřejmě není přesně 1:200). Automatická kalibrace v `tools/pdf_to_dxf.py` však vyšla jinak (0,952, jen 7 shod) a **není spolehlivá**. Pro přesnou práci používat DXF/DWG, ne PDF. Při použití PDF kalibrovat ručně podle více kót.

## MH BIM – co víme z manuálů (docs/manualy/)
- Manuály: AufCALC (povrchy VZT kanálů, DIN 18379), Bauteil (katalog skladeb, U-hodnoty), FbCALC (podlahové vytápění, DIN EN 1264), BCF-Tool.
- Žádný z nich nepopisuje import DWG ani tvorbu modelu. Importované půdorysy se ukládají jako `.dxb`. Chybí manuály **RaumGEO, RohrSYS, KanSYS, Projektverwaltung**.
- Žádný hromadný import z Excelu/CSV v manuálech není; zbývá schránka (kopírování řádků tabulek) a export z KanSYS do AufCALC přes Element-ID.
- Projektové složky `.mh8`/`.mhb8`/`.mhz8` se nesmí upravovat mimo mh-Projektverwaltung. Cesta musí jít přes písmeno disku (ne UNC), bez cloudové synchronizace.
- Web výrobce (mh-software.de) je z cloudu blokovaný; poznatky v `docs/web/` jsou jen ze snippetů vyhledávače a **neověřené**.

## Plán / doporučený postup
1. Z DXF/DWG po podlažích vytěžit soupisy: místnosti, otopná tělesa (typ, výkon), potrubí (trasy, DN), zařízení.
2. Připravit čisté podkladové DXF/DWG (pojmenované hladiny, jen relevantní prvky) pro vložení do MH BIM.
3. V MH BIM model zakládat nad podkladem (zdi, místnosti, potrubí – RohrSYS dimenzuje a vyvažuje sám; hodnoty z výkresů použít jako kontrolu).
4. Výstup: IFC 4 s mh-Data a DWG/PDF.

## Otevřené otázky
- Rozsah zakázky: které profese (topení, VZT, podlahové vytápění, jen místnosti)?
- Chce uživatel soupisy (Excel), čisté podklady (DXF), nebo obojí?
- Manuály RaumGEO / RohrSYS / KanSYS / Projektverwaltung a dokumenty `rohrnetz-planung.pdf`, `heizkoerperauslegung.pdf`, `mh-bim_datenaustauschformate.pdf`.
- Licence MH BIM (Basis vs. Plus; kreslení topných ploch je podle FbCALC manuálu v Plus).
