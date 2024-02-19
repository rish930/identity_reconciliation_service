set -e
set -x
APP_ENV=test pytest test "${@}"