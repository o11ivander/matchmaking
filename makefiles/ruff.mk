ruff_lint:
	# ruff check . --fix ./src
	ruff check .

ruff_fix:
	ruff check . --fix ./src

ruff_lint_full:
	# ruff check . --fix --extend-select E501 ./src
	ruff check . --extend-select E501 ./src

ruff_format:
	ruff format . ./src

ruff:	ruff_fix ruff_format
