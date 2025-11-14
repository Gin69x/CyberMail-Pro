#!/usr/bin/env bash

# CyberMail Pro Installer for Linux
# =================================

set -e

INSTALL_PATH="$HOME/CyberMail-Pro"
GITHUB_REPO="https://github.com/Gin69x/CyberMail-Pro"

GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[1;33m"
CYAN="\033[0;36m"
NC="\033[0m"

function status {
    echo -e "${CYAN}[$(date +'%H:%M:%S')] $1${NC}"
}

function success {
    echo -e "${GREEN}[$(date +'%H:%M:%S')] $1${NC}"
}

function warn {
    echo -e "${YELLOW}[$(date +'%H:%M:%S')] $1${NC}"
}

function error {
    echo -e "${RED}[$(date +'%H:%M:%S')] $1${NC}"
}

# 1. Check Python
status "Checking Python installation..."
if command -v python3 &>/dev/null; then
    PYTHON_VERSION=$(python3 --version)
    success "Python found: $PYTHON_VERSION"
else
    error "Python3 is not installed. Install it with your package manager."
    exit 1
fi

# 2. Check pip
status "Checking pip..."
if ! python3 -m pip --version &>/dev/null; then
    warn "pip not found. Installing..."
    python3 -m ensurepip --upgrade
    python3 -m pip install --upgrade pip
else
    success "pip is installed"
fi

# 3. Check Git
status "Checking Git..."
if ! command -v git &>/dev/null; then
    error "Git is not installed. Install it with your package manager."
    exit 1
else
    success "Git found"
fi

# 4. Create installation directory
status "Creating installation directory at $INSTALL_PATH..."
if [ -d "$INSTALL_PATH" ]; then
    warn "Existing installation detected, removing..."
    rm -rf "$INSTALL_PATH"
fi
mkdir -p "$INSTALL_PATH"
success "Directory created"

# 5. Clone repository
status "Cloning CyberMail Pro repository..."
git clone "$GITHUB_REPO.git" "$INSTALL_PATH" || {
    error "Git clone failed. Check your internet connection."
    exit 1
}
success "Repository cloned"

# 6. Install Python dependencies
status "Installing Python dependencies..."
cd "$INSTALL_PATH"
if [ -f "requirements.txt" ]; then
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt
else
    warn "requirements.txt not found, installing critical dependencies manually"
    python3 -m pip install requests rich colorama urllib3 certifi
fi
success "Dependencies installed"

# 7. Create project files if missing
status "Creating supporting files..."
[ ! -f "working_proxies.txt" ] && cat > working_proxies.txt <<EOL
# Add your proxy servers here (one per line)
# Format: ip:port or host:port
# Example:
# 127.0.0.1:8080
EOL

[ ! -f "accounts.txt" ] && touch accounts.txt

[ ! -d "logs" ] && mkdir logs
[ ! -d "config" ] && mkdir config

cat > config/installation.json <<EOL
{
  "installation_date": "$(date +'%Y-%m-%d %H:%M:%S')",
  "installation_path": "$INSTALL_PATH",
  "version": "2.1.0",
  "auto_update": true,
  "first_run": true
}
EOL
success "Project files created"

# 8. Test installation
status "Testing installation..."
python3 -c "import requests, rich, colorama, urllib3, certifi" &>/dev/null || {
    warn "Some Python modules failed to import, check installation"
}

[ -f "main.py" ] || warn "main.py not found. The program may not run"

success "Installation completed!"

echo -e "${CYAN}Run CyberMail Pro:${NC}"
echo "cd $INSTALL_PATH && python3 main.py"
