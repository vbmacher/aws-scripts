import sys

from awsscripts.sketches.sketches import Sketches
from awsscripts.emr.configurations import EmrConfigurations
from awsscripts.emr.emr import EMR
from awsscripts.sketches.emr import EmrSketchItem


def configure_parser(parser):
    parser.add_argument('-n', '--name', metavar='NAME', type=str, help='cluster name')
    parser.add_argument('-mi', '--master_instance', metavar='INSTANCE', default='m5.xlarge',
                        help='master node instance type')
    parser.add_argument('-ci', '--core_instance', metavar='INSTANCE', default='m5.xlarge',
                        help='core nodes instance type')
    parser.add_argument('-f', '--fleet', metavar='INSTANCE_FLEET',
                        help='instance fleet name (instance fleets must be defined in the sketch)')
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
                        help='Bootstrap scripts (names as defined in the sketch).')
    parser.add_argument('-A', '--applications', metavar='APP', nargs='*',
                        default=['Spark', 'JupyterHub', 'JupyterEnterpriseGateway', 'Hadoop', 'Livy'],
                        help='EMR applications (default: Spark,JupyterHub,JupyterEnterpriseGateway,Hadoop,Livy)')


def execute(args) -> None:
    if not args.sketch:
        print('Sketch not is set, and no default sketch exists')
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

    sketches = Sketches()
    emr_item = EmrSketchItem.from_content(sketches[args.sketch]["emr"])
    configurations = EmrConfigurations()

    if args.core_instance:
        configurations.add_yarn_site(capacity_scheduler={
            "instance_type": args.core_instance,
            "node_count": args.count
        })
        configurations.add_spark(args.core_instance, args.count)
    emr_item.put_configurations(configurations.configurations)

    if args.fleet:
        emr_item.put_instance_fleet(args.fleet, args.master_capacity, args.core_capacity, args.spot)
    if args.master_instance:
        emr_item.put_instance_groups(args.master_instance, args.core_instance, args.count, args.spot)
    if args.emr:
        emr_item.set_emr_label(args.emr)
    if args.name:
        emr_item.set_cluster_name(args.name)
    if args.applications and not emr_item.contains('applications'):
        emr_item.set_applications(args.applications)
    if args.protect and not emr_item.contains('TerminationProtected'):
        emr_item.set_protect(args.protect)
    if args.master_size:
        emr_item.set_master_size_gb(args.master_size)
    if args.core_size:
        emr_item.set_core_size_gb(args.core_size)

    if args.verbose:
        generated = emr_item.generate()
        generated.pop('instance_fleets')
        print(generated)

    boot = []
    if args.boot:
        boot = [emr_item.get_bootstrap_script(b) for b in args.boot]

    emr = EMR(args.verbose)
    cluster_id = emr.start_cluster(
        name=emr_item.get_cluster_name(),
        log_uri=emr_item.get_log_uri(),
        keep_alive=True,
        protect=emr_item.get_protect(),
        applications=emr_item.applications,
        job_flow_role=emr_item.get_job_flow_role(),
        service_role=emr_item.get_service_role(),
        emr_label=emr_item.get_emr_label(),
        instance_fleet=emr_item.get_instance_fleet(),
        instance_fleet_configs=emr_item.get_instance_fleets(),
        instance_groups=emr_item.get_instance_groups(),
        ebs_master_volume_gb=emr_item.get_master_size_gb(),
        ebs_core_volume_gb=emr_item.get_core_size_gb(),
        steps=[{
            'Name': 'Enable debugging',
            'Args': ["state-pusher-script"]
        }],
        tags=emr_item.get_tags(),
        security_groups=emr_item.get_security_groups(),
        subnets=emr_item.get_subnets(),
        configurations=emr_item.get_configurations(),
        keyname=emr_item.get_keyname(),
        bootstrap_scripts=boot
    )

    print(cluster_id)
