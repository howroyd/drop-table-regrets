"""Tests for the CLI module."""

from drop_table_regrets import cli


def test_cli_imports() -> None:
    """Test that CLI module can be imported."""
    assert hasattr(cli, "main")
    assert callable(cli.main)
