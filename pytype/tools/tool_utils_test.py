"""Tests for tool_utils.py."""

import sys

from pytype.platform_utils import path_utils
import tempfile
import shutil
import os
import os
from unittest import mock

class Tempdir:
    """Context manager for creating and cleaning up a temporary directory."""
    def __init__(self):
        self.tempdir = tempfile.mkdtemp()
        self.path = self.tempdir
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        shutil.rmtree(self.tempdir)

# Provide a dummy test_utils module with Tempdir for compatibility
test_utils = type("test_utils", (), {"Tempdir": Tempdir})
from pytype.tools import tool_utils

import unittest


class TestSetupLoggingOrDie(unittest.TestCase):
  """Tests for tool_utils.setup_logging_or_die."""

  def test_negative_verbosity(self):
    with self.assertRaises(SystemExit):
      tool_utils.setup_logging_or_die(-1)

  def test_excessive_verbosity(self):
    with self.assertRaises(SystemExit):
      tool_utils.setup_logging_or_die(3)

  def test_set_level(self):
    # Log level can't actually be set in a test, so we're just testing that the
    # code doesn't blow up.
    tool_utils.setup_logging_or_die(0)
    tool_utils.setup_logging_or_die(1)
    tool_utils.setup_logging_or_die(2)


class TestMakeDirsOrDie(unittest.TestCase):
  """Tests for tool_utils.makedirs_or_die()."""

  def test_make(self):
    with test_utils.Tempdir() as d:
      subdir = path_utils.join(d.path, 'some/path')
      tool_utils.makedirs_or_die(subdir, '')
      self.assertTrue(path_utils.isdir(subdir))

  def test_die(self):
    """Test that makedirs_or_die triggers sys.exit when file_utils.makedirs raises OSError using monkey patch."""
    with mock.patch("pytype.tools.tool_utils.file_utils.makedirs", side_effect=OSError):
      with self.assertRaises(SystemExit):
        tool_utils.makedirs_or_die("dummy/path", "Error")

if __name__ == '__main__':
  unittest.main()
