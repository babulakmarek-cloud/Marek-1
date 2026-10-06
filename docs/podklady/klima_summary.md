# Klimatizace/VZT Mondelez Werk 2 – shrnutí podkladů

**Výstup:** /home/user/Marek-1/vystupy/Klimaanlagen_Werk2.xlsx. List „Anlagen“ má 68 řádků: 52 Klima/Lüftung, 12 DKG a 4 záznamy, které jsou jen v RLT. List „Kontrola“ má 144 rozporů. List „Zdroje“ popisuje vstupy. Texty z PDF jsou ve scratchpad/docs_klima/.

## 0) Zdroje a jak se k sobě mají
- **KlimaanlagenPlan-DM.pdf** (7 stran) je originál, ze kterého ostatní soubory vycházejí:
  - S.1 schéma budovy: věž KH4 (3.–6.OG), KG–2.OG s FW, značka KH2 v EG/KG vpravo a Sprinklerzentrale. Modré značky nemají čísla, ručně jsem jich napočítal asi 52.
  - S.3–4 Klima/Lüftung a S.5 DKG: obsahují křížky (x) i filtry s barvami typu.
  - S.6 souhrn průtoků. S.7 sloupec „Baujahr“ je prázdný. S.2 je prázdná.
- **Übersicht.xlsx/.pdf** je přepis DM. PDF je tisk tohoto xlsx: vznikl z něj (Distiller) a má stejná data. Filtry v něm chybí, kromě DKG.
- **Engineering.xlsx** cituje „PDF S.3–6“, tedy DM. Přidává sloupec Bereich, min/max průtoků a Filterregister. Odhad energie (SFP 1800 W/(m³/s), 4000 h/a) je vlastní předpoklad autora, ne údaj ze zdroje.
- **Kennzahlen_RLT-Anlagen.xlsx** má jiné, vlastní číslování. Tabelle1–3 = Werk 2, záznamy 1–48 (41–48 v sekci „DKG (Umluft-Anlagen)“). Tabelle4 = Sozialgebäude, záznamy 49–53. Celkem 53 záznamů, ne „106–111“.
  - Rozměr listů je A:DW, tedy 127 sloupců (ne 119) a 108–113 řádků. Jeden záznam zabírá blok 5 řádků.
  - Funkce (Befeucht., Kühl., Hzng., WRG, Klappen, Aufschaltung) jsou zakreslené barevnými elipsami, ne hodnotami v buňkách. Zelená = vorhanden, červená = nicht vorhanden. Ke sloupcům jsem je přiřadil podle polohy v drawing*.xml.
  - Navíc obsahuje: RAM/Aufschaltung-Nr., žádanou teplotu a vlhkost (ZL/Raum/ABL) a filtry po třídách ISO (DEMFI ePM1-60 %, ISO Coarse 30/45 %).
- **Klimakarte.pdf** neobsahuje žádné jednotky (viz bod 3).

## 1) Jednotky
- **Klima/Lüftung:** Nr. 1–47 plus 3.1, 18.1, 19.1, 27.1 a 41.1, tedy 52 řádků. Stejný počet je v Ü, Eng i na DM S.6. Podřádky x.1 mají jen filtry, průtok nemají.
- **Deckenkühlgeräte:** 12 ve všech třech zdrojích. Uvádějí jen oběhový vzduch 1./2. stupně, např. Bindler 3 84 600/133 200 m³/h.
- **Budovy:**
  - KH2 je výslovně uvedeno jen u Nr. 27 a 27.1 (Steuerwarte, Looszuluft, EG „M“).
  - Nr. 28–32 jsou v Sozialbau, Nr. 7–8 v OPM.1.
  - U ostatních jednotek budovu KH2/KH4 ze souborů přiřadit nelze. K dispozici je jen podlaží a sekce B/C/D/E/F/M z názvu.
- **Podlaží:** Většina jednotek je ve 2.OG (Nr. 5, 11–25, 38). Dále: KG (1–3.1, 26), EG (6, 27, 28, 34), 1.OG (9, 10, 47), 3.OG (37), 4.OG (36), 5.OG (33, 39–41.1). Ve 6.OG není žádná jednotka.
- **Průtoky:** od 777 m³/h (Nr. 27) po 103 800/91 500 m³/h (Nr. 5 Conchen-Nord). Dále 70 870 (16), 61 500 (13), 55 000 (24), 47 000 (6).
- **Funkce podle DM (originál):** Heizung 35 jednotek, Kühlung 28, Befeuchtung 11, WRG jen 6 (7, 8, 26, 28, 30, 31). Bez ohřevu i chlazení je 12 řádků: 2, 4, 34, 35, 36, 45, 46 a podřádky x.1.
- **Teploty:** jen žádané hodnoty prostoru (15–32 °C), vlhkost 40–55 % rF.
- **Filtry:** typy a rozměry (FP65/FP75, EU6/EU7, 592x592 …). Nová třída H13 platí pro Zucker- a Milchpulvergebläse (DM S.5).
- **Chybí ve všech souborech:** výkony ohřívačů a chladičů (kW), médium, teploty vody, údaje o ventilátorech (kW, typ). Je tam jen údaj „Flachriemen“ (plochý řemen) u 9 jednotek.

## 2) Topné okruhy a chlad
- Hladiny „Heiz Wasser +90 Klima V (lüftung)“ / „+70 Klima R“ se v žádném z těchto 6 souborů nevyskytují. Hledal jsem v textu i ve výkresech.
- Napojení jednotek na rozdělovače, okruhy ani zdroj chladu (KW/medium) tu není. Ze souborů je jen vidět, které jednotky mají ohřívač (35) nebo chladič (28), viz výše.
- DKG mají jen značku „Kühlung“, bez média.

