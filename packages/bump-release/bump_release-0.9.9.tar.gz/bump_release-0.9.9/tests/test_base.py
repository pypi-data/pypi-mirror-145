"""
test_base for :mod:`tests` application.

:creationdate: 04/04/2022 11:21
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: tests.test_base
"""
from typing import Any, Dict

from .fixtures import version_number  # noqa

__author__ = "fguerin"

from bump_release import helpers


def test_version_number(version_number: Dict[str, Any]):  # noqa
    """Test version number parsing and display."""
    _version = helpers.VersionNumber(**version_number["kwargs"])
    assert _version == version_number["version"]
