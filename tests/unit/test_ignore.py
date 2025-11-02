from unittest.mock import patch

import pytest

from validate_sops.ignore import load_ignore_list


@pytest.mark.unit
def test_load_ignore_list_basic(tmp_path):
    f = tmp_path / "ignore"
    f.write_text("file1\nfile2\n# comment\n\n")
    patterns = load_ignore_list(str(f))
    assert patterns == ["file1", "file2"]


@pytest.mark.unit
def test_load_ignore_list_exception(tmp_path):
    f = tmp_path / "ignore"
    f.touch()

    with (
        patch("builtins.open", side_effect=Exception("boom")),
        patch("validate_sops.ignore.LOGGER.warning") as mock_log,
    ):
        result = load_ignore_list(str(f))
        assert result == []
        mock_log.assert_called_once()
