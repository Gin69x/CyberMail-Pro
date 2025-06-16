# install.ps1 - CyberMail Pro Installer
# ================================

param(
    [string]$InstallPath = "$env:USERPROFILE\CyberMail-Pro",
    [string]$GitHubRepo = "https://github.com/yourusername/cybermail-pro"
)

# Colors for terminal output
$Green = "Green"
$Red = "Red"
$Yellow = "Yellow"
$Cyan = "Cyan"

function Write-Status {
    param([string]$Message, [string]$Color = "White")
    Write-Host "[$((Get-Date).ToString('HH:mm:ss'))] $Message" -ForegroundColor $Color
}

function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Install-Python {
    Write-Status "Checking Python installation..." -Color $Cyan
    
    try {
        $pythonVersion = python --version 2>&1
        if ($pythonVersion -match "Python 3\.1[0-9]") {
            Write-Status "Python 3.10+ found: $pythonVersion" -Color $Green
            
            # Check if pip is available
            try {
                python -m pip --version | Out-Null
                Write-Status "pip is available" -Color $Green
            }
            catch {
                Write-Status "pip not found, installing..." -Color $Yellow
                # Try to install pip
                python -m ensurepip --upgrade
            }
            
            return $true
        }
    }
    catch {
        Write-Status "Python not found in PATH" -Color $Yellow
    }
    
    Write-Status "Installing Python 3.11..." -Color $Yellow
    
    # Check if winget is available for faster installation
    try {
        winget --version | Out-Null
        Write-Status "Using winget for Python installation..." -Color $Cyan
        
        winget install --id Python.Python.3.11 -e --source winget --silent --accept-source-agreements --accept-package-agreements
        
        # Refresh PATH
        $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
        
        # Verify installation
        Start-Sleep 3
        $pythonVersion = python --version 2>&1
        if ($pythonVersion -match "Python 3\.1[0-9]") {
            Write-Status "Python installed via winget: $pythonVersion" -Color $Green
            return $true
        }
    }
    catch {
        Write-Status "winget not available, using direct download..." -Color $Yellow
    }
    
    # Fallback to direct download
    $pythonUrl = "https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe"
    $pythonInstaller = "$env:TEMP\python-installer.exe"
    
    try {
        Write-Status "Downloading Python installer..." -Color $Cyan
        Invoke-WebRequest -Uri $pythonUrl -OutFile $pythonInstaller -UseBasicParsing
        
        Write-Status "Installing Python (this may take a few minutes)..." -Color $Cyan
        Start-Process -FilePath $pythonInstaller -ArgumentList "/quiet", "InstallAllUsers=0", "PrependPath=1", "Include_test=0", "Include_pip=1" -Wait
        Remove-Item $pythonInstaller -Force
        
        # Refresh PATH
        $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
        
        # Wait a moment for installation to complete
        Start-Sleep 3
        
        # Verify installation
        $pythonVersion = python --version 2>&1
        if ($pythonVersion -match "Python 3\.1[0-9]") {
            Write-Status "Python installed successfully: $pythonVersion" -Color $Green
            return $true
        } else {
            Write-Status "Python installation verification failed" -Color $Red
            return $false
        }
    }
    catch {
        Write-Status "Failed to install Python: $($_.Exception.Message)" -Color $Red
        Write-Status "Please install Python manually from https://python.org" -Color $Yellow
        return $false
    }
}

function Install-Git {
    Write-Status "Checking Git installation..." -Color $Cyan
    
    try {
        git --version | Out-Null
        Write-Status "Git found" -Color $Green
        return $true
    }
    catch {
        Write-Status "Git not found, installing..." -Color $Yellow
        
        # Install Git via winget if available
        try {
            winget install --id Git.Git -e --source winget --silent
            Write-Status "Git installed successfully" -Color $Green
            return $true
        }
        catch {
            Write-Status "Please install Git manually from https://git-scm.com/" -Color $Red
            return $false
        }
    }
}

function New-CyberMailDirectory {
    Write-Status "Creating installation directory: $InstallPath" -Color $Cyan
    
    if (Test-Path $InstallPath) {
        Write-Status "Removing existing installation..." -Color $Yellow
        Remove-Item $InstallPath -Recurse -Force
    }
    
    New-Item -ItemType Directory -Path $InstallPath -Force | Out-Null
    Write-Status "Directory created successfully" -Color $Green
}

