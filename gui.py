"""
Tkinter GUI for the Bulk File Renamer application.
Provides a user-friendly interface for bulk file renaming operations.
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from typing import Optional

from renamer_engine import BulkRenameConfig, preview_renames, rename_files
from utils import parse_extensions, validate_directory, get_default_backup_dir, get_default_log_file

try:
    from theme_manager import ThemeManager
    THEME_AVAILABLE = True
except ImportError:
    THEME_AVAILABLE = False


class BulkFileRenamerGUI:
    """
    Main GUI application class for the Bulk File Renamer.
    """

    def __init__(self, root):
        """
        Initialize the GUI application.
        """
        self.root = root
        self.root.title("Bulk File Renamer - Desktop Application")
        self.root.geometry("900x800")
        self.root.resizable(True, True)
        
        # Try to set application icon if available
        try:
            icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icon.ico')
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception:
            pass  # Ignore if icon cannot be loaded

        # Variables to store user inputs
        self.directory_var = tk.StringVar()
        self.prefix_var = tk.StringVar()
        self.suffix_var = tk.StringVar()
        self.numbering_var = tk.BooleanVar(value=False)
        self.numbering_start_var = tk.StringVar(value="1")
        self.numbering_padding_var = tk.StringVar(value="3")
        self.timestamp_var = tk.BooleanVar(value=False)
        self.timestamp_format_var = tk.StringVar(value="%Y%m%d%H%M%S")
        self.regex_pattern_var = tk.StringVar()
        self.regex_replacement_var = tk.StringVar()
        self.extensions_var = tk.StringVar()
        self.backup_dir_var = tk.StringVar()
        self.log_file_var = tk.StringVar()
        self.dry_run_var = tk.BooleanVar(value=False)
        
        # Status message variable
        self.status_var = tk.StringVar(value="Ready")
        
        # Initialize theme manager
        self.theme_manager = None
        if THEME_AVAILABLE:
            try:
                self.theme_manager = ThemeManager(root)
            except Exception:
                pass  # Continue without themes if initialization fails

        # Timestamp format presets
        self.timestamp_presets = [
            ("YYYYMMDDHHMMSS", "%Y%m%d%H%M%S"),
            ("YYYY-MM-DD HH:MM:SS", "%Y-%m-%d %H:%M:%S"),
            ("YYYYMMDD", "%Y%m%d"),
            ("YYYY-MM-DD", "%Y-%m-%d"),
            ("Unix Timestamp", "%s"),
        ]

        self._create_widgets()
        self._layout_widgets()

    def _create_widgets(self):
        """
        Create all GUI widgets.
        """
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # === Directory Selection ===
        ttk.Label(main_frame, text="Target Directory:", font=("Arial", 10, "bold")).grid(
            row=0, column=0, sticky=tk.W, pady=(0, 5)
        )
        ttk.Entry(main_frame, textvariable=self.directory_var, width=50).grid(
            row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=(0, 5)
        )
        ttk.Button(main_frame, text="Browse", command=self._browse_directory).grid(
            row=0, column=2, padx=(0, 0), pady=(0, 5)
        )

        # Separator
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).grid(
            row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10
        )

        # === Prefix and Suffix ===
        ttk.Label(main_frame, text="Prefix:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.prefix_var, width=30).grid(
            row=2, column=1, sticky=tk.W, padx=(5, 0), pady=5
        )

        ttk.Label(main_frame, text="Suffix:").grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.suffix_var, width=30).grid(
            row=3, column=1, sticky=tk.W, padx=(5, 0), pady=5
        )

        # === Numbering Options ===
        numbering_frame = ttk.LabelFrame(main_frame, text="Numbering Options", padding="5")
        numbering_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)

        ttk.Checkbutton(
            numbering_frame,
            text="Enable Sequential Numbering",
            variable=self.numbering_var,
        ).grid(row=0, column=0, sticky=tk.W, padx=5)

        ttk.Label(numbering_frame, text="Start:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(numbering_frame, textvariable=self.numbering_start_var, width=10).grid(
            row=1, column=1, sticky=tk.W, padx=5, pady=2
        )

        ttk.Label(numbering_frame, text="Padding (digits):").grid(
            row=1, column=2, sticky=tk.W, padx=5, pady=2
        )
        ttk.Entry(numbering_frame, textvariable=self.numbering_padding_var, width=10).grid(
            row=1, column=3, sticky=tk.W, padx=5, pady=2
        )

        # === Timestamp Options ===
        timestamp_frame = ttk.LabelFrame(main_frame, text="Timestamp Options", padding="5")
        timestamp_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)

        ttk.Checkbutton(
            timestamp_frame,
            text="Append Timestamp",
            variable=self.timestamp_var,
        ).grid(row=0, column=0, sticky=tk.W, padx=5)

        ttk.Label(timestamp_frame, text="Format:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        timestamp_combo = ttk.Combobox(
            timestamp_frame,
            textvariable=self.timestamp_format_var,
            values=[preset[1] for preset in self.timestamp_presets],
            width=25,
        )
        timestamp_combo.grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        timestamp_combo.current(0)
        ttk.Label(
            timestamp_frame,
            text="(Select preset or enter custom format)",
            font=("Arial", 8),
            foreground="gray",
        ).grid(row=2, column=0, columnspan=2, sticky=tk.W, padx=5, pady=2)

        # === Regex Options ===
        regex_frame = ttk.LabelFrame(main_frame, text="Regex Pattern Replacement", padding="5")
        regex_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        regex_frame.columnconfigure(1, weight=1)

        ttk.Label(regex_frame, text="Pattern:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(regex_frame, textvariable=self.regex_pattern_var, width=40).grid(
            row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=2
        )

        ttk.Label(regex_frame, text="Replacement:").grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=2
        )
        ttk.Entry(regex_frame, textvariable=self.regex_replacement_var, width=40).grid(
            row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=2
        )

        # === Extension Filter ===
        ttk.Label(main_frame, text="Extension Filter:").grid(
            row=7, column=0, sticky=tk.W, pady=5
        )
        ttk.Entry(main_frame, textvariable=self.extensions_var, width=30).grid(
            row=7, column=1, sticky=tk.W, padx=(5, 0), pady=5
        )
        ttk.Label(
            main_frame,
            text="(e.g., .jpg .png .txt or jpg, png, txt)",
            font=("Arial", 8),
            foreground="gray",
        ).grid(row=7, column=2, sticky=tk.W, padx=(5, 0), pady=5)

        # === Backup and Log Options ===
        backup_log_frame = ttk.LabelFrame(main_frame, text="Backup & Log Options", padding="5")
        backup_log_frame.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        backup_log_frame.columnconfigure(1, weight=1)

        ttk.Label(backup_log_frame, text="Backup Directory:").grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=2
        )
        ttk.Entry(backup_log_frame, textvariable=self.backup_dir_var, width=40).grid(
            row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=2
        )
        ttk.Button(
            backup_log_frame, text="Browse", command=self._browse_backup_dir
        ).grid(row=0, column=2, padx=5, pady=2)

        ttk.Label(backup_log_frame, text="Log File:").grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=2
        )
        ttk.Entry(backup_log_frame, textvariable=self.log_file_var, width=40).grid(
            row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=2
        )
        ttk.Button(
            backup_log_frame, text="Browse", command=self._browse_log_file
        ).grid(row=1, column=2, padx=5, pady=2)

        ttk.Label(
            backup_log_frame,
            text="(Leave empty for auto-generated paths)",
            font=("Arial", 8),
            foreground="gray",
        ).grid(row=2, column=0, columnspan=3, sticky=tk.W, padx=5, pady=2)

        # === Dry Run Checkbox ===
        ttk.Checkbutton(
            main_frame,
            text="Dry Run Mode (Preview only, no files renamed)",
            variable=self.dry_run_var,
        ).grid(row=9, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))
        
        # === Dark Mode Toggle ===
        if self.theme_manager:
            self.dark_mode_var = tk.BooleanVar(value=False)
            ttk.Checkbutton(
                main_frame,
                text="🌙 Dark Mode",
                variable=self.dark_mode_var,
                command=self._toggle_theme
            ).grid(row=9, column=2, sticky=tk.E, pady=(10, 5))

        # === Preview Area ===
        preview_frame = ttk.LabelFrame(main_frame, text="Preview (Before → After)", padding="5")
        preview_frame.grid(row=10, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(10, weight=1)

        # Create Treeview for preview table
        preview_tree = ttk.Treeview(
            preview_frame, columns=("Original", "New"), show="headings", height=10
        )
        preview_tree.heading("Original", text="Original Name")
        preview_tree.heading("New", text="New Name")
        preview_tree.column("Original", width=350, anchor=tk.W)
        preview_tree.column("New", width=350, anchor=tk.W)

        # Scrollbars for preview
        preview_v_scroll = ttk.Scrollbar(preview_frame, orient=tk.VERTICAL, command=preview_tree.yview)
        preview_h_scroll = ttk.Scrollbar(
            preview_frame, orient=tk.HORIZONTAL, command=preview_tree.xview
        )
        preview_tree.configure(yscrollcommand=preview_v_scroll.set, xscrollcommand=preview_h_scroll.set)

        preview_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        preview_v_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        preview_h_scroll.grid(row=1, column=0, sticky=(tk.W, tk.E))

        self.preview_tree = preview_tree

        # === Action Buttons ===
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=11, column=0, columnspan=3, pady=10)

        ttk.Button(
            button_frame, text="Preview Changes", command=self._preview_changes, width=15
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            button_frame, text="Rename Files", command=self._rename_files, width=15
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            button_frame, text="Undo Last Rename", command=self._undo_last_rename, width=18
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            button_frame, text="Reset", command=self._reset_form, width=12
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            button_frame, text="Exit", command=self._exit_application, width=12
        ).pack(side=tk.LEFT, padx=5)
        
        # === Status Bar ===
        status_frame = tk.Frame(main_frame, relief=tk.SUNKEN, borderwidth=1)
        status_frame.grid(row=12, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.status_label = tk.Label(
            status_frame, 
            textvariable=self.status_var, 
            anchor=tk.W,
            font=("Arial", 9)
        )
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=3)
        
        # Register status widgets with theme manager
        if self.theme_manager:
            self.theme_manager.register_widget(status_frame, 'status_frame')
            self.theme_manager.register_widget(self.status_label, 'status_label')

    def _layout_widgets(self):
        """
        Configure grid weights for proper resizing.
        """
        pass  # Layout is handled in _create_widgets

    def _browse_directory(self):
        """
        Open a directory selection dialog.
        """
        directory = filedialog.askdirectory(title="Select Target Directory")
        if directory:
            self.directory_var.set(directory)

    def _browse_backup_dir(self):
        """
        Open a directory selection dialog for backup location.
        """
        directory = filedialog.askdirectory(title="Select Backup Directory")
        if directory:
            self.backup_dir_var.set(directory)

    def _browse_log_file(self):
        """
        Open a file save dialog for log file location.
        """
        filename = filedialog.asksaveasfilename(
            title="Save Log File As",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if filename:
            self.log_file_var.set(filename)

    def _get_config(self) -> Optional[BulkRenameConfig]:
        """
        Build a BulkRenameConfig from GUI inputs.
        Returns None if validation fails (error shown to user).
        """
        try:
            directory = self.directory_var.get().strip()
            if not directory:
                messagebox.showerror("Error", "Please select a target directory.")
                return None

            validate_directory(directory)

            # Parse extensions
            extensions = parse_extensions(self.extensions_var.get())

            # Validate numbering inputs
            numbering_start = 1
            numbering_padding = 3
            if self.numbering_var.get():
                try:
                    numbering_start = int(self.numbering_start_var.get())
                    if numbering_start < 0:
                        raise ValueError("Numbering start must be non-negative.")
                except ValueError as e:
                    messagebox.showerror("Error", f"Invalid numbering start: {e}")
                    return None

                try:
                    numbering_padding = int(self.numbering_padding_var.get())
                    if numbering_padding < 0:
                        raise ValueError("Numbering padding must be non-negative.")
                except ValueError as e:
                    messagebox.showerror("Error", f"Invalid numbering padding: {e}")
                    return None

            # Get backup and log paths (empty means auto-generate)
            backup_dir = self.backup_dir_var.get().strip() or None
            log_file = self.log_file_var.get().strip() or None

            config = BulkRenameConfig(
                directory=directory,
                prefix=self.prefix_var.get().strip() or None,
                suffix=self.suffix_var.get().strip() or None,
                numbering=self.numbering_var.get(),
                numbering_start=numbering_start,
                numbering_padding=numbering_padding,
                timestamp=self.timestamp_var.get(),
                timestamp_format=self.timestamp_format_var.get(),
                regex_pattern=self.regex_pattern_var.get().strip() or None,
                regex_replacement=self.regex_replacement_var.get().strip() or None,
                extensions=extensions,
                dry_run=self.dry_run_var.get(),
                backup_dir=backup_dir,
                log_file=log_file,
            )

            return config

        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return None
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")
            return None

    def _clear_preview(self):
        """
        Clear the preview table.
        """
        for item in self.preview_tree.get_children():
            self.preview_tree.delete(item)
    
    def _update_status(self, message, is_error=False):
        """
        Update the status bar with a message.
        
        Args:
            message: Status message to display
            is_error: If True, indicates an error condition (future: could change color)
        """
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def _reset_form(self):
        """
        Reset all input fields to their default values.
        """
        # Confirm reset action
        response = messagebox.askyesno(
            "Confirm Reset",
            "This will clear all input fields and preview.\n\nAre you sure?"
        )
        if not response:
            return
        
        # Clear all input variables
        self.directory_var.set("")
        self.prefix_var.set("")
        self.suffix_var.set("")
        self.numbering_var.set(False)
        self.numbering_start_var.set("1")
        self.numbering_padding_var.set("3")
        self.timestamp_var.set(False)
        self.timestamp_format_var.set("%Y%m%d%H%M%S")
        self.regex_pattern_var.set("")
        self.regex_replacement_var.set("")
        self.extensions_var.set("")
        self.backup_dir_var.set("")
        self.log_file_var.set("")
        self.dry_run_var.set(False)
        
        # Clear preview
        self._clear_preview()
        
        # Update status
        self._update_status("Form reset. Ready for new operation.")
    
    def _exit_application(self):
        """
        Exit the application with confirmation.
        """
        response = messagebox.askyesno(
            "Exit Application",
            "Are you sure you want to exit?"
        )
        if response:
            self.root.quit()
    
    def _toggle_theme(self):
        """
        Toggle between light and dark themes.
        """
        if self.theme_manager:
            try:
                new_theme = self.theme_manager.toggle_theme()
                self._update_status(f"Switched to {'dark' if new_theme == 'dark' else 'light'} mode")
            except Exception as e:
                if hasattr(self, 'dark_mode_var'):
                    self.dark_mode_var.set(not self.dark_mode_var.get())
                messagebox.showerror(
                    "Theme Error",
                    f"Failed to change theme: {e}"
                )
    
    def _undo_last_rename(self):
        """
        Undo the most recent rename operation.
        """
        self._update_status("Preparing undo operation...")
        
        # Get current directory
        directory = self.directory_var.get().strip()
        if not directory:
            messagebox.showerror(
                "No Directory Selected",
                "Please select a directory first.\n\n"
                "The undo operation will search for rename logs in this directory."
            )
            self._update_status("Undo cancelled - no directory selected", is_error=True)
            return
        
        # Confirm undo operation
        response = messagebox.askyesno(
            "Confirm Undo",
            f"This will restore files to their original names in:\n{directory}\n\n"
            "The most recent rename operation will be reversed using\n"
            "the backup files and rename log.\n\n"
            "Do you want to continue?"
        )
        
        if not response:
            self._update_status("Undo operation cancelled by user")
            return
        
        try:
            # Import undo module
            from undo import undo_rename
            
            self._update_status("Searching for rename log...")
            
            # Perform undo
            result = undo_rename(directory)
            
            if result['success']:
                # Show success message
                restored_count = result['restored_count']
                skipped_count = result['skipped_count']
                log_file = os.path.basename(result['log_file'])
                backup_dir = os.path.basename(result['backup_dir'])
                
                message = (
                    f"Undo completed successfully!\n\n"
                    f"Restored: {restored_count} file(s)\n"
                    f"Skipped: {skipped_count} file(s)\n\n"
                    f"Log file: {log_file}\n"
                    f"Backup directory: {backup_dir}"
                )
                
                if skipped_count > 0:
                    message += "\n\nSome files were skipped. Common reasons:\n"
                    message += "  - File was not actually renamed\n"
                    message += "  - Backup file missing\n"
                    message += "  - File has been modified since rename"
                
                messagebox.showinfo("Undo Successful", message)
                self._update_status(f"Undo complete: Restored {restored_count} file(s)")
                
                # Clear preview table
                self._clear_preview()
                
            else:
                # Show error message
                error_msg = result.get('error_message', 'Unknown error')
                messagebox.showerror(
                    "Undo Failed",
                    f"Could not undo the rename operation:\n\n{error_msg}\n\n"
                    "Please check that:\n"
                    "  - A rename operation was performed\n"
                    "  - The backup directory exists\n"
                    "  - The rename log file exists"
                )
                self._update_status(f"Undo failed: {error_msg}", is_error=True)
        
        except ImportError:
            messagebox.showerror(
                "Undo Module Missing",
                "The undo module (undo.py) is not available.\n\n"
                "Please ensure all application files are present."
            )
            self._update_status("Undo failed: Module missing", is_error=True)
        
        except Exception as e:
            messagebox.showerror(
                "Undo Error",
                f"An unexpected error occurred during undo:\n\n{e}"
            )
            self._update_status(f"Undo error: {e}", is_error=True)

    def _preview_changes(self):
        """
        Generate and display a preview of rename operations.
        """
        self._update_status("Generating preview...")
        config = self._get_config()
        if not config:
            self._update_status("Preview cancelled - invalid configuration", is_error=True)
            return

        # Set dry_run to True for preview
        config.dry_run = True

        try:
            preview_records = preview_renames(config)
            self._clear_preview()

            if not preview_records:
                messagebox.showinfo("Preview", "No files found to rename.")
                self._update_status("No files to rename", is_error=True)
                return

            for record in preview_records:
                self.preview_tree.insert(
                    "",
                    tk.END,
                    values=(record["original_name"], record["new_name"]),
                )

            messagebox.showinfo(
                "Preview Complete",
                f"Preview generated for {len(preview_records)} file(s).\n"
                "Review the changes above before renaming.",
            )
            self._update_status(f"Preview ready: {len(preview_records)} file(s) will be renamed")

        except ValueError as e:
            messagebox.showerror("Preview Error", str(e))
            self._update_status(f"Preview error: {e}", is_error=True)
        except PermissionError as e:
            messagebox.showerror("Permission Error", str(e))
            self._update_status(f"Permission denied: {e}", is_error=True)
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error during preview: {e}")
            self._update_status(f"Unexpected error: {e}", is_error=True)

    def _rename_files(self):
        """
        Execute the rename operation using the current configuration.
        """
        self._update_status("Preparing rename operation...")
        config = self._get_config()
        if not config:
            self._update_status("Operation cancelled - invalid configuration", is_error=True)
            return

        # Confirm before proceeding (unless dry run)
        if not config.dry_run:
            response = messagebox.askyesno(
                "Confirm Rename",
                f"This will rename files in:\n{config.directory}\n\n"
                "Original files will be backed up.\n\n"
                "Do you want to continue?",
            )
            if not response:
                self._update_status("Rename operation cancelled by user")
                return

        try:
            self._update_status("Renaming files...")
            result = rename_files(config)

            if config.dry_run:
                messagebox.showinfo(
                    "Dry Run Complete",
                    f"Dry run completed for {result['renamed_count']} file(s).\n"
                    "No files were actually renamed.",
                )
                self._update_status(f"Dry run complete: {result['renamed_count']} file(s) processed")
            else:
                messagebox.showinfo(
                    "Rename Complete",
                    f"Successfully renamed {result['renamed_count']} file(s).\n\n"
                    f"Backup directory: {result['backup_dir']}\n"
                    f"Log file: {result['log_file']}",
                )
                # Update preview to show final results
                self._clear_preview()
                for record in result["records"]:
                    self.preview_tree.insert(
                        "",
                        tk.END,
                        values=(record["original_name"], record["new_name"]),
                    )
                self._update_status(f"Success: Renamed {result['renamed_count']} file(s)")

        except FileExistsError as e:
            messagebox.showerror("File Exists Error", str(e))
            self._update_status(f"Error: File already exists", is_error=True)
        except ValueError as e:
            messagebox.showerror("Validation Error", str(e))
            self._update_status(f"Validation error: {e}", is_error=True)
        except PermissionError as e:
            messagebox.showerror("Permission Error", str(e))
            self._update_status(f"Permission denied: {e}", is_error=True)
        except OSError as e:
            messagebox.showerror("File System Error", f"Error accessing files: {e}")
            self._update_status(f"File system error: {e}", is_error=True)
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error during rename: {e}")
            self._update_status(f"Unexpected error: {e}", is_error=True)


def main():
    """
    Launch the GUI application.
    """
    root = tk.Tk()
    app = BulkFileRenamerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

