.PHONY: clear-data test test-cov

clear-data:
	find ./data -type f -exec rm -f {} \;

test:
	pytest -s tests/

test-cov:
	pytest --cov=pysms --cov-report xml:coverage/coverage.xml --cov-report term tests/
