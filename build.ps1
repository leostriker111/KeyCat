# Construye KeyCat.exe (portable, un solo archivo) con PyInstaller.
# Uso:  ./build.ps1
$ErrorActionPreference = "Stop"

pip install pyinstaller | Out-Null

pyinstaller --noconfirm --clean --onefile --windowed `
    --name KeyCat `
    --icon keycat.ico `
    --add-data "es_50k.txt;." `
    --add-data "en_50k.txt;." `
    --add-data "keycat.ico;." `
    --collect-submodules pystray `
    --hidden-import win32timezone `
    keycat.py

Write-Host "`nListo -> dist/KeyCat.exe" -ForegroundColor Green
