from emr.emr import EMR


def configure_parser(parser) -> None:
    parser.add_argument('-c', '--clusterid', metavar='ID', type=str, required=True, help='cluster ID')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode')


def execute(args) -> None:
    emr = EMR(verbose=args.verbose)
    emr.terminate_cluster(args.clusterid)
