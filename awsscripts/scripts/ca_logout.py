import os


def configure_parser(parser):
    parser.add_argument('--pip', action='store_true', help='Configure pip')
    parser.add_argument('--twine', action='store_true', help='Configure twine')


def execute(args) -> None:
    if args.pip:
        os.system('python -m pip config set global.index-url ""')
    if args.twine:
        print("Logging off from Twine is not supported yet!")
