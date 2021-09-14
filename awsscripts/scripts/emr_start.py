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
                        help='master/slave nodes instance type')
    parser.add_argument('-e', '--emr', metavar='LABEL', default='emr-6.3.0', help='EMR release label')
    parser.add_argument('-p', '--protect', help='Set cluster as TerminationProtected', action='store_true')
    parser.add_argument('-c', '--count', metavar='N', default=1, type=int, help='Slave node instances count')
    parser.add_argument('-s', '--size', metavar='GB', default=100, type=int, help='Volume size in GB')
    parser.add_argument('-b', '--boot', metavar='NAME',
                        default="python,jupyter", type=str,
                        help='Bootstrap scripts (comma separated names).' +
                             ' Different scripts might be available on different accounts.')
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
        print("Region: " + environment['region'])
        print(configurations)

    # TODO: upload bootstrap scripts
    # TODO: make configurable
    # emr_scripts_boot = [{
    #     'name': f'Install aws-scripts {__version__}',
    #     'path': environment["bootstrap_scripts"]["install_aws_scripts"],
    #     'args': [__version__]
    # }]
    if args.boot == "":
        boot = []  # emr_scripts_boot
    else:
        boot = [{  # emr_scripts_boot + [{
            'name': 'Run script: ' + b.strip(),
            'path': environment["bootstrap_scripts"][b.strip()],
            'args': []
        } for b in args.boot.split(",")]

    emr = EMR(region=environment['region'])
    cluster_id = emr.start_cluster(
        name=args.name,
        log_uri=environment['log_uri'],
        keep_alive=True,
        protect=args.protect,
        applications=[
            # TODO: make it configurable
            'Spark', 'Ganglia', 'JupyterHub', 'JupyterEnterpriseGateway', 'Hadoop', 'Livy'
        ],
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
        keyname=environment['keyname'],
        volume_size_gb=args.size,
        bootstrap_scripts=boot
    )

    print(cluster_id)


if __name__ == "__main__":
    main()
