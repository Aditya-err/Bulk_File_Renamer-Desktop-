"""
Splash Screen Module for Bulk File Renamer Application

Creates a professional splash screen that displays while the main application loads.
"""

import tkinter as tk
from tkinter import ttk
import os


class SplashScreen:
    """
    Professional splash screen window for application startup.
    """
    
    def __init__(self):
        """
        Initialize and display the splash screen.
        """
        self.splash = tk.Toplevel()
        self.splash.title("")
        
        # Remove window decorations (no title bar, borders)
        self.splash.overrideredirect(True)
        
        # Set window size
        width = 500
        height = 300
        
        # Center on screen
        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.splash.geometry(f"{width}x{height}+{x}+{y}")
        
        # Create main frame with gradient-like background
        main_frame = tk.Frame(self.splash, bg="#2196F3", relief=tk.RAISED, borderwidth=2)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add padding frame
        content_frame = tk.Frame(main_frame, bg="#2196F3")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Application icon/logo (using text as placeholder)
        icon_frame = tk.Frame(content_frame, bg="#1976D2", width=80, height=80)
        icon_frame.pack(pady=(20, 10))
        icon_frame.pack_propagate(False)
        
        icon_label = tk.Label(
            icon_frame,
            text="📁",
            font=("Arial", 40),
            bg="#1976D2",
            fg="white"
        )
        icon_label.pack(expand=True)
        
        # Application name
        app_name = tk.Label(
            content_frame,
            text="Bulk File Renamer",
            font=("Arial", 24, "bold"),
            bg="#2196F3",
            fg="white"
        )
        app_name.pack(pady=(10, 5))
        
        # Version/tagline
        tagline = tk.Label(
            content_frame,
            text="Professional File Renaming Tool",
            font=("Arial", 11),
            bg="#2196F3",
            fg="#E3F2FD"
        )
        tagline.pack(pady=(0, 20))
        
        # Loading message
        self.loading_label = tk.Label(
            content_frame,
            text="Loading application...",
            font=("Arial", 10),
            bg="#2196F3",
            fg="white"
        )
        self.loading_label.pack(pady=(10, 10))
        
        # Progress bar
        self.progress = ttk.Progressbar(
            content_frame,
            mode='indeterminate',
            length=300
        )
        self.progress.pack(pady=(0, 10))
        self.progress.start(10)
        
        # Status message
        self.status_label = tk.Label(
            content_frame,
            text="Initializing components...",
            font=("Arial", 9),
            bg="#2196F3",
            fg="#BBDEFB"
        )
        self.status_label.pack(pady=(5, 10))
        
        # Copyright/version info
        footer = tk.Label(
            content_frame,
            text="Version 1.0.0 | © 2026",
            font=("Arial", 8),
            bg="#2196F3",
            fg="#90CAF9"
        )
        footer.pack(side=tk.BOTTOM, pady=(10, 0))
        
        # Keep window on top
        self.splash.attributes('-topmost', True)
        
        # Update the display
        self.splash.update()
    
    def update_status(self, message):
        """
        Update the status message on the splash screen.
        
        Args:
            message: Status message to display
        """
        if hasattr(self, 'status_label'):
            self.status_label.config(text=message)
            self.splash.update()
    
    def destroy(self):
        """
        Close and destroy the splash screen.
        """
        try:
            self.progress.stop()
            self.splash.destroy()
        except:
            pass


def show_splash_screen():
    """
    Factory function to create and return a splash screen instance.
    
    Returns:
        SplashScreen instance
    """
    return SplashScreen()


if __name__ == "__main__":
    # Test the splash screen
    root = tk.Tk()
    root.withdraw()  # Hide main window
    
    splash = show_splash_screen()
    
    # Simulate loading time
    import time
    for i in range(5):
        time.sleep(0.5)
        splash.update_status(f"Loading component {i+1}/5...")
    
    splash.destroy()
    root.destroy()
