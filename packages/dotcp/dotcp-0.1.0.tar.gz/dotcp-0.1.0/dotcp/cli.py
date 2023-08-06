from argparse import ArgumentParser, RawTextHelpFormatter
from pathlib import PosixPath
from sys import stderr, stdout
from typing import TextIO

from dotcp import __version__


def get_args_parser():
    parser = ArgumentParser(
        prog="dotcp",
        description="copy your dotfiles to directory",
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument(
        "destination",
        type=PosixPath,
        help="directory where dotfiles will be put",
    )
    parser.add_argument(
        "--overwrite",
        "-w",
        action="store_true",
        help="empty directory before copying dotfiles",
    )
    parser.add_argument(
        "--append",
        "-a",
        action="store_true",
        help="append dotfiles to destination directory",
    )
    parser.add_argument(
        "--config", "-c", type=PosixPath, help="path to dot's config file"
    )
    parser.add_argument(
        "--config-home",
        "-ch",
        type=PosixPath,
        help="path to your config home directory (e.g. ~/.config)",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

    return parser


def info(message: str):
    stdout.write(f"{message}\n")


def fatal(message: str):
    stderr.write(f"Fatal error: {message}\n")
    exit(-1)
