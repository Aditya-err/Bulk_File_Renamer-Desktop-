"""
Undo Module for Bulk File Renamer

Provides functionality to undo previous rename operations by:
- Reading the most recent rename log
- Restoring files from backup directory
- Handling edge cases and errors gracefully
"""

import json
import os
import shutil
import glob
from typing import Dict, Optional, List


def find_latest_log(directory: str) -> Optional[str]:
    """
    Find the most recent rename log file in the directory.
    
    Args:
        directory: Directory to search for log files
        
    Returns:
        Path to the most recent log file, or None if not found
    """
    log_pattern = os.path.join(directory, "rename_log_*.json")
    log_files = glob.glob(log_pattern)
    
    if not log_files:
        return None
    
    # Sort by modification time, most recent first
    log_files.sort(key=os.path.getmtime, reverse=True)
    return log_files[0]


def load_rename_log(log_file: str) -> Optional[Dict]:
    """
    Load and parse a rename log file.
    
    Args:
        log_file: Path to the log file
        
    Returns:
        Parsed log data, or None if error
    """
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return None


def undo_rename(directory: str, log_file: Optional[str] = None) -> Dict:
    """
    Undo the most recent rename operation.
    
    Args:
        directory: Directory where files were renamed
        log_file: Optional specific log file to use. If None, finds latest.
        
    Returns:
        Dictionary with results:
            - success: bool
            - restored_count: int
            - skipped_count: int
            - error_message: str (if success is False)
            - log_file: str (path to log used)
            - backup_dir: str (path to backup used)
            - details: list of dicts with restoration details
    """
    result = {
        'success': False,
        'restored_count': 0,
        'skipped_count': 0,
        'error_message': '',
        'log_file': '',
        'backup_dir': '',
        'details': []
    }
    
    # Find log file if not specified
    if log_file is None:
        log_file = find_latest_log(directory)
        if log_file is None:
            result['error_message'] = "No rename log files found in directory."
            return result
    
    result['log_file'] = log_file
    
    # Load log data
    log_data = load_rename_log(log_file)
    if log_data is None:
        result['error_message'] = f"Failed to read log file: {log_file}"
        return result
    
    # Get renamed files list
    renamed_files = log_data.get('renamed_files', [])
    if not renamed_files:
        result['error_message'] = "Log file contains no rename records."
        return result
    
    # Determine backup directory from first record
    first_record = renamed_files[0]
    original_path = first_record.get('original_path', '')
    
    if not original_path:
        result['error_message'] = "Log file format invalid (missing original_path)."
        return result
    
    # Try to find backup directory
    # Look for backup_* directories in the same location
    parent_dir = os.path.dirname(original_path)
    backup_pattern = os.path.join(parent_dir, "backup_*")
    backup_dirs = glob.glob(backup_pattern)
    
    if not backup_dirs:
        result['error_message'] = f"No backup directories found in {parent_dir}"
        return result
    
    # Sort by modification time, use most recent
    backup_dirs.sort(key=os.path.getmtime, reverse=True)
    backup_dir = backup_dirs[0]
    result['backup_dir'] = backup_dir
    
    # Verify backup directory exists
    if not os.path.exists(backup_dir):
        result['error_message'] = f"Backup directory not found: {backup_dir}"
        return result
    
    # Process each renamed file
    restored = 0
    skipped = 0
    
    for record in renamed_files:
        original_name = record.get('original_name', '')
        new_name = record.get('new_name', '')
        original_path = record.get('original_path', '')
        new_path = record.get('new_path', '')
        
        detail = {
            'original_name': original_name,
            'status': ''
        }
        
        # Skip if this file was skipped during rename
        if record.get('skipped'):
            detail['status'] = 'Skipped (was not renamed)'
            result['details'].append(detail)
            skipped += 1
            continue
        
        # Check if backup file exists
        backup_file_path = os.path.join(backup_dir, original_name)
        if not os.path.exists(backup_file_path):
            detail['status'] = f'Backup file not found: {original_name}'
            result['details'].append(detail)
            skipped += 1
            continue
        
        # Check if current file exists (the renamed file)
        if not os.path.exists(new_path):
            detail['status'] = f'Current file missing: {new_name}'
            result['details'].append(detail)
            skipped += 1
            continue
        
        try:
            # Restore: copy backup to original location with original name
            shutil.copy2(backup_file_path, original_path)
            
            # Remove the renamed file (since we restored original)
            if os.path.exists(new_path) and new_path != original_path:
                os.remove(new_path)
            
            detail['status'] = 'Restored successfully'
            result['details'].append(detail)
            restored += 1
            
        except Exception as e:
            detail['status'] = f'Error: {str(e)}'
            result['details'].append(detail)
            skipped += 1
    
    result['restored_count'] = restored
    result['skipped_count'] = skipped
    result['success'] = restored > 0
    
    if restored == 0:
        result['error_message'] = "No files could be restored. Check backup directory."
    
    return result


if __name__ == "__main__":
    # Test function
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python undo.py <directory>")
        sys.exit(1)
    
    directory = sys.argv[1]
    result = undo_rename(directory)
    
    print(f"Success: {result['success']}")
    print(f"Restored: {result['restored_count']}")
    print(f"Skipped: {result['skipped_count']}")
    if result['error_message']:
        print(f"Error: {result['error_message']}")
    print(f"\nLog file: {result['log_file']}")
    print(f"Backup dir: {result['backup_dir']}")
