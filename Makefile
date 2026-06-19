PYTHON ?= python3
TEST_PATTERN ?= test_*.py

.PHONY: test test-unit test-integration

test: test-unit test-integration

test-unit:
	$(PYTHON) -m unittest discover -s tests/unit -p "$(TEST_PATTERN)" -v

test-integration:
	$(PYTHON) -m unittest discover -s tests/integration -p "$(TEST_PATTERN)" -v
