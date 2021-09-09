aws_accounts = {
    'your_account': {
        'emr': {
            "job_flow_role": "EMR_EC2_DefaultRole",
            "service_role": "EMR_DefaultRole",
            "region": "TODO",
            "security_groups": {
                "AdditionalSlaveSecurityGroups": [
                    # TODO
                ],
                "EmrManagedSlaveSecurityGroup": "TODO",
                "EmrManagedMasterSecurityGroup": "TODO",
                "AdditionalMasterSecurityGroups": [
                    # TODO
                ]
            },
            "subnets": [
                # TODO
            ],
            "keyname": "TODO",
            "tags": [
                {
                    "Key": "TODO",
                    "Value": "TODO"
                }
            ],
            "log_uri": "TODO",
            "bootstrap_scripts": {
                # TODO
            }
        },
        'codeartifact': {
            # TODO
        }
    }
}

default_aws_account = 'your_account'
