import os

from accounts import Accounts


def configure_parser(parser):
    parser.add_argument('--pip', action='store_true', help='Configure pip')
    parser.add_argument('--twine', action='store_true', help='Configure twine')


def execute(args) -> None:
    accounts = Accounts()
    env = accounts[args.account]["codeartifact"]

    if args.pip:
        os.system(
            'aws codeartifact login --tool pip ' +
            f'--repository {env["repository"]} --domain {env["domain"]} --domain-owner {env["domain-owner"]}'
        )
    if args.twine:
        os.system(
            'aws codeartifact login --tool twine ' +
            f'--repository {env["repository"]} --domain {env["domain"]} --domain-owner {env["domain-owner"]}'
        )
