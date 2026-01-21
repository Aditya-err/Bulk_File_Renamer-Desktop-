# Splash Screen and Icon Integration - Documentation

## Overview

Your Bulk File Renamer now includes:
- **Custom Application Icon** - Professional branding
- **Startup Splash Screen** - Smooth loading experience

---

## Files Created

| File | Purpose |
|------|---------|
| `splash_screen.py` | Splash screen module |
| `main.py` (updated) | Splash integration and icon loading |
| `create_icon.py` (updated) | Icon generator utility |

---

## Splash Screen Features

✅ **Professional Appearance**
- Clean, modern design
- Blue gradient background
- Application name and tagline
- Version information
- Copyright/footer

✅ **Loading Feedback**
- Status messages
- Animated progress bar
- Component loading stages

✅ **User Experience**
- Centered on screen
- No window decorations (frameless)
- Always on top
- Auto-closes when main app loads

---

## How It Works

### Startup Sequence

```python
1. Create hidden root window
   ↓
2. Show splash screen
   ↓
3. Update status: "Loading modules..."
   ↓
4. Import GUI components
   ↓
5. Update status: "Initializing..."
   ↓
6. Load application icon
   ↓
7. Update status: "Ready!"
   ↓
8. Show main window
   ↓
9. Close splash screen (500ms delay)
```

### Code Structure

**main.py:**
```python
from splash_screen import show_splash_screen

# Show splash
splash = show_splash_screen()

# Update progress
splash.update_status("Loading...")

# Close when ready
splash.destroy()
```

---

## Custom Icon Setup

### Option 1: Generate Icon (Requires Pillow)

```cmd
# Install Pillow
pip install Pillow

# Generate icon
python create_icon.py
```

**Output:**
- `assets/icon.ico` (256x256, multi-resolution)
- `assets/icon_preview.png` (preview image)

### Option 2: Use AI-Generated Icon

I've created a professional icon for you. To use it:

1. Open: `app_icon.webp` (in artifacts)
2. Convert to .ico:
   - Visit: https://convertio.co/webp-ico/
   - Upload the webp file
   - Download as icon.ico
3. Save to: `assets/icon.ico`

### Option 3: Create Custom Icon

1. Design a 256x256px image
2. Use online converter: https://icoconvert.com/
3. Save as `assets/icon.ico`

---

## Icon Features

**Your icon includes:**
- Folder symbol (file management)
- Blue arrow (transformation/renaming)
- Blue gradient background
- "BR" text (Bulk Renamer)
- Professional appearance

**Formats:**
- 256x256 (high resolution)
- 48x48 (window title bar)
- 32x32 (taskbar)
- 16x16 (system tray)

---

## Testing

### Test Splash Screen Only

```cmd
python splash_screen.py
```

This will show the splash screen for 5 seconds with simulated loading.

### Test Full Application

```cmd
python main.py
```

You should see:
1. Splash screen appears (centered)
2. Loading messages update
3. Main window appears
4. Splash screen closes automatically

### Without Splash Screen

If `splash_screen.py` is missing or has errors, the app will:
- Skip splash screen
- Launch main window directly
- No errors or crashes

---

## Customization

### Change Splash Screen Colors

Edit `splash_screen.py`:

```python
# Background color
main_frame = tk.Frame(self.splash, bg="#2196F3")  # Change this

# Icon background
icon_frame = tk.Frame(content_frame, bg="#1976D2")  # And this
```

### Change Splash Screen Text

```python
# Application name
app_name = tk.Label(
    content_frame,
    text="Your App Name",  # Change this
    ...
)

# Tagline
tagline = tk.Label(
    content_frame,
    text="Your tagline here",  # Change this
    ...
)
```

### Adjust Splash Duration

Edit `main.py`:

```python
# Change delay before closing (milliseconds)
root.after(500, splash.destroy)  # Change 500 to desired delay
```

### Disable Splash Screen

Edit `main.py`:

```python
# Comment out splash screen code
# try:
#     from splash_screen import show_splash_screen
#     splash = show_splash_screen()
# except ImportError:
#     pass
```

---

## Troubleshooting

### Issue: Splash screen doesn't appear

**Solution:**
- Check `splash_screen.py` exists
- Verify no syntax errors in splash_screen.py
- Try running: `python splash_screen.py`

### Issue: Icon doesn't show

**Solution:**
- Verify `assets/icon.ico` exists
- Check file path is correct
- Icon loading errors are silently ignored

### Issue: Splash stays too long/short

**Solution:**
- Adjust delay in main.py:
  ```python
  root.after(500, splash.destroy)  # Increase/decrease 500
  ```

### Issue: Application starts slowly

**Solution:**
- This is normal! Splash screen shows progress
- PyInstaller .exe will be faster
- Splash screen hides the loading time

---

## Integration with Build Scripts

### PyInstaller Build

The icon is automatically included:

```cmd
pyinstaller --onefile --windowed --icon=assets/icon.ico --name=BulkFileRenamer main.py
```

### MSI Installer

The icon is referenced in `BulkFileRenamer.wxs`:

```xml
<Icon Id="AppIcon.ico" SourceFile="..\assets\icon.ico" />
```

---

## User Experience

### Before (Without Splash Screen)
1. Double-click executable
2. Wait... (blank screen)
3. Application appears
4. User confused if it's loading

### After (With Splash Screen)
1. Double-click executable
2. Splash screen appears immediately
3. Loading messages update
4. Main application appears
5. Smooth transition!

---

## Technical Details

### Splash Screen Implementation

**Features:**
- `Toplevel` window (separate from main)
- `overrideredirect(True)` (frameless)
- `attributes('-topmost', True)` (always visible)
- `withdraw()` main window (hide until ready)
- `deiconify()` main window (show when ready)

**Non-blocking:**
- Splash screen runs in main thread
- GUI updates via `update()`
- No threading needed
- Clean and simple

### Icon Loading

**Graceful degradation:**
```python
try:
    root.iconbitmap('assets/icon.ico')
except:
    pass  # Continue without icon
```

---

## File Structure

```
File_Renamer_Script/
├── main.py                    # Launcher with splash integration
├── splash_screen.py           # Splash screen module
├── create_icon.py             # Icon generator
├── assets/
│   ├── icon.ico               # Application icon
│   └── icon_preview.png       # Icon preview
└── ...
```

---

## Summary

✅ **Splash Screen:** Professional startup experience  
✅ **Custom Icon:** Branded application  
✅ **Non-blocking:** Smooth user experience  
✅ **Error handling:** Graceful degradation  
✅ **Customizable:** Easy to modify  
✅ **Build integration:** Works with PyInstaller and MSI  

---

## Next Steps

1. **Generate/add custom icon** to `assets/icon.ico`
2. **Test splash screen:** `python main.py`
3. **Rebuild executable:** `build_exe.bat`
4. **Rebuild MSI:** `build_msi.bat`
5. **Verify icon shows** in taskbar and window

---

**Your application now has a professional, polished startup experience!**
