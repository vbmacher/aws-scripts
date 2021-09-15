"""
EMR - Elastic Map Reduce

Helper class to manage EMR clusters using Boto3 Python library.
"""

from typing import List, Dict, Any, Optional

import boto3
from botocore.exceptions import ClientError


class EMR:

    def __init__(self):
        self.emr_client = boto3.client('emr')

    def start_cluster(self,
                      name: str,
                      log_uri: str,
                      keep_alive: bool,
                      protect: bool,
                      applications: List[str],
                      job_flow_role: str,
                      service_role: str,
                      emr_label: str,
                      master_instance: str,
                      node_instance: str,
                      node_count: int,
                      steps: List[Dict[str, Any]],
                      tags: List[str],
                      security_groups: Dict[str, Any],
                      subnets: Dict[str, Any],
                      configurations: List[Dict[str, Any]],
                      keyname: str,
                      volume_size_gb: int,
                      bootstrap_scripts: List[Dict[str, Any]]) -> str:

        """
        Runs a job flow with the specified steps. A job flow creates a cluster of
        instances and adds steps to be run on the cluster. Steps added to the cluster
        are run as soon as the cluster is ready.

        :param bootstrap_scripts: Bootstrap scripts array. Structure:
                    [{
                       'name': 'string',
                       'path': 'string',
                       'args': ['string']
                    }]
        :param keyname: SSH key name to use
        :param volume_size_gb: volume size in GB (x2)
        :param configurations: configurations of this EMR cluster
        :param subnets: list of available subnets
        :param security_groups: security groups
        :param name: The name of the cluster.
        :param log_uri: The URI where logs are stored. This can be an Amazon S3 bucket URL,
                        such as 's3://my-log-bucket'.
        :param keep_alive: When True, the cluster is put into a Waiting state after all
                           steps are run. When False, the cluster terminates itself when
                           the step queue is empty.
        :param protect: sets TerminationProtected to True/False
        :param applications: The applications to install on each instance in the cluster,
                             such as Hive or Spark.
        :param job_flow_role: The IAM role assumed by the cluster.
        :param service_role: The IAM role assumed by the service.
        :param emr_label: EMR release label. E.g. 'emr-5.30.1'
        :param master_instance: Instance type of master node (driver). E.g. 'm5.xlarge'
        :param node_instance: Instance type of "slave" node (core nodes). E.g. 'm5.xlarge'
        :param node_count: Count of "slave" nodes. E.g. 3
        :param steps: The job flow steps to add to the cluster. These are run in order
                      when the cluster is ready. Structure:

                {
                    'Name': 'string',
                    'Args': []
                }
        :param tags: Cluster tags
        :return: The ID of the newly created cluster.
        """

        # TODO: be able to configure instance fleets externally
        try:
            weight = 48
            response = self.emr_client.run_job_flow(
                Name=name,
                LogUri=log_uri,
                ReleaseLabel=emr_label,
                Instances={
                    'KeepJobFlowAliveWhenNoSteps': keep_alive,
                    'TerminationProtected': protect,
                    'InstanceFleets': [
                        {
                            "InstanceFleetType": "MASTER",
                            "TargetOnDemandCapacity": 1,
                            "TargetSpotCapacity": 0,
                            "LaunchSpecifications": {
                                "OnDemandSpecification": {
                                    "AllocationStrategy": "LOWEST_PRICE"
                                }
                            },
                            "InstanceTypeConfigs": [
                                {
                                    "WeightedCapacity": 1,
                                    "EbsConfiguration": {
                                        "EbsBlockDeviceConfigs": [
                                            {
                                                "VolumeSpecification": {
                                                    "SizeInGB": volume_size_gb,
                                                    "VolumeType": "gp2"
                                                },
                                                "VolumesPerInstance": 2
                                            }
                                        ]
                                    },
                                    "BidPriceAsPercentageOfOnDemandPrice": 100,
                                    "InstanceType": master_instance
                                }
                            ],
                            "Name": "Master"
                        },
                        {
                            "InstanceFleetType": "CORE",
                            "TargetOnDemandCapacity": weight * node_count,
                            "TargetSpotCapacity": 0,
                            "LaunchSpecifications": {
                                "OnDemandSpecification": {
                                    "AllocationStrategy": "LOWEST_PRICE"
                                }
                            },
                            "InstanceTypeConfigs": [
                                {
                                    "WeightedCapacity": weight,
                                    "EbsConfiguration": {
                                        "EbsBlockDeviceConfigs": [
                                            {
                                                "VolumeSpecification": {
                                                    "SizeInGB": volume_size_gb,
                                                    "VolumeType": "gp2"
                                                },
                                                "VolumesPerInstance": 2
                                            }
                                        ], "EbsOptimized": True
                                    },
                                    "BidPriceAsPercentageOfOnDemandPrice": 100,
                                    "InstanceType": node_instance
                                }
                            ], "Name": "Core"
                        }
                    ],
                    'Ec2SubnetIds': subnets,
                    'Ec2KeyName': keyname,
                    'EmrManagedMasterSecurityGroup': security_groups["EmrManagedMasterSecurityGroup"],
                    'EmrManagedSlaveSecurityGroup': security_groups["EmrManagedSlaveSecurityGroup"],
                    'AdditionalMasterSecurityGroups': security_groups["AdditionalMasterSecurityGroups"],
                    'AdditionalSlaveSecurityGroups': security_groups["AdditionalSlaveSecurityGroups"]

                    # TODO: ServiceAccessSecurityGroup
                },
                Steps=[{
                    'Name': step['Name'],
                    'ActionOnFailure': 'CONTINUE',
                    'HadoopJarStep': {
                        'Jar': 'command-runner.jar',
                        'Args': step['Args']
                    }
                } for step in steps],
                BootstrapActions=[{
                    'Name': boot['name'],
                    'ScriptBootstrapAction': {
                        'Path': boot['path'],
                        'Args': boot['args']
                    }
                } for boot in bootstrap_scripts],
                Applications=[{'Name': app} for app in applications],
                JobFlowRole=job_flow_role,
                ServiceRole=service_role,
                VisibleToAllUsers=True,
                Configurations=configurations,
                Tags=tags
            )
            cluster_id = response['JobFlowId']
            print("Created cluster %s.", cluster_id)
        except ClientError:
            print("Couldn't create cluster.")
            raise
        else:
            return cluster_id

    def describe_cluster(self, cluster_id: str) -> Dict[str, Any]:
        """
        Gets detailed information about a cluster.

        :param cluster_id: The ID of the cluster to describe.
        :return: The retrieved cluster information.
        """
        try:
            response = self.emr_client.describe_cluster(ClusterId=cluster_id)
            cluster = response['Cluster']
            print(f'Got data for cluster "{cluster["Name"]}"')
        except ClientError:
            print("Couldn't get data for cluster %s.", cluster_id)
            raise
        else:
            return cluster

    def terminate_cluster(self, cluster_id: str):
        """
        Terminates a cluster. This terminates all instances in the cluster and cannot
        be undone. Any data not saved elsewhere, such as in an Amazon S3 bucket, is lost.

        :param cluster_id: The ID of the cluster to terminate.
        """
        try:
            self.emr_client.terminate_job_flows(JobFlowIds=[cluster_id])
            print(f"Terminated cluster {cluster_id}")
        except ClientError:
            print(f"Couldn't terminate cluster {cluster_id}")
            raise

    def add_step(self, cluster_id: str, name: str, args: List[str]) -> str:
        """
        Adds a job step to the specified cluster. This example adds a Spark
        step, which is run by the cluster as soon as it is added.

        :param cluster_id: The ID of the cluster.
        :param name: The name of the step.
        :param args: Arguments to pass to the command-runner.
        :return: The ID of the newly added step.
        """
        try:
            response = self.emr_client.add_job_flow_steps(
                JobFlowId=cluster_id,
                Steps=[{
                    'Name': name,
                    'ActionOnFailure': 'CONTINUE',
                    'HadoopJarStep': {
                        'Jar': 'command-runner.jar',
                        'Args': args
                    }
                }])
            step_id = response['StepIds'][0]
            print(f"Started step {step_id}")
        except ClientError:
            print(f"Couldn't start step '{name}' with URI {args}")
            raise
        else:
            return step_id

    def add_spark_step(self, cluster_id: str, name: str, application_uri: str,
                       jars: List[str], pyfiles: List[str], classname: Optional[str], arguments: List[str]) -> str:
        """
        Adds a job step to the specified cluster.

        :param cluster_id: The ID of the cluster.
        :param name: The name of the step.
        :param application_uri: The URI of the JAR/Python application file
        :param jars: List of additional jars (can be empty)
        :param pyfiles: List of additional Python files (.zip, .egg, .py)
        :param classname: Class name (only if Java application is submitted)
        :param arguments: Arguments to pass to the application.
        :return: The ID of the newly added step.
        """
        jars_arg = ['--jars', ','.join(jars)] if len(jars) == 0 else []
        pyfiles_arg = ['--pyfiles', ','.join(pyfiles)] if len(pyfiles) == 0 else []
        class_arg = ['--class', classname] if classname else []
        return self.add_step(
            cluster_id, name,
            ['spark-submit', '--deploy-mode', 'cluster', '--master', 'yarn', *jars_arg, *pyfiles_arg, *class_arg,
             application_uri, *arguments]
        )

    def list_steps(self, cluster_id: str) -> Dict[str, Any]:
        """
        Gets a list of steps for the specified cluster. In this example, all steps are
        returned, including completed and failed steps.

        :param cluster_id: The ID of the cluster.
        :return: The list of steps for the specified cluster.
        """
        try:
            response = self.emr_client.list_steps(ClusterId=cluster_id)
            steps = response['Steps']
            print(f"Got {len(steps)} steps for cluster {cluster_id}")
        except ClientError:
            print(f"Couldn't get steps for cluster {cluster_id}")
            raise
        else:
            return steps

    def describe_step(self, cluster_id: str, step_id: str) -> Dict[str, Any]:
        """
        Gets detailed information about the specified step, including the current state of
        the step.

        :param cluster_id: The ID of the cluster.
        :param step_id: The ID of the step.
        :return: The retrieved information about the specified step.
        """
        try:
            response = self.emr_client.describe_step(ClusterId=cluster_id, StepId=step_id)
            step = response['Step']
            print(f"Got data for step {step_id}")
        except ClientError:
            print(f"Couldn't get data for step {step_id}")
            raise
        else:
            return step
