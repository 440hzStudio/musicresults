.PHONY: run test lint venv

venv := .env

run: venv
	$(venv)/bin/python musicresults.py

test: venv
	$(venv)/bin/pip install -r requirements.test.txt > /dev/null

lint:
	pylint **/**.py

venv:
	if [ ! -d $(venv) ]; then virtualenv $(venv) --python=python3.6; fi
	$(venv)/bin/pip install -r requirements.txt > /dev/null
