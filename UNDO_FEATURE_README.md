# Undo Feature - Documentation

## Overview

The Bulk File Renamer now includes a powerful **Undo** feature that allows users to reverse rename operations by restoring files from backup directories.

---

## Features

✅ **Automatic Log Detection** - Finds the most recent rename log  
✅ **Backup Restoration** - Restores files from automatic backups  
✅ **Confirmation Dialog** - Prevents accidental undo  
✅ **Detailed Results** - Shows what was restored/skipped  
✅ **Error Handling** - Handles edge cases gracefully  
✅ **Status Feedback** - Real-time status updates  

---

## How It Works

### Rename Operation Creates:
1. **Backup Directory**: `backup_<timestamp>/`
   - Contains copies of original files
2. **Log File**: `rename_log_<timestamp>.json`
   - Records old → new name mappings

### Undo Operation:
1. Finds most recent `rename_log_*.json`
2. Reads the backup directory path
3. Restores each file from backup
4. Removes renamed files
5. Shows detailed results

---

## Using the Undo Feature

### Step 1: Select Directory
- Click **Browse** and select the directory where you renamed files
- This is the SAME directory you used for the rename operation

### Step 2: Click "Undo Last Rename"
- Button is in the main action button row
- Located between "Rename Files" and "Reset"

### Step 3: Confirm Undo
- Review the confirmation dialog
- Shows:
  - Directory path
  - What will be restored
  - Backup source
- Click **Yes** to proceed or **No** to cancel

### Step 4: Review Results
- Success dialog shows:
  - Number of files restored
  - Number of files skipped
  - Log file used
  - Backup directory used

---

## Example Usage

### Scenario: Renamed Files Incorrectly

```
1. You renamed 50 photos with wrong prefix
2. Files are now: "WRONG_001.jpg", "WRONG_002.jpg", etc.
3. You realize the mistake

Solution:
1. Select the same directory
2. Click "Undo Last Rename"
3. Confirm
4. Files restored to: "photo1.jpg", "photo2.jpg", etc.
```

---

## Edge Cases Handled

### No Log File Found
**Error**: "No rename log files found in directory."

**Reason**: No rename operations performed in this directory

**Solution**: Undo not possible (no log to restore from)

### No Backup Directory
**Error**: "No backup directories found in [directory]"

**Reason**: Backup was deleted or moved

**Solution**: Cannot restore without backup files

### Backup File Missing
**Result**: File skipped

**Reason**: Specific backup file was deleted

**Note**: Other files still restored

### File Already Restored
**Result**: File skipped

**Reason**: File doesn't exist at renamed location

**Note**: Safe to skip, might already be restored

---

## Files Involved

### Created Files

| File | Purpose |
|------|---------|
| `undo.py` | Undo module with restoration logic |
| `gui.py` (updated) | Added "Undo Last Rename" button |

### Dependencies

| Module | Usage |
|--------|-------|
| `json` | Read rename logs |
| `glob` | Find log/backup files |
| `shutil` | Copy files from backup |
| `os` | File operations |

---

## Technical Details

### Log File Format

```json
{
  "renamed_files": [
    {
      "original_name": "file1.txt",
      "new_name": "new_file1.txt",
      "original_path": "C:/path/file1.txt",
      "new_path": "C:/path/new_file1.txt",
      "renamed_at": "2026-01-21 14:30:00"
    }
  ],
  "generated_at": "2026-01-21 14:30:00"
}
```

### Undo Process

```python
1. find_latest_log(directory)
   ↓
2. load_rename_log(log_file)
   ↓
3. Find backup directory
   ↓
4. For each renamed file:
   ↓
   a. Check backup exists
   ↓
   b. Check current file exists
   ↓
   c. Copy backup → original location
   ↓
   d. Remove renamed file
   ↓
5. Return results
```

### Return Value

```python
{
    'success': bool,
    'restored_count': int,
    'skipped_count': int,
    'error_message': str,
    'log_file': str,
    'backup_dir': str,
    'details': [
        {
            'original_name': str,
            'status': str
        }
    ]
}
```

---

## GUI Integration

### Button Placement

