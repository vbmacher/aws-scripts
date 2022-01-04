"""
EMR - Elastic Map Reduce

Helper class to manage EMR clusters using Boto3 Python library.
"""

from typing import List, Dict, Any, Optional, Union

import boto3
from botocore.exceptions import ClientError


class EMR:

    def __init__(self, verbose: Optional[bool]):
        self.emr_client = boto3.client('emr')
        self.verbose = verbose

    def start_cluster(self,
                      name: str,
                      log_uri: str,
                      keep_alive: bool,
                      protect: bool,
                      applications: List[str],
                      job_flow_role: str,
                      service_role: str,
                      emr_label: str,
                      instance_fleet: Optional[Dict[str, Any]],
                      instance_groups: Optional[Dict[str, Any]],
                      instance_fleet_configs: Optional[List[Dict[str, Any]]],
                      ebs_master_volume_gb: Optional[int],
                      ebs_core_volume_gb: Optional[int],
                      steps: List[Dict[str, Any]],
                      tags: List[str],
                      security_groups: Dict[str, Any],
                      subnets: Dict[str, Any],
                      configurations: List[Dict[str, Any]],
                      keyname: Optional[str],
                      bootstrap_scripts: List[Dict[str, Any]]) -> str:

        """
        Runs a job flow with the specified steps. A job flow creates a cluster of
        instances and adds steps to be run on the cluster. Steps added to the cluster
        are run as soon as the cluster is ready.

        :param instance_fleet_configs: instance fleet configurations.
        :param bootstrap_scripts: Bootstrap scripts array. Structure:
                    [{
                       'name': 'string',
                       'path': 'string',
                       'args': ['string']
                    }]
        :param instance_fleet Instance fleet definition. It is exclusive with instance_groups.
                    {
                      'master': {
                        'instance_fleet_name': 'string',
                        'TargetOnDemandCapacity': integer,
                        'TargetSpotCapacity': integer,
                        'on_demand_allocation_strategy': 'string'
                      },
                      'core': {
                        'instance_fleet_name': 'string',
                        'TargetOnDemandCapacity': integer,
                        'TargetSpotCapacity': integer,
                        'on_demand_allocation_strategy': 'string'
                      }
                    }
        :param instance_groups Instance group definition. It is exlcusive with instance_fleet.
                    {
                      'master': {
                        'BidPrice': float,
                        'Market': 'string',
                        'InstanceType': 'string',
                        'InstanceCount': integer
                      },
                      'core': {
                        'BidPrice': float,
                        'Market': 'string',
                        'InstanceType': 'string',
                        'InstanceCount': integer
                      }
                    }
        :param keyname: SSH key name to use (optional)
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
        :param steps: The job flow steps to add to the cluster. These are run in order
                      when the cluster is ready. Structure:

                {
                    'Name': 'string',
                    'Args': []
                }
        :param tags: Cluster tags
        :return: The ID of the newly created cluster.
        """

        instances = {
            'KeepJobFlowAliveWhenNoSteps': keep_alive,
            'TerminationProtected': protect,
            'Ec2SubnetIds': subnets,
            'EmrManagedMasterSecurityGroup': security_groups["EmrManagedMasterSecurityGroup"],
            'EmrManagedSlaveSecurityGroup': security_groups["EmrManagedSlaveSecurityGroup"]
        }
        if 'AdditionalMasterSecurityGroups' in security_groups:
            instances['AdditionalMasterSecurityGroups'] = security_groups['AdditionalMasterSecurityGroups']
        if 'AdditionalSlaveSecurityGroups' in security_groups:
            instances['AdditionalSlaveSecurityGroups'] = security_groups['AdditionalSlaveSecurityGroups']
        if 'ServiceAccessSecurityGroup' in security_groups:
            instances['ServiceAccessSecurityGroup'] = security_groups['ServiceAccessSecurityGroup']
        if keyname:
            instances['Ec2KeyName'] = keyname

        if instance_fleet and instance_groups:
            raise RuntimeError("instance_fleet and instance_groups cannot be defined at the same time")
        if instance_fleet and not instance_fleet_configs:
            raise RuntimeError("both instance_fleet and instance_fleet_configs must be defined")

        if instance_fleet:
            master_fleet = EMR._to_instance_fleet_boto('MASTER', instance_fleet['master'], ebs_master_volume_gb,
                                                       instance_fleet_configs)
            core_fleet = EMR._to_instance_fleet_boto('CORE', instance_fleet['core'], ebs_core_volume_gb,
                                                     instance_fleet_configs)
            instances['InstanceFleets'] = [master_fleet, core_fleet]
        elif instance_groups:
            master_group = EMR._to_instance_group_boto('MASTER', instance_groups['master'], ebs_master_volume_gb)
            core_group = EMR._to_instance_group_boto('CORE', instance_groups['core'], ebs_core_volume_gb)
            instances['InstanceGroups'] = [
                master_group, core_group
            ]

        try:
            response = self.emr_client.run_job_flow(
                Name=name,
                LogUri=log_uri,
                ReleaseLabel=emr_label,
                Instances=instances,
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
            self._vprint(f"Created cluster {cluster_id}")
        except ClientError:
            self._vprint("Couldn't create cluster.")
            raise
        else:
            return str(cluster_id)

    @staticmethod
    def _to_instance_fleet_boto(fleet_type: str, fleet: Dict[str, Any], ebs_volume_gb: Optional[int],
                                instance_fleet_configs) -> Dict[str, Any]:
        fleet_config = instance_fleet_configs[fleet['instance_fleet_name']]
        if ebs_volume_gb:
            fleet_config['EbsConfiguration'] = {
                "EbsBlockDeviceConfigs": [
                    {
                        "VolumeSpecification": {
                            "SizeInGB": ebs_volume_gb,
                            "VolumeType": "gp2"
                        },
                        "VolumesPerInstance": 1
                    }
                ]
            }
        fleet_boto = {
            'InstanceFleetType': fleet_type,
            'TargetOnDemandCapacity': fleet['TargetOnDemandCapacity'],
            'TargetSpotCapacity': fleet['TargetSpotCapacity'],
            'InstanceTypeConfigs': fleet_config
        }
        if 'on_demand_allocation_strategy' in fleet:
            fleet_boto['LaunchSpecifications'] = {
                'OnDemandSpecification': {
                    'AllocationStrategy': fleet['on_demand_allocation_strategy']
                }
            }
        return fleet_boto

    @staticmethod
    def _to_instance_group_boto(role: str, instance_group: Dict[str, Any], ebs_volume_gb: Optional[int]) \
            -> Dict[str, Any]:
        group_boto = {
            'Name': role,
            'Market': instance_group['Market'],
            'InstanceRole': role,
            'InstanceType': instance_group['InstanceType'],
            'InstanceCount': instance_group['InstanceCount']
        }
        if 'BidPrice' in instance_group:
            group_boto['BidPrice'] = instance_group['BidPrice']
        if ebs_volume_gb:
            group_boto['EbsConfiguration'] = {
                "EbsBlockDeviceConfigs": [
                    {
                        "VolumeSpecification": {
                            "SizeInGB": ebs_volume_gb,
                            "VolumeType": "gp2"
                        },
                        "VolumesPerInstance": 1
                    }
                ]
            }
        return group_boto

    def describe_cluster(self, cluster_id: str) -> Dict[str, Any]:
        """
        Gets detailed information about a cluster.

        :param cluster_id: The ID of the cluster to describe.
        :return: The retrieved cluster information.
        """
        try:
            response = self.emr_client.describe_cluster(ClusterId=cluster_id)
            cluster = response['Cluster']
            self._vprint(f'Got data for cluster "{cluster["Name"]}"')
        except ClientError:
            self._vprint(f"Couldn't get data for cluster {cluster_id}")
            raise
        else:
            return dict(cluster)

    def terminate_cluster(self, cluster_id: str) -> None:
        """
        Terminates a cluster. This terminates all instances in the cluster and cannot
        be undone. Any data not saved elsewhere, such as in an Amazon S3 bucket, is lost.

        :param cluster_id: The ID of the cluster to terminate.
        """
        try:
            self.emr_client.terminate_job_flows(JobFlowIds=[cluster_id])
            self._vprint(f"Terminated cluster {cluster_id}")
        except ClientError:
            self._vprint(f"Couldn't terminate cluster {cluster_id}")
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
            step_id = str(response['StepIds'][0])
            self._vprint(f"Started step {step_id}")
        except ClientError:
            self._vprint(f"Couldn't start step '{name}' with URI {args}")
            raise
        else:
            return step_id

    def add_spark_step(self, cluster_id: str, name: str, deploy_mode: str, master: str, application_uri: str,
                       jars: Union[List[str], str], pyfiles: Union[List[str], str], classname: Optional[str],
                       arguments: List[str]) -> str:
        """
        Adds a job step to the specified cluster.

        :param master: Application master
        :param deploy_mode: Deploy mode
        :param cluster_id: The ID of the cluster.
        :param name: The name of the step.
        :param application_uri: The URI of the JAR/Python application file
        :param jars: List of additional jars (can be empty)
        :param pyfiles: List of additional Python files (.zip, .egg, .py)
        :param classname: Class name (only if Java application is submitted)
        :param arguments: Arguments to pass to the application.
        :return: The ID of the newly added step.
        """
        jars_str = (','.join(jars) if isinstance(jars, List) else jars) if jars else ''
        pyfiles_str = (','.join(pyfiles) if isinstance(pyfiles, List) else pyfiles) if pyfiles else ''

        jars_arg = ['--jars', jars_str] if jars_str != '' else []
        pyfiles_arg = ['--py-files', pyfiles_str] if pyfiles_str != '' else []
        class_arg = ['--class', classname] if classname else []
        master_arg = ['--master', master] if master else []
        return self.add_step(
            cluster_id, name,
            ['spark-submit', '--deploy-mode', deploy_mode, *master_arg, *jars_arg, *pyfiles_arg, *class_arg,
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
            steps = dict(response['Steps'])
            self._vprint(f"Got {len(steps)} steps for cluster {cluster_id}")
        except ClientError:
            self._vprint(f"Couldn't get steps for cluster {cluster_id}")
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
            step: Dict[str, Any] = response['Step']
            self._vprint(f"Got data for step {step_id}")
        except ClientError:
            self._vprint(f"Couldn't get data for step {step_id}")
            raise
        else:
            return step

    def _vprint(self, msg: str) -> None:
        if self.verbose:
            print(msg)
