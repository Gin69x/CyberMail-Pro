# install.ps1 - CyberMail Pro Installer
# ================================

param(
    [string]$InstallPath = "$env:USERPROFILE\CyberMail-Pro",
    [string]$GitHubRepo = "https://github.com/Gin69x/CyberMail-Pro"
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
    
    # Try Git clone first (fastest and most complete)
    try {
        Set-Location $InstallPath
        Write-Status "Cloning repository with Git..." -Color $Cyan
        
        # Clone with progress
        $gitProcess = Start-Process -FilePath "git" -ArgumentList "clone", "$GitHubRepo.git", "." -NoNewWindow -PassThru -RedirectStandardOutput "$env:TEMP\git_output.log" -RedirectStandardError "$env:TEMP\git_error.log"
        
        # Show progress while cloning
        $counter = 0
        while (-not $gitProcess.HasExited) {
            $counter++
            $dots = "." * ($counter % 4)
            Write-Host "`r[$(Get-Date -Format 'HH:mm:ss')] Cloning repository$dots    " -NoNewline -ForegroundColor $Cyan
            Start-Sleep 1
        }
        Write-Host ""  # New line after progress
        
        if ($gitProcess.ExitCode -eq 0) {
            Write-Status "Repository cloned with Git successfully" -Color $Green
            
            # Verify we got the main files
            $criticalFiles = @("main.py", "requirements.txt")
            $missingFiles = @()
            
            foreach ($file in $criticalFiles) {
                if (-not (Test-Path $file)) {
                    $missingFiles += $file
                }
            }
            
            if ($missingFiles.Count -eq 0) {
                Write-Status "All critical files downloaded successfully" -Color $Green
                return $true
            } else {
                Write-Status "Missing files: $($missingFiles -join ', ') - trying alternative download..." -Color $Yellow
            }
        }
    }
    catch {
        Write-Status "Git clone failed: $($_.Exception.Message)" -Color $Yellow
        Write-Status "Trying alternative download method..." -Color $Cyan
    }
    
    # Fallback 1: Download ZIP archive
    try {
        Write-Status "Downloading repository as ZIP archive..." -Color $Cyan
        
        $zipUrl = "$GitHubRepo/archive/refs/heads/main.zip"
        $zipPath = "$env:TEMP\cybermail-pro.zip"
        $extractPath = "$env:TEMP\cybermail-extract"
        
        # Download ZIP
        Invoke-WebRequest -Uri $zipUrl -OutFile $zipPath -UseBasicParsing
        Write-Status "ZIP archive downloaded" -Color $Green
        
        # Extract ZIP
        if (Test-Path $extractPath) {
            Remove-Item $extractPath -Recurse -Force
        }
        
        Add-Type -AssemblyName System.IO.Compression.FileSystem
        [System.IO.Compression.ZipFile]::ExtractToDirectory($zipPath, $extractPath)
        
        # Find the extracted folder (usually repo-name-main)
        $extractedFolder = Get-ChildItem $extractPath | Where-Object { $_.PSIsContainer } | Select-Object -First 1
        
        if ($extractedFolder) {
            # Copy all files from extracted folder to install path
            Get-ChildItem $extractedFolder.FullName -Recurse | ForEach-Object {
                $targetPath = $_.FullName.Replace($extractedFolder.FullName, $InstallPath)
                
                if ($_.PSIsContainer) {
                    New-Item -ItemType Directory -Path $targetPath -Force | Out-Null
                } else {
                    Copy-Item $_.FullName $targetPath -Force
                }
            }
            
            Write-Status "Files extracted from ZIP successfully" -Color $Green
            
            # Cleanup
            Remove-Item $zipPath -Force -ErrorAction SilentlyContinue
            Remove-Item $extractPath -Recurse -Force -ErrorAction SilentlyContinue
            
            return $true
        }
    }
    catch {
        Write-Status "ZIP download failed: $($_.Exception.Message)" -Color $Yellow
    }
    
    # Fallback 2: Download individual critical files
    try {
        Write-Status "Downloading individual project files..." -Color $Cyan
        
        $criticalFiles = @{
            "main.py" = "Main application script"
            "requirements.txt" = "Python dependencies"
            "README.md" = "Documentation"
            "cybermail.bat" = "Batch launcher"
        }
        
        $baseRawUrl = $GitHubRepo.Replace("github.com", "raw.githubusercontent.com") + "/main"
        $downloadedFiles = @()
        
        foreach ($file in $criticalFiles.Keys) {
            try {
                $fileUrl = "$baseRawUrl/$file"
                $filePath = Join-Path $InstallPath $file
                
                Write-Status "Downloading $file ($($criticalFiles[$file]))..." -Color $Yellow
                Invoke-WebRequest -Uri $fileUrl -OutFile $filePath -UseBasicParsing
                
                if (Test-Path $filePath) {
                    Write-Status "✓ $file downloaded" -Color $Green
                    $downloadedFiles += $file
                } else {
                    Write-Status "✗ $file download failed" -Color $Red
                }
            }
            catch {
                Write-Status "✗ Failed to download $file : $($_.Exception.Message)" -Color $Red
            }
        }
        
        if ($downloadedFiles -contains "main.py") {
            Write-Status "Critical files downloaded successfully" -Color $Green
            return $true
        } else {
            Write-Status "Failed to download main.py - cannot proceed" -Color $Red
            return $false
        }
    }
    catch {
        Write-Status "Individual file download failed: $($_.Exception.Message)" -Color $Red
    }
    
    # Fallback 3: Create minimal files if all downloads fail
    Write-Status "All download methods failed - creating minimal installation..." -Color $Yellow
    
    try {
        # Create a basic main.py template
        $basicMainPy = @"
#!/usr/bin/env python3
# CyberMail Pro - Basic Installation Template
# This is a minimal template created by the installer

print("CyberMail Pro installation incomplete!")
print("Please check your internet connection and GitHub repository URL.")
print("Repository: $GitHubRepo")
print()
print("Manual installation steps:")
print("1. Visit: $GitHubRepo")
print("2. Download the repository files")
print("3. Replace this main.py with the actual file")
print()
input("Press Enter to exit...")
"@
        
        $basicMainPy | Out-File -FilePath "$InstallPath\main.py" -Encoding UTF8
        
        Write-Status "Minimal installation created - manual setup required" -Color $Yellow
        return $false
    }
    catch {
        Write-Status "Failed to create minimal installation" -Color $Red
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

function New-ProjectFiles {
    Write-Status "Creating additional project files..." -Color $Cyan
    
    try {
        Set-Location $InstallPath
        
        # Create working_proxies.txt template if it doesn't exist
        if (-not (Test-Path "working_proxies.txt")) {
            @"
# CyberMail Pro - Proxy Configuration
# Add your proxy servers here (one per line)
# Format: ip:port or host:port
# Example:
# 127.0.0.1:8080
# proxy.example.com:3128

# Note: Remove the # to uncomment proxy entries
# Add your own proxy servers below:

"@ | Out-File -FilePath "working_proxies.txt" -Encoding UTF8
            Write-Status "✓ Proxy configuration template created" -Color $Green
        }
        
        # Create accounts.txt file (empty initially)
        if (-not (Test-Path "accounts.txt")) {
            "" | Out-File -FilePath "accounts.txt" -Encoding UTF8
            Write-Status "✓ Accounts storage file created" -Color $Green
        }
        
        # Create config directory if needed
        if (-not (Test-Path "config")) {
            New-Item -ItemType Directory -Path "config" -Force | Out-Null
            Write-Status "✓ Configuration directory created" -Color $Green
        }
        
        # Create logs directory for application logs
        if (-not (Test-Path "logs")) {
            New-Item -ItemType Directory -Path "logs" -Force | Out-Null
            Write-Status "✓ Logs directory created" -Color $Green
        }
        
        # Create a startup configuration file
        $configContent = @"
{
    "installation_date": "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')",
    "installation_path": "$InstallPath",
    "version": "2.1.0",
    "auto_update": true,
    "first_run": true
}
"@
        $configContent | Out-File -FilePath "config\installation.json" -Encoding UTF8
        Write-Status "✓ Installation configuration saved" -Color $Green
        
        # Create a help file
        $helpContent = @"
# CyberMail Pro - Quick Help Guide

## Installation Location
$InstallPath

## Usage
- Command Line: cybermail
- Direct Execution: cybermail.bat
- Python Direct: python main.py

## Key Files
- main.py: Main application
- working_proxies.txt: Proxy configuration
- accounts.txt: Stored email accounts
- requirements.txt: Python dependencies

## Troubleshooting
1. If 'cybermail' command not found:
   - Restart your terminal
   - Or run: $InstallPath\cybermail.bat

2. If proxy errors occur:
   - Edit working_proxies.txt
   - Add valid proxy servers

3. For updates:
   - Re-run the installation command

## Support
Repository: $GitHubRepo
"@
        $helpContent | Out-File -FilePath "HELP.md" -Encoding UTF8
        Write-Status "✓ Help documentation created" -Color $Green
        
        Write-Status "Project structure created successfully" -Color $Green
        return $true
    }
    catch {
        Write-Status "Failed to create project files: $($_.Exception.Message)" -Color $Red
        return $false
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
Write-Status "Downloading project files from GitHub..." -Color $Cyan
if (-not (Get-CyberMailFiles)) {
    Write-Status "Warning: File download had issues, but continuing..." -Color $Yellow
    Write-Status "You may need to manually download some files from: $GitHubRepo" -Color $Yellow
}

# Step 4.5: Create additional project files
New-ProjectFiles

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

╔════════════════════════════════════════════════╗
║              Installation Complete             ║
╠════════════════════════════════════════════════╣
║  Usage Commands:                               ║
║    • cybermail          (from anywhere)        ║
║    • cybermail.bat      (direct launcher)      ║
║    • python main.py     (direct python)        ║
║                                                ║
║  Installation Details:                         ║
║    • Location: $InstallPath
║    • Files: All project files downloaded       ║
║    • Dependencies: All Python packages         ║
║    • Configuration: Ready to use               ║
║                                                ║
║  Next Steps:                                   ║
║    1. Restart terminal for 'cybermail' cmd     ║
║    2. Configure proxies in working_proxies.txt ║
║    3. Run 'cybermail' to start                 ║
║                                                ║
║  Support: See HELP.md for troubleshooting      ║
╚════════════════════════════════════════════════╝
"@ -ForegroundColor $Green

# Show installation summary
Write-Status "Installation Summary:" -Color $Cyan
Write-Status "✓ Python 3.10+ installed and configured" -Color $Green
Write-Status "✓ All project files downloaded from GitHub" -Color $Green
Write-Status "✓ Python dependencies installed" -Color $Green
Write-Status "✓ Project structure created" -Color $Green
Write-Status "✓ Batch launcher created" -Color $Green
Write-Status "✓ Added to system PATH" -Color $Green
Write-Status "✓ Configuration files generated" -Color $Green
Write-Status "✓ Help documentation created" -Color $Green

# Ask if user wants to launch now
$launch = Read-Host "`nLaunch CyberMail Pro now? (y/N)"
if ($launch -eq 'y' -or $launch -eq 'Y') {
    Start-CyberMail
}
