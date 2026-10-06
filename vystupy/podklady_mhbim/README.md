# Čisté podklady pro MH BIM

| Soubor | Obsah | Prvků |
|---|---|---|
| `6OG_arch.dxf` | stavba: A0_Grundriß, A03_Türen, A05_Bemaßung, A06_Text, A07_Achslinien (bez šraf, bez situace) | 1086 |
| `6OG_heiz.dxf` | topení: všechny hladiny Heiz… / HEIZUNG… | 260 |
| `6OG_nahled.png` | náhled obou vrstev; modrý bod = počátek 0,0 | – |
| `Versorgungsgang_arch.dxf` | stavba (A0…, bez textů průvlaků A06_Text - Unterzüge, bez Lageplanu a průvlaků A11) | 208 |
| `Versorgungsgang_heiz.dxf` | topení | 254 |
| `Versorgungsgang_nahled.png` | náhled; modrý bod = počátek 0,0 | – |

Jednotky jsou mm, formát DXF AC1024 (AutoCAD 2010).

**Každé podlaží má jiné souřadnice.** Proto se každé posouvá na svůj průsečík osy 39 a osy E:

| Výkres | Osa 39 (X) | Osa E (Y) | Kontrola: vzdálenost os A–E |
|---|---|---|---|
| 6.OG | 24331 | 68325 | 20590 mm |
| Versorgungsgang | 20618 | 69827 | 20590 mm ✓ |

**Vztažný bod: průsečík osy 39 a osy E** (spodní fasáda, levý konec budovy). V původním výkresu leží na souřadnicích X = 24331, Y = 68325. Po posunu je to bod 0,0. Pokud podlaží osu 39/E nemá, je potřeba zvolit jiný průsečík a zapsat přepočet.

Vytvořeno z `6.OG_CT.dxf` (Google Drive) příkazem:
```
python tools/mhbim_podklad.py 6.OG_CT.dxf 6OG_arch.dxf --profil arch --bez-srafy --oblast 15000,60000,178000,95000 --posun 24331,68325
python tools/mhbim_podklad.py 6.OG_CT.dxf 6OG_heiz.dxf --profil heiz --oblast 15000,60000,178000,95000 --posun 24331,68325
```
Kontrola: `ezdxf recover` bez chyb a bez oprav u obou souborů.

Versorgungsgang: zdroj `Versorggang.dwg` (Drive) → LibreDWG `dwg2dxf` → `tools/dxf_oprav_zalomeni.py` → ezdxf recover →
```
python tools/mhbim_podklad.py V.dxf Versorgungsgang_arch.dxf --hladiny "^(A0(?!6_Text - Unt)|Nord-Pfeil)" --bez-srafy --oblast=-7000,15000,80000,102000 --posun=20618,69827
python tools/mhbim_podklad.py V.dxf Versorgungsgang_heiz.dxf --profil heiz --oblast=-7000,15000,80000,102000 --posun=20618,69827
```

**Jak najít osu 39/E v dalším podlaží:** `--seznam`, pak na hladině `A07_Achslinien` svislá čára u popisku „39“ (X) a vodorovná čára cca 540 mm nad popiskem „E“ (Y).

**Zbylá podlaží:** DXF na Drive mají 50–900 MB a konektor Drive stáhne nejvýš 10 MB, proto je spusť lokálně stejnými příkazy. Oblast (`--oblast`) uprav podle výkresu, nejdřív zkus `--seznam`.
`Aussentankanlage … Dachbereich 2.OG.dxf` i `Dachbereich 2.OG_CT.dwg` jsou převod z PDF (hladiny PDF_Geometry, Bílá…) bez osové sítě, takže ho nelze bezpečně umístit podle os.
