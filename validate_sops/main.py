import fnmatch
import os
import sys
from argparse import ArgumentParser

from validate_sops.ignore import load_ignore_list
from validate_sops.logger import LOGGER
from validate_sops.sops import is_sops_encrypted


def main():
    parser = ArgumentParser(
        description="Check if files are encrypted with SOPS."
    )
    parser.add_argument("filenames", nargs="+", help="Files to check")
    parser.add_argument(
        "--ignore-file",
        default=".validate-sops-ignore",
        help="Path to a file listing files to ignore (supports glob patterns).",
    )

    args = parser.parse_args()
    ignore_patterns = load_ignore_list(args.ignore_file)

    failed = False

    for file_path in args.filenames:
        rel_path = os.path.relpath(file_path)

        if any(
            fnmatch.fnmatch(rel_path, pattern) for pattern in ignore_patterns
        ):
            LOGGER.info("Skipping ignored file: %s", rel_path)
            continue

        if not is_sops_encrypted(file_path):
            LOGGER.error(
                "❌ The file %s is NOT encrypted with SOPS.", file_path
            )
            failed = True

    if failed:
        sys.exit(1)

    LOGGER.info("✅ All files are properly encrypted with SOPS.")
