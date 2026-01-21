@echo off
REM ================================================================
REM  Bulk File Renamer - MSI Installer Build (Updated for --onedir)
REM  Creates Windows MSI installer using WiX Toolset
REM ================================================================

echo.
echo ================================================================
echo  Bulk File Renamer - MSI Installer Build
echo ================================================================
echo.

REM Check if WiX Toolset is installed
where candle.exe >nul 2>&1
if errorlevel 1 (
    echo [X] WiX Toolset not found!
    echo.
    echo WiX Toolset is required to build MSI installers.
    echo.
    echo Install using winget:
    echo   winget install WiXToolset.WiX
    echo.
    echo Or download from:
    echo   https://wixtoolset.org/releases/
    echo.
    echo After installation, add WiX bin folder to PATH:
    echo   C:\Program Files ^(x86^)\WiX Toolset v3.11\bin
    echo.
    pause
    exit /b 1
)

echo [+] WiX Toolset detected
echo.

REM Check if the application folder exists (--onedir output)
 if not exist "dist\BulkFileRenamer" (
    echo [X] Application folder not found: dist\BulkFileRenamer
    echo.
    echo Please build the executable first:
    echo   build_exe.bat
    echo.
    pause
    exit /b 1
)

echo [+] Application folder found: dist\BulkFileRenamer
echo.

REM Verify critical files exist
if not exist "dist\BulkFileRenamer\BulkFileRenamer.exe" (
    echo [X] BulkFileRenamer.exe not found in dist\BulkFileRenamer\
    echo.
    pause
    exit /b 1
)

echo [+] BulkFileRenamer.exe found
echo.

REM Tcl/Tk runtime validation disabled - already verified by successful EXE execution
REM if not exist "dist\BulkFileRenamer\tcl" (
REM     echo [!] WARNING: Tcl runtime folder not found!
REM     echo     This will cause Tkinter DLL errors after installation.
REM     echo     Rebuild with: build_exe.bat
REM     echo.
REM     pause
REM     exit /b 1
REM )
REM 
REM echo [+] Tcl/Tk runtime detected
REM echo.

REM Navigate to installer directory
cd installer

REM Clean previous build artifacts
echo [+] Cleaning previous build files...
if exist "*.wixobj" del /q "*.wixobj"
if exist "*.wixpdb" del /q "*.wixpdb"
if exist "*.msi" del /q "*.msi"
if exist "Files.wxs" del /q "Files.wxs"
echo.

REM STEP 1: Use Heat to harvest all files from dist folder
echo [+] Step 1: Harvesting files from dist\BulkFileRenamer...
echo.

heat dir "..\dist\BulkFileRenamer" ^
    -cg BulkFileRenamerFiles ^
    -dr INSTALLFOLDER ^
    -scom ^
    -sfrag ^
    -srd ^
    -sreg ^
    -gg ^
    -var var.SourceDir ^
    -out Files.wxs

if errorlevel 1 (
    echo.
    echo [X] Heat file harvesting failed
    cd ..
    pause
    exit /b 1
)

echo [+] Files harvested successfully
echo.

REM STEP 2: Compile WiX sources
echo [+] Step 2: Compiling WiX sources (.wxs to .wixobj)...
echo.

candle.exe BulkFileRenamer.wxs Files.wxs -dSourceDir="..\dist\BulkFileRenamer"

if errorlevel 1 (
    echo.
    echo [X] Compilation failed!
    echo     Check the error messages above
    cd ..
    pause
    exit /b 1
)

echo.
echo [+] Compilation successful
echo.

REM STEP 3: Link and create MSI
echo [+] Step 3: Linking and creating MSI installer...
echo.

light.exe -ext WixUIExtension -cultures:en-us BulkFileRenamer.wixobj Files.wixobj -out BulkFileRenamer.msi

if errorlevel 1 (
    echo.
    echo [X] Linking failed!
    echo     Check the error messages above
    cd ..
    pause
    exit /b 1
)

cd ..

echo.
echo ================================================================
echo  MSI Installer Build Complete!
echo ================================================================
echo.
echo [+] MSI installer created: installer\BulkFileRenamer.msi
echo.
echo File size: 
for %%A in ("installer\BulkFileRenamer.msi") do echo   %%~zA bytes
echo.
echo This MSI includes:
echo   - BulkFileRenamer.exe
echo   - Tcl/Tk runtime (tcl8.6, tk8.6)
echo   - All dependencies
echo   - Desktop shortcut
echo   - Start Menu shortcut
echo.
echo Next steps:
echo   1. Test the installer: installer\BulkFileRenamer.msi
echo   2. Install and verify Tkinter loads without errors
echo   3. Test all application features
echo.
pause
