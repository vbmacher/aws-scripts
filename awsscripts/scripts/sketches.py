from awsscripts.sketches.sketches import Sketches, sketch_items
from awsscripts.sketches.emr import EmrSketchItem


def configure_parser(parser):
    group = parser.add_mutually_exclusive_group()
    parser.add_argument('-d', '--default', help='Make the sketch default', action='store_true')
    parser.add_argument('-cemr', '--configure-emr', metavar='CLUSTER_ID', type=str,
                        help='Configure EMR sketch item from existing EMR cluster')
    parser.add_argument('-l', '--list', action='store_true', help='List existing sketches')
    parser.add_argument('-L', '--list-items', action='store_true', help='List existing sketch items')

    group.add_argument('-c', '--create', metavar='SERVICE', type=str,
                       help=f'Create an item in a sketch. One of: {list(sketch_items)}')
    group.add_argument('-r', '--remove', metavar='SERVICE', type=str,
                       help=f'Remove an existing item from a sketch')


def execute(args) -> None:
    sketches = Sketches()

    if args.list:
        print(list(sketch_items))

    if args.sketch and args.list_items:
        print(sketches.list_sketch_items(args.sketch))

    if args.sketch and hasattr(args, 'default'):
        sketches.make_default(args.sketch)

    if args.sketch and args.create:
        sketches.add_sketch_item(args.sketch, args.create)

    if args.sketch and args.remove:
        sketches.remove_sketch_item(args.sketch, args.remove)

    if args.sketch and args.configure_emr:
        emr_item = EmrSketchItem.from_cluster(args.configure_emr)
        sketches.replace_sketch_item(args.sketch, 'emr', emr_item.generate())
