"""
Tests for updaters
"""
import logging
import re
from pathlib import Path
from typing import Any, Dict

import bump_release
from bump_release import helpers

from .fixtures import config, version_number  # noqa

logger = logging.getLogger("tests")


def test_load_release_file(config: Dict[str, Any]):  # noqa
    """
    Tests the loading and the values of the release.ini file

    :param config: The config dict
    :return:
    """
    for section in config["expected"]["sections"]:
        assert config["config"].has_section(section), f"No `{section}` section in release.ini file"


def test_update_main_project(config: Dict[str, Any], version_number: Dict[str, Any]):  # noqa
    if "main_project" not in config["expected"]["sections"]:
        logger.info("[main_project] not expected for now...")
        return

    str_path = config["config"]["main_project"].get("path")
    assert str_path is not None
    path = Path(str_path)
    assert path.exists(), f"MAIN_PROJECT: Path does not exist: {path}"
    new_row = helpers.update_file(
        path=path,
        pattern=helpers.MAIN_PROJECT_PATTERN,
        template=helpers.MAIN_PROJECT_TEMPLATE,
        version=version_number["version"],
        dry_run=True,
    )
    assert (
        new_row.strip() == f"__version__ = VERSION = \"{version_number['expected']['main']}\""
    ), "MAIN: Versions does not match"


def test_update_sonar_properties(config: Dict[str, Any], version_number: Dict[str, Any]):  # noqa
    if "sonar" not in config["expected"]["sections"]:
        logger.info("[sonar] not expected for now...")
        return

    try:
        str_path = config["config"]["sonar"].get("path")
    except KeyError:
        logger.info("No sonar.properties file found")
        return
    assert str_path is not None
    path = Path(str_path)
    new_row = helpers.update_file(
        path=path,
        pattern=helpers.SONAR_PATTERN,
        template=helpers.SONAR_TEMPLATE,
        version=version_number["version"],
        dry_run=True,
    )
    assert (
        new_row.strip() == f"sonar.projectVersion={version_number['expected']['sonar']}"
    ), "SONAR: Versions does not match"


def test_update_docs(config: Dict[str, Any], version_number: Dict[str, Any]):  # noqa
    if "docs" not in config["expected"]["sections"]:
        logger.info("[docs] not expected for now...")
        return
    try:
        str_path = config["config"].get("docs", "path")
    except KeyError:
        logger.info("No docs found")
        return

    assert str_path is not None
    path = Path(str_path)
    version_pattern = config["config"].get("docs", "version_pattern", fallback=helpers.DOCS_VERSION_PATTERN)
    version_format = config["config"].get("docs", "version_format", fallback=helpers.DOCS_VERSION_FORMAT)
    release_pattern = config["config"].get("docs", "release_pattern", fallback=helpers.DOCS_RELEASE_PATTERN)
    release_format = config["config"].get("docs", "release_format", fallback=helpers.DOCS_RELEASE_FORMAT)

    new_row = helpers.update_file(
        path=path,
        pattern=version_pattern,
        template=version_format,
        version=version_number["version"],
        dry_run=True,
    )
    assert new_row, "No version found in docs"
    assert new_row.strip() == f'version = "{version_number["expected"]["docs"][0]}"', "DOCS: Versions does not match"

    new_row = helpers.update_file(
        path=path,
        pattern=release_pattern,
        template=release_format,
        version=version_number["version"],
        dry_run=True,
    )
    assert new_row, "No release found in docs"
    assert new_row.strip() == f'release = "{version_number["expected"]["docs"][1]}"', "DOCS: Versions does not match"


def test_update_node_packages(config: Dict[str, Any], version_number: Dict[str, Any]):  # noqa
    if "node" not in config["expected"]["sections"]:
        logger.info("[node] not expected for now...")
        return

    try:
        str_path = config["config"].get("node", "path")
    except KeyError:
        logger.info("No node packages found")
        return

    assert str_path is not None
    path = Path(str_path)
    key = config["config"].get("node", "key", fallback=helpers.NODE_KEY)
    new_content = helpers.update_node_packages(path=path, version=version_number["version"], key=key)
    assert new_content, "NODE: New content cannot be empty"


