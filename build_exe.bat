@echo off
REM ================================================================
REM  Bulk File Renamer - PyInstaller Build Script
REM  Creates standalone Windows executable with Tkinter support
REM ================================================================

echo.
echo ================================================================
echo  Bulk File Renamer - Executable Build
echo ================================================================
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo [X] PyInstaller not found!
    echo.
    echo Installing PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo [X] Failed to install PyInstaller
        pause
        exit /b 1
    )
)

echo [+] PyInstaller detected
echo.

REM Hard-coded Tcl/Tk path for Python 3.14
set TCL_PATH=C:\Users\DELL\AppData\Local\Python\pythoncore-3.14-64\tcl

echo [+] Using Tcl/Tk path: %TCL_PATH%
echo.

REM Verify Tcl path exists
if not exist "%TCL_PATH%" (
    echo [X] ERROR: Tcl/Tk directory not found!
    echo     Expected: %TCL_PATH%
    echo.
    echo Please verify your Python installation path.
    pause
    exit /b 1
)

echo [+] Tcl/Tk directory verified
echo.

REM Check if icon exists
if exist "assets\icon.ico" (
    echo [+] Application icon found
    set ICON_FLAG=--icon=assets\icon.ico
) else (
    echo [!] Warning: icon.ico not found in assets folder
    echo     Executable will use default Python icon
    set ICON_FLAG=
)
echo.

REM Clean previous builds
echo [+] Cleaning previous build files...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del /q "*.spec"
echo.

REM Build with PyInstaller
echo [+] Building executable with PyInstaller...
echo     Mode: --onedir (directory-based distribution)
echo     GUI: --windowed (no console window)
echo     Tcl/Tk: Bundled from %TCL_PATH%
echo.

python -m PyInstaller ^
    --onedir ^
    --windowed ^
    --name=BulkFileRenamer ^
    --add-data "%TCL_PATH%;tcl" ^
    --hidden-import=tkinter ^
    --hidden-import=tkinter.ttk ^
    --hidden-import=tkinter.filedialog ^
    --hidden-import=tkinter.messagebox ^
    --hidden-import=splash_screen ^
    --hidden-import=theme_manager ^
    --hidden-import=undo ^
    %ICON_FLAG% ^
    main.py

if errorlevel 1 (
    echo.
    echo [X] Build failed!
    echo     Check the error messages above
    pause
    exit /b 1
)

echo.
echo ================================================================
echo  Build Complete!
echo ================================================================
echo.
echo [+] Executable location: dist\BulkFileRenamer\
echo [+] Main executable: dist\BulkFileRenamer\BulkFileRenamer.exe
echo.
echo IMPORTANT - Folder Structure:
echo   dist\BulkFileRenamer\
echo     ├── BulkFileRenamer.exe
echo     ├── tcl\               (Tcl/Tk runtime)
echo     │   ├── tcl8.6\
echo     │   └── tk8.6\
echo     └── [other dependencies]
echo.
echo This ENTIRE FOLDER must be packaged in the MSI installer!
echo.
echo Next steps:
echo   1. Test: Run dist\BulkFileRenamer\BulkFileRenamer.exe
echo   2. Build MSI: Run build_msi.bat
echo.
pause
