.PHONY: lint, format, import-sort


lint:
	poetry run ruff check

format:
	poetry run black .

import-sort:
	poetry run isort .