def test_update_ansible(config: Dict[str, Any], version_number: Dict[str, Any]):  # noqa
    if "ansible" not in config["expected"]["sections"]:
        logger.info("[ansible] not expected for now...")
        return

    try:
        str_path = config["config"].get("ansible", "path", fallback="vars.yml")
    except KeyError:
        logger.info("No ansible found")
        return
    key = config["config"].get("ansible", "key", fallback=helpers.ANSIBLE_KEY)
    assert str_path is not None
    path = Path(str_path)
    new_content = helpers.updates_yaml_file(path=path, version=version_number["version"], key=key)
    assert new_content, "ANSIBLE: New content cannot be empty"
    with open(path, "r") as f:
        content = f.readlines()
        for line in content:
            if "version" in line:
                assert (
                    line.strip() == f"version: {version_number['expected']['ansible']}"
                ), "ANSIBLE: Versions does not match"
            break


def test_full_update_ansible(config: Dict[str, Any], version_number: Dict[str, Any]):  # noqa
    if "ansible" not in config["expected"]["sections"]:
        logger.info("[ansible] not expected for now...")
        return

    try:
        str_path = config["config"].get("ansible", "path", fallback="vars.yml")
    except KeyError:
        logger.info("No ansible found")
        return
    path = Path(str_path)

    bump_release.RELEASE_CONFIG = config["config"]
    result = bump_release.update_ansible_vars(version=version_number["version"], dry_run=True)
    assert result is not None, "ANSIBLE: New content cannot be empty"

    with open(path, "r") as f:
        content = f.readlines()
        for line in content:
            if "version" in line:
                assert (
                    line.strip() == f"version: {version_number['expected']['ansible']}"
                ), "ANSIBLE: Versions does not match"
            break


def test_full_docs_conf(config: Dict[str, Any], version_number: Dict[str, Any]):  # noqa
    if "docs" not in config["expected"]["sections"]:
        logger.info("[docs] not expected for now...")
        return
    bump_release.RELEASE_CONFIG = config["config"]
    result = bump_release.update_docs_conf(version=version_number["version"], dry_run=True)
    assert result is not None, "DOCS: New content cannot be empty"


def test_full_main_project(config: Dict[str, Any], version_number: Dict[str, Any]):  # noqa
    if "main_project" not in config["expected"]["sections"]:
        logger.info("[main_project] not expected for now...")
        return
    bump_release.RELEASE_CONFIG = config["config"]
    result = bump_release.update_main_file(version=version_number["version"], dry_run=True)
    assert result is not None, "MAIN: New content cannot be empty"


def test_full_node_package(config: Dict[str, Any], version_number: Dict[str, Any]):  # noqa
    if "node" not in config["expected"]["sections"]:
        logger.info("[node] not expected for now...")
        return
    bump_release.RELEASE_CONFIG = config["config"]
    result = bump_release.update_node_package(version=version_number["version"], dry_run=True)
    assert result is not None, "NODE: New content cannot be empty"


def test_full_sonar_properties(config: Dict[str, Any], version_number: Dict[str, Any]):  # noqa
    if "sonar" not in config["expected"]["sections"]:
        logger.info("[sonar] not expected for now...")
        return

    bump_release.RELEASE_CONFIG = config["config"]
    result = bump_release.update_node_package(version=version_number["version"], dry_run=True)
    assert result is not None, "SONAR: New content cannot be empty"


def test_pyproject(config: Dict[str, Any], version_number: Dict[str, Any]):  # noqa
    if "pyproject" not in config["expected"]["sections"]:
        logger.info("[pyproject] not expected for now...")
        return

    bump_release.RELEASE_CONFIG = config["config"]
    result = bump_release.update_pyproject(version=version_number["version"], dry_run=True)
    assert result, "PYPROJECT: New content cannot be empty"
    rows = result.split("\n")
    regex = re.compile(r"""^version = ['"](\w+)\.(\w+)\.(\w+)['"]$""")
    for row in rows:
        match = regex.match(row)
        if match:
            assert (
                row.strip() == f'version = "{version_number["expected"]["pyproject"]}"'
            ), "PYPROJECT: Versions does not match"
            break
