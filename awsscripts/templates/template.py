from typing import Any, Dict, List, Optional


class Template:
    """
    AWS service template
    """

    def __init__(self):
        self.content = {}

    def content(self) -> Dict[str, Any]:
        return self.content

    def contains(self, key: str) -> bool:
        return key in self.content

    def _get(self, key: str) -> Optional[Any]:
        return self[key] if key in self else None

    def put(self, key: str, value: Any) -> None:
        self.content += {
            key: value
        }

    def _put_in_list(self, list_name: str, value: Any):
        self.content.setdefault(list_name, []).append(value)

    def _has_in_list_dict(self, list_name: str, dict_key: str, key: str):
        if list_name in self.content:
            return len(list(filter(lambda b: b[dict_key] == key, self[list_name]))) > 0
        return False

    def _has_in_list(self, list_name: str, key: str):
        if list_name in self.content:
            return len(list(filter(lambda s: s == key, self[list_name]))) > 0
        return False

    def _get_in_list_dict(self, list_name: str, dict_key: str, key: str):
        if self._has_in_list_dict(list_name, dict_key, key):
            return list(filter(lambda c: c[dict_key] == key, self[list_name]))[0]
        else:
            return None

    def _get_list_dict(self, list_name: str) -> List[Dict[str, Any]]:
        return self[list_name] if self.contains(list_name) else []

    def _get_list(self, list_name: str) -> List[str]:
        return self[list_name] if self.contains(list_name) else []

    def _remove_in_list(self, list_name: str, key: str):
        self[list_name] = list(filter(lambda k: k != key, self[list_name]))

    def _remove_in_list_dict(self, list_name: str, dict_key: str, key: str):
        if self._has_in_list_dict(list_name, dict_key, key):
            self[list_name] = list(filter(lambda c: c[dict_key] != key, self[list_name]))

    def generate(self) -> Dict[str, Any]:
        """
        Generate AWS service template (a dictionary)
        :return: template content
        """
        return self.content

    def __getitem__(self, key: str) -> Any:
        return self.content[key]

    def __setitem__(self, key, value):
        self.content[key] = value
