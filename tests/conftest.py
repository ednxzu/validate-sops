import os

import pytest

PROJECT_ROOT = os.path.dirname(__file__)
SECRETS_DIR = os.path.join(PROJECT_ROOT, "secrets")


@pytest.fixture(scope="session")
def secrets_dir():
    return SECRETS_DIR
