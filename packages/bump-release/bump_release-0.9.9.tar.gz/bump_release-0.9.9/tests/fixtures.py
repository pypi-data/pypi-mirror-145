"""
fixtures for :mod:`tests` application.

:creationdate: 04/04/2022 12:00
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: tests.fixtures
"""
import logging
from pathlib import Path

import pytest

from bump_release import helpers

logger = logging.getLogger(__name__)
__author__ = "fguerin"

VERSION_NUMBERS = [
    {
        "version": helpers.VersionNumber(version="0.0.2"),
        "expected": {
            "main": "0.0.2",
            "sonar": "0.0",
            "docs": ["0.0", "0.0.2"],
            "pyproject": "0.0.2",
            "ansible": "0.0.2",
        },
        "kwargs": {"major": "0", "minor": "0", "release": "2"},
    },
    {
        "version": helpers.VersionNumber(version="0.0.2-alpha"),
        "expected": {
            "main": "0.0.2-alpha",
            "sonar": "0.0",
            "docs": ["0.0", "0.0.2-alpha"],
            "pyproject": "0.0.2",
            "ansible": "0.0.2",
        },
        "kwargs": {"version": "0.0.2-alpha"},
    },
    {
        "version": helpers.VersionNumber(version="1.0.0-rc1"),
        "expected": {
            "main": "1.0.0-rc1",
            "sonar": "1.0",
            "docs": ["1.0", "1.0.0-rc1"],
            "pyproject": "1.0.0-rc1",
            "ansible": "1.0.0-rc1",
        },
        "kwargs": {"version": "1.0.0-rc1"},
    },
]

CONFIG_FILES = [
    {"path": Path(__file__).parent / "fixtures" / "empty.ini", "expected": {"sections": []}},
    {
        "path": Path(__file__).parent / "fixtures" / "release.ini",
        "expected": {
            "sections": [
                "main_project",
                "sonar",
                "docs",
                "setup",
                "setup_cfg",
                "ansible",
                "pyproject",
            ]
        },
    },
    {
        "path": Path(__file__).parent / "fixtures" / "release_with_patterns.ini",
        "expected": {
            "sections": [
                "main_project",
                "sonar",
                "docs",
                "setup",
                "setup_cfg",
                "ansible",
                "pyproject",
            ]
        },
    },
]


@pytest.fixture(params=VERSION_NUMBERS)
def version_number(request):
    """Get version number from fixture."""
    logger.info(f"version_number() Version number loaded: {request.param}")
    return request.param


@pytest.fixture(params=CONFIG_FILES)
def config(request):
    """Get empty config."""
    logger.info(f"config() Config loaded: {request.param}")

    release_ini_path = request.param["path"]
    config = helpers.load_release_file(release_ini_path)
    logger.info("config() Config file loaded")
    assert config
    return {
        "config": config,
        "expected": request.param["expected"],
        "path": request.param["path"],
    }
