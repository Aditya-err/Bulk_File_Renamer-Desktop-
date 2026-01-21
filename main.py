"""
Enhanced entry point for the Bulk File Renamer Desktop Application.
Includes Tkinter runtime fix for frozen/packaged execution.

Version: 1.0.0
Author: College Project
License: MIT
"""

import sys
import os


# ============================================================
# CRITICAL: Tkinter Runtime Fix for Frozen Applications
# ============================================================
# This MUST execute BEFORE any tkinter imports
# Fixes: ImportError: DLL load failed while importing _tkinter
# ============================================================

if getattr(sys, 'frozen', False):
    # Running as compiled executable (PyInstaller)
    application_path = sys._MEIPASS  # PyInstaller temp folder
    
    # Set TCL_LIBRARY and TK_LIBRARY environment variables
    # These point to bundled Tcl/Tk runtime inside the frozen app
    os.environ['TCL_LIBRARY'] = os.path.join(application_path, 'tcl', 'tcl8.6')
    os.environ['TK_LIBRARY'] = os.path.join(application_path, 'tcl', 'tk8.6')
    
    # Optional: Add Tcl/Tk DLL directory to PATH for extra safety
    tcl_bin = os.path.join(application_path, 'tcl')
    if os.path.exists(tcl_bin):
        os.environ['PATH'] = tcl_bin + os.pathsep + os.environ.get('PATH', '')

# Now safe to import tkinter
import tkinter as tk
from tkinter import messagebox


def main():
    """
    Main application entry point with splash screen.
    Handles initialization and error recovery.
    """
    splash = None
    
    try:
        # Create hidden root window first
        root = tk.Tk()
        root.withdraw()  # Hide main window initially
        
        # Import and show splash screen
        try:
            from splash_screen import show_splash_screen
            splash = show_splash_screen()
            splash.update_status("Loading application modules...")
        except ImportError:
            # If splash screen module not available, continue without it
            pass
        
        # Import the GUI module (after splash is visible)
        if splash:
            splash.update_status("Initializing GUI components...")
        
        from gui import BulkFileRenamerGUI
        
        # Configure the root window
        if splash:
            splash.update_status("Configuring main window...")
        
        root.deiconify()  # Show main window
        
        # Try to set application icon
        try:
            icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icon.ico')
            if os.path.exists(icon_path):
                root.iconbitmap(icon_path)
                if splash:
                    splash.update_status("Loading application icon...")
        except Exception:
            pass  # Ignore icon loading errors
        
        # Create application instance
        if splash:
            splash.update_status("Finalizing initialization...")
        
        app = BulkFileRenamerGUI(root)
        
        # Close splash screen before showing main window
        if splash:
            root.after(500, splash.destroy)  # Delay to show "Ready" state
            splash.update_status("Ready!")
        
        # Start the event loop
        root.mainloop()
        
    except ImportError as e:
        if splash:
            splash.destroy()
        messagebox.showerror(
            "Import Error",
            f"Failed to import required modules:\n{e}\n\n"
            "Please ensure all files are in the correct location."
        )
        sys.exit(1)
        
    except Exception as e:
        if splash:
            splash.destroy()
        messagebox.showerror(
            "Application Error",
            f"An unexpected error occurred:\n{e}\n\n"
            "The application will now close."
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
