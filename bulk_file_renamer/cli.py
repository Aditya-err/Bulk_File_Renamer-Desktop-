"""
Command-line interface for the Bulk File Renamer project.
"""

import argparse
import sys

from .renamer import BulkRenameConfig, rename_files


def build_parser() -> argparse.ArgumentParser:
    """
    Create and configure the argument parser for the CLI.
    """
    parser = argparse.ArgumentParser(
        description="Bulk File Renamer - rename files with prefixes, suffixes, numbering, timestamps, and regex patterns."
    )
    parser.add_argument(
        "directory",
        help="Path to the directory containing files to rename.",
    )
    parser.add_argument(
        "--prefix",
        help="Optional prefix to add to each file name.",
    )
    parser.add_argument(
        "--suffix",
        help="Optional suffix to add to each file name.",
    )
    parser.add_argument(
        "--numbering",
        action="store_true",
        help="Enable sequential numbering appended to file names.",
    )
    parser.add_argument(
        "--numbering-start",
        type=int,
        default=1,
        help="Starting number for sequential numbering (default: 1).",
    )
    parser.add_argument(
        "--numbering-padding",
        type=int,
        default=3,
        help="Zero-padding width for numbering (default: 3).",
    )
    parser.add_argument(
        "--timestamp",
        action="store_true",
        help="Append a timestamp to each renamed file.",
    )
    parser.add_argument(
        "--timestamp-format",
        default="%Y%m%d%H%M%S",
        help="Time format string used when --timestamp is enabled (default: %%Y%%m%%d%%H%%M%%S).",
    )
    parser.add_argument(
        "--regex-pattern",
        help="Regex pattern to transform file names.",
    )
    parser.add_argument(
        "--regex-replacement",
        help="Replacement string used with --regex-pattern.",
    )
    parser.add_argument(
        "--extensions",
        nargs="+",
        help="Only rename files with these extensions (e.g., --extensions .txt .jpg).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without copying or renaming files.",
    )
    parser.add_argument(
        "--backup-dir",
        help="Custom backup directory path. Defaults to a timestamped folder inside the target directory.",
    )
    parser.add_argument(
        "--log-file",
        help="Custom path for the rename log JSON file.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """
    Entry point for the CLI.
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    config = BulkRenameConfig(
        directory=args.directory,
        prefix=args.prefix,
        suffix=args.suffix,
        numbering=args.numbering,
        numbering_start=args.numbering_start,
        numbering_padding=args.numbering_padding,
        timestamp=args.timestamp,
        timestamp_format=args.timestamp_format,
        regex_pattern=args.regex_pattern,
        regex_replacement=args.regex_replacement,
        extensions=args.extensions,
        dry_run=args.dry_run,
        backup_dir=args.backup_dir,
        log_file=args.log_file,
    )

    try:
        result = rename_files(config)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
        return 1

    if config.dry_run:
        print("Dry run complete. No files were renamed.")
    else:
        print(f"Renamed {result['renamed_count']} files.")
        print(f"Backup directory: {result['backup_dir']}")
        print(f"Log file: {result['log_file']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

