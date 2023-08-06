"""
    stringtime CLI entry point.
    ====================================

    # TODO - unit tests for cli tool as this just bust after method change

"""

import argparse
import os
import sys

from stringtime import Date, __version__


def parse_args():
    parser = argparse.ArgumentParser(
        add_help=False,
        prog="stringtime",
        description="Create dates from natural language strings.",
    )
    parser.add_argument("-h", "--help", action="store_true")
    parser.add_argument("-v", "--version", action="store_true")
    parser.add_argument(
        "-p",
        "--phrase",
        help="Pass a phrase to get a date.",
        type=str,
        nargs="*",
        default=None,
    )
    args = parser.parse_args()
    return args, parser


def do_things(arguments, parser):
    if arguments.help is True:
        print(parser.print_help())
        sys.exit()
    if arguments.version is True:
        # from stringtime import __version__
        print(__version__)
        return __version__
    if arguments.phrase is not None:
        p = " ".join(arguments.phrase)
        d = Date(p)
        print(d)


def run():
    """[Entry point required by setup.py console_scripts.]"""
    args, parser = parse_args()
    do_things(args, parser)


if __name__ == "__main__":
    run()
