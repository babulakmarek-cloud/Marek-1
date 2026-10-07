# Návod: LAN síť přes internet (všechny varianty)

Cíl: propojit počítače z různých míst tak, aby se chovaly, jako by byly v jedné místní síti (hry po LAN, sdílení souborů, vzdálená plocha, domácí server).

## Která varianta se hodí?

| Varianta | Obtížnost | Cena | Vlastní server | Hry po LAN (broadcast) | Vhodné pro |
|---|---|---|---|---|---|
| ZeroTier | nízká | zdarma do 25 zařízení | ne | ano (L2 síť) | hry, kamarádi, rychlé spojení |
| Tailscale | nejnižší | zdarma pro osobní použití | ne | ne (jen IP) | vzdálený přístup, domácí server |
| Radmin VPN | nejnižší | zdarma | ne | ano | hry na Windows |
| Hamachi | nízká | zdarma do 5 zařízení | ne | ano | hry, malé skupiny |
| WireGuard | střední | zdarma | ano | ne (jen IP) | rychlá a trvalá vlastní VPN |
| OpenVPN | vyšší | zdarma | ano | ano (režim TAP) | maximální kompatibilita |

Obecné pravidlo: **na hry použijte ZeroTier nebo Radmin VPN, na vzdálený přístup Tailscale nebo WireGuard**.

---

## 1. ZeroTier

1. Zaregistrujte se na **my.zerotier.com**.
2. Klikněte na **Create A Network**. Vznikne 16místné **Network ID**.
3. (Volitelně) v nastavení sítě zvolte rozsah IP, např. `10.147.17.0/24`. Nechte **Access Control: Private**.
4. Na každém počítači nainstalujte klienta ze **zerotier.com/download**.
   - Linux: `curl -s https://install.zerotier.com | sudo bash`
5. Připojte se k síti:
   - Windows/macOS: ikona ZeroTier, **Join Network**, zadejte Network ID.
   - Linux: `sudo zerotier-cli join <NETWORK_ID>`
6. V konzoli my.zerotier.com zaškrtněte u každého zařízení **Auth?**.
7. Zařízení dostane IP (např. `10.147.17.5`). Zkontrolujte: `ping 10.147.17.x`.
8. Ve Windows nastavte síť ZeroTier jako **Soukromá** (kvůli sdílení a objevování zařízení).

Řešení problémů: pokud je odezva vysoká, spojení jde přes relay. Pomůže povolit UDP 9993 v routeru a firewallu.

---

## 2. Tailscale

1. Nainstalujte ze **tailscale.com/download** na všechna zařízení.
   - Linux: `curl -fsSL https://tailscale.com/install.sh | sh`
2. Spusťte a přihlaste se (Google/Microsoft/GitHub):
   - Linux: `sudo tailscale up`
   - Windows/macOS: ikona v liště, **Log in**.
3. Pro ostatní lidi: v admin konzoli (**login.tailscale.com**) použijte **Share** nebo pozvěte uživatele. Nebo se přihlaste všude stejným účtem.
4. Zařízení se vidí na adresách `100.x.y.z` a podle jména (MagicDNS), např. `ping muj-pc`.
5. Zjištění adres: `tailscale status`.

Volitelně:
- **Subnet router** (zpřístupnění celé domácí sítě): `sudo tailscale up --advertise-routes=192.168.1.0/24`, pak povolte trasu v admin konzoli.
- **Exit node** (veškerý provoz přes jedno zařízení): `sudo tailscale up --advertise-exit-node`.

---

## 3. Radmin VPN (Windows, zdarma)

1. Stáhněte z **radmin-vpn.com** a nainstalujte na všechny počítače.
2. Na jednom počítači: **Síť > Vytvořit síť**, zadejte název a heslo.
3. Ostatní: **Síť > Připojit se k existující síti**, zadejte stejný název a heslo.
4. Každý dostane IP z rozsahu `26.x.x.x`. Ve hře použijte LAN režim nebo zadejte IP hostitele.

