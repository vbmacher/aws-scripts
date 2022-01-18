from accounts import Accounts, templates
from templates.emr_template import EmrTemplate


def configure_parser(parser):
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-c', '--create', metavar='SERVICE', type=str,
                       help=f'Create a service template in the account. One of: {templates.keys()}')
    group.add_argument('-r', '--remove', metavar='SERVICE', type=str,
                       help=f'Remove service template from the account. One of: {templates.keys()}')
    parser.add_argument('-cemr', '--configure-emr', metavar='CLUSTER_ID', type=str,
                        help='Configure EMR template from existing EMR cluster')


def execute(args) -> None:
    accounts = Accounts()

    if args.default:
        accounts.make_default(args.account)

    if args.create:
        accounts.add_template(args.account, args.create)

    if args.remove:
        accounts.remove_template(args.account, args.remove)

    if args.configure_emr:
        emr_template = EmrTemplate.from_cluster(args.configure_emr)
        accounts.replace_template(args.account, 'emr', emr_template.generate())
