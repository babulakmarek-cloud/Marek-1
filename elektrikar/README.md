# Pomůcka elektrikáře

Tři verze téhož obsahu:

| Soubor | K čemu |
|---|---|
| `index.html` | interaktivní webová pomůcka, offline, na PC i v telefonu |
| `Pomucka_elektrikare.xlsx` | Excel se živými vzorci (žlutá = vstup, modrá = výsledek), 17 listů |
| `Tahak_elektrikare.pdf` | tisknutelný tahák A4: vzorce, tabulky a checklisty s políčky |

Excel a PDF se generují skripty v `build/` (`python3 build/build_xlsx.py`, `python3 build/build_pdf.py`; PDF potřebuje Chromium). Společná data zatížitelnosti jsou v `build/data.py`.

## Obsah
- **Elektroinstalace:** úbytek napětí a průřez, zatížitelnost a jistič (A1/B1/B2/C, PVC/XLPE, korekce), impedance smyčky a odpojení (TN), výkon ↔ proud, kompenzace účiníku, bilance příkonu rozvaděče.
- **FVE:** návrh stringu (Voc za mrazu, Vmpp za tepla, MPPT, DC/AC), DC kabel a ztráty, pojistky řetězců a AC jistič, výnos a návratnost, velikost baterie, rozestup řad.
- **MaR:** škálování 4–20 mA / 0–10 V (+ Siemens 0–27648), Pt100/Pt1000/Ni1000/NTC ↔ teplota, chyba 2vodičového čidla, rozpočet napětí proudové smyčky, PID (Ziegler–Nichols), výkon ↔ průtok vody, Kv a autorita ventilu, tahák signálů.
- **Tabulky:** převod jednotek, barvy vodičů, charakteristiky jističů, typy RCD, IP, průřez → jistič, AWG, přehled norem.
- **Checklisty:** výchozí revize, uvedení FVE do provozu (ČSN EN 62446-1), oživení MaR. Stav se ukládá v prohlížeči.

## Upozornění
Výpočty jsou orientační. Rozhoduje projekt, platné normy a odpovědnost oprávněné osoby. Tabulky zatížitelnosti vycházejí z IEC 60364-5-52 / ČSN 33 2000-5-52 (Cu, 30 °C). Před použitím v projektu je ověřte proti aktuálnímu vydání normy.
