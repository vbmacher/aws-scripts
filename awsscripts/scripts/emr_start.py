import argparse
import sys

from accounts import Accounts
from emr.configurations import EmrConfigurations
from emr.emr import EMR
from templates.emr_template import EmrTemplate


def main() -> None:
    accounts = Accounts()
    default_account = accounts.get_default_account()
    default_msg = f' (default={default_account})' if default_account else ''

    parser = argparse.ArgumentParser(description='Starts EMR cluster')
    parser.add_argument('-n', '--name', metavar='NAME', type=str, help='cluster name')
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
    parser.add_argument('-b', '--boot', metavar='NAME', type=str, nargs='*',
                        help='Bootstrap scripts (names as defined in the account).')
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
    template = EmrTemplate.from_content(environment)

    configurations = EmrConfigurations()

    if args.core_instance:
        configurations.add_yarn_site(capacity_scheduler={
            "instance_type": args.core_instance,
            "node_count": args.count
        })
        configurations.add_spark(args.core_instance, args.count)
    template.put_configurations(configurations.configurations)

    if args.fleet:
        template.put_instance_fleet(args.fleet, args.master_capacity, args.core_capacity, args.spot)
    if args.master_instance:
        template.put_instance_groups(args.master_instance, args.core_instance, args.count, args.spot)
    if args.emr:
        template.set_emr_label(args.emr)
    if args.name:
        template.set_cluster_name(args.name)
    if args.applications and not ('applications' in environment):
        template.set_applications(args.applications)
    if args.protect and not ('TerminationProtected' in environment):
        template.set_protect(args.protect)
    if args.master_size:
        template.set_master_size_gb(args.master_size)
    if args.core_size:
        template.set_core_size_gb(args.core_size)

    if args.verbose:
        generated = template.generate()
        generated.pop('instance_fleets')
        print(generated)

    boot = []
    if args.boot:
        boot = [template.get_bootstrap_script(b) for b in args.boot]

    emr = EMR(args.verbose)
    cluster_id = emr.start_cluster(
        name=template.get_cluster_name(),
        log_uri=template.get_log_uri(),
        keep_alive=True,
        protect=template.get_protect(),
        applications=template.applications,
        job_flow_role=template.get_job_flow_role(),
        service_role=template.get_service_role(),
        emr_label=template.get_emr_label(),
        instance_fleet=template.get_instance_fleet(),
        instance_fleet_configs=template.get_instance_fleets(),
        instance_groups=template.get_instance_groups(),
        ebs_master_volume_gb=template.get_master_size_gb(),
        ebs_core_volume_gb=template.get_core_size_gb(),
        steps=[{
            'Name': 'Enable debugging',
            'Args': ["state-pusher-script"]
        }],
        tags=template.get_tags(),
        security_groups=template.get_security_groups(),
        subnets=template.get_subnets(),
        configurations=template.get_configurations(),
        keyname=template.get_keyname(),
        bootstrap_scripts=boot
    )

    print(cluster_id)


if __name__ == "__main__":
    main()
