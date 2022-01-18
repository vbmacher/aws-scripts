import argparse

import accounts as acc
import ca_login
import ca_logout
import emr_isidle
import emr_start
import emr_submit
import emr_terminate
import mwaa
from accounts import Accounts


def main() -> None:
    accounts = Accounts()
    default_account = accounts.get_default_account()
    default_msg = f' (default={default_account})' if default_account else ''

    parser = argparse.ArgumentParser(description='AWSome Scripts')
    parser.add_argument('-a', '--account', metavar='ACCOUNT', default=default_account,
                        help=f"AWS account{default_msg}. One of: {accounts.list()}")
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode')

    subparsers = parser.add_subparsers(title='services')
    pemr = subparsers.add_parser('emr')
    pmwaa = subparsers.add_parser('mwaa')
    pca = subparsers.add_parser('ca')
    paccounts = subparsers.add_parser('a')

    # Accounts
    paccounts.set_defaults(func=acc.execute)
    acc.configure_parser(paccounts)

    # EMR
    pemr_subparsers = pemr.add_subparsers(title='EMR')
    pemr_start = pemr_subparsers.add_parser('start', description='starts EMR cluster')
    pemr_start.set_defaults(func=emr_start.execute)
    emr_start.configure_parser(pemr_start)

    pemr_submit = pemr_subparsers.add_parser('submit', description='submits Spark step')
    pemr_submit.set_defaults(func=emr_submit.execute)
    emr_submit.configure_parser(pemr_submit)

    pemr_terminate = pemr_subparsers.add_parser('terminate', description='terminates EMR cluster')
    pemr_terminate.set_defaults(func=emr_terminate.execute)
    emr_terminate.configure_parser(pemr_terminate)

    pemr_isidle = pemr_subparsers.add_parser('isidle', description='determines if EMR cluster is idle')
    pemr_isidle.set_defaults(func=emr_isidle.execute)
    emr_isidle.configure_parser(pemr_isidle)

    # CodeArtifact
    pca_subparsers = pca.add_subparsers(title='CodeArtifact')
    pca_login = pca_subparsers.add_parser('login', description='login to CA')
    pca_login.set_defaults(func=ca_login.execute)
    ca_login.configure_parser(pca_login)

    pca_logout = pca_subparsers.add_parser('logout', description='logout from CA')
    pca_logout.set_defaults(func=ca_logout.execute)
    ca_logout.configure_parser(pca_logout)

    # MWAA
    pmwaa.set_defaults(func=mwaa.execute)
    mwaa.configure_parser(pmwaa)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
