install:
	pip install --upgrade pip &&\
	pip install -r requirements.txt

.PHONY: test
test:
	pytest tests/