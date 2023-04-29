from spekulatio.models import AttributeFile


def test_attribute_file_dir_yaml(fixtures_path):
    path = fixtures_path / "attribute-file" / "dirs" / "dir1"
    attribute_file = AttributeFile(path=path)

    assert len(attribute_file.attributes) == 1
    assert len(attribute_file._index) == 1
    assert attribute_file._index["foo"].name == "foo"
    assert attribute_file._index["foo"].value == 3
    assert attribute_file._index["foo"].scope == "descendants"
    assert attribute_file._index["foo"].operation == "replace"


def test_attribute_file_dir_json(fixtures_path):
    path = fixtures_path / "attribute-file" / "dirs" / "dir2"
    attribute_file = AttributeFile(path=path)

    assert len(attribute_file.attributes) == 1
    assert len(attribute_file._index) == 1
    assert attribute_file._index["foo"].name == "foo"
    assert attribute_file._index["foo"].value == 3
    assert attribute_file._index["foo"].scope == "descendants"
    assert attribute_file._index["foo"].operation == "replace"