```
[Preview Changes] [Rename Files] [Undo Last Rename] [Reset] [Exit]
```

### User Flow

```
User clicks "Undo Last Rename"
    ↓
Status: "Preparing undo operation..."
    ↓
Verification: Directory selected?
    ↓
Confirmation dialog
    ↓
Status: "Searching for rename log..."
    ↓
Perform undo operation
    ↓
Success dialog OR Error dialog
    ↓
Status: "Undo complete: Restored N file(s)"
```

---

## Error Messages

### No Directory Selected
```
Title: No Directory Selected
Message: Please select a directory first.

The undo operation will search for rename logs 
in this directory.
```

### Undo Failed
```
Title: Undo Failed
Message: Could not undo the rename operation:
[Error details]

Please check that:
  - A rename operation was performed
  - The backup directory exists
  - The rename log file exists
```

### Success
```
Title: Undo Successful
Message: Undo completed successfully!

Restored: X file(s)
Skipped: Y file(s)

Log file: rename_log_123456.json
Backup directory: backup_123456
```

---

## Limitations

❌ **Cannot undo multiple times**
- Each undo restores from ONE backup
- To undo multiple operations, run undo multiple times
- Each time uses the NEXT most recent log

❌ **Backup must exist**
- If backup directory deleted, undo not possible
- Keep backups until sure rename is correct

❌ **Files must not be modified**
- If renamed files were edited, backups are OLD versions
- Undo will restore old version (data loss possible)
- Dialog warns about this

---

## Best Practices

✅ **Keep backups** until you verify rename is correct

✅ **Test with dry-run** before actual rename

✅ **Check results** before deleting backups

✅ **Undo immediately** if mistake discovered

✅ **One operation at a time** - easier to track

---

## Testing

### Test Scenario 1: Simple Undo

```bash
# 1. Create test files
mkdir test_undo
cd test_undo
echo "test" > file1.txt
echo "test" > file2.txt

# 2. Rename using app
# Use app to rename: file1.txt → renamed1.txt

# 3. Verify backup created
dir backup_*

# 4. Undo using app
# Click "Undo Last Rename"

# 5. Verify restoration
dir file1.txt  # Should exist again
```

### Test Scenario 2: Multiple Files

```bash
# 1. Create 10 test files
for i in 1..10:
    create file{i}.txt

# 2. Bulk rename with prefix
# Result: TEST_file1.txt, TEST_file2.txt, etc.

# 3. Undo
# Click "Undo Last Rename"

# 4. Verify all restored
# Back to: file1.txt, file2.txt, etc.
```

---

## Command Line Usage

You can also use the undo module from command line:

```bash
python undo.py "C:\path\to\directory"
```

Output:
```
Success: True
Restored: 10
Skipped: 0

Log file: C:\path\rename_log_123456.json
Backup dir: C:\path\backup_123456
```

---

## Troubleshooting

### Issue: "No rename log files found"

**Check:**
- Are you in the correct directory?
- Was a rename operation performed?
- Look for `rename_log_*.json` files

### Issue: "No backup directories found"

**Check:**
- Was backup created during rename?
- Look for `backup_*` folders
- Was backup manually deleted?

### Issue: "Some files skipped"

**Reasons:**
- Backup file missing → can't restore that file
- Renamed file missing → already restored or moved
- Permission denied → need admin rights

### Issue: Undo button disabled/grayed

**Check:**
- Is a directory selected?
- Try selecting directory again

---

## Future Enhancements

Potential improvements:

- [ ] **Multiple undo levels** - Undo stack for multiple operations
- [ ] **Selective undo** - Choose which files to restore
- [ ] **Undo history** - View all past rename operations
- [ ] **Backup management** - Clean old backups automatically
- [ ] **Diff preview** - Show what will change before undo

---

## Summary

✅ **One-click undo** for rename operations  
✅ **Automatic backup detection**  
✅ **Safe with confirmation**  
✅ **Detailed feedback**  
✅ **Handles edge cases**  

The undo feature provides a safety net for your file renaming operations!

---

**Tip**: Always verify your renames are correct before deleting backup directories. The undo feature relies on these backups to restore files.
