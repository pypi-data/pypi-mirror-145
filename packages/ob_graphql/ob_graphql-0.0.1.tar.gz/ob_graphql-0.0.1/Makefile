help:
	@echo "Targets:"
	@echo "    make test"
	@echo "    make lint"
	@echo "    make clean"
	@echo "    make clean-test"
	@echo "    make mkdocs"

test:
	python -m unittest tests.test_client

lint:
	pre-commit run --all-files

mkdocs:
	mkdocs serve --livereload

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache