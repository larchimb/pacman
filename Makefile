ARG ?= config.json
ZIP = pacman.zip

.PHONY: install run debug clean clean_all build lint lint-strict

install:
	uv sync

run:
	uv run python pac-man.py $(ARG)

debug:
	uv run python -m pdb pac-man.py $(ARG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache
	rm -rf build/ dist/

clean_all: clean
	rm -rf .venv
	rm -f $(ZIP)

build:
	uv run pyinstaller pac-man.spec
	cp config.json dist/pac-man/
	zip -r $(ZIP) dist/pac-man

lint:
	uv run flake8 .
	uv run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	uv run flake8 .
	uv run mypy . --strict
