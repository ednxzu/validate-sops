import os
import sys
from unittest.mock import patch

import pytest

from validate_sops.main import main


@pytest.mark.integration
def test_ignore_file_feature(secrets_dir, tmp_path):
    ignored_file = os.path.join(secrets_dir, "unencrypted.json")
    failing_file = os.path.join(secrets_dir, "unencrypted.yaml")
    ignore_file = tmp_path / ".validate-sops-ignore"
    ignore_file.write_text(os.path.relpath(ignored_file) + "\n")

    with (
        patch.object(
            sys,
            "argv",
            [
                "validate-sops",
                ignored_file,
                failing_file,
                "--ignore-file",
                str(ignore_file),
            ],
        ),
        patch("validate_sops.main.LOGGER.info") as mock_info,
        patch("validate_sops.main.LOGGER.error") as mock_error,
        patch("sys.exit") as mock_exit,
    ):
        main()

    mock_info.assert_any_call(
        "Skipping ignored file: %s", os.path.relpath(ignored_file)
    )
    mock_error.assert_any_call(
        "❌ The file %s is NOT encrypted with SOPS.", failing_file
    )
    mock_exit.assert_called_once_with(1)


@pytest.mark.integration
def test_nonexistent_ignore_file(secrets_dir, tmp_path):
    failing_file = os.path.join(secrets_dir, "unencrypted.json")
    ignore_file = tmp_path / "nonexistent-ignore"

    with (
        patch.object(
            sys,
            "argv",
            ["validate-sops", failing_file, "--ignore-file", str(ignore_file)],
        ),
        patch("validate_sops.main.LOGGER.error") as mock_error,
        patch("sys.exit") as mock_exit,
    ):
        main()

    mock_error.assert_any_call(
        "❌ The file %s is NOT encrypted with SOPS.", failing_file
    )
    mock_exit.assert_called_once_with(1)


@pytest.mark.integration
def test_ignore_file_with_comments(secrets_dir, tmp_path):
    ignored_file = os.path.join(secrets_dir, "unencrypted.json")
    failing_file = os.path.join(secrets_dir, "unencrypted.yaml")
    ignore_file = tmp_path / ".validate-sops-ignore"
    ignore_file.write_text(
        "# comment\n\n" + os.path.relpath(ignored_file) + "\n"
    )

    with (
        patch.object(
            sys,
            "argv",
            [
                "validate-sops",
                ignored_file,
                failing_file,
                "--ignore-file",
                str(ignore_file),
            ],
        ),
        patch("validate_sops.main.LOGGER.info") as mock_info,
        patch("validate_sops.main.LOGGER.error") as mock_error,
        patch("sys.exit") as mock_exit,
    ):
        main()

    mock_info.assert_any_call(
        "Skipping ignored file: %s", os.path.relpath(ignored_file)
    )
    mock_error.assert_any_call(
        "❌ The file %s is NOT encrypted with SOPS.", failing_file
    )
    mock_exit.assert_called_once_with(1)


@pytest.mark.integration
def test_ignore_multiple_patterns(secrets_dir, tmp_path):
    ignored_file1 = os.path.join(secrets_dir, "unencrypted.json")
    ignored_file2 = os.path.join(secrets_dir, "unencrypted.yaml")
    failing_file = os.path.join(secrets_dir, "unencrypted.env")
    ignore_file = tmp_path / ".validate-sops-ignore"
    ignore_file.write_text(
        os.path.relpath(ignored_file1)
        + "\n"
        + os.path.relpath(ignored_file2)
        + "\n"
    )

    with (
        patch.object(
            sys,
            "argv",
            [
                "validate-sops",
                ignored_file1,
                ignored_file2,
                failing_file,
                "--ignore-file",
                str(ignore_file),
            ],
        ),
        patch("validate_sops.main.LOGGER.info") as mock_info,
        patch("validate_sops.main.LOGGER.error") as mock_error,
        patch("sys.exit") as mock_exit,
    ):
        main()

    mock_info.assert_any_call(
        "Skipping ignored file: %s", os.path.relpath(ignored_file1)
    )
    mock_info.assert_any_call(
        "Skipping ignored file: %s", os.path.relpath(ignored_file2)
    )
    mock_error.assert_any_call(
        "❌ The file %s is NOT encrypted with SOPS.", failing_file
    )
    mock_exit.assert_called_once_with(1)


@pytest.mark.integration
def test_ignore_file_with_patterns(secrets_dir, tmp_path):
    ignored_file1 = os.path.join(secrets_dir, "unencrypted.json")
    ignored_file2 = os.path.join(secrets_dir, "unencrypted.yaml")
    failing_file = os.path.join(secrets_dir, "unencrypted.env")
    ignore_file = tmp_path / ".validate-sops-ignore"
    ignore_file.write_text("tests/secrets/*.json\n" + "tests/secrets/*.yaml\n")

    with (
        patch.object(
            sys,
            "argv",
            [
                "validate-sops",
                ignored_file1,
                ignored_file2,
                failing_file,
                "--ignore-file",
                str(ignore_file),
            ],
        ),
        patch("validate_sops.main.LOGGER.info") as mock_info,
        patch("validate_sops.main.LOGGER.error") as mock_error,
        patch("sys.exit") as mock_exit,
    ):
        main()

    mock_info.assert_any_call(
        "Skipping ignored file: %s", os.path.relpath(ignored_file1)
    )
    mock_info.assert_any_call(
        "Skipping ignored file: %s", os.path.relpath(ignored_file2)
    )
    mock_error.assert_any_call(
        "❌ The file %s is NOT encrypted with SOPS.", failing_file
    )
    mock_exit.assert_called_once_with(1)
