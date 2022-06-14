SRC := .

.PHONY: dependencies

dependencies:
	pip install -r $(SRC)/requirements.txt

install:
	pip install actinia-python-client

installdev: dependencies
	pip install -e .

test: dependencies
	pip install pytest
	python -m pytest tests/
