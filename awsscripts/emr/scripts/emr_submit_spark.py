import argparse
from awsscripts.emr.helpers.emr import EMR
from awsscripts.emr.helpers.aws_accounts import aws_accounts, default_aws_account


def main():
    parser = argparse.ArgumentParser(description='Submits Apache Spark step')
    parser.add_argument('-a', '--account', metavar='ACCOUNT', default=default_aws_account,
                        help=f"AWS account (default='{default_aws_account}'). One of: {aws_accounts.keys()}")
    parser.add_argument('--clusterid', metavar='ID', type=str, required=True, help='cluster ID')
    parser.add_argument('--stepname', metavar='STEP_NAME', type=str, required=True, help='step name')
    parser.add_argument('--jar', metavar='URI', type=str, required=True, help='JAR file URI')
    parser.add_argument('--classname', metavar='CLASS', type=str, required=True, help='Class to run')

    args = parser.parse_args()

    environment = aws_accounts[args.account]["emr"]
    emr = EMR(region=environment['region'])

    step_id = emr.add_spark_step(args.clusterid, args.stepname, args.jar, args.classname, [])
    print(step_id)


if __name__ == "__main__":
    main()
