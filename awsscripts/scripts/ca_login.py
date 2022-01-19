import os

import sys
from awsscripts.sketches.sketches import Sketches


def configure_parser(parser):
    parser.add_argument('--pip', action='store_true', help='Configure pip')
    parser.add_argument('--twine', action='store_true', help='Configure twine')


def execute(args) -> None:
    if not args.sketch:
        print('Sketch not is set, and no default sketch exists')
        sys.exit(1)

    sketches = Sketches()
    sketch = sketches[args.sketch]['codeartifact']

    if args.pip:
        os.system(
            'aws codeartifact login --tool pip ' +
            f'--repository {sketch["repository"]} --domain {sketch["domain"]} --domain-owner {sketch["domain-owner"]}'
        )
    if args.twine:
        os.system(
            'aws codeartifact login --tool twine ' +
            f'--repository {sketch["repository"]} --domain {sketch["domain"]} --domain-owner {sketch["domain-owner"]}'
        )
