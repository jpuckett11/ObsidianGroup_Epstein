# Download and install Obsidian for Windows
# Run in PowerShell: .\get-obsidian.ps1

Write-Host "=== Obsidian Vault Viewer - Windows Installer ===" -ForegroundColor Cyan
Write-Host ""

$url = "https://github.com/obsidianmd/obsidian-releases/releases/latest/download/Obsidian.exe"
$out = "$env:TEMP\ObsidianSetup.exe"

Write-Host "Downloading latest Obsidian..."
Invoke-WebRequest -Uri $url -OutFile $out -UseBasicParsing

Write-Host "Running installer..."
Start-Process -FilePath $out -Wait

Write-Host ""
Write-Host "=== Installation Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "To open the investigation vault:"
Write-Host "  1. Launch Obsidian"
Write-Host "  2. Click 'Open folder as vault'"
Write-Host "  3. Select the 'obsidian-vault' folder from this repository"
Write-Host ""
Write-Host "The vault contains interconnected research files with cross-references."
Write-Host "Use the Graph View (Ctrl+G) to visualize connections between entities."
