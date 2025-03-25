.PHONY: all install lint test coverage help

all: help

install:
	uv sync

test:
	uv run pytest tests/

coverage:
	uv run pytest --cov \
		--cov-report term \
	tests/

format:
	uv run isort .
	uv run black .

lint:
	uv run flake8 .
	uv run mypy .

help:
	@echo '===================='
	@echo '-- RUNTIME --'
	@echo 'install      - install dependencies'
	@echo '-- LINTING --'
	@echo 'format       - run code formatters'
	@echo 'lint         - run linters'
	@echo '-- TESTS --'
	@echo 'coverage     - run unit tests and generate coverage report'
	@echo 'test         - run unit tests'
	