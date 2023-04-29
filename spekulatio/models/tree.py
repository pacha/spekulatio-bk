from pathlib import Path
from typing import Generator

from spekulatio import Model
from spekulatio.models import InputDir
from spekulatio.errors import SpekulatioInternalError
from .node import Node


class Tree(Model):
    input_index: dict[str, Node] = {}
    _root: Node

    @property
    def root(self):
        return self._root

    def from_input_dir(self, input_dir: InputDir):
        # attach root
        self.add_node(path=Path("."), input_dir=input_dir)

        # attach children
        for path in input_dir:
            self.add_node(path, input_dir)

    def setup(self):
        for node in self:
            node.setup()

    def build(self):
        for node in self:
            node.build()

    def add_node(self, path: Path, input_dir: InputDir):
        path_id = str(path)
        is_root_path = path_id == "."
        try:
            # get already existing node
            node = self.input_index[path_id]
            node.input_dirs.append(input_dir)
        except KeyError:
            # create node
            node = Node(
                input_path=path,
                input_dirs=[input_dir],
            )
            # add parent
            if is_root_path:
                self._root = node
                node.parent = None
            else:
                try:
                    parent_path_id = str(path.parent)
                    node.parent = self.input_index[parent_path_id]
                    node.parent.children.append(node)
                except KeyError:
                    raise SpekulatioInternalError(
                        f"Error while trying to attach path: { path_id }. "
                        "Parent hasn't been attached first."
                    )
            # add node to index
            self.input_index[path_id] = node
        return node

    def traverse_tree(cls, node) -> Generator[Node, None, None]:
        yield node
        for child in node.children:
            yield from cls.traverse_tree(child)

    def __len__(self):
        return len(self.input_index)

    def __iter__(self) -> Generator[Node, None, None]:  # type: ignore
        yield from self.traverse_tree(self._root)

    def __str__(self):
        return str(self._root)
