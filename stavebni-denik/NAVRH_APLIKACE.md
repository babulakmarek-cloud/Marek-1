# Aplikace „Stavební deník + zakázky" – návrh

Cíl: jedna aplikace pro živnostníka/malou firmu (montáže, topení, instalace), použitelná **na stavbě z mobilu** a v kanceláři z PC.

## 1. Moduly

| Modul | Co umí |
|---|---|
| **Zákazníci** | karta zákazníka (kontakt, IČO/DIČ, adresy staveb), historie zakázek, poznámky |
| **Zakázky** | číslo, stav (poptávka → nabídka → realizace → předáno → fakturováno), termíny, rozpočet vs. skutečnost |
| **Nabídky** | tvorba z ceníku/šablon (položky, množství, sleva, DPH), PDF export, odeslání e-mailem, převod nabídky na zakázku |
| **Faktury** | z nabídky/zakázky jedním klikem; zálohová, konečná, dobropis; číselná řada, splatnost, QR platba (SPAYD), PDF; stav úhrady |
| **Stavební deník** | denní zápis: datum, počasí, pracovníci, hodiny, provedené práce, problémy, **fotky s popisem**, GPS/místo, podpis zákazníka při předání |
| **Fotodokumentace** | galerie dle zakázky/podlaží/fáze (před–během–po–závada), popisky, export do PDF protokolu |
| **Materiál** | ceník + sklad, plán vs. skutečná spotřeba na zakázce, upozornění na překročení, náklad |
| **Pokrok** | etapy s vahou a % hotovo, Ganttův graf, celkový pokrok, porovnání plán/skutečnost |
| **Vyhodnocení** | marže zakázky, spotřeba materiálu, odpracované hodiny, report pro zákazníka (PDF) |

## 2. Hlavní toky

1. Zákazník → **nabídka** (z ceníku) → odsouhlasení → **zakázka** se zděděnými položkami jako plán materiálu.
2. Na stavbě: mobil → „Nový zápis" → fotky (z fotoaparátu), diktování popisu, výběr materiálu (−sklad) → uloží se i offline.
3. Večer automaticky: pokrok %, spotřeba vs. plán, upozornění „trubka 90 % čerpáno".
4. Předání: PDF **předávací protokol** + deník + fotky → podpis na displeji → **faktura** z reálně provedených položek.

## 3. Datový model (zjednodušeně)

```
Customer(id, name, ico, dic, email, phone, billing_address)
Site(id, customer_id, address, note)
Job(id, customer_id, site_id, number, name, status, start, end_plan, budget)
Quote(id, job_id, number, date, valid_until, status)      QuoteItem(quote_id, item_id, qty, unit_price, vat)
Invoice(id, job_id, number, type, issued, due, paid_at)   InvoiceItem(invoice_id, text, qty, unit_price, vat)
Item(id, name, unit, price_buy, price_sell, stock)        -- ceník + sklad
DiaryEntry(id, job_id, date, weather, temp, workers, hours, work_done, issues, author)
Photo(id, entry_id, job_id, file, caption, phase, area, taken_at, lat, lon)
MaterialUse(id, entry_id, job_id, item_id, qty, date)
Stage(id, job_id, name, weight, plan_from, plan_to, actual_from, actual_to, percent)
```

Vyhodnocení = pohledy nad těmito tabulkami (spotřeba = Σ MaterialUse / plán z QuoteItem; pokrok = Σ(váha × %)/Σ váha).

## 4. Technologie (doporučení)

| Varianta | Pro | Proti |
|---|---|---|
| **A. PWA (React/Vue + backend + SQLite/Postgres)** – doporučeno | jedna kódová báze pro mobil i PC, instalace na plochu, offline fronta, foto z kamery, PDF na serveru | nutný hosting (levný VPS) |
| B. No-code (Airtable/Glide/Base44) | start za dny | omezení v PDF fakturách, měsíční poplatky |
| C. Excel + Power Automate | nic nového se neučit | fotky a mobil neohrabané |

Doporučená sestava A: React PWA + FastAPI/Node, PostgreSQL, úložiště fotek (S3-kompatibilní), generování PDF (WeasyPrint), přihlášení e-mail+heslo, denní záloha.

## 5. Etapy realizace

1. **MVP (2–3 týdny):** zákazníci, zakázky, deník s fotkami, PDF deníku.
2. **Obchod (+2 týdny):** ceník, nabídky, faktury s číselnou řadou a QR platbou.
3. **Materiál a pokrok (+2 týdny):** spotřeba vs. plán, etapy, Gantt, dashboard marže.
4. **Doladění:** offline režim, podpis při předání, export do účetnictví (Pohoda/Money – XML/CSV).

## 6. Otevřené otázky

- Fakturace v CZ/SK/DE (DPH, jazyk dokladů, reverse charge)? – podle toho měnit šablony.
- Pracuje v aplikaci jen jeden uživatel, nebo i montéři/subdodavatelé s omezenými právy?
- Existující účetnictví, se kterým má faktura komunikovat?
- Mají fotky po exportu jít i do předávacího protokolu pro kontrolní orgány / investora?

Do doby, než aplikace vznikne, slouží jako zárodek datového modelu a procesů **`stavebni-denik.xlsx`** (listy odpovídají tabulkám výše).
