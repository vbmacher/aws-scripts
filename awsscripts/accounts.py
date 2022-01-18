"""
AWS Accounts helper class
"""
import json
from pathlib import Path
from typing import List, Optional, Dict, Any

from templates.codeartifact_template import CodeArtifactTemplate
from templates.emr_template import EmrTemplate

templates = {
    'emr': EmrTemplate(),
    'codeartifact': CodeArtifactTemplate()
}


class Accounts:

    def __init__(self) -> None:
        self.home = Path.home() / '.aws-scripts' / 'accounts'
        self.home.mkdir(parents=True, exist_ok=True)

    def list(self) -> List[str]:
        """
        Lists available accounts
        :return: list of account names
        """
        return [p.stem for p in self.home.glob("*.json") if p != 'default']

    def get_default_account(self) -> Optional[str]:
        """
        Get default account name
        :return: default account name, None if any
        """
        default = (self.home / '.default.json')
        if default.exists():
            if default.is_symlink():
                return str(default.readlink().name.removesuffix('.json'))
            else:
                return str(default.name.removesuffix('.json'))
        else:
            return None

    def make_default(self, account: str) -> None:
        """
        Sets an account to become a default one
        :param account: account name
        :return: nothing
        """
        default = (self.home / '.default.json')
        if not default.exists() or default.is_symlink():
            self._create_account(account)
            default.unlink(missing_ok=True)
            default.symlink_to(self._get_account_path(account))
            print(f'"{account}" was set as default')
        else:
            print('Default account is not a symlink')

    def add_template(self, account: str, template_name: str) -> None:
        """
        Adds an template to the account
        :param account:
        :param template_name:
        :return:
        """
        if template_name not in templates:
            print(f'Unknown template name. Available templates: {templates.keys()}')
            return

        self._create_account(account)
        content = self._load_content(account)
        if template_name not in content:
            content[template_name] = templates[template_name].generate()
            self._write_content(account, content)
            print(f'"{template_name}" template has been added to file {self._get_account_path(account)}.\n'
                  'Please fill up missing values.')
        else:
            print(f'Could not add "{template_name}" template to the account, because it already exists')

    def remove_template(self, account: str, template_name: str) -> None:
        """
        Removes a key (template name) from given account (not an undoable action!). It ignores key which is
        not a known template name.
        :param account: account name (must exist)
        :param template_name: template name (key). The key must exist directly in the account
        :return: nothing
        """
        if not self._exists(account):
            print(f'Account "{account}" does not exist')
            return
        if template_name not in templates:
            print(f'Unknown template name. Available templates: {templates.keys()}')
            return
        content = self._load_content(account)
        if template_name not in content:
            print(f'Could not remove "{template_name}" template from the account, because it does not exist')
        else:
            content.pop(template_name, None)
            self._write_content(account, content)
            print(f'"{template_name}" template has been removed from file {self._get_account_path(account)}')

    def replace_template(self, account: str, template_name: str, template_content: Dict[str, Any]) -> None:
        """
        Replaces a template with given content.

        :param account: account name
        :param template_name: template name
        :param template_content: template content
        :return: nothing
        """
        if template_name not in templates:
            print(f'Unknown template name. Available templates: {templates.keys()}')
            return

        self._create_account(account)
        content = self._load_content(account)
        content[template_name] = template_content
        self._write_content(account, content)
        print(f'"{template_name}" template was updated in file {self._get_account_path(account)}.')

    def __getitem__(self, key: str) -> Dict[str, Any]:
        return self._load_content(key, interpret=True)

    def _load_content(self, account: str, interpret=False) -> Dict[str, Any]:
        with self._get_account_path(account).open() as f:
            raw_content = f.read()
            if not raw_content:
                return {}
            content: Dict[str, Any] = json.loads(raw_content)
            if interpret:
                return self._interpret_content(content)
            else:
                return content

    def _write_content(self, account: str, content: Dict[str, Any]) -> None:
        with self._get_account_path(account).open('w') as f:
            json.dump(content, f, indent=2)

    def _exists(self, account: str) -> bool:
        return self._get_account_path(account).exists()

    def _create_account(self, account: str) -> None:
        if not self._exists(account):
            self._get_account_path(account).touch()

    def _get_account_path(self, account: str) -> Path:
        filename = account if account.endswith('.json') else account + '.json'
        return self.home / filename

    def _interpret_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Interprets special keys in JSON content:
          {
            "include": "str" or ["str", ...]     <-- read content from another account(s) and use it as a "base"
          }
        :param content: JSON content
        :return: interpreted content
        """
        result: Dict[str, Any] = {}
        if "include" in content:
            to_include = content["include"]
            if type(to_include) is list:
                for account in to_include:
                    result = {**result, **self._load_content(account)}
            else:
                result = {**result, **self._load_content(to_include)}
        return {**result, **content}
