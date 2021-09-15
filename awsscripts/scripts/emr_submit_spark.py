import argparse

from awsscripts.helpers.emr import EMR


def main():
    parser = argparse.ArgumentParser(description='Submits Apache Spark step')
    parser.add_argument('-c', '--clusterid', metavar='ID', type=str, required=True, help='cluster ID')
    parser.add_argument('-s', '--stepname', metavar='STEP_NAME', type=str, required=True, help='step name')
    parser.add_argument('-p', '--pyfiles', metavar='PATH', type=str, nargs='*', help='Additional python files')
    parser.add_argument('-j', '--jars', metavar='PATH', type=str, nargs='*', help='Additional JAR files')

    parser.add_argument('-C', '--classname', metavar='FULL_NAME', type=str, help='Java class to run')
    parser.add_argument('application', metavar='URI', type=str, help='Application JAR/Python main file')
    parser.add_argument('arguments', metavar='ARG', type=str, nargs='*', help='Command-line arguments')

    args = parser.parse_args()

    emr = EMR()
    step_id = emr.add_spark_step(
        args.clusterid, args.stepname, args.application, args.jars, args.pyfiles, args.classname, args.arguments
    )
    print(step_id)


if __name__ == "__main__":
    main()