## 3) Klimakarte
- Jde o export klimatické mapy (DIN/TS 12831-1, DIN 4710) pro PSČ 79539 Lörrach. Metadata PDF obsahují titul „Bestandsaufnahme_Heizung_Mondelez_Loerrach.xlsx“.
- Hodnoty: Norm-Außentemperatur −10 °C, roční průměr 10,8 °C, průměr topného období 2,2 °C, nadmořská výška 282 m, klimatická zóna 12.
- Heizgradtage: 2 443 Kd (161 dní) při topné hranici 10 °C, 3 064 Kd (241 dní) při 15 °C. Tabulky jsou po měsících.
- Je to vstup pro výpočet tepelných ztrát a energie, ne seznam zařízení.

## 4) Rozdíly mezi zdroji (vše v listu Kontrola)
- **Křížky funkcí:**
  - Übersicht se liší od DM u 33 jednotek, Engineering u 38. Křížky jsou posunuté nebo stlačené do sousedních sloupců.
  - Příklady: u Nr. 1 je podle DM jen Heizung (Ü: Kühl+WRG, Eng: vše Ja). U Nr. 5 Kühl + Flachriemen (Ü: všech 5).
  - WRG je v Ü/Eng uvedené často, v DM jen u 6 jednotek. Ke křížkům v obou Excelech nemám důvěru.
- **Übersicht.xlsx:**
  - U Nr. 1 chybí Zuluft 7 800 (Eng i DM ho mají).
  - Hlavička má 20 sloupců (A–T), data sahají do sloupce U. Vlhkost 0,55 je pod hlavičkou „Autom. Absch.“.
  - Sloupec „Temperatur Zuluft“ (P) obsahuje ve skutečnosti teplotu prostoru.
  - Standortübersicht: součet 55 ≠ 52 řádků. Nr. 36 a 40 jsou zároveň ve 2.OG, 29 je i v EG i v Sozialbau. 18.1, 19.1 a 42–46 nejsou zařazené. Ve 2.OG je uvedeno 22 položek, rozpis jich má 19.
- **Engineering.xlsx:** Nr. 2 má 19° (v DM patří k Nr. 3). Aufschaltung je „0.8“/„0.7“ i v DM (pravděpodobně 08/07).
- **DM S.6 vs S.3:**
  - Nr. 9 je na S.6 „Nussrösterei“, na S.3 „Kabaverpackung“.
  - U Nr. 7/8 je na S.6 Zuluft 8 000 / Abluft 24 000, na S.3 Zuluft 8 000/24 000 / Abluft 8 000.
  - U Nr. 39 je na S.6 Zuluft „---“ (S.3: 6 000–12 000).
- **RLT vs Plan:**
  - Přiřazení podle názvu, průtoku a Aufsch-Nr. jsem udělal u 49 z 53 záznamů. U 10 z nich je nejisté (v listu Anlagen jsou označené „?“).
  - Neshody průtoků: RLT 5 Primärluft D 27 000 vs Nr. 21 12 150–24 300; RLT 26 „3x LUWA“ 3×12 900 vs „4 Luwa“ 47 000; RLT 34 „3x Umluft je 15 000“ vs „2x je 24 500“; RLT 36 1 500 vs Nr. 9 15 000; RLT 31 Nußkeller 8 600 vs Nr. 3 13 100.
  - OPM Abluft je v RLT 6 500, v Plan 8 000.
  - RLT 16 a 19 jsou duplicitní „Walzensaal-Süd“. Walzensaal-Nord (Nr. 13) v RLT chybí.
  - Aufsch-Nr. se liší u R&D (34/35/36 vs 35/36/34) a u Formenwaschanlage (24 vs 14).
- **Jen v RLT:** W&D 5 (15 000), 2x Büro HR-Bereich (800), Lüftung Kugelmühlen ECRU (12 000/6 000, WINCC).
- **Jen v Plan (bez RLT):** 10, 13, 22, 45, 46, 47 a podřádky x.1. DKG 1, 4, 5, 7 a 12 nemají záznam v RLT.

## 5) Vstup pro mh-BIM (KanSYS/RohrSYS) a co chybí
- **Použitelné:**
  - Pro KanSYS: seznam a označení jednotek (Nr. + RLT/RAM-Nr.), průtoky přívodu, odvodu a oběhového vzduchu, podlaží/sekce, žádané teploty a vlhkosti, filtry (rozměry, počty, třídy) a klapky.
  - Pro RohrSYS: které jednotky mají ohřívač nebo chladič (podle DM).
- **Chybí:**
  - Výkony registrů (kW) a teplotní spády (+90/+70 apod.).
  - Médium (ohřívací voda, pára, chladicí voda), DN a umístění přípojek.
  - Příslušnost k okruhům a rozdělovačům, poloha jednotek ve výkresu (souřadnice/místnost), KH2/KH4 u jednotlivých jednotek.
  - Výkon a typ ventilátorů, rok výroby (DM S.7 prázdný).
- Tato data bude potřeba získat ze schématu topení / seznamu rozdělovačů nebo zaměřením.

## Ověření údaje z Notionu
- **„47 zařízení (Anlage 1–47)“:** sedí na hlavní čísla. S podřádky x.1 je to 52 řádků. RLT má jiných 53 záznamů.
- **„12 stropních chladicích zařízení“:** sedí (Ü, Eng i DM). RLT má v sekci DKG jen 8 záznamů.
- **„KH4 + KH2“:** popisky jsou jen na schématu DM S.1. U jednotlivých jednotek je KH2 uvedeno jen u 27 a 27.1.
- **„KG až 6.OG“:** schéma tyto podlaží zobrazuje, ale ve 6.OG je 0 jednotek.
