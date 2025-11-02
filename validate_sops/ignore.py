import os

from validate_sops.logger import LOGGER


def load_ignore_list(ignore_file):
    if not os.path.exists(ignore_file):
        return []
    try:
        with open(ignore_file, encoding="utf-8") as f:
            return [
                line.strip()
                for line in f
                if line.strip() and not line.startswith("#")
            ]
    except Exception as e:
        LOGGER.warning("Could not read ignore file %s: %s", ignore_file, e)
        return []
