set -x

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place src test --exclude=__init__.py
black src test