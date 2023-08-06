import logging

from arkive.console.action import music_show, music_flat, music_nest
from arkive.console.parser import get_parser

logging.basicConfig()


def get_logging_level(verbosity: int) -> int:
    levels = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]
    return levels[min(verbosity, 3)]


def run_app(argv: list):
    arg_parser = get_parser()
    if len(argv) == 1:
        arg_parser.print_help()
        return
    args = arg_parser.parse_args()

    verbosity = getattr(args, "verbosity", 0)
    logging.root.setLevel(get_logging_level(verbosity))

    auth = {}
    if args.cmd and args.cloud:
        if args.token:
            auth = {"auth": args.token}
        elif args.username and args.password:
            auth = {"username": args.username, "password": args.password}

    if args.cmd == "show":
        music_show(args.folder, args.cloud, auth)
    elif args.cmd == "flat":
        music_flat(args.folder, args.output, args.cloud, auth)
    elif args.cmd == "nest":
        music_nest(args.folder, args.output, args.cloud, auth)
