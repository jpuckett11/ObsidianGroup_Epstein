#!/bin/bash
# Download and install Obsidian for Linux
# Run: chmod +x get-obsidian.sh && ./get-obsidian.sh

echo "=== Obsidian Vault Viewer - Linux Installer ==="
echo ""

# Detect architecture
ARCH=$(uname -m)
if [ "$ARCH" = "x86_64" ]; then
    echo "Detected: x86_64 Linux"
    URL="https://github.com/obsidianmd/obsidian-releases/releases/latest/download/Obsidian.AppImage"
    OUT="Obsidian.AppImage"
elif [ "$ARCH" = "aarch64" ]; then
    echo "Detected: ARM64 Linux"
    URL="https://github.com/obsidianmd/obsidian-releases/releases/latest/download/Obsidian-arm64.AppImage"
    OUT="Obsidian-arm64.AppImage"
else
    echo "Unsupported architecture: $ARCH"
    echo "Download manually from https://obsidian.md/download"
    exit 1
fi

echo "Downloading latest Obsidian..."
wget -q --show-progress "$URL" -O "$OUT"
chmod +x "$OUT"

echo ""
echo "=== Installation Complete ==="
echo "Run with: ./$OUT"
echo ""
echo "To open the investigation vault:"
echo "  1. Launch Obsidian"
echo "  2. Click 'Open folder as vault'"
echo "  3. Select the 'obsidian-vault' folder from this repository"
echo ""
echo "The vault contains interconnected research files with cross-references."
echo "Use the Graph View (Ctrl+G) to visualize connections between entities."
