from __future__ import print_function

import base64
import json
import sys

import boto3
import requests

from awsscripts.sketches.sketches import Sketches


def configure_parser(parser):
    parser.add_argument('-e', '--environment', metavar='NAME', type=str, help='MWAA environment')
    parser.add_argument('command', metavar='COMMAND/ARG', type=str, nargs='+', help='MWAA CLI command')


def execute(args) -> None:
    if args.sketch and not args.environment:
        sketches = Sketches()
        if 'mwaa' in sketches[args.sketch]:
            environment = sketches[args.sketch]['mwaa']['environment']
        else:
            print('MWAA environment is not set, and no environment is defined in the sketch')
            sys.exit(1)
    elif args.environment:
        environment = args.environment
    else:
        print('Sketch and MWAA environment are not set')
        sys.exit(1)

    client = boto3.client('mwaa')
    token_with_server = client.create_cli_token(Name=environment)
    token = token_with_server['CliToken']
    server = token_with_server['WebServerHostname']

    r = json.loads(requests.post(f'https://{server}/aws_mwaa/cli', data=args.command, headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'text/plain'
    }).text)

    print(base64.b64decode(r['stdout']))
    print(base64.b64decode(r['stderr']), file=sys.stderr)
