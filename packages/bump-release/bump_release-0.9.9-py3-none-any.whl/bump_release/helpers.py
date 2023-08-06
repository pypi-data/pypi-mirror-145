"""
helpers for :mod:`bump_release` application

:creationdate: 16/09/2019 08:18
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: bump_release.helpers

"""
import configparser
import json
import logging
import os
import re
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union

from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO

__author__ = "fguerin"

RELEASE_CONFIG = None
BASE_DIR = os.getcwd()
# region Constants
# Node (JSON value update)
NODE_PACKAGE_FILE: str = "package.json"
NODE_KEY: str = "version"

# main (re search and replace)
MAIN_PROJECT_PATTERN: str = r"^__version__\s*=\s*VERSION\s*=\s*['\"]([\d\w]+)\.([\d\w]+)\.([\d\w]+)['\"]$"
MAIN_PROJECT_TEMPLATE: str = '__version__ = VERSION = "{major}.{minor}.{release}"'

# Ansible yaml key
ANSIBLE_KEY: str = "git.version"

# sonar (re search and replace)
SONAR_PATTERN: str = r"^sonar.projectVersion=([\d\w]+\.[\d\w]+)$"
SONAR_TEMPLATE: str = "sonar.projectVersion={major}.{minor}"

# setup.py file
SETUP_PATTERN: str = r"^\s*version=['\"]([\d\w]+)\.([\d\w]+)\.([\d\w]+)['\"],$"
SETUP_TEMPLATE: str = '    version="{major}.{minor}.{release}",'

# setup.cfg file
SETUP_CFG_PATTERN: str = r"^version = ([\d\w]+)\.([\d\w]+)\.([\d\w]+)$"
SETUP_CFG_TEMPLATE: str = "version = {major}.{minor}.{release}"

# Sphinx (re search and replace)
DOCS_VERSION_PATTERN: str = r"^version\s*=\s*[\"'](.*)[\"']$"
DOCS_VERSION_FORMAT: str = 'version = "{major}.{minor}"'
DOCS_RELEASE_PATTERN: str = r"^release\s*=\s*[\"'](.*)[\"']$"
DOCS_RELEASE_FORMAT: str = 'release = "{major}.{minor}.{release}"'

RELEASE_INI_PATTERN: str = r"^current_release\s*=\s*['\"]?([\d\w]+)\.([\d\w]+)\.([\d\w]+)['\"]?$"
RELEASE_INI_TEMPLATE: str = "current_release = {major}.{minor}.{release}"

# pyproject.toml file
PYPROJECT_KEY = "project.version"

# endregion Constants
logger = logging.getLogger(__name__)


@dataclass
class VersionNumber:
    """Release number."""

    major: int
    minor: int
    release: int

    def __init__(self, **kwargs):
        """Initialize the release number"""
        super().__init__()
        if "version" in kwargs:
            self.major, self.minor, self.release = kwargs["version"].split(".")
        elif "major" in kwargs and "minor" in kwargs and "release" in kwargs:
            self.major = kwargs.get("major", 0)
            self.minor = kwargs.get("minor", 0)
            self.release = kwargs.get("release", 0)
        else:
            raise ValueError(f"Invalid version number: {kwargs}")

    def __str__(self):
        """Get the string representation of the release number"""
        return f"{self.major}.{self.minor}.{self.release}"

    def __repr__(self):
        """Get the representation of the release number"""
        return f"{self.major}.{self.minor}.{self.release}"


def load_release_file(release_file: Union[Path, str]) -> configparser.ConfigParser:
    """
    Loads the release.ini file, and parse the configuration.

    :param release_file: Path to the release file
    :return: Loaded config
    """
    release_config = configparser.ConfigParser()
    release_config.read(release_file)
    return release_config


