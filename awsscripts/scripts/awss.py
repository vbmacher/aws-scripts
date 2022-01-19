import argparse

import awsscripts.scripts.ca_login as ca_login
import awsscripts.scripts.ca_logout as ca_logout
import awsscripts.scripts.emr_isidle as emr_isidle
import awsscripts.scripts.emr_start as emr_start
import awsscripts.scripts.emr_submit as emr_submit
import awsscripts.scripts.emr_terminate as emr_terminate
import awsscripts.scripts.mwaa as mwaa
import awsscripts.scripts.sketches as ske
from awsscripts.sketches.sketches import Sketches


def main() -> None:
    sketches = Sketches()
    default_sketch = sketches.get_default()
    default_msg = f' (default={default_sketch})' if default_sketch else ''

    parser = argparse.ArgumentParser(description='AWSome Scripts')
    parser.set_defaults(func=(lambda a: 0))
    parser.add_argument('-s', '--sketch', metavar='SKETCH', default=default_sketch, required=False,
                        help=f"AWS sketch{default_msg}. One of: {sketches.list()}")
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode')

    subparsers = parser.add_subparsers(title='Available commands')
    pemr = subparsers.add_parser('emr', help='elastic map reduce')
    pmwaa = subparsers.add_parser('mwaa', help='managed workflows for apache airflow')
    pca = subparsers.add_parser('ca', help='code artifact')
    psketches = subparsers.add_parser('s', help='sketches')

    # Sketches
    psketches.set_defaults(func=ske.execute)
    ske.configure_parser(psketches)

    # EMR
    pemr_subparsers = pemr.add_subparsers(title='EMR subcommands')
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
    pca_subparsers = pca.add_subparsers(title='CodeArtifact subcommands')
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
