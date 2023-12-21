SRC := .

.PHONY: installdev

install:
	pip install actinia-python-client

installdev:
	pip3 install pip-tools
	pip install -e .

mockedtest: installdev
	pip install pytest
	python -m pytest tests_mocked/

test: installdev
	pip install pytest
	python -m pytest tests/

devtest: installdev
	pip install pytest
	python -m pytest tests/ -m dev
