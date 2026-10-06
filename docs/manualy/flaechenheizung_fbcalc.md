# Manuál mh-software "Flächenheizung" (modul mh-FBCALC / FbCALC, mh-BIM 8), 94 s.
Čísla stran = tištěné číslo = číslo strany PDF. Zdroj: pdftotext (text), obrázky nečteny.
Pozor: manuál (jen "Flächenheizung") je referenční příručka masek FbCALC; o importu DWG/DXF, o rozdělovačích a o atributech nemá téměř nic (viz bod 6).

## 1. Účel a datový model
- Návrh podlahového vytápění dle DIN EN 1264; stropní a stěnové přibližně také (s. 6). Rozdělovač (Verteiler) a "plošné chlazení" v tomto manuálu nejsou popsány jako funkce; chlazení se v textu nevyskytuje.
- Heizlast z mh-EN12831 je užitečná, ne nutná; s ní jde návrh téměř automaticky (s. 6).
- Společný datový základ všech modulů mh (s. 10). Každý modul má vlastní výpočetní jádro, ostatní ho nespouštějí; změna v tepelné ztrátě se projeví až po nové kalkulaci/Aktualisierung (s. 10-11).
- Data místnosti: (a) Raumbuch = společné údaje (číslo, název, stavební prvky), (b) Anlagen-Daten = specifické pro modul (u FbCALC: navržené plochy, data Aufenthalts- a Randzone) (s. 67-68). Mazání: celá místnost, nebo jen data modulu (s. 68, 70).
- Místnost je v každém modulu "aktivní" nebo šedá (zobrazená, ale nezapočtená); aktivace tlačítkem "Aktivieren" nebo inicializací (s. 69).
- Hierarchie: projekt > Anlage (modul, např. FbCALC) > budova/stavební díl > podlaží > byt > místnost; číslo místnosti má 4 části = uzly stromu (s. 67). Uvnitř místnosti: Heizzone (Zone) > Aufenthaltszone a/nebo Randzone > Heizkreise (s. 79, 83-86).
- Hodnoty se ukládají automaticky, není příkaz Uložit (s. 7).
- Heizzonen-Gruppen = katalog předvoleb (výrobce, produkt, tv, spreizung, tFB); vazba je jen kopírováním (F2/dvojklik), ne reference (s. 58).
- Katalogy: Hersteller-Katalog (výrobce > produktové řady > rozteče trubek) je uložen mimo projekt; při první Anlage se kopíruje do projektu (s. 17, 55).

## 2. Postup práce
A) Rychlý návrh po výpočtu tepelných ztrát (s. 7-8):
 1. Projektdaten: přirážka k tepelné ztrátě atd. 2. Initialisierung: podmínky pro každý typ místnosti, sloupec A/R-Zone (A / R / A+R), max. podíl Randzone. 3. Kontrola výsledků v záložce Flächenheizung, chyby přes seznam chyb. 4. Opakovat pro všechny místnosti. 5. Záložky Raumliste a Flächenheizungsliste (přehled). 6. Tisk/náhled. Doporučeno zóny po úpravě fixovat (Fix), aby se výkon a rozteč neměnily (s. 8).
 Detail inicializace 14 kroků: s. 75-76 (rozsah, mazání už navržených zón, výrobce/produkt, tv, krytí su, A/R, max. teplota podlahy a spreizung, tlačítko Initialisieren; místnosti bez zbytkového výkonu u radiátorů se vynechají).
