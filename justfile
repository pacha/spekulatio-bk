
project_dir := justfile_directory()

export PYTHONPATH := project_dir

# list recipes
@default:
  just --list

@test:
  pytest --capture=no tests/

@format:
  black {{ project_dir }}

@check:
  mypy {{ project_dir }}/spekulatio/

@cli:
  ipython

