# 📁 Bulk File Renamer - Desktop Application

**A professional, fully offline Windows desktop application to rename multiple files safely and efficiently using a clean GUI.**

**Built using Python + Tkinter, packaged as an EXE & MSI installer, with support for preview, undo, logging, and dark mode.**

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)
![Status](https://img.shields.io/badge/Status-Production-success.svg)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage Guide](#usage-guide)
- [Building Executable](#building-executable)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## 🎯 Overview

**Bulk File Renamer** is a fully offline desktop application designed for students and professionals who need to rename multiple files efficiently. Built with Python and Tkinter, it provides a user-friendly graphical interface for complex file renaming tasks without requiring any internet connection.

### Key Highlights

✅ **100% Offline** - No internet dependency, no cloud APIs  
✅ **Professional GUI** - Clean Tkinter interface with status feedback  
✅ **Modular Architecture** - Separated business logic from UI  
✅ **Automatic Backups** - Original files are backed up before renaming  
✅ **JSON Logging** - Complete audit trail of all operations  
✅ **Portable Executable** - Can be bundled as `.exe` for distribution  

---

## ✨ Features

### Core Renaming Features

- **Prefix & Suffix** - Add text before or after file names
- **Sequential Numbering** - Auto-number files with customizable padding
- **Timestamp Appending** - Add current date/time to file names
- **Regex Pattern Replacement** - Advanced find-and-replace using regular expressions
- **Extension Filtering** - Process only specific file types (.txt, .jpg, etc.)

### Safety & Recovery

- **Preview Mode** - See changes before applying them
- **Dry Run** - Test operations without modifying files
- **Automatic Backups** - Originals copied before renaming
- **Undo Support** - JSON log enables manual rollback
- **Collision Detection** - Prevents overwriting existing files

### User Interface

- **Folder Browser** - Easy directory selection
- **Live Preview Table** - Shows Original → New name mappings
- **Status Bar** - Real-time operation feedback
- **Reset Button** - Clear all inputs instantly
- **Confirmation Dialogs** - Prevents accidental operations
- **Error Messages** - Clear, actionable error reporting

---
## ✨ Other Features

- 📁 Select any target directory  
- 🔤 Add prefix and suffix  
- 🔢 Sequential numbering with custom start & padding  
- 🕒 Append timestamps (custom formats supported)  
- 🧩 Regex-based filename replacement  
- 🎯 Extension filtering (`.jpg`, `.png`, `.txt`, etc.)  
- 👀 Preview before renaming (Dry Run)  
- ↩️ Undo last rename  
- 💾 Backup original files automatically  
- 📝 Optional log file generation  
- 🌙 Dark Mode / ☀️ Light Mode  
- 📴 100% offline (no internet required)
  
---

## 🛠️ Technologies Used

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.7+ |
| **GUI Framework** | Tkinter (built-in) |
| **Build Tool** | PyInstaller |
| **Architecture** | MVC Pattern (Model-View-Controller) |
| **Dependencies** | Python Standard Library Only |

**Why Tkinter?**
- ✅ Built into Python (no external dependencies)
- ✅ Cross-platform (Windows, macOS, Linux)
- ✅ Lightweight and fast
- ✅ Perfect for college projects

---

## 📂 Project Structure

```
File_Renamer_Script/
│
├── main.py                  # Application entry point
├── gui.py                   # Tkinter GUI implementation
├── renamer_engine.py        # Core renaming logic (backend)
├── utils.py                 # Helper functions
│
├── assets/                  # Application assets
│   ├── icon.ico             # Application icon (optional)
│   └── README_ASSETS.txt    # Icon customization guide
│
├── build_exe.bat            # Windows build script
├── create_icon.py           # Icon generator utility
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

### Module Descriptions

| File | Purpose |
|------|---------|
| `main.py` | Launches the application, handles errors |
| `gui.py` | Complete Tkinter interface (470+ lines) |
| `renamer_engine.py` | Business logic for file operations |
| `utils.py` | Extension parsing, validation helpers |
| `build_exe.bat` | Automated PyInstaller build script |
| `create_icon.py` | Generates placeholder icon |

---

## 🚀 Installation


### Option 1: Run from Source (Developers)

**Prerequisites:**
- Python 3.7 or higher
- No additional packages required (uses stdlib only)

**Steps:**

1. **Clone or download this repository**
   ```bash
   cd File_Renamer_Script
   ```

2. **Run the application**
   ```bash
   python main.py
   ```

3. **Optional: Install dependencies for building**
   ```bash
   pip install -r requirements.txt
   ```

### Option 2: Run Executable (End Users)

1. **Download the `.exe` file** from the `dist/` folder (after building)
2. **Double-click** `BulkFileRenamer.exe`
3. **No Python installation required!**

---

## 📦 Download

The ready-to-use Windows installer (`.msi`) is available under **GitHub Releases**.

👉 Go to **Releases** → Download → Install → Use

---

## 📖 Usage Guide

### Step-by-Step Instructions

#### 1. Launch the Application
- Run `python main.py` or double-click the `.exe`

#### 2. Select Target Directory
- Click **"Browse"** next to "Target Directory"
- Choose the folder containing files to rename

#### 3. Configure Renaming Options

**Basic Options:**
- **Prefix**: Text to add at the start (e.g., `IMG_`)
- **Suffix**: Text to add before extension (e.g., `_edited`)

**Numbering:**
- ☑️ Enable Sequential Numbering
- Start: `1` (or any number)
- Padding: `3` (e.g., 001, 002, 003)

**Timestamp:**
- ☑️ Append Timestamp
- Format: `%Y%m%d%H%M%S` (e.g., 20260121130000)

**Regex (Advanced):**
- Pattern: `old_text` (or regex like `\d+`)
- Replacement: `new_text`

**Extension Filter:**
- Example: `.jpg .png` or `jpg, png`
- Leave empty to process all files

#### 4. Preview Changes
- Click **"Preview Changes"**
- Review the Original → New table
- Verify all changes look correct

#### 5. Execute Rename
- Click **"Rename Files"**
- Confirm the operation
- Check status bar for success message

#### 6. Verify Results
- Backup folder created: `backup_<timestamp>/`
- Log file created: `rename_log_<timestamp>.json`
- Files successfully renamed in target directory

### Example Scenarios

#### Scenario 1: Add Prefix and Number Photos
```
Settings:
  Directory: C:\Users\Photos
  Prefix: Vacation2026_
  Numbering: ☑️ Enabled (Start: 1, Padding: 3)
  Extensions: .jpg .png

Result:
  photo.jpg      → Vacation2026_001.jpg
  image.png      → Vacation2026_002.png
  sunset.jpg     → Vacation2026_003.jpg
```

#### Scenario 2: Remove Dates Using Regex
```
Settings:
  Directory: C:\Users\Documents
  Regex Pattern: \d{8}_
  Regex Replacement: (empty)
  
Result:
  20260121_report.pdf → report.pdf
  20260120_memo.docx  → memo.docx
```

---

## 🔨 Building Executable

### Using the Build Script (Recommended)

**Windows:**

1. **Run the build script**
   ```cmd
   build_exe.bat
   ```

2. **Wait for completion** (2-3 minutes)

3. **Find your executable**
   ```
   dist/BulkFileRenamer.exe
   ```

4. **Test the .exe**
   - Double-click to launch
   - Verify all features work

### Manual PyInstaller Command

If you prefer manual build:

```bash
# Install PyInstaller
pip install pyinstaller

# Build with icon
pyinstaller --onefile --windowed --icon=assets/icon.ico --name=BulkFileRenamer main.py

# Build without icon
pyinstaller --onefile --windowed --name=BulkFileRenamer main.py
```

### PyInstaller Options Explained

| Option | Purpose |
|--------|---------|
| `--onefile` | Bundle everything into a single .exe |
| `--windowed` | No console window (GUI only) |
| `--icon=path` | Custom application icon |
| `--name=Name` | Output executable name |

### Expected Output

```
dist/
  └── BulkFileRenamer.exe   (~10-15 MB)

build/                      (temporary, can delete)
BulkFileRenamer.spec        (PyInstaller config)
```

---

## 🐛 Troubleshooting

### Common Issues

#### Issue: "Python not found"
**Solution:** Install Python 3.7+ from [python.org](https://www.python.org/downloads/)

#### Issue: "No module named 'tkinter'"
**Solution:** Tkinter is usually included with Python. If missing:
- **Windows:** Reinstall Python (check "tcl/tk" option)
- **Linux:** `sudo apt-get install python3-tk`

#### Issue: "Permission denied" when renaming
**Solution:**
- Close any programs using the files
- Run as Administrator (if needed)
- Check folder permissions

#### Issue: ".exe doesn't open"
**Solution:**
- Rebuild with `--windowed` removed to see error messages
- Check Windows Defender/Antivirus (false positives are common)
- Ensure all source files are in the same directory

#### Issue: "Icon not showing"
**Solution:**
- Run `python create_icon.py` to generate an icon
- Or download a free icon and save as `assets/icon.ico`
- Rebuild the executable

---

## 📸 Screenshots

> **Note:** Add your own screenshots here after running the application

### Main Window
*[Screenshot placeholder: Main application interface]*

### Preview Table
*[Screenshot placeholder: Before/After preview]*

### Success Dialog
*[Screenshot placeholder: Successful rename confirmation]*

---

## 🎓 College Project Notes

This project demonstrates:

✅ **GUI Development** - Professional Tkinter interface  
✅ **Modular Design** - Clean separation of concerns  
✅ **Error Handling** - Robust exception management  
✅ **File I/O** - Reading directories, copying files  
✅ **Regular Expressions** - Advanced text processing  
✅ **Software Packaging** - Distributing as executable  

### Submission Checklist

- [ ] Source code files (`main.py`, `gui.py`, etc.)
- [ ] Built executable (`.exe` file)
- [ ] README documentation (this file)
- [ ] Screenshots of running application
- [ ] Sample test files/folders
- [ ] Project presentation/report

---

## 📄 License

MIT License

Copyright (c) 2026 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED.

---

## 🤝 Credits

**Developed by:** [Your Name]  
**Course:** [Your Course Name]  
**College:** [Your College Name]  
**Year:** 2026  

**Technologies:**
- Python Programming Language
- Tkinter GUI Framework
- PyInstaller Packaging Tool

---

## 📞 Support

For issues or questions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review the [Usage Guide](#usage-guide)
3. Inspect log files in the target directory
4. Contact: [Your Email]

---

**Made with ❤️ using Python + Tkinter**

*100% Offline • No Dependencies • College Project Ready*
