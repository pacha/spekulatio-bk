from pathlib import Path

from pydantic import root_validator

from spekulatio import Model
from spekulatio.models import Attribute
from spekulatio.lib.get_dict import get_dict_from_json
from spekulatio.lib.get_dict import get_dict_from_yaml
from spekulatio.lib.get_dict import get_dict_from_python
from spekulatio.lib.get_dict import get_dict_from_executable
from spekulatio.lib.get_dict import get_dict_from_frontmatter

values_files = {
    "{prefix}_values.yaml": get_dict_from_yaml,
    "{prefix}_values.yml": get_dict_from_yaml,
    "{prefix}_values.json": get_dict_from_json,
    "{prefix}_values.py": get_dict_from_python,
    "{prefix}_values": get_dict_from_executable,
}


class AttributeFile(Model):
    path: Path
    has_frontmatter: bool = False
    attributes: list[Attribute] = []
    _index: dict = {}

    @root_validator
    def check_no_frontmatter_in_dirs(cls, items):
        path = items["path"]
        has_frontmatter = items["has_frontmatter"]
        if path.is_dir() and has_frontmatter:
            raise ValueError(f"Can't read the frontmatter of a directory ({path})")
        return items

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        prefix = "" if self.path.is_dir() else self.path.name
        attributes_dict = {}

        # get values from a values file (if any)
        for filename_template, function in values_files.items():
            filename = filename_template.format(prefix=prefix)
            values_path = self.path / filename
            if values_path.exists():
                attributes_dict.update(function(values_path))
                break

        # get attributes from frontmatter
        if self.has_frontmatter:
            attributes_dict.update(get_dict_from_frontmatter(self.path))

        # set value objects
        for key, value in attributes_dict.items():
            attribute = Attribute(name=key, value=value)
            self.attributes.append(attribute)
            self._index[key] = attribute
