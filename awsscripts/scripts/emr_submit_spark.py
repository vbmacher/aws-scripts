import argparse

from awsscripts.helpers.emr import EMR


def main() -> None:
    parser = argparse.ArgumentParser(description='Submits Apache Spark step')
    parser.add_argument('-c', '--clusterid', metavar='ID', type=str, required=True, help='cluster ID')
    parser.add_argument('-s', '--stepname', metavar='STEP_NAME', type=str, required=True, help='step name')
    parser.add_argument('-p', '--py-files', metavar='PATH', type=str,
                        help='Additional python files (separate with comma (","))')
    parser.add_argument('-j', '--jars', metavar='PATH', type=str,
                        help='Additional JAR files (separate with comma (","))')
    parser.add_argument('-d', '--deploy-mode', metavar='MODE', type=str, default='cluster',
                        help='Spark deploy mode (default=cluster)')
    parser.add_argument('-m', '--master', metavar='MASTER', type=str,
                        help='Application master')
    parser.add_argument('-v', '--verbose', help='Verbose output', action='store_true')
    parser.add_argument('-C', '--classname', metavar='FULL_NAME', type=str, help='Java class to run')
    parser.add_argument('application', metavar='URI', type=str, help='Application JAR/Python main file')
    parser.add_argument('arguments', metavar='ARG', type=str, nargs='*', help='Command-line arguments')

    args = parser.parse_args()

    emr = EMR(args.verbose)
    step_id = emr.add_spark_step(
        args.clusterid, args.stepname, args.deploy_mode, args.master, args.application, args.jars, args.py_files,
        args.classname, args.arguments
    )
    print(step_id)


if __name__ == "__main__":
    main()