function Get-CyberMailFiles {
    Write-Status "Downloading CyberMail Pro from GitHub..." -Color $Cyan
    
    try {
        Set-Location $InstallPath
        git clone $GitHubRepo.git .
        Write-Status "Repository cloned successfully" -Color $Green
        return $true
    }
    catch {
        Write-Status "Failed to clone repository: $($_.Exception.Message)" -Color $Red
        return $false
    }
}

function Install-Dependencies {
    Write-Status "Installing Python dependencies..." -Color $Cyan
    
    try {
        Set-Location $InstallPath
        
        # Create requirements.txt if it doesn't exist
        if (-not (Test-Path "requirements.txt")) {
            @"
requests>=2.31.0
rich>=13.7.0
pywin32>=306; sys_platform == "win32"
colorama>=0.4.6
urllib3>=2.0.0
certifi>=2023.7.22
"@ | Out-File -FilePath "requirements.txt" -Encoding UTF8
        }
        
        Write-Status "Upgrading pip..." -Color $Cyan
        python -m pip install --upgrade pip --quiet
        
        Write-Status "Installing core dependencies..." -Color $Cyan
        
        # Install dependencies one by one with progress
        $dependencies = @(
            "requests>=2.31.0",
            "rich>=13.7.0", 
            "colorama>=0.4.6",
            "urllib3>=2.0.0",
            "certifi>=2023.7.22"
        )
        
        # Add Windows-specific dependency
        if ($env:OS -eq "Windows_NT") {
            $dependencies += "pywin32>=306"
        }
        
        foreach ($dep in $dependencies) {
            $depName = ($dep -split ">=|==|~=")[0]
            Write-Status "Installing $depName..." -Color $Yellow
            
            $result = python -m pip install $dep --quiet --no-warn-script-location 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Status "✓ $depName installed" -Color $Green
            } else {
                Write-Status "⚠ $depName installation warning (may still work): $result" -Color $Yellow
            }
        }
        
        # Fallback: try requirements.txt if individual installs had issues
        Write-Status "Verifying installation with requirements.txt..." -Color $Cyan
        python -m pip install -r requirements.txt --quiet --no-warn-script-location
        
        Write-Status "All dependencies installed successfully" -Color $Green
        return $true
    }
    catch {
        Write-Status "Failed to install dependencies: $($_.Exception.Message)" -Color $Red
        Write-Status "Attempting fallback installation..." -Color $Yellow
        
        # Fallback: try basic installation without version constraints
        try {
            python -m pip install requests rich colorama urllib3 certifi --quiet
            if ($env:OS -eq "Windows_NT") {
                python -m pip install pywin32 --quiet
            }
            Write-Status "Fallback installation completed" -Color $Green
            return $true
        }
        catch {
            Write-Status "Fallback installation also failed: $($_.Exception.Message)" -Color $Red
            return $false
        }
    }
}

function New-BatchFile {
    Write-Status "Creating batch launcher..." -Color $Cyan
    
    $batchContent = @"
@echo off
cd /d "$InstallPath"
python main.py %*
pause
"@
    
    $batchPath = "$InstallPath\cybermail.bat"
    $batchContent | Out-File -FilePath $batchPath -Encoding ASCII
    
    Write-Status "Batch file created: $batchPath" -Color $Green
}