---

## 4. Hamachi (LogMeIn)

1. Stáhněte z **vpn.net**, nainstalujte a vytvořte účet.
2. **Síť > Vytvořit novou síť**, zadejte ID a heslo.
3. Ostatní zvolí **Připojit se k existující síti**.
4. IP adresy jsou z rozsahu `25.x.x.x`. Zdarma je limit 5 zařízení.

---

## 5. WireGuard (vlastní VPN server)

### Požadavky
- Server s veřejně dostupnou IP (VPS, nebo doma s port forwardingem a DDNS, např. DuckDNS).
- Linux na serveru (Debian/Ubuntu), UDP port `51820` otevřený.

### Server
```bash
sudo apt update && sudo apt install -y wireguard
umask 077
wg genkey | tee server.key | wg pubkey > server.pub
```

Povolte předávání paketů mezi klienty:
```bash
echo 'net.ipv4.ip_forward=1' | sudo tee /etc/sysctl.d/99-wg.conf
sudo sysctl --system
```

`/etc/wireguard/wg0.conf`:
```ini
[Interface]
Address = 10.8.0.1/24
ListenPort = 51820
PrivateKey = <obsah server.key>

[Peer]
# klient 1
PublicKey = <veřejný klíč klienta 1>
AllowedIPs = 10.8.0.2/32

[Peer]
# klient 2
PublicKey = <veřejný klíč klienta 2>
AllowedIPs = 10.8.0.3/32
```

Spuštění a start po restartu:
```bash
sudo systemctl enable --now wg-quick@wg0
sudo ufw allow 51820/udp   # pokud používáte ufw
```

### Klient (Linux/Windows/macOS/telefon)
1. Nainstalujte klienta z **wireguard.com/install**.
2. Vygenerujte klíče (ve Windows: **Add Empty Tunnel**, vygeneruje se automaticky; Linux: `wg genkey | tee c.key | wg pubkey > c.pub`).
3. Konfigurace klienta:
```ini
[Interface]
Address = 10.8.0.2/24
PrivateKey = <soukromý klíč klienta>

[Peer]
PublicKey = <veřejný klíč serveru (server.pub)>
Endpoint = vase-domena-nebo-ip:51820
AllowedIPs = 10.8.0.0/24
PersistentKeepalive = 25
```
4. Veřejný klíč klienta přidejte do `[Peer]` na serveru a restartujte: `sudo systemctl restart wg-quick@wg0`.
5. Zapněte tunel a otestujte: `ping 10.8.0.1`, `ping 10.8.0.3`.

Tip: pro veškerý internetový provoz přes server dejte klientovi `AllowedIPs = 0.0.0.0/0` a na serveru přidejte NAT (`iptables -t nat -A POSTROUTING -s 10.8.0.0/24 -o eth0 -j MASQUERADE`).

---

## 6. OpenVPN (vlastní VPN server)

### Nejrychlejší cesta: instalační skript
Na serveru (Debian/Ubuntu, root):
```bash
curl -O https://raw.githubusercontent.com/angristan/openvpn-install/master/openvpn-install.sh
chmod +x openvpn-install.sh
sudo ./openvpn-install.sh
```
Odpovězte na otázky (veřejná IP/doména, port `1194`, protokol UDP, DNS) a zadejte jméno prvního klienta. Skript vytvoří soubor `jmeno.ovpn`.

Další klienty přidáte opětovným spuštěním skriptu (**Add a new user**).

### Klient
1. Nainstalujte **OpenVPN Connect** (openvpn.net) nebo na Linuxu `sudo apt install openvpn`.
2. Importujte soubor `.ovpn` a připojte se. Linux: `sudo openvpn --config jmeno.ovpn`.

### Aby se klienti viděli navzájem
Do `/etc/openvpn/server.conf` přidejte:
```
client-to-client
```
a restartujte: `sudo systemctl restart openvpn@server`.