B) Návrh nezávislý na tepelných ztrátách (s. 8-9): Gebäude-Schnelldefinition (otevře se, pokud budova ještě neexistuje) > Gebäudestruktur > Projektdaten (Initialisierung zde nemá smysl) > vytvořit místnost (tlačítko Neu, krátké označení bytu a místnosti) > vyplnit hlavičku a zóny v záložce Flächenheizung > Raumliste, Flächenheizungsliste > tisk. Ruční postup polí: s. 80-81.
C) S plochami z RohrSYS (s. 9): předpoklad bezchybně zadaná budova v RaumGEO; Projektdaten + Initialisierung (předvolby); v RohrSYS se graficky kreslí Aufenthaltszonen, Randzonen a Sperrflächen a topné okruhy se navrhují tam; v FbCALC pak jen seznamy a tisk. Videa: "Heizflächen zeichnen, Verteiler konstruieren und anbinden, Heizflächen berechnen" (s. 79).
D) Kombinace s radiátory (s. 9-10): dvě varianty (radiátory většina + podlahovka zbytek; nebo naopak); tlačítko "init. Raum"; po dokončení v HkCALC "Aktualisierung" (fixovat a přepočítat).
E) Aktualisierung (s. 76-77): změna tepelné ztráty přepočte stávající zóny, počet zón se nemění; volby Fixierung beachten / aufheben / fixieren und berechnen (módy q, Q, q+VA, Q+VA, VA+dt, VA+tfb).
F) Globale Änderung (s. 77-78): hromadná změna (výrobce, tv, režim, krytí, skladba, systémové vestavby); doporučeno předem zálohovat projekt kopií. "opt. Vorlauftemperatur" (s. 78).
G) Kontrola: záložka Kennlinienfeld (s. 88-91), Meldungen: Fehler musí být opraveny, Hinweise lze (s. 93). Výsledky vždy ověřit vlastní odpovědností (s. 38).

## 3. Vstupy, import/export
- Místnosti: z Heizlast/RaumGEO (Q-Raum, Norm-Innentemperatur, plocha po zaškrtnutí voleb; s. 80) nebo ručně (Q-Raum, teplota, plocha, Q-Extern; s. 80). Q-FH-Bedarf = Q-Raum minus radiátory a externí zdroj (s. 83). "Anzahl gleicher Räume" ovlivňuje výkaz materiálu (s. 83).
- Gebäudestruktur: OKRF nad terénem, výška podlaží, světlá výška; volitelně výška skladby podlahy, tloušťka stropu, parapet (jen pro popisky; s. 53-54, 71). Schnelldefinition: max. 3znakové označení budovy (s. 71). Změna struktury neovlivní už vytvořené místnosti (s. 55, 73).
- Podlahová skladba (záložka Schichtaufbau, s. 87-88): z Raumbuchu (včetně teploty sousední místnosti) nebo ručně z Bauteilkatalogu; vrstvy se typují B (Belag), LV (Lastverteilschicht), D (Dämmung), WL (Wärmeleiteinrichtung, jen systém typu B), U (tragender Untergrund). Tepelný odpor krytiny: "dle skladby" nebo "dle normy korigovat" (min. 0,1 m²K/W). Krytí su. Výchozí skladba v Projektdaten pro případ, že ji nelze převzít (s. 74). Skladbu nelze fixovat (s. 81).
- Hersteller-Katalog (s. 55-58): typ systému (podlaha/stěna/strop), typ A/B/C dle DIN EN 1264, činitel pro zvláštní konstrukce, data trubky (jmenovitý a vnější průměr, stěna, lambda, drsnost, max. délka role 120/240 m, držáky/m), ochranný obal, noppen, Wärmeleiteinrichtungen, Kennlinienfeld; rozteče trubek -> orientační délka trubky na m².
- Heizkreise/Rozdělovače: Zuleitung = trubka od rozdělovače k ploše místnosti, délka včetně zpátečky; slouží jen pro celkovou délku (výkaz) a tlakovou ztrátu, tepelná ztráta přívodu se NEzapočítá (kompenzovat nižší tv) (s. 81-82, 85-86). Vorschlagswert délky přívodu v Projektdaten (s. 74); max. tlaková ztráta okruhu vč. přívodu (s. 73). Okruhy: Nr., Q, L, A, m, w, Δp (s. 86); v režimu RohrSYS: RC-Id = číslo objektu topné plochy (s. 85), délka přívodu se bere po první T-kus (zpravidla rozdělovací lišta) (s. 85-86). Ruční úprava počtu/délky okruhů volbou "Manuell bearbeiten", tlačítko "Nummerieren" (ne v režimu RohrSYS; s. 84).
- Import/export: v manuálu NENÍ popsán import ani export DWG/DXF pro FbCALC. Jediné zmínky: výstup tisku do PDF nebo TXT (TAB-oddělený, čitelný v Excelu) (s. 51); barvy/layery pro PDF a DWG export a Darstellungs-Sets patří do Vorgabe-Projektů (s. 16); komprimace projektu (.mhz8) zahrnuje importované půdorysy v interním formátu .dxb, ne původní DXF/DWG (s. 35). IFC jen v seznamu funkcí Basis/Plus licence (s. 20-22).
- Výstupy: Raumliste (tL, QRaum, Q-FB, QExtern, QHK, QDiff; s. 91), Flächenheizungsliste (záložky Heizzone, Aufenthaltszone, Randzone, Heizkreis; chybné zóny červeně; s. 91-92), tisk/PDF/TXT (s. 50-51).
- Rohrnetz (RohrSYS) čerpá výsledky FbCALC bez jejich aktualizace; okruhy zobrazuje jako symbol topné plochy, ne skutečné trubky (s. 11).

