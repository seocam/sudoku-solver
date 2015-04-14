

all:
	echo .

test:
	flake8 sudoku.py
	nosetests --with-coverage
