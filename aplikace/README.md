# Stavební deník – aplikace

Zakázky, zákazníci, deník s fotkami, materiál (plán vs. spotřeba), pokrok, nabídky a faktury v CZK / EUR, více uživatelů (role Admin / Montér). Neprovádí účetnictví ani se s žádným neprovazuje.

## Spuštění
```
pip install -r requirements.txt
python app.py            # http://127.0.0.1:5000
```
Při prvním spuštění se zobrazí formulář pro vytvoření administrátora. Data (SQLite, fotky, tajný klíč) jsou v `data/` (cesta jde změnit proměnnou `DENIK_DATA`; zálohujte celou složku).
Pro přístup z mobilu na stavbě: `HOST=0.0.0.0 python app.py` a jen přes HTTPS reverzní proxy (nginx/Caddy) – nevystavujte Flask vývojový server přímo na internet; pro ostrý provoz `gunicorn app:app`.

## Role
- **Montér:** deník, fotky, zápis materiálu, procenta pokroku. Nevidí ceny ani doklady.
- **Admin:** vše + zákazníci, ceník, doklady, uživatelé, údaje firmy.

## Doklady
Číslování `N`/`F`/`Z` + rok + pořadí. DPH režimy: CZ 21 %, DE 19 %, přenesená daňová povinnost / reverse charge. Doklad pro německého zákazníka se tiskne německy. Tisk → „Uložit jako PDF“ v prohlížeči.
**Před ostrým použitím nechte texty a DPH režimy zkontrolovat účetní/daňovým poradcem.**
