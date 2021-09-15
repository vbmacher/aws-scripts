import argparse
from awsscripts.helpers.emr import EMR

from awsscripts.helpers.accounts import Accounts
from awsscripts.helpers.spark import *


def main():
    accounts = Accounts()
    default_account = accounts.get_default_account()
    default_msg = f' (default={default_account})' if default_account else ''

    parser = argparse.ArgumentParser(description='Starts EMR cluster')
    parser.add_argument('-n', '--name', metavar='NAME', type=str, required=True, help='cluster name')
    parser.add_argument('-i', '--instance', metavar='INSTANCE', default='m5.xlarge',
                        help='master/core nodes instance type')
    parser.add_argument('-e', '--emr', metavar='LABEL', default='emr-6.3.0', help='EMR release label')
    parser.add_argument('-p', '--protect', help='Set cluster as TerminationProtected', action='store_true')
    parser.add_argument('-c', '--count', metavar='N', default=1, type=int, help='Core node instances count')
    parser.add_argument('-s', '--size', metavar='GB', default=100, type=int, help='EBS volume size in GB')
    parser.add_argument('-S', '--spot', help='Use Spot core nodes', action='store_true')
    parser.add_argument('-b', '--boot', metavar='PATH', type=str, nargs='*',
                        help='Bootstrap scripts (path to S3).')
    parser.add_argument('-A', '--applications', metavar='APP', nargs='*',
                        default=['Spark', 'JupyterHub', 'JupyterEnterpriseGateway', 'Hadoop', 'Livy'],
                        help='EMR applications (default: Spark,JupyterHub,JupyterEnterpriseGateway,Hadoop,Livy)')
    parser.add_argument('-a', '--account', metavar='ACCOUNT', default=default_account,
                        help=f"AWS account{default_msg}. One of: {accounts.list()}")
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode')

    args = parser.parse_args()

    environment = accounts[args.account]["emr"]
    configurations = \
        get_spark_configurations(args.instance, args.count) + \
        get_hdfs_site_configuration() + \
        get_livy_configuration() + \
        get_emrfs_site_configuration() + \
        get_yarn_site_configurations(capacity_scheduler={
            "instance_type": args.instance,
            "node_count": args.count
        })

    if args.verbose:
        print("EC2 Instance: " + args.instance)
        print("Volume size in GB: " + args.size)
        print(configurations)

    boot = []
    if args.boot:
        boot = [{
            'name': 'Run script: ' + b.strip(),
            'path': b,
            'args': []
        } for b in args.boot]

    emr = EMR(args.verbose)
    cluster_id = emr.start_cluster(
        name=args.name,
        log_uri=environment['log_uri'],
        keep_alive=True,
        protect=args.protect,
        applications=args.applications,
        job_flow_role=environment['job_flow_role'],
        service_role=environment['service_role'],
        emr_label=args.emr,
        master_instance=args.instance,
        node_instance=args.instance,
        node_count=args.count,
        steps=[{
            'Name': 'Enable debugging',
            'Args': ["state-pusher-script"]
        }],
        tags=environment['tags'],
        security_groups=environment['security_groups'],
        subnets=environment['subnets'],
        configurations=configurations,
        keyname=environment['keyname'] if 'keyname' in environment else None,
        volume_size_gb=args.size,
        bootstrap_scripts=boot,
        spot=args.spot
    )

    print(cluster_id)


if __name__ == "__main__":
    main()
