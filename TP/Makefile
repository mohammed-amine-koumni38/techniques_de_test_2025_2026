.PHONY: test unit_test perf_test coverage lint doc

test:
	python -m pytest tests/ --tb=short

unit_test:
	python -m pytest tests/ --tb=short -m "not performance"

perf_test:
	python -m pytest tests/ --tb=short -m performance

coverage:
	python -m coverage run -m pytest tests/ --tb=short
	python -m coverage report
	python -m coverage html

lint:
	python -m ruff check .


doc:
	python -m pdoc --html --output-dir docs triangulator