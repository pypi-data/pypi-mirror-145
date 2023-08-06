"""
__main__ for :mod:`bump_release` application

:creationdate: 17/09/2019 11:52
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: bump_release.__main__

"""
import sys

import bump_release

__author__ = "fguerin"


def main(*args):
    return bump_release.bump_release()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
