# Návod: termoelektrický generátor (TEG) z půdy nebo od kamen

*Zpracováno ze scénáře videa „Na půdě je v létě přes 50 °C…“ (kanál Stavba jinak). Přepis byl poškozený automatickým rozpoznáním řeči, proto jsou názvy, jednotky a čísla sjednocená a opravená (viz kapitola 2).*

## 1. O co jde
Termoelektrický generátor (TEG) je keramická destička 40 × 40 mm z teluridu bismutu. Pokud je jedna strana horká a druhá studená, vyrábí stejnosměrné napětí (Seebeckův jev, objeven 1821). Pracuje tiše, bez pohyblivých dílů a bez slunce, takže jde využít teplý plech střechy, půdu nebo kouřovod kamen.

**Nejdůležitější pravidlo:** teplo samo nic nedává, rozhoduje **rozdíl teplot (ΔT)**. Bez chlazení studené strany výkon spadne k nule.

## 2. Realistická očekávání (důležité – opravy oproti videu)
Ve scénáři jsou výkony „3–7 W na modul“ a „36–48 W z 12 modulů“. Při reálném ΔT 40–60 °C to **nesedí s katalogy běžných modulů**:

| Modul | Údaj | Zdroj |
|---|---|---|
| SP1848-27145 (levný, 40×40) | ΔT 20 °C: 0,97 V / 225 mA; ΔT 40 °C: 1,8 V / 368 mA | [katalogová data prodejce](https://littlebirdelectronics.com.au/products/thermoelectric-generator-teg-module-sp1848-27145-40-x-40mm.md) |
| European Thermodynamics GM200-161-12-40 | max. 1,49 W, 9,96 V (při velkém ΔT, horká strana stovky °C) | [RS](https://uk.rs-online.com/web/p/peltier-modules/7650025?gb=s) |

Z toho plyne:
- Při ΔT ≈ 40 °C dá levný modul orientačně **0,3–0,6 W**, ne 3–7 W. 12 modulů tedy dá spíš **4–8 W**, při ΔT 60 °C možná 10 W (výkon roste zhruba s kvadrátem ΔT).
- Napětí 4 modulů v sérii je při ΔT 40 °C kolem **7 V**, ne 12 V. Regulátor proto musí zvládat nízký vstup (od cca 3–5 V) nebo použijte step-up měnič.
- Účinnost 5–8 % je u teluridu bismutu horní odhad pro velké ΔT; při malých rozdílech je výrazně nižší.
- V tvrzení o Voyageru jsou generátory s Si-Ge, ne jen telurid bismutu. Údaje o 17 klimatických zónách, 1 % degradaci za 10 let a konkrétním kutilovi z Arizony nejsou ověřené – berte je jako ilustraci, ne jako záruku.
- Návratnost „3–4 roky“ ze scénáře při ~5 W průměru neplatí; ber to jako **pokusný projekt / napájení čidel a LED**, ne jako úsporu.

Dobrý cíl: LED osvětlení půdy, bezdrátová čidla vlhkosti a teploty v krovu, nabíječka telefonu u kamen, rádio.

## 3. Seznam dílů (varianta 12 modulů, 3 řetězce × 4 moduly)
Původní ceny z videa jsou v USD; orientační ceny v CZK si ověřte u prodejce.

| Díl | Počet | Poznámka | Cena z videa |
|---|---|---|---|
| TEG modul 40×40 mm, min. 150 °C (např. SP1848-27145) | 12 | **Generátorový** typ, ne běžný chladicí Peltier TEC1-12706 (ten má max. ~80–100 °C a spoj uvnitř degraduje) | 68 USD |
| Hliníkový žebrovaný chladič | 24 (2 na modul) | Může být ze starého PC; studená strana musí být velká | 42 USD |
| Teplovodivá pasta do vysokých teplot | 1 tuba | Např. Arctic Silver / jiná značková | 9 USD |
| Regulátor / step-up měnič pro nízké vstupní napětí | 1 | Běžný solární MPPT (vstup 18–50 V) nepůjde; hledejte vstup od ~3–5 V | 28 USD |
| Měděný lankový vodič 3,5 mm² (12 AWG) + očkové konektory | cívka + sáček | Nad 20 m trasy zvolte 5 mm² (10 AWG) | 31 USD |
| Rozvodná krabice IP + nerezový spojovací materiál | 1 sada | | 22 USD |
| Autobaterie / AGM 12 V, 35 Ah | 1 | Volitelné (lze použít starou) | 78 USD |
| Pojistka 15 A (automobilová) + uzemnění | 1 | Ochrana před přepětím | < 5 USD |
| Překližka 12 mm, cca 60 × 45 cm | 1 | Montážní deska | – |
| Hliníkové úhelníky, distanční sloupky, ohebná hliníková hadice Ø 100 mm | dle potřeby | Přívod studeného vzduchu | – |
| Multimetr / wattmetr, 2 teploměry | – | Měření | – |

Celkem podle videa 278 USD (bez baterie cca 200 USD). Samotné moduly jsou jen malá část.

## 4. Postup stavby

### Krok 1 – příprava modulů (cca 40 min)
1. Položte desku na rovný stůl, pracujte čistě a bez prachu.
2. Na **teplou** stranu modulu naneste **tenký, průsvitný** film pasty (žiletkou nebo starou kartou). Pasta není lepidlo, jen vyplňuje mikroskopické mezery. Je-li vrstva bílá jako poleva, setřete a opakujte.
3. Přitlačte chladič (nebo hliníkovou desku) a držte 10 s.
4. Otočte, totéž na **studené** straně.
5. Opakujte pro všech 12 modulů.

### Krok 2 – sestavení pole
1. Uspořádejte moduly do mřížky 3 × 4 na překližce cca 60 × 45 cm.
2. Přichyťte distančními sloupky a šrouby, dotažení cca **2,8 Nm**. Nepřetahujte, keramika praská.
3. **Zapojení bez pájení:** 4 moduly sériově = 1 řetězec; 3 řetězce paralelně na společné + a − svorky v rozvodné krabici (očka a šrouby). Pozor na polaritu (červený +, černý −).

### Krok 3 – montáž na půdě (cca 3 h)
1. Horké chladiče přitiskněte **naplocho** k bednění / spodní straně plechové krytiny na **jižní straně**; upevněte hliníkovými úhelníky ke krokvím.
2. Studená strana míří **dolů** do prostoru půdy. Žebra svisle nebo do proudu vzduchu, nikdy tak, aby se v nich držel horký vzduch. Desku nakloňte alespoň 30° od vodorovné.
3. Vedete-li studený vzduch, přiveďte ohebnou hadici Ø 100 mm od spodního větracího otvoru u okapu (nebo ze sklepa, severního otvoru) ke krytu kolem studených žeber.
4. Půda musí být **větraná** (otvory u okapu a hřebene), jinak se vyrovná teplota obou stran a výkon klesne.
5. Vodič veďte z krabice podél trámu dolů do garáže. Trasa do 20 m: 3,5 mm², delší: 5 mm².
6. Do plusového vodiče mezi krabici a regulátor dejte pojistku 15 A; krabici uzemněte.
7. Zapojte na regulátor a z něj na baterii.

### Krok 4 – měření a výchozí hodnoty
Zapište si (datum, hodina, venkovní teplota):
- napětí a proud (multimetr) a vypočtený výkon (W = V × A),
- teplotu bednění (teplá strana),
- teplotu vzduchu u studených žeber,
- ΔT.

Ta čtyři čísla jsou vaše výchozí hodnota, každé vylepšení porovnávejte s ní.

## 5. Zimní varianta u kamen (kouřovod)
Plášť komína nebo kouřovodu má klidně 150 °C, pár metrů dál je pár stupňů. Rozdíl je větší než na letní půdě a běží, když topíte, tedy v nejtemnějších měsících.
- Modul **nikdy přímo na plech** u kamen. Použijte **hliníkový mezikus**, aby horká strana nepřesáhla limit modulu (≈ 150 °C u SP1848; uvádějte-li váš modul 300 °F = 149 °C, platí totéž).
- Studená strana: velký chladič ve vzduchu místnosti.
- Půdní pole a kamna lze spojit na jednu baterii přes **diody** (aby se větve nevybíjely navzájem).
- Pozor na požární bezpečnost: nic hořlavého u kouřovodu, žádné zásahy do kamen bez revizního technika.

## 6. Vylepšení
- **Vodní chlazení studené strany** (sud s dešťovkou, měděný vodní blok, malé čerpadlo spouštěné termostatem) – může zvýšit ΔT o desítky °C, počítejte ale spotřebu čerpadla.
- Sériové zapojení zvyšuje napětí, paralelní proud; ladění vždy podle regulátoru.
- Rozšíření: druhá banka potřebuje **vlastní přívod studeného vzduchu** (jinak se zahřívá společný prostor a ΔT klesá).

## 7. Časté chyby
1. Příliš silná vrstva pasty.
2. Žebra chladiče orientovaná tak, že se v nich drží horký vzduch.
3. Tenký vodič na dlouhé trase (při 12 V ztráty přes 15 %).
4. Zavřená, nevětraná půda.
5. Běžný solární regulátor (nízké vstupní napětí ho „neprobudí“).
6. Příliš vysoká teplota na modulu (nad 150 °C u levných TEG).
7. Očekávání, že to nahradí fotovoltaiku. TEG je doplněk pro noc a pro místa bez kabelu.

## 8. Kontakty a kde objednat v ČR
Ceny a dostupnost se mění, **před objednávkou si je ověřte**. Přímý odkaz na SP1848-27145 v ČR, který jsem našel: [Kaufland.cz – SP1848 27145 TEG modul (cca 322 Kč)](https://www.kaufland.cz/product/512123341/).

| Co | Kde | Poznámka |
|---|---|---|
| TEG moduly SP1848-27145 (40×40 mm) | [Kaufland.cz](https://www.kaufland.cz/product/512123341/) | Prodejce z marketplace, doba dodání ověřit |
| TEG moduly European Thermodynamics (GM200-161-12-40 apod.) | [RS Components](https://cz.rs-online.com) – hledat „Seebeck Effect Module“ (kód 7650025) | Kvalitní, dražší, vyšší výkon |
| TEG a Peltier moduly, chladiče, vodiče, pojistky | [GM electronic](https://www.gme.cz), [TME](https://www.tme.eu/cz), [Hadex](https://www.hadex.cz), [Conrad.cz](https://www.conrad.cz) | Vyhledat „termoelektrický generátor“, „Seebeck“, „TEG“; dostupnost jsem neověřoval |
| Moduly, chladiče, step-up měniče | [AliExpress](https://www.aliexpress.com) | Levné, dodání týdny; hledat „SP1848-27145 TEG“ |
| Regulátory/step-up měniče pro 3–20 V DC | výše uvedené e-shopy, hledat „MPPT 5 V“, „DC-DC step-up 3–30 V“ | Pro malé větrné turbíny nebo nízkonapěťové zdroje |
| Hliníková hadice, úhelníky, překližka, vodiče, pojistky | Hornbach, Bauhaus, OBI, Hobby market | |

Telefonní čísla a e-maily prodejců jsem záměrně nevymýšlel; najdete je v kontaktech jednotlivých e-shopů.

## 9. Bezpečnost
- Pracujte na půdě opatrně (žebřík, horko, hrozí přehřátí). Plech může mít přes 60 °C.
- 12 V DC je z hlediska úrazu nízké, ale baterie umí dát velký zkratový proud – vždy pojistka.
- Pole je tvořeno 12 V instalací; nejde o síťové napětí. Jakékoliv připojení do domácí sítě 230 V patří **elektrikáři s oprávněním**.
- U kamen a komína dodržujte bezpečné vzdálenosti a požární předpisy.

## 10. Doporučení pro první pokus
Začněte levně: **1–2 moduly**, chladič, multimetr a LED. Změřte ΔT a reálné watty na své půdě a až potom kupte všech 12.
