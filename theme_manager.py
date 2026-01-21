"""
Theme Manager for Bulk File Renamer Application

Provides Light and Dark theme support for the entire application.
Uses ttk.Style for consistent theming across all widgets.
"""

import tkinter as tk
from tkinter import ttk


class ThemeManager:
    """
    Manages application themes (Light and Dark modes).
    """
    
    # Light Theme Colors
    LIGHT_THEME = {
        'bg': '#FFFFFF',
        'fg': '#000000',
        'select_bg': '#0078D4',
        'select_fg': '#FFFFFF',
        'entry_bg': '#FFFFFF',
        'entry_fg': '#000000',
        'entry_border': '#CCCCCC',
        'button_bg': '#E1E1E1',
        'button_fg': '#000000',
        'button_active_bg': '#0078D4',
        'button_active_fg': '#FFFFFF',
        'button_disabled_bg': '#F0F0F0',
        'button_disabled_fg': '#A0A0A0',
        'frame_bg': '#F5F5F5',
        'label_bg': '#FFFFFF',
        'label_fg': '#000000',
        'tree_bg': '#FFFFFF',
        'tree_fg': '#000000',
        'tree_select_bg': '#0078D4',
        'tree_select_fg': '#FFFFFF',
        'tree_heading_bg': '#E8E8E8',
        'tree_heading_fg': '#000000',
        'scrollbar_bg': '#F0F0F0',
        'scrollbar_troughcolor': '#E8E8E8',
        'status_bg': '#E8E8E8',
        'status_fg': '#333333',
    }
    
    # Dark Theme Colors
    DARK_THEME = {
        'bg': '#1E1E1E',
        'fg': '#E0E0E0',
        'select_bg': '#4A90E2',
        'select_fg': '#FFFFFF',
        'entry_bg': '#2D2D2D',
        'entry_fg': '#E0E0E0',
        'entry_border': '#404040',
        'button_bg': '#3C3C3C',
        'button_fg': '#E0E0E0',
        'button_active_bg': '#4A90E2',
        'button_active_fg': '#FFFFFF',
        'button_disabled_bg': '#2A2A2A',
        'button_disabled_fg': '#666666',
        'frame_bg': '#252525',
        'label_bg': '#1E1E1E',
        'label_fg': '#E0E0E0',
        'tree_bg': '#2D2D2D',
        'tree_fg': '#E0E0E0',
        'tree_select_bg': '#4A90E2',
        'tree_select_fg': '#FFFFFF',
        'tree_heading_bg': '#3C3C3C',
        'tree_heading_fg': '#E0E0E0',
        'scrollbar_bg': '#3C3C3C',
        'scrollbar_troughcolor': '#2D2D2D',
        'status_bg': '#252525',
        'status_fg': '#B0B0B0',
    }
    
    def __init__(self, root):
        """
        Initialize the theme manager.
        
        Args:
            root: The root Tk window
        """
        self.root = root
        self.style = ttk.Style(root)
        self.current_theme = 'light'  # Default to light theme
        
        # Store references to widgets that need manual theme updates
        self.themed_widgets = []
        
        # Apply initial theme
        self.apply_theme('light')
    
    def apply_theme(self, theme_name):
        """
        Apply a theme to the application.
        
        Args:
            theme_name: 'light' or 'dark'
        """
        if theme_name not in ['light', 'dark']:
            theme_name = 'light'
        
        self.current_theme = theme_name
        colors = self.LIGHT_THEME if theme_name == 'light' else self.DARK_THEME
        
        # Configure ttk.Style for various widgets
        self._configure_treeview(colors)
        self._configure_entry(colors)
        self._configure_combobox(colors)
        self._configure_button(colors)
        self._configure_checkbutton(colors)
        self._configure_radiobutton(colors)
        self._configure_label(colors)
        self._configure_frame(colors)
        self._configure_labelframe(colors)
        self._configure_scrollbar(colors)
        self._configure_separator(colors)
        
        # Update root window background
        self.root.configure(bg=colors['bg'])
        
        # Update manually tracked widgets
        self._update_manual_widgets(colors)
    
    def _configure_treeview(self, colors):
        """Configure Treeview widget style."""
        self.style.configure(
            'Treeview',
            background=colors['tree_bg'],
            foreground=colors['tree_fg'],
            fieldbackground=colors['tree_bg'],
            borderwidth=1,
            relief='solid'
        )
        self.style.map(
            'Treeview',
            background=[('selected', colors['tree_select_bg'])],
            foreground=[('selected', colors['tree_select_fg'])]
        )
        
        # Treeview headings
        self.style.configure(
            'Treeview.Heading',
            background=colors['tree_heading_bg'],
            foreground=colors['tree_heading_fg'],
            borderwidth=1,
            relief='raised'
        )
        self.style.map(
            'Treeview.Heading',
            background=[('active', colors['button_active_bg'])],
            foreground=[('active', colors['button_active_fg'])]
        )
    
    def _configure_entry(self, colors):
        """Configure Entry widget style."""
        self.style.configure(
            'TEntry',
            fieldbackground=colors['entry_bg'],
            foreground=colors['entry_fg'],
            borderwidth=1,
            relief='solid',
            insertcolor=colors['entry_fg']
        )
        self.style.map(
            'TEntry',
            fieldbackground=[
                ('disabled', colors['button_disabled_bg']),
                ('readonly', colors['entry_bg'])
            ],
            foreground=[
                ('disabled', colors['button_disabled_fg']),
                ('readonly', colors['entry_fg'])
            ],
            bordercolor=[
                ('focus', colors['select_bg']),
                ('!focus', colors['entry_border'])
            ]
        )
    
    def _configure_combobox(self, colors):
        """Configure Combobox widget style."""
        self.style.configure(
            'TCombobox',
            fieldbackground=colors['entry_bg'],
            foreground=colors['entry_fg'],
            background=colors['button_bg'],
            borderwidth=1,
            arrowcolor=colors['fg'],
            insertcolor=colors['entry_fg']
        )
        self.style.map(
            'TCombobox',
            fieldbackground=[
                ('readonly', colors['entry_bg']),
                ('disabled', colors['button_disabled_bg'])
            ],
            foreground=[
                ('readonly', colors['entry_fg']),
                ('disabled', colors['button_disabled_fg'])
            ],
            selectbackground=[('readonly', colors['select_bg'])],
            selectforeground=[('readonly', colors['select_fg'])],
            arrowcolor=[
                ('disabled', colors['button_disabled_fg']),
                ('!disabled', colors['fg'])
            ]
        )
    
    def _configure_button(self, colors):
        """Configure Button widget style."""
        self.style.configure(
            'TButton',
            background=colors['button_bg'],
            foreground=colors['button_fg'],
            borderwidth=1,
            relief='raised',
            padding=(10, 5)
        )
        self.style.map(
            'TButton',
            background=[
                ('active', colors['button_active_bg']),
                ('disabled', colors['button_disabled_bg']),
                ('!disabled', colors['button_bg'])
            ],
            foreground=[
                ('active', colors['button_active_fg']),
                ('disabled', colors['button_disabled_fg']),
                ('!disabled', colors['button_fg'])
            ],
            relief=[
                ('pressed', 'sunken'),
                ('!pressed', 'raised')
            ]
        )
    
    def _configure_checkbutton(self, colors):
        """Configure Checkbutton widget style."""
        self.style.configure(
            'TCheckbutton',
            background=colors['bg'],
            foreground=colors['fg']
        )
        self.style.map(
            'TCheckbutton',
            background=[
                ('active', colors['bg']),
                ('!active', colors['bg'])
            ],
            foreground=[
                ('disabled', colors['button_disabled_fg']),
                ('!disabled', colors['fg'])
            ],
            indicatorbackground=[
                ('selected', colors['select_bg']),
                ('!selected', colors['entry_bg'])
            ]
        )
    
    def _configure_radiobutton(self, colors):
        """Configure Radiobutton widget style."""
        self.style.configure(
            'TRadiobutton',
            background=colors['bg'],
            foreground=colors['fg']
        )
        self.style.map(
            'TRadiobutton',
            background=[
                ('active', colors['bg']),
                ('!active', colors['bg'])
            ],
            foreground=[
                ('disabled', colors['button_disabled_fg']),
                ('!disabled', colors['fg'])
            ],
            indicatorbackground=[
                ('selected', colors['select_bg']),
                ('!selected', colors['entry_bg'])
            ]
        )
    
    def _configure_label(self, colors):
        """Configure Label widget style."""
        self.style.configure(
            'TLabel',
            background=colors['label_bg'],
            foreground=colors['label_fg']
        )
    
    def _configure_frame(self, colors):
        """Configure Frame widget style."""
        self.style.configure(
            'TFrame',
            background=colors['frame_bg']
        )
    
    def _configure_labelframe(self, colors):
        """Configure LabelFrame widget style."""
        self.style.configure(
            'TLabelframe',
            background=colors['frame_bg'],
            foreground=colors['fg'],
            borderwidth=2,
            relief='groove'
        )
        self.style.configure(
            'TLabelframe.Label',
            background=colors['frame_bg'],
            foreground=colors['fg']
        )
    
    def _configure_scrollbar(self, colors):
        """Configure Scrollbar widget style."""
        # Vertical Scrollbar
        self.style.configure(
            'Vertical.TScrollbar',
            background=colors['scrollbar_bg'],
            troughcolor=colors['scrollbar_troughcolor'],
            borderwidth=1,
            arrowcolor=colors['fg']
        )
        self.style.map(
            'Vertical.TScrollbar',
            background=[
                ('active', colors['button_active_bg']),
                ('!active', colors['scrollbar_bg'])
            ],
            arrowcolor=[
                ('disabled', colors['button_disabled_fg']),
                ('!disabled', colors['fg'])
            ]
        )
        
        # Horizontal Scrollbar
        self.style.configure(
            'Horizontal.TScrollbar',
            background=colors['scrollbar_bg'],
            troughcolor=colors['scrollbar_troughcolor'],
            borderwidth=1,
            arrowcolor=colors['fg']
        )
        self.style.map(
            'Horizontal.TScrollbar',
            background=[
                ('active', colors['button_active_bg']),
                ('!active', colors['scrollbar_bg'])
            ],
            arrowcolor=[
                ('disabled', colors['button_disabled_fg']),
                ('!disabled', colors['fg'])
            ]
        )
    
    def _configure_separator(self, colors):
        """Configure Separator widget style."""
        self.style.configure(
            'TSeparator',
            background=colors['entry_border']
        )
    
    def _update_manual_widgets(self, colors):
        """Update widgets that need manual color configuration."""
        for widget_info in self.themed_widgets[:]:  # Create a copy to iterate safely
            widget = widget_info['widget']
            widget_type = widget_info['type']
            
            try:
                if widget_type == 'status_label':
                    widget.configure(
                        background=colors['status_bg'],
                        foreground=colors['status_fg']
                    )
                elif widget_type == 'status_frame':
                    widget.configure(background=colors['status_bg'])
                elif widget_type == 'text':
                    widget.configure(
                        background=colors['entry_bg'],
                        foreground=colors['entry_fg'],
                        insertbackground=colors['entry_fg'],
                        selectbackground=colors['select_bg'],
                        selectforeground=colors['select_fg']
                    )
            except tk.TclError:
                # Widget no longer exists, remove from list
                self.themed_widgets.remove(widget_info)
    
    def register_widget(self, widget, widget_type):
        """
        Register a widget for manual theme updates.
        
        Args:
            widget: The widget to register
            widget_type: Type identifier for the widget ('status_label', 'status_frame', 'text')
        """
        self.themed_widgets.append({
            'widget': widget,
            'type': widget_type
        })
        
        # Apply current theme immediately
        colors = self.get_current_colors()
        try:
            if widget_type == 'status_label':
                widget.configure(
                    background=colors['status_bg'],
                    foreground=colors['status_fg']
                )
            elif widget_type == 'status_frame':
                widget.configure(background=colors['status_bg'])
            elif widget_type == 'text':
                widget.configure(
                    background=colors['entry_bg'],
                    foreground=colors['entry_fg'],
                    insertbackground=colors['entry_fg'],
                    selectbackground=colors['select_bg'],
                    selectforeground=colors['select_fg']
                )
        except tk.TclError:
            pass
    
    def toggle_theme(self):
        """Toggle between light and dark themes."""
        new_theme = 'dark' if self.current_theme == 'light' else 'light'
        self.apply_theme(new_theme)
        return new_theme
    
    def get_current_theme(self):
        """Get the current theme name."""
        return self.current_theme
    
    def get_current_colors(self):
        """Get the current theme's color dictionary."""
        return self.LIGHT_THEME if self.current_theme == 'light' else self.DARK_THEME


