flake8_lint:
	flake8 --config=setup.cfg ./src

lint: flake8_lint
