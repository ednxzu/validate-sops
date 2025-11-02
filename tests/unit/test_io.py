from unittest.mock import patch

import pytest

from validate_sops.io import read_file


@pytest.mark.unit
def test_read_file_success(tmp_path):
    f = tmp_path / "file.txt"
    f.write_text("hello", encoding="utf-8")
    assert read_file(str(f)) == "hello"


@pytest.mark.unit
def test_read_file_not_found():
    with patch("validate_sops.io.LOGGER.error") as mock_log:
        assert read_file("missing.txt") is None
        mock_log.assert_called_once_with("File not found: %s", "missing.txt")


@pytest.mark.unit
def test_read_file_permission_denied():
    with (
        patch("builtins.open", side_effect=PermissionError),
        patch("validate_sops.io.LOGGER.error") as mock_log,
    ):
        assert read_file("restricted.txt") is None
        mock_log.assert_called_once_with(
            "Permission denied: %s", "restricted.txt"
        )


@pytest.mark.unit
def test_read_file_unicode_error():
    with (
        patch(
            "builtins.open",
            side_effect=UnicodeDecodeError("utf-8", b"", 0, 1, "error"),
        ),
        patch("validate_sops.io.LOGGER.error") as mock_log,
    ):
        assert read_file("corrupt.txt") is None
        mock_log.assert_called_once()
