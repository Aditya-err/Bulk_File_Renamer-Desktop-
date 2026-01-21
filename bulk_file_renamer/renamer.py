"""
Core renaming logic for the Bulk File Renamer project.
"""

import json
import os
import re
import shutil
import time


class BulkRenameConfig:
    """
    Configuration container for rename operations.
    """

    def __init__(
        self,
        directory,
        prefix=None,
        suffix=None,
        numbering=False,
        numbering_start=1,
        numbering_padding=3,
        timestamp=False,
        timestamp_format="%Y%m%d%H%M%S",
        regex_pattern=None,
        regex_replacement=None,
        extensions=None,
        dry_run=False,
        backup_dir=None,
        log_file=None,
    ):
        self.directory = directory
        self.prefix = prefix or ""
        self.suffix = suffix or ""
        self.numbering = numbering
        self.numbering_start = numbering_start
        self.numbering_padding = numbering_padding
        self.timestamp = timestamp
        self.timestamp_format = timestamp_format
        self.regex_pattern = regex_pattern
        self.regex_replacement = regex_replacement
        self.extensions = self._normalize_extensions(extensions)
        self.dry_run = dry_run
        self.backup_dir = backup_dir
        self.log_file = log_file

    @staticmethod
    def _normalize_extensions(extensions):
        if not extensions:
            return None
        normalized = []
        for ext in extensions:
            if not ext:
                continue
            ext = ext.lower()
            if not ext.startswith("."):
                ext = f".{ext}"
            normalized.append(ext)
        return normalized or None

    def validate(self):
        """
        Validate the configuration before running the rename.
        """
        if not self.directory:
            raise ValueError("A directory path is required.")

        if not os.path.exists(self.directory):
            raise ValueError(f"Directory not found: {self.directory}")

        if not os.path.isdir(self.directory):
            raise ValueError(f"Path is not a directory: {self.directory}")

        if self.numbering and self.numbering_padding < 0:
            raise ValueError("Numbering padding must be non-negative.")

        if self.numbering and self.numbering_start < 0:
            raise ValueError("Numbering start must be non-negative.")

        if bool(self.regex_pattern) != bool(self.regex_replacement):
            raise ValueError("Both --regex-pattern and --regex-replacement are required together.")


def rename_files(config: BulkRenameConfig):
    """
    Rename files according to the provided configuration.
    """
    config.validate()
    files = _collect_files(config.directory, config.extensions)

    if not files:
        raise ValueError("No files found to rename. Check the directory or extension filters.")

    backup_dir = config.backup_dir or os.path.join(
        config.directory, f"backup_{int(time.time())}"
    )
    log_file = config.log_file or os.path.join(
        config.directory, f"rename_log_{int(time.time())}.json"
    )

    rename_records = []
    counter = config.numbering_start

    for file_path in files:
        original_name = os.path.basename(file_path)
        new_name = _build_new_name(original_name, config, counter)
        new_path = os.path.join(config.directory, new_name)

        if config.numbering:
            counter += 1

        record = {
            "original_name": original_name,
            "new_name": new_name,
            "original_path": file_path,
            "new_path": new_path,
        }

        if config.dry_run:
            print(f"[DRY-RUN] {original_name} -> {new_name}")
            rename_records.append(record)
            continue

        if os.path.abspath(file_path) == os.path.abspath(new_path):
            record["skipped"] = "Name unchanged."
            rename_records.append(record)
            continue

        if os.path.exists(new_path):
            raise FileExistsError(f"Target file already exists: {new_path}")

        _ensure_directory(backup_dir)
        backup_path = os.path.join(backup_dir, original_name)
        shutil.copy2(file_path, backup_path)

        os.replace(file_path, new_path)

        record["renamed_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
        rename_records.append(record)

    if not config.dry_run:
        _write_log(log_file, rename_records)

    return {
        "renamed_count": len(rename_records),
        "backup_dir": backup_dir if not config.dry_run else None,
        "log_file": log_file if not config.dry_run else None,
        "dry_run": config.dry_run,
        "records": rename_records,
    }


def _collect_files(directory, extensions):
    """
    Gather files from a directory, optionally filtering by extension.
    """
    files = []
    try:
        for entry in os.scandir(directory):
            if entry.is_file():
                if extensions:
                    _, ext = os.path.splitext(entry.name)
                    if ext.lower() not in extensions:
                        continue
                files.append(entry.path)
    except PermissionError as exc:
        raise PermissionError(f"Permission denied while accessing directory: {directory}") from exc
    return sorted(files)


def _build_new_name(original_name, config, counter):
    """
    Construct the new file name based on configuration options.
    """
    stem, extension = os.path.splitext(original_name)
    new_stem = stem

    if config.regex_pattern and config.regex_replacement:
        try:
            new_stem = re.sub(config.regex_pattern, config.regex_replacement, new_stem)
        except re.error as exc:
            raise ValueError(f"Invalid regex pattern: {exc}") from exc

    if not new_stem:
        raise ValueError(f"Regex produced an empty file name for {original_name}.")

    if config.prefix:
        new_stem = f"{config.prefix}{new_stem}"

    if config.suffix:
        new_stem = f"{new_stem}{config.suffix}"

    if config.numbering:
        padding = max(0, config.numbering_padding)
        number_token = str(counter).zfill(padding) if padding else str(counter)
        new_stem = f"{new_stem}{number_token}"

    if config.timestamp:
        timestamp_str = time.strftime(config.timestamp_format).replace(" ", "_")
        new_stem = f"{new_stem}{timestamp_str}"

    return f"{new_stem}{extension}"


def _ensure_directory(path):
    """
    Create the directory if it does not exist.
    """
    if not os.path.exists(path):
        os.makedirs(path)


def _write_log(log_path, records):
    """
    Write rename operations to a JSON log file.
    """
    data = {"renamed_files": records, "generated_at": time.strftime("%Y-%m-%d %H:%M:%S")}
    with open(log_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