### Pro hry s broadcastem
Standardní režim (TUN) broadcast nepřenáší. Pro skutečný L2 přenos je potřeba režim **TAP** (`dev tap` + bridge). Nastavení je složitější. Pro hry je pak jednodušší použít ZeroTier nebo Radmin VPN.

### Ruční konfigurace (stručně)
Využijte `easy-rsa` pro vytvoření CA, serverového certifikátu a klientských certifikátů, pak nastavte `server.conf` (`port 1194`, `proto udp`, `dev tun`, `server 10.9.0.0 255.255.255.0`, `tls-crypt`). Pro většinu lidí je skript výše rychlejší a bezpečnější.

---

## Port forwarding doma (pro WireGuard/OpenVPN)

1. Zjistěte lokální IP serveru: `ip a`. Nastavte pro něj pevnou IP nebo DHCP rezervaci v routeru.
2. V routeru (obvykle `192.168.0.1` nebo `192.168.1.1`) přesměrujte **UDP 51820** (WireGuard) nebo **UDP 1194** (OpenVPN) na server.
3. Pokud máte dynamickou veřejnou IP, zřiďte DDNS (DuckDNS, No-IP) a v klientech použijte doménu.
4. Pokud je váš operátor za CGNAT (veřejná IP není vaše), port forwarding nebude fungovat. Použijte ZeroTier, Tailscale nebo VPS.

---

## Seznam potřebných materiálů

### Pro všechny varianty
| Co | Poznámka |
|---|---|
| Počítač nebo telefon u každého účastníka | Windows, macOS, Linux, Android nebo iOS |
| Funkční připojení k internetu | Pro hry je vhodná odezva pod 50 ms. |
| Účet správce na počítači | Instalace klienta vyžaduje administrátorská práva. |
| E-mailová adresa | Pro registraci (ZeroTier, Tailscale, Hamachi). |
| Dohodnuté sdílení údajů | Network ID, název sítě a heslo. Předávejte je soukromě. |

### Podle varianty
- **ZeroTier, Tailscale, Radmin VPN, Hamachi:** účet na službě (u Radmin VPN není potřeba) a klient z oficiálních stránek. Žádný server ani úprava routeru. Radmin VPN funguje jen na Windows.
- **WireGuard:** server (VPS s Linuxem, nebo domácí počítač či Raspberry Pi běžící nepřetržitě), veřejná IP nebo doména (u dynamické IP DDNS), přístup do routeru kvůli port forwardingu (UDP 51820), SSH přístup a klient na každém zařízení.
- **OpenVPN:** totéž, ale port UDP 1194. Navíc instalační skript z GitHubu a klient OpenVPN Connect.

### Doporučené vybavení navíc
| Co | Proč |
|---|---|
| Záloha klíčů a konfigurací (`.ovpn`, `*.key`) | Obnova po ztrátě serveru. Uchovávejte je v soukromí. |
| Správce hesel | Bezpečné uložení hesel a klíčů. |
| UPS pro domácí server | Server běží nepřetržitě. |
| DHCP rezervace pro server v routeru | Port forwarding by jinak přestal fungovat. |

### Kontrola před začátkem
- [ ] Operátor vám nedává IP za CGNAT. Pokud ano, použijte ZeroTier, Tailscale nebo VPS.
- [ ] Windows má síť nastavenou jako **Soukromá**, pokud chcete sdílet soubory.
- [ ] Firewall povoluje potřebný UDP port.
- [ ] Máte přístup k administraci routeru (pro server doma).

---

## Kde co objednat (Česko)

Ceny a dostupnost se mění, před nákupem je ověřte na webu obchodu.

### Hardware (server doma, Raspberry Pi, UPS, router)
| Obchod | Web | Co tam hledat |
|---|---|---|
| Alza | https://www.alza.cz | Mini PC, Raspberry Pi, UPS, routery, SSD, kabely |
| CZC.cz | https://www.czc.cz | Mini PC, UPS, routery, síťové prvky |
| Mironet | https://www.mironet.cz | Počítače, síťové prvky, UPS |
| RPishop.cz | https://rpishop.cz | Raspberry Pi, napájecí zdroje, microSD, pouzdra |
| Laskakit | https://www.laskakit.cz | Raspberry Pi a příslušenství |

