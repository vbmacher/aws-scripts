import argparse

from emr.emr import EMR


def main() -> None:
    parser = argparse.ArgumentParser(description='Terminates EMR cluster')
    parser.add_argument('-c', '--clusterid', metavar='ID', type=str, required=True, help='cluster ID')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode')

    args = parser.parse_args()

    emr = EMR(verbose=args.verbose)
    emr.terminate_cluster(args.clusterid)


if __name__ == "__main__":
    main()
