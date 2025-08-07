# Variables

# Commands
.PHONY: project_install ollama_install ollama_pull_gemma3 ollama_start

all: install ollama_start

install: ollama_install project_install
	@echo "Installed devcontainer..."

PROJECT_DIRECTORY:=development/
project_install:
	@echo "Installing..."
	$(MAKE) -C $(PROJECT_DIRECTORY)

OLLAMA_URL:=https://ollama.com/install.sh
ollama_install:
	@echo "Installing Ollama..."
	curl -fsSL $(OLLAMA_URL) | sh

ollama_start:
	@echo "Starting Ollama..."
	ollama serve