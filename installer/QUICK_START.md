# Quick Reference: Building MSI Installer

## Prerequisites
1. Install WiX Toolset: `winget install WiXToolset.WiX`
2. Build the .exe: `build_exe.bat`

## Build MSI
```cmd
build_msi.bat
```

## Output
- **Installer:** `installer\BulkFileRenamer.msi`
- **Size:** ~10-20MB
- **Type:** Offline installer

## Installation Features
- ✅ Installs to Program Files
- ✅ Desktop shortcut
- ✅ Start Menu shortcut
- ✅ Uninstall support
- ✅ Add/Remove Programs entry

## Test Installation
1. Double-click `BulkFileRenamer.msi`
2. Follow installation wizard
3. Launch from Desktop or Start Menu

## Uninstall
- Settings → Apps → Bulk File Renamer → Uninstall
- Or: Start Menu → Uninstall Bulk File Renamer

## Customization
Edit `installer\BulkFileRenamer.wxs`:
- Product name (line 19)
- Version (line 21)
- Manufacturer (line 22)

## Troubleshooting
- **WiX not found:** Add to PATH: `C:\Program Files (x86)\WiX Toolset v3.11\bin`
- **.exe not found:** Run `build_exe.bat` first
- **Icon missing:** Run `python create_icon.py`

## Full Documentation
See: `installer\README_INSTALLER.md`
