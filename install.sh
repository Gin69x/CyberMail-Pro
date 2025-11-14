#!/usr/bin/env bash

set -e

# =====================================
# CyberMail Pro Installer (Linux/Arch)
# =====================================

TARGET_DIR="$HOME/.cybermail_pro"
LAUNCHER="$HOME/.local/bin/cybermail"
REPO="https://github.com/Gin69x/CyberMail-Pro"

echo "[*] Starting CyberMail Pro installation..."

# Step 1: Check for Python
if ! command -v python3 &>/dev/null; then
    echo "[!] Python 3 not found. Please install python3."
    exit 1
fi

PY_VER=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if [[ ${PY_VER%%.*} -lt 3 || ${PY_VER%%.*} -eq 3 && ${PY_VER#*.} -lt 10 ]]; then
    echo "[!] Python 3.10+ required. Found $PY_VER"
    exit 1
fi
echo "[✔] Python $PY_VER detected"

# Step 2: Check for Git
if ! command -v git &>/dev/null; then
    echo "[!] Git not found. Please install git."
    exit 1
fi
echo "[✔] Git detected"

# Step 3: Clone repository
if [[ -d "$TARGET_DIR" ]]; then
    echo "[*] Existing installation found, removing..."
    rm -rf "$TARGET_DIR"
fi

echo "[*] Cloning CyberMail Pro into $TARGET_DIR..."
git clone "$REPO.git" "$TARGET_DIR"

# Step 4: Create virtual environment
echo "[*] Creating Python virtual environment..."
python3 -m venv "$TARGET_DIR/venv"

# Step 5: Activate venv and install dependencies
echo "[*] Installing dependencies inside virtual environment..."
source "$TARGET_DIR/venv/bin/activate"
pip install --upgrade pip

# Install requirements if file exists, fallback to essential packages
if [[ -f "$TARGET_DIR/requirements.txt" ]]; then
    pip install -r "$TARGET_DIR/requirements.txt"
else
    echo "[*] requirements.txt not found, installing essential packages..."
    pip install requests rich colorama urllib3 certifi
fi

# Step 6: Ensure necessary directories/files exist
[[ -f "$TARGET_DIR/working_proxies.txt" ]] || touch "$TARGET_DIR/working_proxies.txt"
[[ -f "$TARGET_DIR/accounts.txt" ]] || touch "$TARGET_DIR/accounts.txt"
[[ -d "$TARGET_DIR/config" ]] || mkdir "$TARGET_DIR/config"
[[ -d "$TARGET_DIR/logs" ]] || mkdir "$TARGET_DIR/logs"

# Create a default config JSON if missing
CONFIG_FILE="$TARGET_DIR/config/installation.json"
if [[ ! -f "$CONFIG_FILE" ]]; then
cat > "$CONFIG_FILE" <<EOF
{
    "installation_date": "$(date '+%Y-%m-%d %H:%M:%S')",
    "installation_path": "$TARGET_DIR",
    "version": "2.1.0",
    "auto_update": true,
    "first_run": true
}
EOF
fi

# Step 7: Create launcher in ~/.local/bin
mkdir -p "$HOME/.local/bin"
cat > "$LAUNCHER" <<EOF
#!/usr/bin/env bash
source "$TARGET_DIR/venv/bin/activate"
python "$TARGET_DIR/main.py" "\$@"
EOF
chmod +x "$LAUNCHER"

echo "[✔] Launcher created at $LAUNCHER"

# Step 8: Optional: Add ~/.local/bin to PATH for current session
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo "[*] Adding ~/.local/bin to PATH for current session..."
    export PATH="$HOME/.local/bin:$PATH"
fi

# Step 9: Finish installation
echo "[✔] Installation complete!"
echo "[*] You can now run CyberMail Pro anywhere using:"
echo "      cybermail"
echo "[*] Make sure ~/.local/bin is in your PATH permanently for future sessions:"
echo "      echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc"

