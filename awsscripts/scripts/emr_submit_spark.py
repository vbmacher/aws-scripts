import argparse

from awsscripts.helpers.accounts import Accounts
from awsscripts.helpers.emr import EMR


def main():
    accounts = Accounts()
    default_account = accounts.get_default_account()
    default_msg = f' (default={default_account})' if default_account else ''

    parser = argparse.ArgumentParser(description='Submits Apache Spark step')
    parser.add_argument('-a', '--account', metavar='ACCOUNT', default=default_account,
                        help=f"AWS account{default_msg}. One of: {accounts.list()}")
    parser.add_argument('--clusterid', metavar='ID', type=str, required=True, help='cluster ID')
    parser.add_argument('--stepname', metavar='STEP_NAME', type=str, required=True, help='step name')
    parser.add_argument('--jar', metavar='URI', type=str, required=True, help='JAR file URI')
    parser.add_argument('--classname', metavar='CLASS', type=str, required=True, help='Class to run')

    args = parser.parse_args()

    environment = accounts[args.account]["emr"]
    emr = EMR(region=environment['region'])

    # TODO support Python steps
    step_id = emr.add_spark_step(args.clusterid, args.stepname, args.jar, args.classname, [])
    print(step_id)


if __name__ == "__main__":
    main()
