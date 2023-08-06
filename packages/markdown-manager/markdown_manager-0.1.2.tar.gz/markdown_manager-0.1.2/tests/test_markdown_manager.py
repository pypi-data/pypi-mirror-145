#!/usr/bin/env python

"""Tests for `markdown_manager` package."""


import unittest
from click.testing import CliRunner

from markdown_manager import cli


class TestMarkdown_manager(unittest.TestCase):
    """Tests for `markdown_manager` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.cli)
        assert result.exit_code == 0
        assert "Usage: cli" in result.output
        help_result = runner.invoke(cli.cli, ["--help"])
        assert help_result.exit_code == 0
        assert "--help  Show this message and exit." in help_result.output
