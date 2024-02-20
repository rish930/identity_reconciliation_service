set -e
set -x

black src test --check
flake8 src test