## 4. Konvence názvů a atributů
- Název projektu i Anlage: smysluplný, co nejkratší, bez speciálních znaků (s. 14). Složka projektu .mh8 (plná verze) / .mhb8 (Basis); komprimovaný .mhz8 (s. 14, 24, 34). Přejmenování/kopírování jen přes mh-Projektverwaltung, nikdy v průzkumníku (s. 14, 24). Cesta přes písmeno disku, ne UNC; cloud (OneDrive, SharePoint) při práci nepřípustný (s. 14).
- Raumnummer ze 4 částí (uzly stromu pod projektem), tvar "Kurzbezeichnung:Langbezeichnung" odděleno dvojtečkou; změna Kurzbezeichnung se promítne do všech modulů (s. 67, 70). Přesný význam 4 částí je v obrázku (nečteno).
- Zkratky polí: Zone, Grp, Hst/Herst, Prod, Modus, QSoll/QIst, qSoll/qIst, VA (Verlegeabstand), tv, Theta F,m, Sigma, dT, Fix, su, tFB (s. 75, 83-84). Režim Zone "RohrSYS" (s. 84-85).
- Podlaží: krátké označení např. "4.OG" (s. 54).

## 5. Co lze připravit mimo software
- Podle manuálu (nepřímo): podklady jako čísla a tabulky, tj. Q-Raum, teploty, plochy, skladby podlah (vrstvy s tloušťkou, lambda, typ B/LV/D/WL/U), data výrobce (rozteče, trubka, Kennlinie), délky přívodů, rozdělení do zón/skupin. Žádná šablona pro hromadný import není v manuálu popsána.
- Připravit lze: výběr výrobce a produktu, předvolby podle typů místností (tFB, spreizung, tv, krytí), schéma pojmenování podlaží/bytů/místností, Vorgabe-Projekt (hlavička tisku, logo 1:1 nebo hlavička 1:10, šablony popisků, katalogy) (s. 15-17, 52).
- Zkopírování tabulkových řádků přes schránku mezi dokumenty stejné struktury (s. 41).

## 6. Otevřené otázky
1. Import/export DWG/DXF do/z FbCALC: v manuálu není. Kresba ploch se dělá v RohrSYS (příslušný manuál nemáme), DXF/DWG import půdorysu je zřejmě v RaumGEO/RohrSYS. Potřebujeme manuál RaumGEO/RohrSYS.
2. Rozdělovač: není popsán objekt rozdělovače ani přiřazení okruhů k rozdělovači v FbCALC; jen video "Verteiler konstruieren und anbinden" (s. 79) a "neues Verteiler-Objekt" v Plus licenci RohrSYS (s. 22). Je nutné prověřit.
3. Plošné chlazení: modul se v textu věnuje jen vytápění; funkce chlazení neověřena.
4. Význam 4 částí čísla místnosti (s. 67) a obrázky formulářů (s. 79-90): nečteno, v případě potřeby doplnit z obrázků.
5. Vztah zón/okruhů k pojmenování atributů při IFC exportu (mhData, s. 23): detaily nejsou.
6. Plus vs. Basis licence: pro kreslení ploch v RohrSYS je uvedeno jako Plus ("Einzeichnen und Berechnen von Heizflächen", s. 22); ověřit licenci.
