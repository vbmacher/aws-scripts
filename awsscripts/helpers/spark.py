import math
from typing import Any, Dict, List, Optional

from awsscripts.helpers.ec2 import ec2_instances


def get_spark_configurations(instance_type: str, node_count: int) -> List[Dict[str, Any]]:
    """
    Generates Spark configurations for creating EMR cluster, based on EC2 instance type and node count.
    According to: https://github.com/vbmacher/knowledge-notes/blob/master/spark/spark-parameters/spark-parameters.md

    :param instance_type: AWS instance type
    :param node_count: Node count (including master)
    :return: Configurations of Spark parameters (list)
    """

    ec2 = ec2_instances[instance_type]
    gbits2gbytes = 1.07374

    spark_cores = 5
    spark_executors_per_node = (ec2["cpu"] - 1) / spark_cores
    spark_executors = max(1, int(spark_executors_per_node * node_count - 1))  # 1 executor for ApplicationMaster in YARN
    spark_raw_memory_per_executor = ec2["memory"] / spark_executors_per_node
    spark_memory_overhead = max(0.384, 0.07 * spark_raw_memory_per_executor)
    spark_memory_per_executor = int((spark_raw_memory_per_executor - spark_memory_overhead) * gbits2gbytes)
    spark_driver_cores = ec2["cpu"]
    spark_driver_memory = int(math.floor(spark_memory_per_executor * 0.6))
    spark_default_parallelism = int(math.ceil(spark_executors_per_node * spark_cores * 2))

    return [
        {
            'Classification': 'spark',
            'Properties': {
                'maximizeResourceAllocation': 'false',
            }
        },
        {
            "Classification": "spark-defaults",
            "Properties": {
                'spark.sql.parquet.fs.optimized.committer.optimization-enabled': 'true',
                'spark.network.timeout': '300s',
                'spark.sql.broadcastTimeout': '108000',
                'spark.sql.hive.filesourcePartitionFileCacheSize': '1073741824',
                'spark.rpc.message.maxSize': '2047',
                'spark.rpc.askTimeout': '300',
                'spark.task.maxFailures': '10',
                'spark.serializer': 'org.apache.spark.serializer.KryoSerializer',
                'spark.shuffle.service.enabled': 'true',
                'spark.dynamicAllocation.enabled': 'true',
                'spark.executor.heartbeatInterval': '20s',
                'spark.executor.extraJavaOptions': '-XX:+UseG1GC',
                'spark.cleaner.periodicGC.interval': '600min',
                'spark.executor.cores': f'{spark_cores}',
                'spark.executor.memory': f'{spark_memory_per_executor}G',
                'spark.executor.instances': f'{spark_executors}',
                'spark.driver.cores': f'{spark_driver_cores}',
                'spark.driver.memory': f'{spark_driver_memory}G',
                'spark.driver.maxResultSize': f'{spark_driver_memory}G',
                'spark.default.parallelism': f'{spark_default_parallelism}',
                'spark.sql.shuffle.partitions': '1200'
            }
        }
    ]


def get_yarn_site_configurations(remote_log_dir: Optional[str] = None,
                                 capacity_scheduler: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    Generates yarn.site configurations used when creating EMR cluster.

    :param remote_log_dir: Turns on log aggregation into remote directory. Expects S3 path. (default=None)
    :type remote_log_dir: Optional[str]
    :param capacity_scheduler: Sets up CapacityScheduler in YARN. The argument expects the following configuration:

      {
        "instance_type": "AWS EC2 instance type",
        "node_count": instances count
      }

    By default, it is empty.
    :type capacity_scheduler: Optional[bool]
    :return: Configurations of yarn.site (list)
    """
    result = {}
    if remote_log_dir:
        result.update({
            "yarn.log-aggregation-enable": "true",
            "yarn.log-aggregation.retain-seconds": "-1",
            "yarn.nodemanager.remote-app-log-dir": remote_log_dir
        })

    if capacity_scheduler:
        # Description: The maximum percentage of resources preempted in a single round. You can use this value
        # to restrict the pace at which Containers are reclaimed from the cluster. After computing the total
        # desired preemption, the policy scales it back to this limit. This should be set to
        #   (memory-of-one-NodeManager)/(total-cluster-memory)
        # For example, if one NodeManager has 32 GB, and the total cluster resource is 100 GB, the
        # total_preemption_per_round should set to 32/100 = 0.32. The default value is 0.1 (10%).

        node_memory = ec2_instances[capacity_scheduler["instance_type"]]["memory"]
        yarn_total_preemption_per_round = node_memory / (node_memory * capacity_scheduler["node_count"])

        result.update({
            "yarn.resourcemanager.scheduler.class":
                "org.apache.hadoop.yarn.server.resourcemanager.scheduler.capacity.CapacityScheduler",
            "yarn.resourcemanager.scheduler.monitor.enable": "true",
            "yarn.resourcemanager.scheduler.monitor.policies":
                "org.apache.hadoop.yarn.server.resourcemanager.monitor.capacity.ProportionalCapacityPreemptionPolicy",
            "yarn.scheduler.capacity.resource-calculator":
                "org.apache.hadoop.yarn.util.resource.DominantResourceCalculator",
            "yarn.resourcemanager.monitor.capacity.preemption.total_preemption_per_round":
                str(yarn_total_preemption_per_round)
        })

    return [
        {
            "Classification": "yarn-site",
            "Properties": result
        }
    ]


def get_hdfs_site_configuration(dfs_replication: int = 2):
    return [{
        'Classification': 'hdfs-site',
        'Properties': {
            'dfs.replication': str(dfs_replication)
        }
    }]


def get_livy_configuration(session_timeout: str = "12h"):
    return [{
        "Classification": "livy-conf",
        "Properties": {
            "livy.server.session.timeout": session_timeout
        }
    }]


def get_emrfs_site_configuration(fs_s3_max_connections: int = 100):
    # addresses the "Timeout waiting for connection from pool" error
    return [
        {
            'Classification': 'emrfs-site',
            'Properties': {
                'fs.s3.maxConnections': str(fs_s3_max_connections)
            }
        }
    ]


def get_spark_steps(steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Generates Spark steps used when creating EMR cluster.
    :param steps: List of simplified Step definitions. Structure:
       [
         {
           'name': 'step name string',
           'actionOnFailure': 'one of: TERMINATE_CLUSTER, CONTINUE, CANCEL_AND_WAIT',
           'conf': ['key=value'], // optional
           'jars': ['string'], // optional
           'pyfiles': ['string'],  // optional
           'class': 'main-class string', // optional
           'application': 'Application JAR/Python file name',
           'args': ['string'] // optional
         }
       ]
    :return: List of Spark steps usable when creating EMR cluster (properly formatted)
    """

    def step_conf(step):
        result = ['spark-submit', '--master', 'yarn', '--deploy-mode', 'cluster']
        if 'conf' in step:
            for setting in step["conf"]:
                result += ['--conf', setting]
        if 'pyfiles' in step:
            result += ['--py-files', ','.join(step["pyfiles"])]
        if 'jars' in step:
            result += ['--jars', ','.join(step["jars"])]
        if 'class' in step:
            result += ['--class', step["class"]]
        result += [step["application"]]
        if 'args' in step:
            result += step["args"]
        return result

    return [
        {
            'Name': step["name"],
            'ActionOnFailure': step["actionOnFailure"],
            'HadoopJarStep': {
                'Jar': 'command-runner.jar',
                'Args': step_conf(step)
            }
        } for step in steps
    ]
