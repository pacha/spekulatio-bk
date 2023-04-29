from spekulatio.models import InputDir


def test_instantiation(fixtures_path):
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
    gitkeep = input_dir.path / ".gitkeep"
    assert gitkeep.is_file()


def test_traversal(fixtures_path):
    input_dir = InputDir(root_path=fixtures_path, path="traversal-input-dir")
    paths = [str(path) for path in input_dir]
    paths.sort()
    correct_output = [
        "dir1",
        "dir1/dir3",
        "dir1/dir3/file4.md",
        "dir1/file3.md",
        "dir2",
        "dir2/file5.md",
        "file1.md",
        "file2.md",
    ]
    assert paths == correct_output
