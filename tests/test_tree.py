from pathlib import Path

import pytest

from spekulatio.models import Tree
from spekulatio.models import InputDir
from spekulatio.errors import SpekulatioInternalError


def test_root_node_attachment(fixtures_path):
    input_dir = InputDir(root_path=fixtures_path, path="empty-input-dir")
    tree = Tree()
    tree.add_node(path=Path("."), input_dir=input_dir)
    assert len(tree) == 1


def test_wrong_root_node_attachment(fixtures_path):
    input_dir = InputDir(root_path=fixtures_path, path="empty-input-dir")
    tree = Tree()
    with pytest.raises(SpekulatioInternalError):
        tree.add_node(path=Path("bar/foo.txt"), input_dir=input_dir)


def test_parent_child_relationship(fixtures_path):
    input_dir = InputDir(root_path=fixtures_path, path="empty-input-dir")
    tree = Tree()
    root = tree.add_node(path=Path("."), input_dir=input_dir)
    dir1 = tree.add_node(path=Path("dir1"), input_dir=input_dir)
    file1 = tree.add_node(path=Path("dir1/file1.txt"), input_dir=input_dir)
    dir2 = tree.add_node(path=Path("dir1/dir2"), input_dir=input_dir)
    file2 = tree.add_node(path=Path("dir1/dir2/file2.txt"), input_dir=input_dir)
    file3 = tree.add_node(path=Path("file3.txt"), input_dir=input_dir)

    assert root.parent is None
    assert dir1.parent == root
    assert dir1 in root.children
    assert dir2.parent == dir1
    assert dir2 in dir1.children
    assert file3.parent == root

    assert len(root.children) == 2
    assert len(dir1.children) == 2
    assert len(dir2.children) == 1
    assert len(file1.children) == 0
    assert len(file2.children) == 0
    assert len(file3.children) == 0

    assert len(tree) == 6

    expected_ids = {
        ".",
        "dir1",
        "dir1/file1.txt",
        "dir1/dir2",
        "dir1/dir2/file2.txt",
        "file3.txt",
    }
    actual_ids = set(tree.input_index.keys())
    assert expected_ids == actual_ids


def test_from_input_dir(fixtures_path):
    input_dir = InputDir(root_path=fixtures_path, path="traversal-input-dir")
    tree = Tree()
    tree.from_input_dir(input_dir=input_dir)

    expected_ids = {
        ".",
        "dir1",
        "dir1/dir3",
        "dir1/dir3/file4.md",
        "dir1/file3.md",
        "dir2",
        "dir2/file5.md",
        "file1.md",
        "file2.md",
    }
    actual_ids = set(tree.input_index.keys())
    assert expected_ids == actual_ids
    # tree.setup()
    # tree.build()