def update_file(
    path: Path,
    pattern: str,
    template: str,
    version: VersionNumber,
    dry_run: Optional[bool] = False,
) -> Optional[str]:
    """
    Performs the **real** update of the `path` files, aka. replaces the row matched
    with `pattern` with `version_format` formatted according to `release`.

    :param path: path of the file to update
    :param pattern: regexp to replace
    :param template: release format
    :param version: Release number tuple (major, minor, release)
    :param dry_run: If `True`, no operation performed
    :return: New row
    """
    logger.debug(f"Updating {pattern}")
    version_re = re.compile(pattern)

    old_row, new_row = None, None
    counter = None
    with path.open(mode="r") as ifile:
        content_lines = ifile.readlines()
    new_content = deepcopy(content_lines)
    found = False
    for counter, row in enumerate(content_lines):
        searched = version_re.search(row)
        if searched:
            logging.debug(f"update_file({path}) a *MATCHING* row has been found:\n{counter} {row.strip()}")
            found = True
            old_row = deepcopy(row)
            new_row = template.format(major=version.major, minor=version.minor, release=version.release)
            if old_row.endswith("\r\n"):
                new_row += "\r\n"
            elif old_row.endswith("\r"):
                new_row += "\r"
            elif old_row.endswith("\n"):
                new_row += "\n"
            break

    if not found:
        raise ValueError(f"No row matching {pattern} found in {path} file.")

    if old_row and new_row:
        logging.info(f"update_file({path}) old_row:\n{old_row.strip()}\nnew_row:\n{new_row.strip()}")

    if dry_run:
        logging.info(
            f"update_file({path}) No operation performed, dry_run = {dry_run}",
        )
        return new_row

    if new_row and counter is not None:
        new_content[counter] = new_row
        with path.open(mode="w") as output_file:
            output_file.writelines(new_content)
        logging.info(f"update_file({path}) File updated.")
        return new_row

    raise UpdateException(f"An error has append on updating release for file {path}")


def update_node_packages(
    path: Path,
    version: VersionNumber,
    key: str = NODE_KEY,
    dry_run: bool = False,
) -> str:
    """
    Updates the package.json file

    :param path: Node root directory
    :param version: Release number
    :param dry_run: If `True`, no operation performed
    :param key: json dict key (default: "release")
    :return: Nothing
    """
    try:
        with path.open(mode="r") as package_file:
            package = json.loads(package_file.read())
        new_package = deepcopy(package)
        new_package[key] = str(version)
        updated = json.dumps(new_package, indent=4)
        if not dry_run:
            with path.open(mode="w") as package_file:
                package_file.write(updated)
        return updated
    except IOError as ioe:
        raise UpdateException(f"update_node_packages() Unable to perform {package_file} update: {ioe}")


class MyYAML(YAML):
    """
    Wrapper around ruamel.yaml to output directly strings
    """

    def dump(self, data, stream=None, **kw):
        inefficient = False
        if stream is None:
            inefficient = True
            stream = StringIO()
        YAML.dump(self, data, stream, **kw)
        if inefficient:
            return stream.getvalue()


def updates_yaml_file(
    path: Path,
    version: VersionNumber,
    key: str = ANSIBLE_KEY,
    dry_run: bool = False,
) -> str:
    """
    Replaces the version number in a YAML file, aka. ansible vars files

    :param path: Path to the yaml file
    :param version: New version to apply, as a tuple (major, minor, release)
    :param key: key in the files, as xxx.yyy
    :param dry_run: If True, no action is performed
    :returns: new file content
    """
    yaml = MyYAML()
    with path.open(mode="r") as vars_file:
        document = yaml.load(vars_file)
    node = document
    split_key = key.split(".")
    for _key in split_key:
        if _key == split_key[-1] and not dry_run:
            node.update({_key: str(version)})
        node = node.get(_key)
    logging.debug(f"updates_yml_file({vars_file}) node value = {node}")
    new_content = yaml.dump(document)
    if not dry_run:
        with path.open(mode="w") as vars_file:
            vars_file.write(new_content)
    return new_content


def update_toml_file(path: Path, version: VersionNumber, key: str = PYPROJECT_KEY, dry_run: bool = False) -> str:
    """
    Update a toml file with the new version.
    """
    try:
        import tomli
        import tomli_w
    except ImportError as ie:
        raise UpdateException(f"update_toml_file() Unable to perform {path} update: tomli not found", ie)
    with path.open(mode="r") as toml_file:
        document = tomli.loads(toml_file.read())

    # Update the version
    split_key = key.split(".")

    node = document
    for _key in split_key:
        if _key == split_key[-1]:
            node.update({_key: str(version)})
        node = node.get(_key)

    # Write the updated file
    new_content = tomli_w.dumps(document)
    if not dry_run:
        with path.open(mode="w") as toml_file:
            toml_file.write(new_content)
    return new_content


class UpdateException(Exception):
    """
    An error has occurred during the release updating
    """

    pass


class NothingToDoException(UpdateException):
    """
    An error has occurred during the release updating: Nothing to do...
    """

    pass
