PYTHON ?= python3
TEST_PATTERN ?= test_*.py
TEST_ENV ?= PYTHONDONTWRITEBYTECODE=1

.PHONY: test test-unit test-integration

test: test-unit test-integration

test-unit:
	$(TEST_ENV) $(PYTHON) -m unittest discover -s tests/unit -p "$(TEST_PATTERN)" -v

test-integration:
	$(TEST_ENV) $(PYTHON) -m unittest discover -s tests/integration -p "$(TEST_PATTERN)" -v
