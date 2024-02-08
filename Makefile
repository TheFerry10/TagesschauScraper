PYTHON=python3.11
ENV_NAME=.env
SHELL := /bin/bash
DIRS = src tests
export PYTHONPATH=.
export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1

.PHONY: clean
clean:
	find . -name "*.swp" -o -name "__pycache__" -o -name ".mypy_cache" | xargs rm -fr
	rm -fr $(ENV_NAME)

.PHONY: setup
setup:
	$(PYTHON) -m venv $(ENV_NAME)
	$(ENV_NAME)/bin/python -m pip install --upgrade pip
	$(ENV_NAME)/bin/python -m pip install -r requirements.txt

.PHONY: unittest
unittest:
	$(ENV_NAME)/bin/python -m doctest tests/unit/*.py
	$(ENV_NAME)/bin/python -m pytest tests/unit/*.py

.PHONY: integrationtest
integrationtest:
	$(ENV_NAME)/bin/python -m doctest tests/integration/*.py
	$(ENV_NAME)/bin/python -m pytest tests/integration/*.py

.PHONY: test
test: unittest integrationtest

.PHONY: typehint
typehint:
	$(ENV_NAME)/bin/python -m mypy $(DIRS)

.PHONY: format
format:
	$(ENV_NAME)/bin/python -m black --line-length=79 --preview $(DIRS)

.PHONY: lint
lint:
	$(ENV_NAME)/bin/python -m flake8 $(DIRS) --ignore=E501 --max-line-length=79

.PHONY: checklist
checklist: typehint format lint test

.PHONY: convert_readme
convert_readme:
	pandoc -f markdown -t rst -o README.rst README.md
