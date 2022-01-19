from typing import Dict, Any, Optional, List

from awsscripts.ec2.ec2 import ec2_instances
from awsscripts.emr.emr import EMR
from awsscripts.sketches.sketchitem import SketchItem


class EmrSketchItem(SketchItem):

    def has_configuration(self, name: str) -> bool:
        """
        Determines if a configuration (with given classification name) exists.
        :param name: classification name
        :return: true if the configuration exists; false otherwise
        """
        return self._has_in_list_dict('configurations', 'Classification', name)

    def get_configuration(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Gets configuration by classification name
        :param name: classification name
        :return: configuration if exists; None otherwise
        """
        return self._get_in_list_dict('configurations', 'Classification', name)

    def get_configurations(self) -> List[Dict[str, Any]]:
        """
        Get all defined configurations
        :return: all defined configurations
        """
        return self._get_list_dict('configurations')

    def remove_configuration(self, name: str) -> None:
        """
        Removes configuration if exists.
        :param name: classification name
        :return: nothing
        """
        self._remove_in_list_dict('configurations', 'Classification', name)

    def put_configuration(self, name: str, properties: Dict[str, Any]) -> None:
        """
        Adds or replaces configuration.
        :param name: classification name
        :param properties: properties
        :return: nothing
        """
        self._remove_in_list_dict('configurations', 'Classification', name)
        self._put_in_list('configurations', {
            'Classification': name,
            'Properties': properties
        })

    def put_configurations(self, configurations: List[Dict[str, Any]]) -> None:
        """
        Add/replace one or more configuration (raw)
        :param configurations: raw configurations
        :return: nothing
        """
        names = map(lambda c: c['Classification'], configurations)
        for name in names:
            self.remove_configuration(name)
        for config in configurations:
            self.put_configuration(config['Classification'], config['Properties'])

    def has_bootstrap_script(self, name: str) -> bool:
        return self._has_in_list_dict('bootstrap_scripts', 'name', name)

    def remove_bootstrap_script(self, name: str) -> None:
        self._remove_in_list_dict('bootstrap_scripts', 'name', name)

    def put_bootstrap_script(self, name: str, path: str, args: List[str]) -> None:
        self._put_in_list('bootstrap_scripts', {
            'name': name,
            'path': path,
            'args': args
        })

    def get_bootstrap_scripts(self) -> List[Dict[str, Any]]:
        return self._get_list_dict('bootstrap_scripts')

    def get_bootstrap_script(self, name: str) -> Dict[str, Any]:
        return self._get_in_list_dict('bootstrap_scripts', 'name', name)

    def set_log_uri(self, log_uri: str) -> None:
        self['log_uri'] = log_uri

    def get_log_uri(self) -> str:
        return self._get('log_uri')

    def has_subnet(self, subnet: str) -> bool:
        return self._has_in_list('subnets', subnet)

    def remove_subnet(self, subnet: str) -> None:
        self._remove_in_list('subnets', subnet)

    def put_subnet(self, subnet: str) -> None:
        self.remove_subnet(subnet)
        self._put_in_list('subnets', subnet)

    def get_subnets(self) -> List[str]:
        return self._get_list('subnets')

    def put_security_groups(self, sg: Dict[str, Any]) -> None:
        self['security_groups'] = sg

    def get_security_groups(self) -> Dict[str, Any]:
        return self['security_groups'] if 'security_groups' in self else {
            'AdditionalSlaveSecurityGroups': [],
            'EmrManagedSlaveSecurityGroup': 'TODO',
            'EmrManagedMasterSecurityGroup': 'TODO',
            'AdditionalMasterSecurityGroups': []
        }

    def set_job_flow_role(self, job_flow_role: str) -> None:
        self['job_flow_role'] = job_flow_role

    def get_job_flow_role(self) -> str:
        return self['job_flow_role'] if 'job_flow_role' in self else 'IamInstanceProfile'

    def set_service_role(self, job_flow_role: str) -> None:
        self['service_role'] = job_flow_role

    def get_service_role(self) -> str:
        return self['service_role'] if 'service_role' in self else 'EMR_DefaultRole'

    def set_keyname(self, keyname: str) -> None:
        self['keyname'] = keyname

    def get_keyname(self) -> str:
        return self._get('keyname')

    def put_tags(self, tags: List[Dict[str, str]]) -> None:
        names = map(lambda t: t['Key'], tags)
        for name in names:
            self._remove_in_list_dict('tags', 'Key', name)
        for tag in tags:
            self._put_in_list('tags', tag)

    def get_tags(self) -> List[Dict[str, str]]:
        return self._get_list_dict('tags')

    def put_instance_fleet(self, name: str, master_capacity: int, core_capacity: int, spot: bool):
        self['instance_fleet'] = {
            'master': {
                'instance_fleet_name': name,
                'TargetOnDemandCapacity': master_capacity,
                'TargetSpotCapacity': 0,
                'on_demand_allocation_strategy': 'LOWEST_PRICE'
            },
            'core': {
                'instance_fleet_name': name,
                'TargetOnDemandCapacity': core_capacity if not spot else 0,
                'TargetSpotCapacity': core_capacity if spot else 0,
                'on_demand_allocation_strategy': 'LOWEST_PRICE'
            }
        }

    def get_instance_fleet(self):
        return self._get('instance_fleet')

    def get_instance_fleets(self):
        return self._get('instance_fleets')

    def put_instance_groups(self, master_instance: str, core_instance: str, count: int, spot: bool):
        self['instance_groups'] = {
            'master': {
                'Market': 'ON_DEMAND',
                'InstanceType': master_instance,
                'InstanceCount': 1
            },
            'core': {
                'Market': 'ON_DEMAND' if not spot else 'SPOT',
                'InstanceType': core_instance,
                'InstanceCount': count
            }
        }

    def get_instance_groups(self):
        return self._get('instance_groups')

    def set_emr_label(self, emr: str):
        self['emr_label'] = emr

    def get_emr_label(self) -> Optional[str]:
        return self._get('emr_label')

    def set_cluster_name(self, name: str):
        self['cluster_name'] = name

    def get_cluster_name(self) -> Optional[str]:
        return self._get('cluster_name')

    def set_applications(self, applications: List[str]):
        self['applications'] = applications

    def get_applications(self) -> Optional[List[str]]:
        return self._get('applications')

    def set_protect(self, protect: bool):
        self['TerminationProtected'] = protect

    def get_protect(self) -> Optional[bool]:
        return self._get('TerminationProtected')

    def set_master_size_gb(self, size: int) -> None:
        self['master_size_gb'] = size

    def get_master_size_gb(self) -> Optional[int]:
        return self._get('master_size_gb')

    def set_core_size_gb(self, size: int) -> None:
        self['core_size_gb'] = size

    def get_core_size_gb(self) -> Optional[int]:
        return self._get('core_size_gb')

    def generate(self):
        return self.content() + {
            'job_flow_role': self.get_job_flow_role(),
            'service_role': self.get_service_role(),
            'security_groups': self.get_security_groups(),
            'instance_fleets': EmrSketchItem._generate_instance_fleets()
        }

    @staticmethod
    def _generate_instance_fleets():
        result = {}
        for instance, values in ec2_instances.items():
            name = 'mem/cpu=' + str(round(values['memory'] / values['cpu'], 2))
            weight = int(max(values['cpu'] / 4, values['memory'] / 32))
            if weight > 0:
                value = {
                    'InstanceType': instance,
                    'WeightedCapacity': weight
                }
                if values['storage'] > 0:
                    result.setdefault('ssd;' + name, []).append(value)
                else:
                    result.setdefault('ebs;' + name, []).append(value)
                result.setdefault(name, []).append(value)
        return result

    @staticmethod
    def from_cluster(cluster_id: str):
        emr_item = EmrSketchItem()
        emr = EMR(verbose=False)
        cluster = emr.describe_cluster(cluster_id)
        ec2 = cluster['Ec2InstanceAttributes']

        for b in cluster['BootstrapActions']:
            emr_item.put_bootstrap_script(b['Name'], b['ScriptPath'], b['Args'])

        subnets = ec2['RequestedEc2SubnetIds'] if ec2['RequestedEc2SubnetIds'] else [ec2['Ec2SubnetId']]
        for subnet in subnets:
            emr_item.put_subnet(subnet)

        security_groups = {
            'EmrManagedMasterSecurityGroup': ec2['EmrManagedMasterSecurityGroup'],
            'EmrManagedSlaveSecurityGroup': ec2['EmrManagedSlaveSecurityGroup'],
        }
        if 'AdditionalMasterSecurityGroups' in ec2:
            security_groups['AdditionalMasterSecurityGroups'] = ec2['AdditionalMasterSecurityGroups']
        if 'AdditionalSlaveSecurityGroups' in ec2:
            security_groups['AdditionalSlaveSecurityGroups'] = ec2['AdditionalSlaveSecurityGroups']
        if 'ServiceAccessSecurityGroup' in ec2:
            security_groups['ServiceAccessSecurityGroup'] = ec2['ServiceAccessSecurityGroup']
        emr_item.put_security_groups(security_groups)

        emr_item.set_job_flow_role(ec2['IamInstanceProfile'])
        # template.set_service_role(???)
        emr_item.set_log_uri(cluster['LogUri'])
        emr_item.put_configurations(cluster['Configurations'])
        emr_item.put_tags(cluster['Tags'])

        if 'Ec2KeyName' in ec2:
            emr_item.set_keyname(ec2['Ec2KeyName'])
        return emr_item

    @staticmethod
    def from_content(content: Dict[str, Any]):
        emr_item = EmrSketchItem()
        emr_item.content = content
        return emr_item
