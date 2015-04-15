

all: install

install:
	pip install nose coverage flake8

test:
	flake8 sudoku.py
	nosetests --with-coverage
