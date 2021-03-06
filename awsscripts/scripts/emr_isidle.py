from datetime import datetime, timedelta, timezone

import boto3


def configure_parser(parser) -> None:
    parser.add_argument('-c', '--cluster', metavar='CLUSTER_ID', type=str, required=True, help='cluster ID')
    parser.add_argument('-i', '--idleness', metavar='HOURS', type=int, default=2,
                        help='Idleness time in hours (default=2)')


def execute(args) -> None:
    min_age = timedelta(hours=args.idleness)
    period_seconds = 300  # 5-minute period, available for 63 days

    cloudwatch = boto3.client('cloudwatch')

    now = datetime.now(timezone.utc)
    response = cloudwatch.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'emrIdleClusters',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ElasticMapReduce',
                        'MetricName': 'IsIdle',
                        'Dimensions': [{
                            'Name': 'JobFlowId',
                            'Value': args.cluster
                        }]
                    },
                    'Period': period_seconds,
                    'Stat': 'Maximum',
                    'Unit': 'None'
                },

                'Label': '${SUM}',
                'ReturnData': True,
            },
        ],
        StartTime=now - min_age,
        EndTime=now,
        ScanBy='TimestampDescending'
    )['MetricDataResults'][0]

    idle_cluster_value = int(min_age.total_seconds() / period_seconds)  # all 5-minute intervals must be 1.0
    is_idle = response['Label'] == str(idle_cluster_value)

    idle_period = 0
    for v in response['Values']:
        if v == 1.0:
            idle_period += 5  # each 1.0 means 5 minutes idleness
        else:
            break

    if is_idle:
        print("Cluster is idle now")
    print(f"Cluster was idle for {idle_period} minutes")
