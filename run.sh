#!/bin/bash

cd "$( dirname "${BASH_SOURCE[0]}" )" || exit
venv=.env

if [ ! -d $venv ]; then
    virtualenv $venv --python=python3.6
fi

$venv/bin/pip install -r requirements.txt > /dev/null
$venv/bin/python musicresults.py
