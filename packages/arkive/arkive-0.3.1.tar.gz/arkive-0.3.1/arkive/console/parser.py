from argparse import ArgumentParser
from pathlib import Path

from arkive import __version__


def get_parser() -> ArgumentParser:
    cloud = ArgumentParser(add_help=False)

    cloud.add_argument("-c", "--cloud", type=str, metavar="SERVICE", choices=["pcloud"])
    cloud.add_argument("-t", "--token", type=str)
    cloud.add_argument("-u", "--username", type=str)
    cloud.add_argument("-p", "--password", type=str)

    cloud.add_argument("-v", "--verbosity", action="count", help="increase output verbosity", default=0)

    parser = ArgumentParser(prog="arkive")
    parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {__version__}")

    commands = parser.add_subparsers(dest="cmd", title="commands", metavar="<command>")

    show = commands.add_parser("show", parents=[cloud], help="display actions collection inside a given folder.")
    show.add_argument("folder", type=Path)

    flat = commands.add_parser("flat", parents=[cloud], help="flatten actions files inside a given folder.")
    flat.add_argument("folder", type=Path)
    flat.add_argument("-o", "--output", type=Path)

    nest = commands.add_parser("nest", parents=[cloud], help="nesting actions files inside a given folder.")
    nest.add_argument("folder", type=Path)
    nest.add_argument("-o", "--output", type=Path)

    return parser
