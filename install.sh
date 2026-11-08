#!/usr/bin/env bash
# Ghost-WiFi Installer
# By Gh0st-Bx1 | github.com/Ghost-Bx1

G="\033[92m"; Y="\033[93m"; R="\033[91m"; C="\033[96m"
W="\033[97m"; D="\033[2m"; N="\033[1m"; X="\033[0m"
EQ="════════════════════════════════════════════════════════════════════"
HL="────────────────────────────────────────────────────────────────────"

banner() {
    echo -e "${G}╔${EQ}╗${X}"
    echo -e "${G}║${X}                                                                    ${G}║${X}"
    echo -e "${G}║${X}       ${G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠛⠛⠿⠟⠉⠛⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿${X}       ${G}║${X}"
    echo -e "${G}║${X}       ${G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠉⢀⣠⣤⣶⣶⣶⣶⣶⣶⣤⣀⠢⢝⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿${X}       ${G}║${X}"
    echo -e "${G}║${X}       ${G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⡡⢀⣴⡿⢋⡴⢿⣿⣿⣿⣿⣿⣿⣿⢷⣦⡑⠈⡛⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿${X}       ${G}║${X}"
    echo -e "${G}║${X}       ${G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⡜⢠⣾⣿⣤⣋⣴⣿⣿⣿⣿⣿⣿⣿⣿⣷⣌⠻⣶⣦⣤⣤⣀⠉⠻⣿⣿⣿⡿⠿⢛⢛⡻⠿⣿⣿⣿⣿${X}       ${G}║${X}"
    echo -e "${G}║${X}       ${G}⣿⠿⠟⠟⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⢀⣿⣿⣿⡿⠛⠛⠻⣿⣿⣿⡿⠛⠛⢿⣿⣿⣧⠉⠉⣁⣈⣉⣁⢀⣿⣿⢋⠄⣁⣴⣶⣄⠐⢌⢻⣿⣿${X}       ${G}║${X}"
    echo -e "${G}║${X}      ${G}⡏⠀⣴⣦⣄⠢⡙⢿⣿⣿⣿⣿⣿⣿⡇⠀⣼⣿⣿⣿⠅⠀⠀  ⢹⣿⡿⠁⠀⠀⠀⢹⣿⣿⡆⠀⣿⣿⣿⣿⣿⡟⠁⢀⣴⣿⣿⣿⣿⣷⡈⠎⢿⣿${X}       ${G}║${X}"
    echo -e "${G}║${X}      ${G}⡇⠀⣿⣿⣿⣷⣌⠀⠙⢿⣿⣿⣿⣿⠀⢀⣿⣿⣿⣿⠀⠀⠀  ⠀⠈⣿⡇⠀⠀⠀⠀⠈⢿⣿⡇⠁⢻⣿⣿⣿⡿⠁⢠⣾⣿⣿⣿⡿⢿⣿⣷⠀⠘⣿${X}      ${G}║${X}"
    echo -e "${G}║${X}       ${G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿${X}       ${G}║${X}"
    echo -e "${G}║${X}                                                                    ${G}║${X}"
    echo -e "${G}║${X}  ${G}${N}GHOST-WIFI INSTALLER${X}                                              ${G}║${X}"
    echo -e "${G}║${X}  ${C}v3.3.0  ${D}WiFi Attack & Audit Framework${X}                             ${G}║${X}"
    echo -e "${G}║${X}  ${D}${HL:0:44}${X}                      ${G}║${X}"
    echo -e "${G}║${X}  ${W}By Gh0st-Bx1  ${D}│  github.com/Ghost-Bx1${X}                             ${G}║${X}"
    echo -e "${G}║${X}  ${D}${HL:0:44}${X}                      ${G}║${X}"
    echo -e "${G}║${X}                                                                    ${G}║${X}"
    echo -e "${G}╚${EQ}╝${X}"
    echo
}

info()  { echo -e "  ${C}[*]${X} $*"; }
ok()    { echo -e "  ${G}[+]${X} $*"; }
warn()  { echo -e "  ${Y}[~]${X} $*"; }
err()   { echo -e "  ${R}[!]${X} $*"; }
step()  { echo -e "\n${G}  >${X} ${W}$*${X}"; }

# ── Root check ────────────────────────────────────────────────────────────────
if [[ $EUID -ne 0 ]]; then
    err "Run as root: sudo bash install.sh"
    exit 1
fi

banner

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_BIN="/usr/local/bin/ghost-wifi"
INSTALL_DIR="/opt/ghost-wifi"

# ── OS detect ─────────────────────────────────────────────────────────────────
step "Detecting system..."
if command -v apt-get &>/dev/null; then
    PKG_MGR="apt"
    info "Package manager: apt (Debian/Ubuntu/Kali)"
elif command -v pacman &>/dev/null; then
    PKG_MGR="pacman"
    info "Package manager: pacman (Arch)"
elif command -v dnf &>/dev/null; then
    PKG_MGR="dnf"
    info "Package manager: dnf (Fedora/RHEL)"
