import argparse
import sys

from awsscripts.helpers.emr import EMR

from awsscripts.helpers.accounts import Accounts
from awsscripts.helpers.spark import get_yarn_site_configurations, get_spark_configurations, \
    get_hdfs_site_configuration, get_livy_configuration, get_emrfs_site_configuration


def main() -> None:
    accounts = Accounts()
    default_account = accounts.get_default_account()
    default_msg = f' (default={default_account})' if default_account else ''

    parser = argparse.ArgumentParser(description='Starts EMR cluster')
    parser.add_argument('-n', '--name', metavar='NAME', type=str, required=True, help='cluster name')
    parser.add_argument('-mi', '--master_instance', metavar='INSTANCE', default='m5.xlarge',
                        help='master node instance type')
    parser.add_argument('-ci', '--core_instance', metavar='INSTANCE', default='m5.xlarge',
                        help='core nodes instance type')
    parser.add_argument('-f', '--fleet', metavar='INSTANCE_FLEET',
                        help='instance fleet name (instance fleets must be defined in the account)')
    parser.add_argument('-e', '--emr', metavar='LABEL', default='emr-6.4.0', help='EMR release label')
    parser.add_argument('-p', '--protect', help='set cluster as TerminationProtected', action='store_true')
    parser.add_argument('-c', '--count', metavar='N', default=1, type=int, help='core node instances count')
    parser.add_argument('-mc', '--master_capacity', metavar='N', type=int,
                        help='master node target capacity (instance fleet units)')
    parser.add_argument('-cc', '--core_capacity', metavar='N', type=int,
                        help='core node target capacity (instance fleet units)')
    parser.add_argument('-ms', '--master_size', metavar='GB', default=100, type=int,
                        help='EBS volume size in GB (master node)')
    parser.add_argument('-cs', '--core_size', metavar='GB', default=100, type=int,
                        help='EBS volume size in GB (core nodes)')
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

    if not args.account:
        print('Account not is set, and no default account exists')
        sys.exit(1)

    # TODO: find all of these values in the account, and check only if they are not present
    if args.fleet and (args.master_instance or args.core_instance):
        print('Instance types are mutually exclusive with instance fleet')
        sys.exit(1)
    if (args.master_instance and not args.core_instance) or (args.core_instance and not args.master_instance):
        print('Master and Core node instances must be defined')
        sys.exit(1)
    if args.core_instance and not args.count:
        print('Core node instances count must be defined')
        sys.exit(1)
    if args.fleet and not args.master_capacity:
        print('Master node target on_demand capacity must be defined')
        sys.exit(1)
    if args.fleet and not args.core_capacity:
        print('Core node target on_demand capacity must be defined')
        sys.exit(1)

    environment = accounts[args.account]["emr"]
    configurations = \
        get_hdfs_site_configuration() + \
        get_livy_configuration() + \
        get_emrfs_site_configuration()

    if args.core_instance:
        configurations += get_yarn_site_configurations(capacity_scheduler={
            "instance_type": args.core_instance,
            "node_count": args.count
        })
        configurations += get_spark_configurations(args.core_instance, args.count)

    if args.verbose:
        if args.master_instance:
            print(f'EC2 Master node instance: {args.master_instance}')
        if args.core_instance:
            print(f'EC2 Core node instance: {args.core_instance}')
        if args.fleet:
            print(f'Instance fleet: {args.fleet}')
        print(f'Volume size in GB: {args.size}')
        print(configurations)

    boot = []
    if args.boot:
        boot = [{
            'name': 'Run script: ' + b.strip(),
            'path': b,
            'args': []
        } for b in args.boot]

    emr = EMR(args.verbose)
    instance_fleet_configs = environment['instance_fleets'] if 'instance_fleets' in environment else None
    cluster_id = emr.start_cluster(
        name=args.name,
        log_uri=environment['log_uri'],
        keep_alive=True,
        protect=args.protect,
        applications=args.applications,
        job_flow_role=environment['job_flow_role'],
        service_role=environment['service_role'],
        emr_label=args.emr,
        instance_fleet={
            'master': {
                'instance_fleet_name': args.fleet,
                'TargetOnDemandCapacity': args.master_capacity,
                'TargetSpotCapacity': 0,
                'on_demand_allocation_strategy': 'LOWEST_PRICE'
            },
            'core': {
                'instance_fleet_name': args.fleet,
                'TargetOnDemandCapacity': args.core_capacity if not args.spot else 0,
                'TargetSpotCapacity': args.core_capacity if args.spot else 0,
                'on_demand_allocation_strategy': 'LOWEST_PRICE'
            }
        } if args.fleet else None,
        instance_fleet_configs=instance_fleet_configs,
        instance_groups={
            'master': {
                'Market': 'ON_DEMAND',
                'InstanceType': args.master_instance,
                'InstanceCount': 1
            },
            'core': {
                'Market': 'ON_DEMAND' if not args.spot else 'SPOT',
                'InstanceType': args.core_instance,
                'InstanceCount': args.count
            }
        } if args.master_instance else None,
        ebs_master_volume_gb=args.master_size if args.master_size else None,
        ebs_core_volume_gb=args.core_size if args.core_size else None,
        steps=[{
            'Name': 'Enable debugging',
            'Args': ["state-pusher-script"]
        }],
        tags=environment['tags'],
        security_groups=environment['security_groups'],
        subnets=environment['subnets'],
        configurations=configurations,
        keyname=environment['keyname'] if 'keyname' in environment else None,
        bootstrap_scripts=boot
    )

    print(cluster_id)


if __name__ == "__main__":
    main()
