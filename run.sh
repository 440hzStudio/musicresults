#!/bin/bash

cd "$( dirname "${BASH_SOURCE[0]}" )"
venv=.env

if [ ! -d $venv ]; then
    virtualenv $venv --python=python3.6
fi

source $venv/bin/activate
pip install -r requirements.txt > /dev/null

python musicresults.py

deactivate
