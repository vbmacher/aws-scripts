from __future__ import print_function

import argparse
import boto3
import requests
import json
import sys
import base64


def main():
    parser = argparse.ArgumentParser(description='MWAA CLI Proxy')
    parser.add_argument('-e', '--environment', metavar='NAME', type=str, required=True, help='MWAA environment')
    parser.add_argument('command', metavar='COMMAND/ARG', type=str, nargs='+', help='MWAA CLI command')

    args = parser.parse_args()

    client = boto3.client('mwaa')
    token_with_server = client.create_cli_token(Name=args.environment)
    token = token_with_server['CliToken']
    server = token_with_server['WebServerHostname']

    r = json.loads(requests.post(f'https://{server}/aws_mwaa/cli', data=args.command, headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'text/plain'
    }).text)

    print(base64.b64decode(r['stdout']))
    print(base64.b64decode(r['stderr']), file=sys.stderr)


if __name__ == "__main__":
    main()
