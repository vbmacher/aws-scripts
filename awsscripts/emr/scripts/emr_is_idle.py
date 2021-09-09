import argparse
import boto3
from datetime import datetime, timedelta, timezone


def main():
    parser = argparse.ArgumentParser(description='Determines if an EMR cluster is idle at least 2 hours')
    parser.add_argument('-c', '--cluster', metavar='CLUSTER_ID', type=str, required=True, help='cluster ID')

    args = parser.parse_args()
    min_age = timedelta(hours=2)
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
        print(f"Cluster is idle now")
    print(f"Cluster was idle for {idle_period} minutes")


if __name__ == "__main__":
    main()
