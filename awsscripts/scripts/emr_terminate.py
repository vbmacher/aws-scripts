import argparse
from awsscripts.emr.helpers.emr import EMR
from awsscripts.accounts import accounts, default_account


def main():
    parser = argparse.ArgumentParser(description='Terminates EMR cluster')
    parser.add_argument('-a', '--account', metavar='ACCOUNT', default=default_account,
                        help=f"AWS account (default='{default_account}'). One of: {accounts.keys()}")
    parser.add_argument('-c', '--clusterid', metavar='ID', type=str, required=True, help='cluster ID')

    args = parser.parse_args()

    environment = accounts[args.account]["emr"]
    emr = EMR(region=environment['region'])

    emr.terminate_cluster(args.clusterid)


if __name__ == "__main__":
    main()
