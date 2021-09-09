import argparse
from awsscripts.emr.helpers.emr import EMR
from awsscripts.emr.helpers.aws_accounts import aws_accounts, default_aws_account


def main():
    parser = argparse.ArgumentParser(description='Terminates EMR cluster')
    parser.add_argument('-a', '--account', metavar='ACCOUNT', default=default_aws_account,
                        help=f"AWS account (default='{default_aws_account}'). One of: {aws_accounts.keys()}")
    parser.add_argument('-c', '--clusterid', metavar='ID', type=str, required=True, help='cluster ID')

    args = parser.parse_args()

    environment = aws_accounts[args.account]["emr"]
    emr = EMR(region=environment['region'])

    emr.terminate_cluster(args.clusterid)


if __name__ == "__main__":
    main()
