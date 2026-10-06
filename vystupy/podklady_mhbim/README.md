# Čisté podklady pro MH BIM

| Soubor | Obsah | Prvků |
|---|---|---|
| `6OG_arch.dxf` | stavba: A0_Grundriß, A03_Türen, A05_Bemaßung, A06_Text, A07_Achslinien (bez šraf, bez situace) | 1086 |
| `6OG_heiz.dxf` | topení: všechny hladiny Heiz… / HEIZUNG… | 260 |
| `6OG_nahled.png` | náhled obou vrstev; modrý bod = počátek 0,0 | – |

Jednotky jsou mm, formát DXF AC1024 (AutoCAD 2010).

**Vztažný bod: průsečík osy 39 a osy E** (spodní fasáda, levý konec budovy). V původním výkresu leží na souřadnicích X = 24331, Y = 68325. Po posunu je to bod 0,0. Stejný bod se musí použít pro všechna podlaží s touto osovou sítí. Pokud podlaží osu 39/E nemá, je potřeba zvolit jiný průsečík a zapsat přepočet.

Vytvořeno z `6.OG_CT.dxf` (Google Drive) příkazem:
```
python tools/mhbim_podklad.py 6.OG_CT.dxf 6OG_arch.dxf --profil arch --bez-srafy --oblast 15000,60000,178000,95000 --posun 24331,68325
python tools/mhbim_podklad.py 6.OG_CT.dxf 6OG_heiz.dxf --profil heiz --oblast 15000,60000,178000,95000 --posun 24331,68325
```
Kontrola: `ezdxf recover` bez chyb a bez oprav u obou souborů.

**Zbylá podlaží:** DXF na Drive mají 50–900 MB a konektor Drive stáhne nejvýš 10 MB, proto je spusť lokálně stejnými příkazy. Oblast (`--oblast`) uprav podle výkresu, nejdřív zkus `--seznam`.
`Aussentankanlage … Dachbereich 2.OG.dxf` je převod z PDF (hladiny PDF_Geometry, Bílá…) bez osové sítě, takže ho nelze bezpečně umístit podle os.
