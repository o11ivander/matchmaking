# Makefile

include makefiles/*.mk

.PHONY: flake8_lint lint isort_formatter black_formatter format test_run test_clear test local_test coverage local_coverage coverage_clear mypy
