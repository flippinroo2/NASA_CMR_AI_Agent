# Variables

# Commands
.PHONY: clean install nuke reinstall

all: reinstall

data_scraper: reinstall

clean:
	@echo "Cleaning..."
	@rm -rf "__pycache__"

install:
	@echo "Installing..."
	poetry install --no-root

nuke: clean
	@echo "Nuking..."
	@rm -rf ".venv" "poetry.lock"

reinstall: nuke install
	@echo "Reinstalled..."

test:
	@echo "Testing NASA CMR AI Agent..."
	python -m unittest discover -s tests