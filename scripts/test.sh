set -e
set -x
APP_ENV=test pytest --cov=src --cov-report=term-missing --cov-config=.coveragerc test "${@}"