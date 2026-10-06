# Podkladové DXF pro MH BIM

Výřez z původních výkresů (DXF AC1024, jednotky mm), jen hladiny potřebné jako podklad pro model:
půdorys (`A0_Grundriß*`, `Geometrie*`), dveře, schodiště, kóty, osy, texty (`A06_Text*`) a všechny topné hladiny (`Heiz*`, `HEIZUNG*`, `Armaturen`).
Odstraněna strojní dispozice (`A11_Belegung`, `Kugelmischer`, `*_Layout`…), elektro (`A12_EL_Verteiler`) a nepoužité bloky.
Počet prvků v každém souboru byl po uložení ověřen opětovným načtením.

| Soubor | Zdroj | Velikost |
|---|---|---|
| 1UG_podklad.dxf | 1.UG_CT.dxf | 9,2 MB |
| 3OG_podklad.dxf | 3.OG_CT.dxf | 2,4 MB |
| 4OG_podklad.dxf | 4.OG_CT.dxf | 4,6 MB |
| 5OG_podklad.dxf | 5.OG_CT.dxf | 4,9 MB |
| 6OG_podklad.dxf | 6.OG_CT.dxf | 2,1 MB |
| Versorgungsgang_podklad.dxf | Versorggang.dxf | 2,8 MB |
| Sozialgebaeude_podklad.dxf | Sozialgebäude (Silberhalle, Altes Pförtnerhaus).dxf | 2,5 MB |

`*_hladiny.txt` = co bylo ponecháno a co odstraněno (počty prvků na hladinu).

**K ověření:** odstraněny byly i hladiny `0` a `Level …` (např. 1.UG: `0` 12 846 prvků, `Level 31` 6 946). Pravděpodobně jde o vložené strojní modely, ale ověřeno to není – pokud v podkladu něco chybí (stěny, sloupy), je to nejspíš tam.
**Chybí:** EG, 1.OG, 2.OG (DWG/DXF nejsou v relaci k dispozici), Dachbereich (DXF je převod z PDF bez měřítka v mm).
