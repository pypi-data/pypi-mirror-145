#!/usr/bin/env python

"""mite-cli

Usage:
    mite-cli new <project_dir> [options]
    mite-cli --help

Options:
    --log-level=LEVEL       Set logger level: DEBUG, INFO, WARNING, ERROR, CRITICAL [default: INFO]
    -n --novenv             Don't create a python virtual environment
    --help                  Show this message

"""  # noqa: E501

import logging

from docopt import docopt

from .new_project import new_project

logger = logging.getLogger(__name__)


def setup_logging(opts):
    logging.basicConfig(level=opts["--log-level"], format="<%(levelname)s> %(message)s")


def main():
    opts = docopt(__doc__)
    setup_logging(opts)
    if opts["new"]:
        new_project(opts["<project_dir>"], opts["--novenv"])


if __name__ == "__main__":
    main()
