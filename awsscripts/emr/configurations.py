from typing import List, Dict, Any, Optional
import math

from ec2 import ec2_instances


class EmrConfigurations:

    def __init__(self):
        self.configurations = []

    def add_spark(self, instance_type: str, node_count: int) -> None:
        self.configurations += EmrConfigurations._generate_spark(instance_type, node_count)

    def add_yarn_site(self, remote_log_dir: Optional[str] = None,
                      capacity_scheduler: Optional[Dict[str, Any]] = None) -> None:
        self.configurations += EmrConfigurations._generate_yarn_site(remote_log_dir, capacity_scheduler)

    def add_hdfs_site(self, dfs_replication: int = 2) -> None:
        self.configurations += EmrConfigurations._generate_hdfs_site(dfs_replication)

    def add_livy(self, session_timeout: str = "12h"):
        self.configurations += EmrConfigurations._generate_livy(session_timeout)

    def add_emrfs_site(self, fs_s3_max_connections: int = 100):
        self.configurations += EmrConfigurations._generate_emrfs_site(fs_s3_max_connections)

    @staticmethod
    def _generate_spark(instance_type: str, node_count: int) -> List[Dict[str, Any]]:
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
        spark_executors = max(1,
                              int(spark_executors_per_node * node_count - 1))  # 1 executor for ApplicationMaster in YARN
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

    @staticmethod
    def _generate_yarn_site(remote_log_dir: Optional[str] = None,
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
        :type capacity_scheduler: Optional[Dict[str, Any]]
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

    @staticmethod
    def _generate_hdfs_site(dfs_replication: int = 2) -> List[Dict[str, Any]]:
        """
        Generates configuration for 'hdfs-site'.
        :param dfs_replication: DFS replication (2 by default)
        :return: hdfs-site configuration
        """
        return [{
            'Classification': 'hdfs-site',
            'Properties': {
                'dfs.replication': str(dfs_replication)
            }
        }]

    @staticmethod
    def _generate_livy(session_timeout: str = "12h") -> List[Dict[str, Any]]:
        """
        Generates Livy configuration.
        :param session_timeout: session timeout (default=12h)
        :return: livy configuration
        """
        return [{
            "Classification": "livy-conf",
            "Properties": {
                "livy.server.session.timeout": session_timeout
            }
        }]

    @staticmethod
    def _generate_emrfs_site(fs_s3_max_connections: int = 100) -> List[Dict[str, Any]]:
        """
        Generates emrfs-site configuration.
        :param fs_s3_max_connections:  max S3 connections (default=100). Can address the
         "Timeout waiting for connection from pool" error
        :return: emrfs-site configuration
        """
        #
        return [
            {
                'Classification': 'emrfs-site',
                'Properties': {
                    'fs.s3.maxConnections': str(fs_s3_max_connections)
                }
            }
        ]
