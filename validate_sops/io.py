from validate_sops.logger import LOGGER


def read_file(file_path):
    try:
        with open(file_path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        LOGGER.error("File not found: %s", file_path)
    except PermissionError:
        LOGGER.error("Permission denied: %s", file_path)
    except UnicodeDecodeError:
        LOGGER.error("Unable to decode file: %s", file_path)
    except Exception as e:
        LOGGER.error("Unexpected error reading %s: %s", file_path, e)
    return None
