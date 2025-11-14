#!/usr/bin/env bash

# ================================
# CyberMail Pro Linux Installer
# ================================

set -e

# Colors for terminal output
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
CYAN="\033[0;36m"
NC="\033[0m"

function echo_status() {
    local color="$2"
    echo -e "${color}[$(date +%H:%M:%S)] $1${NC}"
}

# =========================
# Step 0: Determine install path
# =========================
if [ "$(id -u)" -eq 0 ]; then
    INSTALL_PATH="/usr/local/bin/cybermail"
    echo_status "Running as root: system-wide installation" $CYAN
else
    INSTALL_PATH="$HOME/bin/cybermail"
    mkdir -p "$HOME/bin"
    echo_status "Running as normal user: installing to $HOME/bin" $CYAN
fi

# =========================
# Step 1: Check Python 3.10+
# =========================
if command -v python3 >/dev/null 2>&1; then
    PYTHON_VER=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    PYTHON_MAJOR=$(echo "$PYTHON_VER" | cut -d. -f1)
    PYTHON_MINOR=$(echo "$PYTHON_VER" | cut -d. -f2)
    if [ "$PYTHON_MAJOR" -lt 3 ] || { [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]; }; then
        echo_status "Python 3.10+ required, found $PYTHON_VER" $YELLOW
        echo_status "Please install Python 3.10+ and re-run this installer." $RED
        exit 1
    else
        echo_status "Python $PYTHON_VER detected ✅" $GREEN
    fi
else
    echo_status "Python3 not found. Please install Python 3.10+ first." $RED
    exit 1
fi

# =========================
# Step 2: Check Git
# =========================
if ! command -v git >/dev/null 2>&1; then
    echo_status "Git not found. Please install Git before continuing." $RED
    exit 1
else
    echo_status "Git detected ✅" $GREEN
fi

# =========================
# Step 3: Clone repository
# =========================
TMP_DIR=$(mktemp -d)
REPO_URL="https://github.com/Gin69x/CyberMail-Pro.git"
echo_status "Cloning repository into temporary directory..." $CYAN
git clone "$REPO_URL" "$TMP_DIR"

# Copy files to target installation folder
TARGET_DIR="$HOME/.cybermail_pro"
mkdir -p "$TARGET_DIR"
cp -r "$TMP_DIR/"* "$TARGET_DIR/"
rm -rf "$TMP_DIR"
echo_status "Project files copied to $TARGET_DIR ✅" $GREEN

# =========================
# Step 4: Install Python dependencies
# =========================
echo_status "Installing Python dependencies..." $CYAN
python3 -m pip install --upgrade pip --quiet
python3 -m pip install -r "$TARGET_DIR/requirements.txt" --quiet
echo_status "Dependencies installed ✅" $GREEN

# =========================
# Step 5: Create helper files if missing
# =========================
# working_proxies.txt
if [ ! -f "$TARGET_DIR/working_proxies.txt" ]; then
    cat > "$TARGET_DIR/working_proxies.txt" <<EOL
# CyberMail Pro Proxy List
# Add one proxy per line (ip:port)
# Example:
# 127.0.0.1:8080
EOL
    echo_status "working_proxies.txt created ✅" $GREEN
fi

# accounts.txt
if [ ! -f "$TARGET_DIR/accounts.txt" ]; then
    touch "$TARGET_DIR/accounts.txt"
    echo_status "accounts.txt created ✅" $GREEN
fi

# logs directory
mkdir -p "$TARGET_DIR/logs"

# config directory
mkdir -p "$TARGET_DIR/config"
cat > "$TARGET_DIR/config/installation.json" <<EOL
{
    "installation_date": "$(date '+%Y-%m-%d %H:%M:%S')",
    "installation_path": "$TARGET_DIR",
    "version": "2.1.0",
    "auto_update": true,
    "first_run": true
}
EOL
echo_status "Configuration files created ✅" $GREEN

# =========================
# Step 6: Install as command
# =========================
# Copy this script itself as 'cybermail' for system-wide/user-wide execution
if [ "$(id -u)" -eq 0 ]; then
    BIN_PATH="/usr/local/bin/cybermail"
else
    BIN_PATH="$HOME/bin/cybermail"
    # Ensure ~/bin is in PATH
    if ! echo "$PATH" | grep -q "$HOME/bin"; then
        echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
        if [ -n "$FISH_VERSION" ]; then
            echo 'set -gx PATH $HOME/bin $PATH' >> ~/.config/fish/config.fish
        fi
        echo_status "Added ~/bin to PATH. Restart terminal or run 'source ~/.bashrc'" $YELLOW
    fi
fi

# Create launcher
cat > "$BIN_PATH" <<EOL
#!/usr/bin/env bash
python3 "$TARGET_DIR/main.py" "\$@"
EOL

chmod +x "$BIN_PATH"
echo_status "Installer registered as command: cybermail ✅" $GREEN

# =========================
# Step 7: Completion message
# =========================
echo -e "${CYAN}
╔════════════════════════════════╗
║  CyberMail Pro Installation ✅  ║
╠════════════════════════════════╣
║ Run anywhere: cybermail         ║
║ Project location: $TARGET_DIR ║
╚════════════════════════════════╝
${NC}"

echo_status "You can now run 'cybermail' from any terminal." $GREEN
