# MSI Installer - README Addendum

## 🔧 Building MSI Installer (Advanced)

For professional distribution, you can create a Windows MSI installer using WiX Toolset.

### Prerequisites

**Install WiX Toolset:**

```cmd
# Option 1: Using winget (recommended)
winget install WiXToolset.WiX

# Option 2: Manual download
# Visit: https://wixtoolset.org/releases/
```

**Verify WiX Installation:**
```cmd
candle.exe -?
light.exe -?
```

### Building the MSI

**Quick Build:**

```cmd
# 1. Build the .exe first
build_exe.bat

# 2. Build the MSI installer
build_msi.bat
```

**Output:**
- `installer\BulkFileRenamer.msi` (~10-20 MB)

### Manual MSI Build

```cmd
# Navigate to installer directory
cd installer

# Compile WiX source
candle.exe BulkFileRenamer.wxs

# Link and create MSI
light.exe -ext WixUIExtension -cultures:en-us BulkFileRenamer.wixobj

# Return to project root
cd ..
```

### MSI Installer Features

The MSI installer provides:

✅ **Professional Installation**
- Installs to: `C:\Program Files\Bulk File Renamer\`
- Installation wizard with license agreement
- Progress indicators
- Rollback on failure

✅ **Shortcuts**
- Desktop shortcut
- Start Menu entry: `Bulk File Renamer`
- Start Menu entry: `Uninstall Bulk File Renamer`

✅ **Windows Integration**
- Appears in Settings → Apps
- Shows application icon and version
- Supports clean uninstallation
- Add/Remove Programs entry

✅ **Upgrade Support**
- Detects existing installations
- Prevents downgrade
- Allows version upgrades

### Testing the MSI

**Install:**
1. Double-click `installer\BulkFileRenamer.msi`
2. Follow installation wizard
3. Launch from Desktop or Start Menu

**Uninstall:**
- Settings → Apps → Bulk File Renamer → Uninstall
- Or: Start Menu → Uninstall Bulk File Renamer

### MSI Customization

Edit `installer\BulkFileRenamer.wxs` to customize:
- Product name and version
- Installation directory
- File associations
- Additional files to include

**Full Documentation:** See `installer\README_INSTALLER.md`

---

**Note:** Add this section to your main README.md after the "Building Executable" section.
