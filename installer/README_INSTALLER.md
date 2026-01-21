# MSI Installer Setup Guide

## Overview

This directory contains the WiX Toolset configuration for creating a professional Windows MSI installer for the Bulk File Renamer application.

---

## Prerequisites

### 1. WiX Toolset Installation

**Option A: Using winget (Recommended)**
```cmd
winget install WiXToolset.WiX
```

**Option B: Manual Download**
1. Visit: https://wixtoolset.org/releases/
2. Download WiX Toolset 3.11 or later
3. Run the installer
4. Add WiX bin folder to PATH:
   - Default location: `C:\Program Files (x86)\WiX Toolset v3.11\bin`
   - Add to System Environment Variables → PATH

**Verify Installation:**
```cmd
candle.exe -?
light.exe -?
```

If these commands show help text, WiX is installed correctly.

### 2. Application Executable

The MSI installer requires the built application executable:
```cmd
# Build the .exe first
build_exe.bat
```

This creates: `dist\BulkFileRenamer.exe`

---

## Quick Start

### Build MSI Installer

**One Command:**
```cmd
build_msi.bat
```

This will:
1. ✅ Check WiX Toolset installation
2. ✅ Verify executable exists
3. ✅ Compile WiX source (.wxs → .wixobj)
4. ✅ Link and create MSI installer
5. ✅ Output: `installer\BulkFileRenamer.msi`

---

## Manual Build Process

If you prefer to build manually:

### Step 1: Navigate to installer directory
```cmd
cd installer
```

### Step 2: Compile WiX source
```cmd
candle.exe BulkFileRenamer.wxs
```

This creates: `BulkFileRenamer.wixobj`

### Step 3: Link and create MSI
```cmd
light.exe -ext WixUIExtension -cultures:en-us BulkFileRenamer.wixobj
```

This creates: `BulkFileRenamer.msi`

---

## File Structure

```
installer/
├── BulkFileRenamer.wxs     # WiX configuration (XML)
├── License.rtf             # License agreement for installer UI
├── README_INSTALLER.md     # This file
├── BulkFileRenamer.wixobj  # Compiled object (generated)
├── BulkFileRenamer.wixpdb  # Debug symbols (generated)
└── BulkFileRenamer.msi     # Final installer (generated)
```

---

## Customization

### Change Product Information

Edit `BulkFileRenamer.wxs`:

```xml
<!-- Line 18-22: Product Details -->
<Product 
  Name="Bulk File Renamer"        <!-- Application name -->
  Version="1.0.0.0"                <!-- Version number -->
  Manufacturer="YourName"          <!-- Your name/company -->
  UpgradeCode="...">               <!-- Keep same for upgrades -->
```

### Change Installation Location

Default: `C:\Program Files\Bulk File Renamer`

To change, edit line 68:
```xml
<Directory Id="INSTALLFOLDER" Name="Bulk File Renamer">
```

### Add More Files

Edit lines 89-110 to add additional components:

```xml
<Component Id="MyNewFile" Guid="UNIQUE-GUID-HERE">
  <File 
    Id="MyFileID" 
    Name="myfile.txt" 
    Source="..\myfile.txt" 
    KeyPath="yes" />
</Component>
```

Then reference in ComponentGroup:
```xml
<ComponentGroup Id="ProductComponents">
  <ComponentRef Id="MainExecutable" />
  <ComponentRef Id="Documentation" />
  <ComponentRef Id="MyNewFile" />  <!-- Add this -->
</ComponentGroup>
```

### Generate New GUIDs

GUIDs must be unique. Generate new ones:

**PowerShell:**
```powershell
[guid]::NewGuid()
```

**Online:** https://www.guidgenerator.com/

---

## Installer Features

### What the MSI Installer Does

✅ **Installation**
- Installs to: `C:\Program Files\Bulk File Renamer\`
- Copies: `BulkFileRenamer.exe`
- Copies: `README.md` (documentation)
- Registers application in Windows

✅ **Shortcuts**
- Desktop: `Bulk File Renamer`
- Start Menu: `Bulk File Renamer`
- Start Menu: `Uninstall Bulk File Renamer`

✅ **Add/Remove Programs**
- Appears in Windows Settings → Apps
- Shows application icon
- Supports clean uninstallation
- Displays version, publisher, help link

✅ **Upgrade Support**
- Detects previous installations
- Prevents downgrade (newer → older)
- Allows upgrade (older → newer)

---

## Testing the Installer

### Install
1. Double-click `BulkFileRenamer.msi`
2. Follow installation wizard
3. Click "Install"
4. Check installation:
   - Desktop shortcut appears
   - Start Menu entry appears
   - Files in `C:\Program Files\Bulk File Renamer\`

### Verify Installation
```cmd
# Check if installed
dir "C:\Program Files\Bulk File Renamer"