Pro domácí VPN server stačí Raspberry Pi 4/5 nebo malé mini PC, napájecí zdroj, microSD karta (min. 16 GB) nebo SSD a ethernetový kabel (server připojte kabelem, ne Wi-Fi).

### VPS server (pro WireGuard / OpenVPN, bez port forwardingu doma)
| Poskytovatel | Web | Poznámka |
|---|---|---|
| WEDOS | https://www.wedos.cz | Český poskytovatel, VPS s podporou v češtině |
| Forpsi | https://www.forpsi.cz | Český poskytovatel, VPS |
| Active24 | https://www.active24.cz | Český poskytovatel, VPS |
| Hetzner Cloud | https://www.hetzner.com/cloud | Levný zahraniční (Německo), servery v EU |
| Contabo | https://contabo.com | Levný zahraniční, více výkonu za cenu |

Při objednávce zvolte Linux (Debian nebo Ubuntu LTS), 1 vCPU a 1 GB RAM. Pro VPN to stačí. Zvolte lokalitu v Evropě kvůli nízké odezvě.

### DDNS (jen pro server doma s dynamickou IP)
| Služba | Web |
|---|---|
| DuckDNS (zdarma) | https://www.duckdns.org |
| No-IP | https://www.noip.com |

---

## Kde stáhnout (oficiální zdroje)

Stahujte vždy z oficiálních stránek. Fungují i z Česka a jsou bezpečnější než zrcadla třetích stran.

| Program | Odkaz ke stažení | Platformy |
|---|---|---|
| ZeroTier | https://www.zerotier.com/download/ | Windows, macOS, Linux, Android, iOS |
| ZeroTier (konzole) | https://my.zerotier.com | Web |
| Tailscale | https://tailscale.com/download | Windows, macOS, Linux, Android, iOS |
| Radmin VPN | https://www.radmin-vpn.com/cz/ | Windows (česká verze stránek) |
| Hamachi | https://vpn.net | Windows, macOS, Linux |
| WireGuard | https://www.wireguard.com/install/ | Windows, macOS, Linux, Android, iOS |
| OpenVPN Connect | https://openvpn.net/client/ | Windows, macOS, Linux, Android, iOS |
| OpenVPN instalační skript | https://github.com/angristan/openvpn-install | Linux server |
| Raspberry Pi Imager (zápis OS na kartu) | https://www.raspberrypi.com/software/ | Windows, macOS, Linux |

---

## Bezpečnost

- Sdílejte Network ID, hesla a klíče jen s důvěryhodnými lidmi.
- Soukromé klíče (`*.key`, `.ovpn`) nikdy nenahrávejte do veřejného repozitáře.
- U ZeroTieru vždy ručně schvalujte zařízení.
- Nevystavujte RDP (3389) ani SMB (445) přímo do internetu. Používejte je jen přes VPN.
- Aktualizujte systém i klienty.

---

## Rychlá diagnostika

| Příznak | Příčina / řešení |
|---|---|
| Zařízení se nevidí | Zařízení není autorizované (ZeroTier), firewall blokuje ICMP, nebo je jiná podsíť. |
| Ping jde, sdílení ne | Síť je ve Windows nastavená jako Veřejná. Přepněte na Soukromá. |
| Vysoká odezva | Provoz jde přes relay. Otevřete UDP v routeru. |
| WireGuard se nespojí | Špatný klíč, port nepřesměrován, nebo CGNAT. Zkontrolujte `sudo wg show`. |
| Klienti se nevidí navzájem | Chybí `ip_forward` a `AllowedIPs = 10.8.0.0/24` (WireGuard), nebo `client-to-client` (OpenVPN). |
| Hra nevidí ostatní | Použijte ZeroTier/Radmin a zadejte IP hostitele ručně. |
