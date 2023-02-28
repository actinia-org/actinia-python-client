SRC := .

.PHONY: dependencies

dependencies:
	pip install -r $(SRC)/requirements.txt

install:
	pip install actinia-python-client

installdev: dependencies
	pip install -e .

mockedtest: dependencies
	pip install pytest
	python -m pytest tests_mocked/

test: dependencies
	pip install pytest
	python -m pytest tests/

devtest:
	pip install -r $(SRC)/requirements.txt
	pip install pytest
	python -m pytest tests/ -m dev
