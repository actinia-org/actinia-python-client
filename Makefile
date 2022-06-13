SRC := .

install:
	pip install actinia-python-client

installdev:
	pip install -r $(SRC)/requirements.txt
	pip install -e .

test:
	pip install -r $(SRC)/requirements.txt
	pip install pytest
	python -m pytest tests/

devtest:
	pip install -r $(SRC)/requirements.txt
	pip install pytest
	python -m pytest tests/ -m dev
