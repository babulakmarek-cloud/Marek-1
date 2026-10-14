# Pomůcka autoelektrika 12 / 24 / 48 V

Tři verze téhož obsahu:

| Soubor | K čemu |
|---|---|
| `index.html` | interaktivní webová pomůcka, offline, na PC i v telefonu. Přepínač 12 / 24 / 48 V přepíše výchozí hodnoty ve všech kartách |
| `Pomucka_autoelektrika.xlsx` | Excel se živými vzorci (žlutá = vstup, modrá = výsledek), 13 listů |
| `Tahak_autoelektrika.pdf` | tisknutelný tahák A4: vzorce, tabulky, checklisty s políčky |

## Obsah
- **Kabely a jištění:** úbytek napětí a průřez (včetně kostry jako zpětného vodiče), pojistka + kabel + odhad zkratového proudu, výkon ↔ proud ↔ odpor, srovnání 12/24/48 V, startér (startovací proud, kabel + a −, úbytek do 0,5 V / 1 V, tabulka min. průřezů podle proudu a délky).
- **Baterie:** výdrž a kapacita, stav nabití olova z napětí, doba nabíjení, sestavení sériově/paralelně.
- **Zdroje a měniče:** DC-DC měnič/nabíječ, střídač → 230 V, solární MPPT regulátor.
- **Energetická bilance:** denní spotřeba, kapacita baterie a solár; LED + předřadný rezistor (řada E24).
- **Tabulky:** typická napětí podle soustavy, průřez → proud → pojistka, barvy pojistek, svorky a relé, příkony, AWG.
- **Checklisty:** nový okruh, diagnostika baterie a nabíjení, ostrovní systém.

Excel a PDF se generují skripty v `build/` (`python3 build/build_xlsx.py`, `python3 build/build_pdf.py`; PDF potřebuje Chromium). Společná data (tabulka kabelů, pojistky) jsou v `build/data.py`.

## Upozornění
Výpočty jsou orientační. Tabulka trvalých proudů kabelů je konzervativní (měď, ve svazku). Rozhodují údaje výrobce vozidla, baterie a měniče. Pro 48 V používej pojistky, relé a vypínače s DC napětím ≥ 58 V.