# Convenience function for standalone usage
def create_theme_manager(root):
    """
    Create and return a ThemeManager instance.
    
    Args:
        root: The root Tk window
        
    Returns:
        ThemeManager instance
    """
    return ThemeManager(root)


if __name__ == "__main__":
    # Test the theme manager
    root = tk.Tk()
    root.title("Theme Manager Test")
    root.geometry("500x400")
    
    theme_manager = ThemeManager(root)
    
    # Create test widgets
    frame = ttk.Frame(root, padding=20)
    frame.pack(fill=tk.BOTH, expand=True)
    
    ttk.Label(frame, text="Theme Manager Test", font=("Arial", 14, "bold")).pack(pady=10)
    
    # Test various widgets
    ttk.Label(frame, text="Entry Widget:").pack(pady=5, anchor=tk.W)
    ttk.Entry(frame, width=30).pack(pady=5)
    
    ttk.Label(frame, text="Button Widget:").pack(pady=5, anchor=tk.W)
    ttk.Button(frame, text="Normal Button").pack(pady=5)
    ttk.Button(frame, text="Disabled Button", state='disabled').pack(pady=5)
    
    ttk.Label(frame, text="Checkbutton Widget:").pack(pady=5, anchor=tk.W)
    ttk.Checkbutton(frame, text="Test Checkbox").pack(pady=5)
    
    ttk.Label(frame, text="Combobox Widget:").pack(pady=5, anchor=tk.W)
    combo = ttk.Combobox(frame, values=["Option 1", "Option 2", "Option 3"])
    combo.pack(pady=5)
    
    # Theme toggle button
    def toggle():
        new_theme = theme_manager.toggle_theme()
        theme_button.config(text=f"Switch to {'Light' if new_theme == 'dark' else 'Dark'} Mode")
    
    theme_button = ttk.Button(frame, text="Switch to Dark Mode", command=toggle)
    theme_button.pack(pady=20)
    
    root.mainloop()
