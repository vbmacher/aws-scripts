import argparse

from awsscripts.helpers.accounts import Accounts
from awsscripts.helpers.emr import EMR


def main():
    accounts = Accounts()
    default_account = accounts.get_default_account()
    default_msg = f' (default={default_account})' if default_account else ''

    parser = argparse.ArgumentParser(description='Terminates EMR cluster')
    parser.add_argument('-a', '--account', metavar='ACCOUNT', default=default_account,
                        help=f"AWS account{default_msg}. One of: {accounts.list()}")
    parser.add_argument('-c', '--clusterid', metavar='ID', type=str, required=True, help='cluster ID')

    args = parser.parse_args()

    environment = accounts[args.account]["emr"]
    emr = EMR(region=environment['region'])

    emr.terminate_cluster(args.clusterid)


if __name__ == "__main__":
    main()
