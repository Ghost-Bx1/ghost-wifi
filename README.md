<div align="center">

# Ghost-WiFi

[![Ghost-WiFi](https://img.shields.io/badge/Ghost--WiFi-WiFi%20Security-red?style=for-the-badge)](https://github.com/Ghost-Bx1/ghost-wifi)

> WiFi attack and audit framework - 38 modules: monitor mode, deauth, WPA/WPA2 handshake, PMKID, WPS, Evil Twin, cracking, radar/distance mapping, ARP MITM, DNS spoofing, and more.

```
  GHOST-WIFI  v3.2.0  |  WiFi Attack & Audit Framework
  By Gh0st-Bx1        |  github.com/Ghost-Bx1
```

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?style=flat-square&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Linux-lightgrey?style=flat-square)
![Category](https://img.shields.io/badge/Category-WiFi%20Security-red?style=flat-square)
![By Gh0st-Bx1](https://img.shields.io/badge/By-Gh0st--Bx1-black?style=flat-square&logo=github)

</div>

---

## Overview

Ghost-WiFi is a comprehensive WiFi attack and audit framework. Zero pip dependencies (stdlib only, optional colorama). Wraps the full aircrack-ng suite with clean CLI ergonomics.

| Module           | Technique                                                       |
|------------------|-----------------------------------------------------------------|
| `ifaces`         | List wireless interfaces, mode, driver, MAC                    |
| `monitor`        | Start/stop/check monitor mode via airmon-ng                    |
| `scan`           | Passive AP + client scan with airodump-ng, JSON export         |
| `hop`            | Channel hopping across selected channels                       |
| `deauth`         | 802.11 deauthentication flood (broadcast or targeted)          |
| `capture`        | WPA/WPA2 4-way handshake capture with auto deauth trigger      |
| `pmkid`          | Clientless PMKID capture with hcxdumptool + hashcat export     |
| `wps`            | WPS scan, Pixie Dust (reaver -K), PIN brute-force, bully       |
| `evil-twin`      | Rogue AP with hostapd + dnsmasq DHCP, captive portal ready     |
| `crack`          | Offline cracking via aircrack-ng (CPU) or hashcat (GPU)        |
| `wep`            | WEP cracking: ARP injection, fragmentation, chop-chop          |
| `clients`        | Track clients per AP, log MACs and probed ESSIDs               |
| `karma`          | KARMA attack - respond to all probe requests                   |
| `handshake`      | Verify, convert (.hc22000/.hccapx), or strip capture files    |
| `info`           | Dependency checker - shows installed/missing tools             |
| `auto`           | Automated attack chain: scan -> deauth -> capture              |
| `decloak`        | Hidden SSID detection via probe/association                    |
| `eapol`          | EAPOL frame re-injection                                       |
| `signal`         | Live RSSI tracking with signal bar + estimated distance        |
| `nic-detect`     | Deep NIC analysis: chipset, injection, bands, TX power, bus    |
| `beacon-flood`   | Beacon flood with fake SSIDs via aireplay-ng                   |
| `probe-hunt`     | Capture probe requests and build device map                    |
| `captive-portal` | Standalone HTTP captive portal for credential capture          |
| `mdk4`           | MDK4 wrapper: beacon/deauth/auth-DoS/probe/EAPOL/TKIP attacks  |
| `fingerprint`    | AP and client fingerprinting with vendor OUI lookup            |
| `injection-test` | Test packet injection capability on a monitor interface        |
| `channelfix`     | Force a specific channel on a wireless interface               |
| `5ghz-scan`      | Dedicated 5GHz band scan                                       |
| `radar`          | WiFi radar: ASCII map of all APs sorted by estimated distance  |
| `distance`       | Quick RSSI-to-distance scan of all visible networks            |
| `wifi-map`       | ASCII topology map: APs with associated clients tree           |
| `channel-survey` | 2.4GHz/5GHz channel utilization chart + congestion hints       |
| `ap-watch`       | Live monitor for AP appearance/disappearance events            |
| `pcap-analyze`   | Analyze .cap/.pcap: handshakes, PMKIDs, frame stats            |
| `pmkid-crack`    | All-in-one pipeline: hcxdumptool -> hcxpcapngtool -> hashcat   |
| `deauth-detect`  | Passive detection of deauthentication storm attacks            |
| `arp-mitm`       | ARP poisoning MITM with bidirectional arpspoof + tcpdump dump  |
| `handshake-hunt` | Automated multi-AP handshake collector with deauth bursts      |
| `dns-spoof`      | DNS spoofing via bettercap caplet or dnsspoof hosts file       |

---

## Requirements

```
Python 3.7+
Linux only (requires raw socket / monitor mode support)

Core (required):
  aircrack-ng   - airmon-ng, airodump-ng, aireplay-ng, aircrack-ng

Optional by module:
  reaver        - WPS Pixie Dust and PIN brute-force
  bully         - Alternative WPS attacker
  hcxdumptool   - PMKID clientless capture
  hcxtools      - hcxpcapngtool, cap2hccapx conversion
  hashcat       - GPU-accelerated cracking (mode 22000 / 2500)
  hostapd       - Evil Twin AP daemon
  dnsmasq       - Evil Twin DHCP/DNS
  bettercap     - KARMA, MITM framework
  macchanger    - MAC address randomization
  mdk4          - Beacon flood, auth-DoS, TKIP MIC attacks
  john          - CPU-based hash cracking
  iw            - signal, distance, nic-detect, 5ghz-scan
```

```bash
# Install core + common extras (Debian/Ubuntu/Kali):
sudo apt install aircrack-ng reaver bully hcxdumptool hcxtools \
                 hashcat hostapd dnsmasq bettercap macchanger mdk4 iw
```

---

## Installation

```bash
git clone https://github.com/Ghost-Bx1/ghost-wifi
cd ghost-wifi
python ghost-wifi.py info
```

---

## Usage

### Check dependencies

```bash
python ghost-wifi.py info
```

### List interfaces

```bash
python ghost-wifi.py ifaces
```

### Enable monitor mode

```bash
sudo python ghost-wifi.py monitor -i wlan0 --action start
# Stop:
sudo python ghost-wifi.py monitor -i wlan0mon --action stop
```

### Scan for APs and clients

```bash
# 30-second passive scan
sudo python ghost-wifi.py scan -i wlan0mon --duration 30

# Save to JSON
sudo python ghost-wifi.py scan -i wlan0mon --duration 60 -o scan.json

# 5GHz only
sudo python ghost-wifi.py scan -i wlan0mon --band a
```

### Deauthentication attack

```bash
# Broadcast deauth (kick all clients from AP)
sudo python ghost-wifi.py deauth -i wlan0mon --bssid AA:BB:CC:DD:EE:FF

# Target specific client, 10 frames
sudo python ghost-wifi.py deauth -i wlan0mon --bssid AA:BB:CC:DD:EE:FF \
    --client 11:22:33:44:55:66 --count 10 --channel 6

# Randomize interval between bursts (IDS evasion)
sudo python ghost-wifi.py deauth -i wlan0mon --bssid AA:BB:CC:DD:EE:FF \
    --rand-interval --interval-min 2 --interval-max 8
```

### Capture WPA/WPA2 handshake

```bash
# Auto deauth + capture
sudo python ghost-wifi.py capture -i wlan0mon \
    --bssid AA:BB:CC:DD:EE:FF --essid "HomeNetwork" --channel 6

# Passive mode only (no deauth)
sudo python ghost-wifi.py capture -i wlan0mon \
    --bssid AA:BB:CC:DD:EE:FF --channel 6 --passive --timeout 180
```

### PMKID attack (clientless WPA2)

```bash
# Capture PMKID from all APs
sudo python ghost-wifi.py pmkid -i wlan0mon --duration 60

# Target specific AP
sudo python ghost-wifi.py pmkid -i wlan0mon \
    --bssid AA:BB:CC:DD:EE:FF --duration 90 -o pmkid.pcapng
```

### WPS attacks

```bash
# Scan for WPS-enabled APs
sudo python ghost-wifi.py wps -i wlan0mon --action scan

# Pixie Dust attack
sudo python ghost-wifi.py wps -i wlan0mon --bssid AA:BB:CC:DD:EE:FF \
    --channel 6 --action pixie

# PIN brute-force
sudo python ghost-wifi.py wps -i wlan0mon --bssid AA:BB:CC:DD:EE:FF \
    --channel 6 --action pin

# Bully (alternative)
sudo python ghost-wifi.py wps -i wlan0mon --bssid AA:BB:CC:DD:EE:FF \
    --channel 6 --action bully
```

### Evil Twin / Rogue AP

```bash
# Create rogue AP matching target network
sudo python ghost-wifi.py evil-twin -i wlan0 --essid "CoffeeShop_Free" --channel 6

# With BSSID spoofing
sudo python ghost-wifi.py evil-twin -i wlan0 \
    --essid "HomeNetwork" --bssid AA:BB:CC:DD:EE:FF --channel 11
```

Clients that connect receive DHCP from 192.168.1.x. Combine with `captive-portal` for credential capture in authorized red team assessments.

### Crack handshake offline

```bash
# aircrack-ng (CPU)
python ghost-wifi.py crack --cap capture-01.cap --wordlist /usr/share/wordlists/rockyou.txt

# hashcat (GPU, mode 22000 = WPA2)
python ghost-wifi.py crack --cap hashes.hc22000 --hashcat \
    --wordlist /usr/share/wordlists/rockyou.txt

# With hashcat rules
python ghost-wifi.py crack --cap hashes.hc22000 --hashcat \
    --wordlist wordlist.txt --rules /usr/share/hashcat/rules/best64.rule

# Mask attack
python ghost-wifi.py crack --cap hashes.hc22000 --hashcat \
    --mask "?d?d?d?d?d?d?d?d"

# Combo attack (two wordlists)
python ghost-wifi.py crack --cap hashes.hc22000 \
    --wordlist names.txt --wordlist2 numbers.txt
```

### WEP cracking

```bash
# ARP injection (fastest)
sudo python ghost-wifi.py wep -i wlan0mon \
    --bssid AA:BB:CC:DD:EE:FF --channel 6 --attack arp

# Fragmentation
sudo python ghost-wifi.py wep -i wlan0mon \
    --bssid AA:BB:CC:DD:EE:FF --channel 6 --attack frag

# ChopChop
sudo python ghost-wifi.py wep -i wlan0mon \
    --bssid AA:BB:CC:DD:EE:FF --channel 6 --attack chopchop
```

### Client tracking

```bash
# Track all clients
sudo python ghost-wifi.py clients -i wlan0mon --duration 60

# Track clients of specific AP
sudo python ghost-wifi.py clients -i wlan0mon \
    --bssid AA:BB:CC:DD:EE:FF --channel 6 --duration 120 -o clients.json
```

### KARMA attack

```bash
# Respond to all probe requests
sudo python ghost-wifi.py karma -i wlan0mon
```

### Channel hopping

```bash
# Hop all 2.4GHz channels
sudo python ghost-wifi.py hop -i wlan0mon

# Hop specific channels, fast
sudo python ghost-wifi.py hop -i wlan0mon --channels 1,6,11 --delay 0.3
```

### Handshake tools

```bash
# Verify handshake in capture
python ghost-wifi.py handshake --cap capture-01.cap --action verify

# Convert to hashcat format (.hc22000)
python ghost-wifi.py handshake --cap capture-01.cap --action convert -o hashes.hc22000

# Strip non-handshake packets
python ghost-wifi.py handshake --cap capture-01.cap --action strip -o clean.cap
```

### Automated attack chain

```bash
# Full auto: scan -> select target -> deauth -> capture
sudo python ghost-wifi.py auto -i wlan0mon --duration 60
```

### Hidden SSID detection

```bash
sudo python ghost-wifi.py decloak -i wlan0mon --channel 6
```

### Signal tracking

```bash
# Track live RSSI + estimated distance for a specific AP
sudo python ghost-wifi.py signal -i wlan0mon --bssid AA:BB:CC:DD:EE:FF \
    --duration 60 --interval 2
```

Shows a live bar like `[||||||||||||............] -65 dBm  ~18m`

### NIC analysis

```bash
# Deep chipset, driver, injection, band, TX power analysis
sudo python ghost-wifi.py nic-detect
sudo python ghost-wifi.py nic-detect -i wlan0
```

### Beacon flood

```bash
# Flood with 500 fake SSIDs
sudo python ghost-wifi.py beacon-flood -i wlan0mon --count 500
```

### Probe request capture

```bash
# Build a map of devices searching for networks
sudo python ghost-wifi.py probe-hunt -i wlan0mon --duration 60 -o probes.json
```

### Captive portal

```bash
# Start HTTP credential capture portal on port 8080
sudo python ghost-wifi.py captive-portal --port 8080
```

### MDK4 attacks

```bash
# Beacon flood
sudo python ghost-wifi.py mdk4 -i wlan0mon --mode b

# Deauth all clients
sudo python ghost-wifi.py mdk4 -i wlan0mon --mode d --bssid AA:BB:CC:DD:EE:FF

# Auth DoS
sudo python ghost-wifi.py mdk4 -i wlan0mon --mode a --bssid AA:BB:CC:DD:EE:FF
```

### AP and client fingerprinting

```bash
sudo python ghost-wifi.py fingerprint -i wlan0mon --duration 30 -o fingerprint.json
```

### Injection test

```bash
sudo python ghost-wifi.py injection-test -i wlan0mon

# Extended test against specific AP
sudo python ghost-wifi.py injection-test -i wlan0mon --bssid AA:BB:CC:DD:EE:FF
```

### 5GHz scan

```bash
sudo python ghost-wifi.py 5ghz-scan -i wlan0mon --duration 30 -o 5ghz.json
```

---

## Distance Estimation (v3.1.0+)

Ghost-WiFi uses the **Log Distance Path Loss model** to estimate the physical distance to each access point from its RSSI (signal strength in dBm):

```
d = 10 ^ ((TxPower - RSSI) / (10 * n))
```

Where:
- `RSSI` - measured signal strength in dBm (e.g. -65)
- `TxPower` - reference power at 1 meter (default: -50 dBm)
- `n` - path loss exponent (configure with `--path-n`):
  - `2.0` - free space / outdoor line-of-sight
  - `2.7` - typical indoor environment (default)
  - `3.5` - heavy walls / obstructed environment

Distances are **estimates** - real-world accuracy depends on the environment, AP hardware, and obstacles. Use as a relative proximity guide, not an exact measurement.

### WiFi Radar - ASCII map sorted by distance

```bash
# Scan 20s and show all APs by proximity
sudo python ghost-wifi.py radar -i wlan0mon

# Scan 30s, 5GHz, show only 10 closest
sudo python ghost-wifi.py radar -i wlan0mon --duration 30 --band a --top 10

# Indoor environment tuning
sudo python ghost-wifi.py radar -i wlan0mon --path-n 3.5

# Save to JSON
sudo python ghost-wifi.py radar -i wlan0mon -o radar.json
```

Color coding: green = <15m, yellow = 15-50m, red = >50m

### Quick distance scan

```bash
# Scan all visible networks and show estimated distance
sudo python ghost-wifi.py distance -i wlan0mon

# Filter by specific AP
sudo python ghost-wifi.py distance -i wlan0mon --bssid AA:BB:CC:DD:EE:FF

# Free space tuning (outdoor)
sudo python ghost-wifi.py distance -i wlan0mon --path-n 2.0 --tx-power -40
```

---

## Reference

### Global flags

| Flag              | Description                        |
|-------------------|------------------------------------|
| `-v / --verbose`  | Verbose output                     |
| `-o / --output`   | Save results to JSON/file          |
| `--no-banner`     | Suppress the startup banner        |

### `scan` flags

| Flag              | Description                                            |
|-------------------|--------------------------------------------------------|
| `-i / --interface`| Monitor mode interface                                 |
| `--channel N`     | Lock to channel N                                      |
| `--band`          | a (5GHz), b (2.4GHz), abg (both)                      |
| `--duration N`    | Scan duration in seconds (default: 30)                 |

### `deauth` flags

| Flag                | Description                                                       |
|---------------------|-------------------------------------------------------------------|
| `-i / --interface`  | Monitor mode interface (required)                                 |
| `--bssid`           | Target AP MAC address                                             |
| `--bssid-list`      | Comma-separated BSSIDs for multi-target rotation                  |
| `--client`          | Target client MAC (default: broadcast FF:FF:FF:FF:FF:FF)          |
| `--count N`         | Deauth frames per burst (0 = continuous)                          |
| `--channel N`       | AP channel                                                        |
| `--mac-rand`        | Randomize source MAC before attack                                |
| `--rand-interval`   | Randomize delay between bursts (IDS evasion)                      |
| `--interval-min N`  | Minimum delay seconds (default: 1.0)                              |
| `--interval-max N`  | Maximum delay seconds (default: 5.0)                              |

### `capture` flags

| Flag              | Description                                            |
|-------------------|--------------------------------------------------------|
| `-i / --interface`| Monitor mode interface (required)                      |
| `--bssid`         | Target AP MAC (required)                               |
| `--essid`         | AP name (for display)                                  |
| `--channel N`     | AP channel                                             |
| `--passive`       | No deauth - passive capture only                       |
| `--timeout N`     | Max wait time in seconds (default: 120)                |
| `--mac-rand`      | Randomize MAC before capture                           |

### `crack` flags

| Flag              | Description                                            |
|-------------------|--------------------------------------------------------|
| `--cap`           | Capture file (.cap, .hc22000)                          |
| `--wordlist`      | Wordlist file (default: built-in mini-list)            |
| `--wordlist2`     | Second wordlist for combo attack                       |
| `--hashcat`       | Use hashcat instead of aircrack-ng                     |
| `--hash-mode N`   | Hashcat mode (default: 22000 for WPA2)                 |
| `--rules FILE`    | Hashcat rules file                                     |
| `--mask`          | Hashcat mask attack pattern (e.g. `?d?d?d?d?d?d?d?d`) |

### `radar` flags

| Flag              | Description                                            |
|-------------------|--------------------------------------------------------|
| `-i / --interface`| Monitor interface (auto-detect if omitted)             |
| `--duration N`    | Scan duration in seconds (default: 20)                 |
| `--band`          | Frequency band: a, b, abg, abgn                        |
| `--top N`         | Show only N closest networks                           |
| `--path-n N`      | Path loss exponent (default: 2.7)                      |
| `--tx-power N`    | Reference TX power at 1m in dBm (default: -50)         |

### `distance` flags

| Flag              | Description                                            |
|-------------------|--------------------------------------------------------|
| `-i / --interface`| Wireless interface (auto-detect if omitted)            |
| `--bssid`         | Filter by specific BSSID                               |
| `--path-n N`      | Path loss exponent (default: 2.7)                      |
| `--tx-power N`    | Reference TX power at 1m in dBm (default: -50)         |

### `signal` flags

| Flag              | Description                                            |
|-------------------|--------------------------------------------------------|
| `-i / --interface`| Wireless interface (required)                          |
| `--bssid`         | Target AP BSSID (required)                             |
| `--duration N`    | Tracking duration in seconds (default: 30)             |
| `--interval N`    | Reading interval in seconds (default: 2)               |

---

## Attack Workflows

### WPA2 Personal (fastest path)

```bash
# 1. Enable monitor mode
sudo python ghost-wifi.py monitor -i wlan0 --action start

# 2. Scan for target
sudo python ghost-wifi.py scan -i wlan0mon --duration 30

# 3a. PMKID (clientless, no deauth needed)
sudo python ghost-wifi.py pmkid -i wlan0mon --bssid TARGET_BSSID -o pmkid.pcapng
python ghost-wifi.py crack --cap pmkid.hc22000 --hashcat --wordlist rockyou.txt

# 3b. Handshake capture (requires active client)
sudo python ghost-wifi.py capture -i wlan0mon --bssid TARGET_BSSID --channel 6 -o capture
python ghost-wifi.py crack --cap capture-01.cap --wordlist rockyou.txt
```

### WPS target

```bash
sudo python ghost-wifi.py wps -i wlan0mon --action scan
sudo python ghost-wifi.py wps -i wlan0mon --bssid TARGET_BSSID --channel 6 --action pixie
```

### WiFi reconnaissance

```bash
# Step 1 - Build a proximity map
sudo python ghost-wifi.py radar -i wlan0mon --duration 30

# Step 2 - Fingerprint APs and clients
sudo python ghost-wifi.py fingerprint -i wlan0mon --duration 30

# Step 3 - Probe requests (what devices are searching for)
sudo python ghost-wifi.py probe-hunt -i wlan0mon --duration 60
```

---

## Ghost Toolkit

| Tool | Description |
|------|-------------|
| [ghost-ad](https://github.com/Ghost-Bx1/ghost-ad) | Active Directory - LDAP, Kerberoasting, AS-REP Roasting, BloodHound-lite |
| [ghost-cloud](https://github.com/Ghost-Bx1/ghost-cloud) | Cloud Security - AWS, Azure and GCP misconfiguration scanner |
| [ghost-fuzz](https://github.com/Ghost-Bx1/ghost-fuzz) | Web Fuzzing - directory brute-force, parameter fuzzing, vhost enumeration |
| [ghost-osint](https://github.com/Ghost-Bx1/ghost-osint) | OSINT - domain, email and IP intelligence from public sources |
| [ghost-privesc](https://github.com/Ghost-Bx1/ghost-privesc) | Privilege Escalation - Linux privesc checker, 17 vectors, GTFOBins |
| [ghost-recon](https://github.com/Ghost-Bx1/ghost-recon) | Reconnaissance - DNS, SSL, WAF, subdomain enumeration, email security |
| [ghost-report](https://github.com/Ghost-Bx1/ghost-report) | Reporting - pentest report generator from any ghost-* JSON output |
| [ghost-scan](https://github.com/Ghost-Bx1/ghost-scan) | Port Scanner - async TCP/UDP scanner with banner grabbing and CVE correlation |
| [ghost-shell](https://github.com/Ghost-Bx1/ghost-shell) | Payload Generation - reverse shell and web shell generator, 25+ languages |
| [ghost-spray](https://github.com/Ghost-Bx1/ghost-spray) | Credential Attacks - password spraying, stuffing, default credential testing |
| [ghost-wifi](https://github.com/Ghost-Bx1/ghost-wifi) | WiFi Attacks - monitor mode, deauth, WPA/WPA2 capture, PMKID, WPS, Evil Twin, radar |

---

## Disclaimer

For use in authorized environments only. Penetration testing, CTF competitions, and wireless security research with explicit permission from the network owner. WiFi attacks against networks you do not own or have written authorization to test are illegal in most jurisdictions. The author is not responsible for misuse.

---

**By [Gh0st-Bx1](https://github.com/Ghost-Bx1)**
