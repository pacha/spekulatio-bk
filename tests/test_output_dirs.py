from spekulatio.models import OutputDir


def test_instantiation(fixtures_path):
    output_dir = OutputDir(root_path=fixtures_path, path="empty-output-dir")
    gitkeep = output_dir.path / ".gitkeep"
    assert gitkeep.is_file()
