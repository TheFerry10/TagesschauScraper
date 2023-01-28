PYTHON=python3.9
ENV_NAME=.env
# export PYTHONPATH=src

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

.PHONY: typehint
typehint:
	mypy tagesschauscraper tests

.PHONY: format
format:
	black --line-length=79 tagesschauscraper tests

.PHONY: lint
lint: 
	black --check --line-length=79 tagesschauscraper tests

.PHONY: checklist
checklist: typehint format test
	


