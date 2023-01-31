PYTHON=python3.9
ENV_NAME=.env
SHELL := /bin/bash
export PYTHONPATH=.


.PHONY: clean
clean:
	find . -name "*.swp" -o -name "__pycache__" -o -name ".mypy_cache" | xargs rm -fr
	rm -fr $(ENV_NAME)

.PHONY: setup
setup:
	$(PYTHON) -m venv $(ENV_NAME)
	$(ENV_NAME)/bin/python -m pip install --upgrade pip
	$(ENV_NAME)/bin/python -m pip install -r requirements.txt

.PHONY: test
test:
	$(ENV_NAME)/bin/python -m doctest tests/*.py
	$(ENV_NAME)/bin/python -m pytest tests/*.py

.PHONY: build
build:
	$(ENV_NAME)/bin/python setup.py sdist bdist_wheel

.PHONY: typehint
typehint:
	$(ENV_NAME)/bin/python -m mypy tagesschauscraper tests examples

.PHONY: format 
format:
	$(ENV_NAME)/bin/python -m black --line-length=79 --preview tagesschauscraper tests examples

.PHONY: lint
lint:
	$(ENV_NAME)/bin/python -m flake8 tagesschauscraper tests examples --ignore=E501 --max-line-length=79

.PHONY: checklist
checklist: typehint format lint test

.PHONY: convert_readme
convert_readme:
	pandoc -f markdown -t rst -o README.rst README.md
	


