VENV = venv
PYTHON = $(VENV)/bin/python3


setup:
	python3 -m venv $(VENV)
	. $(VENV)/bin/activate
	pip3 install poetry
	poetry install