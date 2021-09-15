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
    parser.add_argument('--jar', metavar='URI', type=str, help='JAR file URI')
    parser.add_argument('--classname', metavar='CLASS', type=str, help='Class to run')
    parser.add_argument('--pyfiles', metavar='PATH', type=str, nargs='*', help='Additional python files')
    parser.add_argument('python_main', metavar='PATH', type=str, help='Python main file')
    parser.add_argument('arguments', metavar='ARG', type=str, nargs='*', help='Command-line arguments')

    args = parser.parse_args()

    environment = accounts[args.account]['emr']
    emr = EMR(region=environment['region'])

    if args.classname:
        step_id = emr.add_spark_jar_step(args.clusterid, args.stepname, args.jar, args.classname, args.arguments)
    elif args.python_main:
        step_id = emr.add_spark_python_step(
            args.clusterid, args.stepname, args.python_main, args.pyfiles, args.arguments
        )
    else:
        raise RuntimeError('classname or python main file must be defined!')
    print(step_id)


if __name__ == "__main__":
    main()
