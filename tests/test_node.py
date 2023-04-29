from pathlib import Path

from spekulatio.models import Node
from spekulatio.models import InputDir


def test_no_action(fixtures_path):
    input_dir = InputDir(root_path=fixtures_path, path="empty-input-dir")
    node = Node(
        input_path=Path("foo/bar.md"),
        input_dirs=[input_dir],
    )
    assert not node.action


def test_action(fixtures_path):
    input_dir = InputDir(
        root_path=fixtures_path,
        **{
            "path": "empty-input-dir",
            "transformations": [
                {
                    "pattern": {
                        "type": "glob",
                        "scope": "filename",
                        "value": "*.md",
                    },
                    "action": {
                        "name": "debug",
                    },
                    "output_name_template": "{{ input_path.stem }}.html",
                }
            ],
        }
    )
    node_md = Node(
        input_path=Path("foo/bar.md"),
        input_dirs=[input_dir],
    )
    assert node_md.action.name == "debug"

    node_txt = Node(
        input_path=Path("foo/bar.txt"),
        input_dirs=[input_dir],
    )
    assert not node_txt.action


def test_default_output_name(fixtures_path):
    input_dir = InputDir(root_path=fixtures_path, path="empty-input-dir")
    node = Node(
        input_path=Path("foo/bar.md"),
        input_dirs=[input_dir],
    )
    assert node.output_name == "bar.md"


def test_output_name(fixtures_path):
    # create input dir
    input_dir = InputDir(
        root_path=fixtures_path,
        **{
            "path": "empty-input-dir",
            "transformations": [
                {
                    "pattern": {
                        "type": "glob",
                        "scope": "filename",
                        "value": "*.md",
                    },
                    "action": {
                        "name": "debug",
                    },
                    "output_name_template": "{{ input_path.stem }}.html",
                }
            ],
        }
    )
    # create node
    input_path = Path("foo/bar.md")
    node = Node(
        input_path=input_path,
        input_dirs=[input_dir],
    )
    node._local_data = {"input_path": input_path}

    assert node.output_name == "bar.html"


def test_output_path(fixtures_path):
    input_dir = InputDir(root_path=fixtures_path, path="empty-input-dir")
    root_node = Node(
        input_path=Path("."),
        input_dirs=[input_dir],
    )
    node1 = Node(
        input_path=Path("dir1"),
        input_dirs=[input_dir],
        parent=root_node,
    )
    node2 = Node(
        input_path=Path("foo.txt"),
        input_dirs=[input_dir],
        parent=node1,
    )
    assert node1.output_path == Path("dir1")
    assert node2.output_path == Path("dir1/foo.txt")


def test_output_path(fixtures_path):
    input_dir = InputDir(
        root_path=fixtures_path,
        **{
            "path": "empty-input-dir",
            "transformations": [
                {
                    "pattern": {
                        "type": "glob",
                        "scope": "filename",
                        "value": "*.md",
                    },
                    "action": {
                        "name": "debug",
                    },
                    "output_name_template": "{{ input_path.stem }}.html",
                }
            ],
        }
    )
    root_node = Node(
        input_path=Path("."),
        input_dirs=[input_dir],
    )
    node1 = Node(
        input_path=Path("dir1"),
        input_dirs=[input_dir],
        parent=root_node,
    )
    node1._local_data = {"var1": "a_dir", "_output_name_template": "{{ var1 }}"}
    node2_input_path = Path("foo.md")
    node2 = Node(
        input_path=node2_input_path,
        input_dirs=[input_dir],
        parent=node1,
    )
    node2._local_data = {"input_path": node2_input_path}
    assert node1.output_path == Path("a_dir")
    assert node2.output_path == Path("a_dir/foo.html")
    assert node2.output_id == "a_dir/foo.html"
