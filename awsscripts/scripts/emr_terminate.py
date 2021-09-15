import argparse

from awsscripts.helpers.emr import EMR


def main():
    parser = argparse.ArgumentParser(description='Terminates EMR cluster')
    parser.add_argument('-c', '--clusterid', metavar='ID', type=str, required=True, help='cluster ID')

    args = parser.parse_args()

    emr = EMR()
    emr.terminate_cluster(args.clusterid)


if __name__ == "__main__":
    main()
