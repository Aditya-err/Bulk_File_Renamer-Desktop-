"""
Utility functions for the Bulk File Renamer GUI application.
Helper functions for common operations.
"""

import os


def parse_extensions(ext_string):
    """
    Parse a space-separated or comma-separated string of extensions.
    Returns a list of normalized extensions or None if empty.
    
    Examples:
        ".jpg .png .txt" -> [".jpg", ".png", ".txt"]
        "jpg, png, txt" -> [".jpg", ".png", ".txt"]
        "" -> None
    """
    if not ext_string or not ext_string.strip():
        return None
    
    # Split by comma or space
    extensions = []
    for part in ext_string.replace(",", " ").split():
        ext = part.strip()
        if ext:
            extensions.append(ext)
    
    return extensions if extensions else None


def validate_directory(path):
    """
    Validate that a path exists and is a directory.
    Returns True if valid, raises ValueError otherwise.
    """
    if not path or not path.strip():
        raise ValueError("Directory path cannot be empty.")
    
    if not os.path.exists(path):
        raise ValueError(f"Directory not found: {path}")
    
    if not os.path.isdir(path):
        raise ValueError(f"Path is not a directory: {path}")
    
    return True


def get_default_backup_dir(target_directory):
    """
    Generate a default backup directory path inside the target directory.
    """
    import time
    return os.path.join(target_directory, f"backup_{int(time.time())}")


def get_default_log_file(target_directory):
    """
    Generate a default log file path inside the target directory.
    """
    import time
    return os.path.join(target_directory, f"rename_log_{int(time.time())}.json")

