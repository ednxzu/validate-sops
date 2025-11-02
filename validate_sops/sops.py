import json

import yaml

from validate_sops.io import read_file
from validate_sops.logger import LOGGER


def is_sops_encrypted_json_or_yaml(data):
    return (
        isinstance(data, dict) and "sops" in data and "version" in data["sops"]
    )


def is_sops_encrypted_env(content):
    return any(
        line.strip().startswith("sops_version=")
        for line in reversed(content.splitlines())
    )


def is_sops_encrypted(file_path):
    file_ext = file_path.lower().split(".")[-1]
    content = read_file(file_path)
    if content is None:
        return False

    parsers = {
        "json": lambda c: is_sops_encrypted_json_or_yaml(json.loads(c)),
        "yaml": lambda c: is_sops_encrypted_json_or_yaml(yaml.safe_load(c)),
        "yml": lambda c: is_sops_encrypted_json_or_yaml(yaml.safe_load(c)),
        "env": is_sops_encrypted_env,
    }

    if file_ext in parsers:
        try:
            return parsers[file_ext](content)
        except (json.JSONDecodeError, yaml.YAMLError):
            LOGGER.error("Invalid %s syntax in %s", file_ext, file_path)
        except Exception as e:
            LOGGER.error("Error processing %s: %s", file_path, e)
    else:
        LOGGER.warning("Unsupported file type: %s", file_path)
    return False
