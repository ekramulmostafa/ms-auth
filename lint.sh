#!/bin/bash
source venv/bin/activate
retv=0

print_name() { echo -e "\n$1"; }

trap "retv=1" ERR

# We need an access to python virtual environment for running this script as PyCharm external tool
# source "${PY_INTERPRETER_DIRECTORY}/activate" 2> /dev/null

print_name "Flake8"
flake8 --config=.flake8

print_name "Pylint"
find . -iname "*.py" -not -path "./venv/*" -not -path "./migrations/*" | xargs pylint --rcfile=.pylint --reports=no

exit ${retv}