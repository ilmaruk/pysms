.PHONY: clear clear-data test test-cov

clean:
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

clean-data:
	find ./data -type f -exec rm -f {} \;

test:
	pytest -s tests/

test-cov:
	pytest --cov=pysms --cov-report xml:coverage/coverage.xml --cov-report term tests/
