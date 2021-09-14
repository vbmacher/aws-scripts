"""
AWS Accounts helper class
"""
import json
from pathlib import Path

templates = {
    'emr': {
        'job_flow_role': 'EMR_EC2_DefaultRole',
        'service_role': 'EMR_DefaultRole',
        'region': 'TODO',
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


class Accounts:

    def __init__(self):
        self.home = Path.home() / '.aws-scripts' / 'accounts'
        self.home.mkdir(parents=True, exist_ok=True)

    def list(self):
        return [p.stem for p in self.home.glob("*.json") if p != 'default']

    def get_default_account(self):
        default = (self.home / '.default.json')
        if default.exists():
            if default.is_symlink():
                return default.readlink().name.removesuffix('.json')
            else:
                return default.name.removesuffix('.json')
        else:
            return None

    def make_default(self, account):
        default = (self.home / '.default.json')
        if not default.exists() or default.is_symlink():
            self._create_account(account)
            default.unlink(missing_ok=True)
            default.symlink_to(self._get_account_path(account))
            print(f'"{account}" was set as default')
        else:
            print('Default account is not a symlink')

    def add_template(self, account, template_name):
        if template_name not in templates:
            print(f'Unknown template name. Available templates: {templates.keys()}')
            return

        self._create_account(account)
        content = self._load_content(account)
        if template_name not in content:
            content[template_name] = templates[template_name]
            self._write_content(account, content)
            print(f'"{template_name}" template has been added to file {self._get_account_path(account)}.'
                  'Please fill up missing values.')
        else:
            print(f'Could not add "{template_name}" template to the account, because it already exists')

    def remove_template(self, account, template_name):
        if not self._exists(account):
            print(f'Account "{account}" does not exist')
            return
        content = self._load_content(account)
        if template_name not in content:
            print(f'Could not remove "{template_name}" template from the account, because it does not exist')
        else:
            content.pop(template_name, None)
            self._write_content(account, content)
            print(f'"{template_name}" template has been removed from file {self._get_account_path(account)}')

    def __getitem__(self, key):
        return self._load_content(key)

    def _load_content(self, account):
        with self._get_account_path(account).open() as f:
            raw_content = f.read()
            if not raw_content:
                return {}
            return json.loads(raw_content)

    def _write_content(self, account, content):
        with self._get_account_path(account).open('w') as f:
            json.dump(content, f, indent=2)

    def _exists(self, account):
        return self._get_account_path(account).exists()

    def _create_account(self, account):
        if not self._exists(account):
            self._get_account_path(account).touch()

    def _get_account_path(self, account):
        filename = account if account.endswith('.json') else account + '.json'
        return self.home / filename
