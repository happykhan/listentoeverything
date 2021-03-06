#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `listentoeverything` package."""


import unittest
from click.testing import CliRunner

from listentoeverything import listen
from listentoeverything import cli


class TestListentoeverything(unittest.TestCase):
    """Tests for `listentoeverything` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
#        result = runner.invoke(cli.main)
#        assert result.exit_code == 0
 #       assert 'listentoeverything.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert '  --help              Show this message and exit.' in help_result.output

    def test_yaml(self):
        """Test the YAML."""
        yaml = listen.load_config('example_listen.yml')
        assert yaml['reddit']['user_agent'] == 'listenonspotify'