else
    warn "Unknown package manager - skipping apt install"
    PKG_MGR="unknown"
fi

PYTHON=$(command -v python3 || command -v python)
if [[ -z "$PYTHON" ]]; then
    err "Python 3 not found. Install python3 first."
    exit 1
fi
ok "Python: $($PYTHON --version 2>&1)"

# ── Install dependencies ───────────────────────────────────────────────────────
step "Installing dependencies..."

APT_PKGS=(
    aircrack-ng
    reaver
    bully
    hcxdumptool
    hcxtools
    hashcat
    hostapd
    dnsmasq
    bettercap
    macchanger
    mdk4
    tshark
    ethtool
    dsniff
    iw
    usbutils
    pixiewps
    rfkill
)

if [[ "$PKG_MGR" == "apt" ]]; then
    info "Updating package list..."
    apt-get update -qq 2>/dev/null
    info "Installing: ${APT_PKGS[*]}"
    apt-get install -y -qq "${APT_PKGS[@]}" 2>/dev/null
    ok "APT packages installed"
elif [[ "$PKG_MGR" == "pacman" ]]; then
    PACMAN_PKGS=(aircrack-ng reaver hashcat hostapd dnsmasq macchanger mdk4 tshark dsniff iw usbutils)
    pacman -S --noconfirm --needed "${PACMAN_PKGS[@]}" 2>/dev/null
    ok "Pacman packages installed"
else
    warn "Skipping package install - install manually:"
    warn "  ${APT_PKGS[*]}"
fi

# ── Python optional deps ───────────────────────────────────────────────────────
step "Checking Python packages..."
if ! $PYTHON -c "import colorama" 2>/dev/null; then
    info "Installing colorama (optional, for Windows color support)..."
    $PYTHON -m pip install colorama --quiet 2>/dev/null && ok "colorama installed" || warn "colorama skipped"
else
    ok "colorama already available"
fi

# ── Copy files ─────────────────────────────────────────────────────────────────
step "Installing ghost-wifi..."

mkdir -p "$INSTALL_DIR"

# Copy main script
cp "$SCRIPT_DIR/ghost-wifi.py" "$INSTALL_DIR/ghost-wifi.py"
chmod +x "$INSTALL_DIR/ghost-wifi.py"
ok "Copied ghost-wifi.py -> $INSTALL_DIR/"

# Copy README if present
[[ -f "$SCRIPT_DIR/README.md" ]] && cp "$SCRIPT_DIR/README.md" "$INSTALL_DIR/"

# Create wordlists dir
mkdir -p "$INSTALL_DIR/wordlists"

# ── Wrapper in /usr/local/bin ──────────────────────────────────────────────────
cat > "$INSTALL_BIN" << 'WRAPPER'
#!/usr/bin/env bash
exec python3 /opt/ghost-wifi/ghost-wifi.py "$@"
WRAPPER
chmod +x "$INSTALL_BIN"
ok "Wrapper created: $INSTALL_BIN"

# ── Wordlist hint ──────────────────────────────────────────────────────────────
step "Checking wordlists..."
if [[ -f /usr/share/wordlists/rockyou.txt ]]; then
    ok "rockyou.txt found: /usr/share/wordlists/rockyou.txt"
elif [[ -f /usr/share/wordlists/rockyou.txt.gz ]]; then
    info "Decompressing rockyou.txt.gz..."
    gunzip /usr/share/wordlists/rockyou.txt.gz && ok "rockyou.txt extracted"
else
    warn "rockyou.txt not found"
    warn "On Kali: apt install wordlists && gunzip /usr/share/wordlists/rockyou.txt.gz"
fi

# ── Verify install ─────────────────────────────────────────────────────────────
step "Verifying installation..."
echo

TOOLS=(aircrack-ng airodump-ng aireplay-ng airmon-ng hcxdumptool hcxpcapngtool hashcat reaver bully hostapd dnsmasq bettercap macchanger mdk4 tshark iw ethtool)
MISSING=()

for t in "${TOOLS[@]}"; do
    if command -v "$t" &>/dev/null; then
        ok "$t"
    else
        warn "$t  ${D}(not found)${X}"
        MISSING+=("$t")
    fi
done

echo
if [[ ${#MISSING[@]} -eq 0 ]]; then
    ok "All tools installed!"
else
    warn "${#MISSING[@]} tool(s) missing: ${MISSING[*]}"
fi

# ── Done ───────────────────────────────────────────────────────────────────────
echo
echo -e "${G}  ╔══════════════════════════════════════╗${X}"
echo -e "${G}  ║${X}  ${G}${N}Installation complete!${X}              ${G}║${X}"
echo -e "${G}  ║${X}  ${D}Run:${X} ${W}ghost-wifi info${X}                  ${G}║${X}"
echo -e "${G}  ║${X}  ${D}Or:${X}  ${W}ghost-wifi --help${X}                ${G}║${X}"
echo -e "${G}  ╚══════════════════════════════════════╝${X}"
echo
