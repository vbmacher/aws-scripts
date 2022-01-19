import json
from pathlib import Path
from typing import List, Optional, Dict, Any

from awsscripts.sketches.ca import CodeArtifactSketchItem
from awsscripts.sketches.emr import EmrSketchItem
from awsscripts.sketches.mwaa import MWAASketchItem

sketch_items = {
    'emr': EmrSketchItem(),
    'codeartifact': CodeArtifactSketchItem(),
    'mwaa': MWAASketchItem()
}


class Sketches:
    """
    Sketches class. It manages sketch files and their content.
    """

    def __init__(self) -> None:
        self.home = Path.home() / '.aws-scripts' / 'sketches'
        self.home.mkdir(parents=True, exist_ok=True)

    def list(self) -> List[str]:
        """
        Lists available sketches
        :return: list of sketch names
        """
        return [p.stem for p in self.home.glob("*.json") if p != 'default']

    def get_default(self) -> Optional[str]:
        """
        Get default sketch name
        :return: default sketch name, None if any
        """
        default = (self.home / '.default.json')
        if default.exists():
            if default.is_symlink():
                return str(default.readlink().name.removesuffix('.json'))
            else:
                return str(default.name.removesuffix('.json'))
        else:
            return None

    def make_default(self, sketch: str) -> None:
        """
        Sets an sketch to become a default one
        :param sketch: sketch name
        :return: nothing
        """
        default = (self.home / '.default.json')
        if not default.exists() or default.is_symlink():
            self._create_sketch(sketch)
            default.unlink(missing_ok=True)
            default.symlink_to(self._get_sketch_path(sketch))
            print(f'"{sketch}" was set as default')
        else:
            print('Default sketch is not a symlink')

    def list_sketch_items(self, sketch: str) -> List[str]:
        sketch_content = self._load_content(sketch)
        return list(sketch_content)

    def add_sketch_item(self, sketch: str, sketch_item: str) -> None:
        """
        Add a sketch item to a sketch
        :param sketch: sketch name
        :param sketch_item: sketch item name
        :return: nothing
        """
        if sketch_item not in sketch_items:
            print(f'Unknown sketch item name. Available sketch items: {sketch_items.keys()}')
            return

        self._create_sketch(sketch)
        content = self._load_content(sketch)
        if sketch_item not in content:
            content[sketch_item] = sketch_items[sketch_item].generate()
            self._write_content(sketch, content)
            print(f'"{sketch_item}" sketch item has been added to file {self._get_sketch_path(sketch)}.\n'
                  'Please fill up missing values.')
        else:
            print(f'Could not add "{sketch_item}" sketch item to the sketch, because it already exists')

    def remove_sketch_item(self, sketch: str, sketch_item: str) -> None:
        """
        Removes a sketch item from a sketch (not an undoable action!). It does nothing if the name is not known.
        :param sketch: sketch name (must exist)
        :param sketch_item: sketch item name. The sketch item must exist directly in the sketch
         (not e.g. by inheritance)
        :return: nothing
        """
        if not self._exists(sketch):
            print(f'Sketch "{sketch}" does not exist')
            return
        if sketch_item not in sketch_items:
            print(f'Unknown sketch item. Available sketch items: {sketch_items.keys()}')
            return
        content = self._load_content(sketch)
        if sketch_item not in content:
            print(f'Could not remove "{sketch_item}" sketch item from the sketch, because it does not exist')
        else:
            content.pop(sketch_item, None)
            self._write_content(sketch, content)
            print(f'"{sketch_item}" sketch item has been removed from file {self._get_sketch_path(sketch)}')

    def replace_sketch_item(self, sketch: str, sketch_item: str, content: Dict[str, Any]) -> None:
        """
        Replaces a sketch item with new content.

        :param sketch: sketch name
        :param sketch_item: sketch item name
        :param content: new sketch item content
        :return: nothing
        """
        if sketch_item not in sketch_items:
            print(f'Unknown sketch item name. Available sketch items: {sketch_items.keys()}')
            return

        self._create_sketch(sketch)
        sketch_content = self._load_content(sketch)
        sketch_content[sketch_item] = content
        self._write_content(sketch, sketch_content)
        print(f'"{sketch_item}" sketch item has been updated in file {self._get_sketch_path(sketch)}.')

    def __getitem__(self, key: str) -> Dict[str, Any]:
        return self._load_content(key, interpret=True)

    def _load_content(self, sketch: str, interpret=False) -> Dict[str, Any]:
        with self._get_sketch_path(sketch).open() as f:
            raw_content = f.read()
            if not raw_content:
                return {}
            content: Dict[str, Any] = json.loads(raw_content)
            if interpret:
                return self._interpret_content(content)
            else:
                return content

    def _write_content(self, sketch: str, content: Dict[str, Any]) -> None:
        with self._get_sketch_path(sketch).open('w') as f:
            json.dump(content, f, indent=2)

    def _exists(self, sketch: str) -> bool:
        return self._get_sketch_path(sketch).exists()

    def _create_sketch(self, sketch: str) -> None:
        if not self._exists(sketch):
            self._get_sketch_path(sketch).touch()

    def _get_sketch_path(self, sketch: str) -> Path:
        filename = sketch if sketch.endswith('.json') else sketch + '.json'
        return self.home / filename

    def _interpret_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Interprets special keys in JSON content:
          {
            "include": "str" or ["str", ...]     <-- read content from another sketch(es) and use it as a "base"
          }
        :param content: JSON content
        :return: interpreted content
        """
        result: Dict[str, Any] = {}
        if "include" in content:
            to_include = content["include"]
            if type(to_include) is list:
                for sketch in to_include:
                    result = {**result, **self._load_content(sketch)}
            else:
                result = {**result, **self._load_content(to_include)}
        return {**result, **content}
