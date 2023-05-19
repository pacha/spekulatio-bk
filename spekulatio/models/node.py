from pathlib import Path
from typing import Optional

from jinja2 import Template
from pydantic import validator

from spekulatio import Model
from .input_dir import InputDir
from .attribute_file import AttributeFile
from .transformation import Transformation


class Node(Model):
    # path information
    input_path: Path
    input_dirs: list[InputDir]

    # relationships
    parent: Optional["Node"] = None
    prev_sibling: Optional["Node"] = None
    next_sibling: Optional["Node"] = None
    children: list["Node"] = []

    # memoized attributes
    _transformation: Optional[Transformation] = None
    _output_name: Optional[str] = None
    _output_path: Optional[Path] = None

    # data
    _descendants_data: dict = {}
    _children_data: dict = {}
    _local_data: dict = {}
    _data: Optional[dict] = None

    @validator("input_dirs")
    def check_input_dirs(cls, value):
        if len(value) == 0:
            raise ValueError("Can't create node without at least one input root")
        return value

    @property
    def data(self) -> dict:
        if self._data is None:
            data = {}
            data.update(self._descendants_data)
            data.update(self._children_data)
            data.update(self._local_data)
            self._data = data
        return self._data

    @property
    def depth(self) -> int:
        return len(self.input_path.parts)

    @property
    def transformation(self):
        if not self._transformation:
            input_dir = self.input_dirs[-1]
            self._transformation = input_dir.get_transformation(self.input_path)
        return self._transformation

    @property
    def action(self):
        try:
            return self.transformation.action
        except AttributeError:
            # return none if there's no transformation for this file
            return None

    @property
    def input_id(self) -> str:
        return str(self.input_path)

    @property
    def input_name(self) -> str:
        return self.input_path.name or "."

    @property
    def output_name(self) -> str:
        if self._output_name:
            return self._output_name
        elif "_output_name_template" in self.data:
            template = Template(self.data["_output_name_template"])
            self._output_name = template.render(**self.data)
        elif self.transformation:
            template = Template(self.transformation.output_name_template)
            self._output_name = template.render(**self.data)
        else:
            self._output_name = self.input_name
        return self._output_name

    @property
    def output_path(self) -> Path:
        if not self.parent:
            return Path(".")
        return self.parent.output_path / self.output_name

    @property
    def output_id(self) -> str:
        return str(self.output_path)

    def get_full_input_path(self, input_dir):
        return input_dir.absolute_path / self.input_path

    def get_full_output_path(self, output_dir):
        return output_dir.absolute_path / self.output_path

    def setup(self):
        self.set_data()
        self.sort_children()
        self.set_relationships()

    def set_data(self):
        # set data from parent
        if self.parent:
            self._descendants_data.update(self.parent._descendants_data)
            self._local_data.update(self.parent._children_data)
        # set data from overriden paths
        for input_dir in self.input_dirs:
            full_input_path = self.get_full_input_path(input_dir)
            attribute_set = AttributeFile(path=full_input_path)
            attribute_set.update(
                descendants_data=self._descendants_data,
                children_data=self._children_data,
                local_data=self._local_data,
            )

    def sort_children(self):
        print(f"setup [sort_children]:\n{self}")

    def set_relationships(self):
        print(f"setup [set_relationships]:\n{self}")

    def build(self):
        print(f"build:\n{self}")

    def __eq__(self, other) -> bool:
        return self.input_id == other.input_id

    def __str__(self) -> str:
        return f"|{self.depth * '--'}in : {self.input_name}\n|{self.depth * '  '}out: {self.output_name}"
