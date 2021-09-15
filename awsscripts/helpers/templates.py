from awsscripts.helpers.emr import EMR

templates = {
    'emr': {
        'job_flow_role': 'EMR_EC2_DefaultRole',
        'service_role': 'EMR_DefaultRole',
        'security_groups': {
            'AdditionalSlaveSecurityGroups': [
                # TODO
            ],
            'EmrManagedSlaveSecurityGroup': 'TODO',
            'EmrManagedMasterSecurityGroup': 'TODO',
            'AdditionalMasterSecurityGroups': [
                # TODO
            ]
        },
        'subnets': [
            # TODO
        ],
        'keyname': 'TODO',
        'tags': [
            {
                'Key': 'TODO',
                'Value': 'TODO'
            }
        ],
        'log_uri': 'TODO',
        'bootstrap_scripts': {
            # TODO
        }
    },
    'codeartifact': {
        'repository': 'TODO',
        'domain': 'TODO',
        'domain-owner': 'TODO'
    }
}


class Template:

    @staticmethod
    def configure_emr_from_cluster(cluster_id: str):
        emr = EMR(verbose=True)
        cluster = emr.describe_cluster(cluster_id)
        ec2 = cluster['Ec2InstanceAttributes']

        subnets = ec2['RequestedEc2SubnetIds'] if ec2['RequestedEc2SubnetIds'] else [ec2['Ec2SubnetId']]
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

        result = {
            'job_flow_role': ec2['IamInstanceProfile'],
            'service_role': 'EMR_DefaultRole',
            'security_groups': security_groups,
            'subnets': subnets,
            'tags': cluster['Tags'],
            'log_uri': cluster['LogUri'],
            'bootstrap_scripts': {
                # TODO
            }
        }
        if 'Ec2KeyName' in ec2:
            result['keyname'] = ec2['Ec2KeyName']
        return result