# Run from command line
"C:\Program Files\Bulk File Renamer\BulkFileRenamer.exe"
```

### Uninstall

**Option 1: Control Panel**
1. Open Settings → Apps → Installed apps
2. Find "Bulk File Renamer"
3. Click "Uninstall"
4. Confirm

**Option 2: Start Menu**
1. Start → Bulk File Renamer
2. Click "Uninstall Bulk File Renamer"
3. Confirm

**Option 3: MSI File**
```cmd
# Using the MSI file
msiexec /x BulkFileRenamer.msi

# Or double-click the MSI again and choose "Remove"
```

### Verify Uninstallation
- Desktop shortcut removed
- Start Menu entries removed
- Program Files folder removed
- Registry entries cleaned

---

## Troubleshooting

### Error: "WiX Toolset not found"

**Solution:**
1. Install WiX Toolset (see Prerequisites)
2. Add to PATH: `C:\Program Files (x86)\WiX Toolset v3.11\bin`
3. Restart command prompt
4. Verify: `candle.exe -?`

### Error: "BulkFileRenamer.exe not found"

**Solution:**
1. Run `build_exe.bat` first
2. Verify: `dist\BulkFileRenamer.exe` exists

### Error: "icon.ico not found"

**Solution:**
1. Run `python create_icon.py` to generate icon
2. Or comment out icon references in .wxs file:
   ```xml
   <!-- <Icon Id="AppIcon.ico" Source="..\assets\icon.ico" /> -->
   ```

### Error: "Compilation failed"

**Solution:**
- Check BulkFileRenamer.wxs for XML syntax errors
- Ensure all file paths are correct
- Verify GUIDs are valid format

### Error: "Another version already installed"

**Solution:**
1. Uninstall existing version first
2. Or increment version number in .wxs
3. Or change UpgradeCode (not recommended)

### Warning: "ICE** validation warning"

**Solution:**
- Most ICE warnings can be ignored
- To suppress: `light.exe -sval BulkFileRenamer.wixobj`

---

## Distribution

### Single File Distribution

The generated `BulkFileRenamer.msi` is a **single, standalone installer**:
- ✅ No dependencies
- ✅ Fully offline
- ✅ Self-contained
- ✅ ~10-20MB file size

### Sharing the Installer

1. **Direct Download**
   - Upload to file hosting (Google Drive, Dropbox, etc.)
   - Share download link

2. **GitHub Release**
   - Create GitHub release
   - Attach .msi file as asset
   - Users download from Releases page

3. **College Submission**
   - Include .msi in submission folder
   - Provide installation instructions
   - Include README documentation

---

## Advanced Topics

### Code Signing (Optional)

For production distribution, sign the MSI:

```cmd
# Requires code signing certificate
signtool.exe sign /f mycert.pfx /p password BulkFileRenamer.msi
```

### Custom UI Dialogs

WiX supports custom dialog sequences. See:
- WiX documentation: https://wixtoolset.org/documentation/
- Custom UI tutorial: https://www.firegiant.com/wix/tutorial/

### Localization

Add multiple languages:
```cmd
light.exe -cultures:en-us,fr-fr,de-de BulkFileRenamer.wixobj
```

---

## Resources

- **WiX Tutorial:** https://www.firegiant.com/wix/tutorial/
- **WiX Documentation:** https://wixtoolset.org/documentation/
- **WiX Schema Reference:** http://wixtoolset.org/documentation/manual/v3/xsd/
- **Community Forum:** https://stackoverflow.com/questions/tagged/wix

---

## Version History

- **1.0.0** - Initial MSI installer release
  - Desktop shortcut
  - Start Menu shortcuts
  - Uninstall support
  - Add/Remove Programs integration

---

## Support

For issues with the installer:
1. Check [Troubleshooting](#troubleshooting) section
2. Verify WiX Toolset installation
3. Check build logs for errors
4. Review WiX documentation

---

**Created with WiX Toolset 3.11+**
