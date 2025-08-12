# Variables

# Commands
.PHONY: clean install nuke reinstall

all: reinstall

data_scraper: reinstall

clean:
	@echo "Cleaning..."
	@rm -rf "__pycache__"

generate_requirements:
	@echo "Generating requirements.txt file..."
	poetry export -f requirements.txt --output requirements.txt

install:
	@echo "Installing..."
	poetry install --no-root

nuke: clean
	@echo "Nuking..."
	@rm -rf ".venv" "poetry.lock"

reinstall: nuke install
	@echo "Reinstalled..."

ruff_check_project:
	@echo "Fixing imports using ruff..."
	ruff check .

ruff_fix_imports:
	@echo "Fixing imports using ruff..."
	ruff check --select F401 --fix . --exclude .venv,__pycache__
	ruff check --select I001 --fix . --exclude .venv,__pycache__

test:
	@echo "Testing NASA CMR AI Agent..."
	python -m unittest discover -s tests