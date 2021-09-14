import argparse
import os
from os.path import splitext, basename
import sys

from awsscripts.accounts import accounts, default_account


def main():
    parser = argparse.ArgumentParser(description='CodeArtifact login/logout script')
    parser.add_argument('-a', '--account', metavar='ACCOUNT', default=default_account,
                        help=f"AWS account (default='{default_account}'). One of: {accounts.keys()}")
    parser.add_argument('-l', '--login', action='store_true', help='Log in to CodeArtifact')
    parser.add_argument('-L', '--logout', action='store_true', help='Log out from CodeArtifact')
    parser.add_argument('--pip', action='store_true', help='Configure pip')
    parser.add_argument('--twine', action='store_true', help='Configure twine')

    args = parser.parse_args()
    env = accounts[args.account]["codeartifact"]

    if not args.login and not args.logout:
        print(f"Type `{splitext(basename(__file__))[0]} --help` for usage information.")
        sys.exit(1)

    if args.login:
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
    if args.logout:
        if args.pip:
            os.system('python -m pip config set global.index-url ""')
        if args.twine:
            print("Logging off from Twine is not supported yet!")


if __name__ == "__main__":
    main()