function Add-ToPath {
    Write-Status "Adding CyberMail to system PATH..." -Color $Cyan
    
    try {
        $currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
        
        if ($currentPath -notlike "*$InstallPath*") {
            $newPath = "$currentPath;$InstallPath"
            [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
            
            # Update current session PATH
            $env:PATH += ";$InstallPath"
            
            Write-Status "Added to PATH successfully" -Color $Green
        } else {
            Write-Status "Already in PATH" -Color $Green
        }
    }
    catch {
        Write-Status "Failed to add to PATH: $($_.Exception.Message)" -Color $Red
    }
}

function Test-Installation {
    Write-Status "Testing installation..." -Color $Cyan
    
    try {
        Set-Location $InstallPath
        
        # Test each dependency individually
        $dependencies = @{
            "requests" = "HTTP library"
            "rich" = "Terminal UI library"
            "colorama" = "Color support"
            "urllib3" = "HTTP client"
            "certifi" = "SSL certificates"
        }
        
        # Add Windows-specific test
        if ($env:OS -eq "Windows_NT") {
            $dependencies["win32api"] = "Windows API (pywin32)"
        }
        
        Write-Status "Testing individual dependencies..." -Color $Cyan
        $allPassed = $true
        
        foreach ($dep in $dependencies.Keys) {
            try {
                $testResult = python -c "import $dep; print('OK')" 2>&1
                if ($testResult -like "*OK*") {
                    Write-Status "✓ $($dependencies[$dep]) - OK" -Color $Green
                } else {
                    Write-Status "✗ $($dependencies[$dep]) - Failed" -Color $Red
                    $allPassed = $false
                }
            }
            catch {
                Write-Status "✗ $($dependencies[$dep]) - Error: $($_.Exception.Message)" -Color $Red
                $allPassed = $false
            }
        }
        
        if ($allPassed) {
            Write-Status "All dependency tests passed!" -Color $Green
            
            # Test if main script exists and can be imported
            if (Test-Path "main.py") {
                Write-Status "✓ Main script found" -Color $Green
                
                # Try to validate Python syntax
                $syntaxTest = python -m py_compile main.py 2>&1
                if ($LASTEXITCODE -eq 0) {
                    Write-Status "✓ Python syntax validation passed" -Color $Green
                } else {
                    Write-Status "⚠ Python syntax warning: $syntaxTest" -Color $Yellow
                }
            } else {
                Write-Status "⚠ main.py not found - will be downloaded from repository" -Color $Yellow
            }
            
            return $true
        } else {
            Write-Status "Some dependencies failed - installation may have issues" -Color $Yellow
            return $false
        }
    }
    catch {
        Write-Status "Installation test error: $($_.Exception.Message)" -Color $Red
        return $false
    }
}

function Start-CyberMail {
    Write-Status "Launching CyberMail Pro..." -Color $Green
    
    try {
        Set-Location $InstallPath
        python main.py
    }
    catch {
        Write-Status "Failed to launch CyberMail: $($_.Exception.Message)" -Color $Red
    }
}

# Main installation process
Write-Host @"
╔══════════════════════════════════════════════╗
║         CyberMail Pro Installer v2.1         ║
║     Enterprise Email Management Platform     ║
╚══════════════════════════════════════════════╝
"@ -ForegroundColor $Cyan

Write-Status "Starting installation process..." -Color $Green

# Check if running as administrator for system-wide installation
if (-not (Test-Administrator)) {
    Write-Status "Running as standard user (recommended)" -Color $Yellow
}

# Step 1: Install Python
if (-not (Install-Python)) {
    Write-Status "Installation failed: Python installation required" -Color $Red
    exit 1
}

# Step 2: Install Git
if (-not (Install-Git)) {
    Write-Status "Installation failed: Git installation required" -Color $Red
    exit 1
}

# Step 3: Create directory
New-CyberMailDirectory

# Step 4: Download files
if (-not (Get-CyberMailFiles)) {
    Write-Status "Installation failed: Could not download files" -Color $Red
    exit 1
}

# Step 5: Install dependencies
Write-Status "Installing Python dependencies..." -Color $Cyan
if (-not (Install-Dependencies)) {
    Write-Status "Warning: Some dependencies may not have installed correctly" -Color $Yellow
    Write-Status "Continuing with installation..." -Color $Yellow
    
    # Try manual installation of critical dependencies
    Write-Status "Attempting manual installation of critical packages..." -Color $Yellow
    try {
        python -m pip install requests --quiet
        python -m pip install rich --quiet
        python -m pip install colorama --quiet
        Write-Status "Critical dependencies installed" -Color $Green
    }
    catch {
        Write-Status "Manual installation failed - some features may not work" -Color $Red
    }
}

# Step 6: Create batch file
New-BatchFile

# Step 7: Add to PATH
Add-ToPath

# Step 8: Test installation
if (-not (Test-Installation)) {
    Write-Status "Installation completed with warnings" -Color $Yellow
} else {
    Write-Status "Installation completed successfully!" -Color $Green
}

Write-Host @"

╔══════════════════════════════════════════════╗
║              Installation Complete           ║
╠══════════════════════════════════════════════╣
║  Usage:                                      ║
║    Command Line: cybermail                   ║
║    Direct Path:  $InstallPath                ║
║                                              ║
║  Restart your terminal to use 'cybermail'    ║
╚══════════════════════════════════════════════╝
"@ -ForegroundColor $Green

# Ask if user wants to launch now
$launch = Read-Host "`nLaunch CyberMail Pro now? (y/N)"
if ($launch -eq 'y' -or $launch -eq 'Y') {
    Start-CyberMail
}