#!/bin/bash
set -x
python setup.py sdist bdist_wheel || exit
twine upload dist/* || exit

