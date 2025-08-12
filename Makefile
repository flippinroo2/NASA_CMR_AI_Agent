# Variables

# Commands
.PHONY: project_install ollama_install ollama_pull_gemma3 ollama_start

all: install ollama_start

CURRENT_DIRECTORY:=$(shell pwd)
dev:
	@echo "Opening project in devcontainer"
	code --folder-uri vscode-remote://dev-container+${CURRENT_DIRECTORY}

install: ollama_install project_install
	@echo "Installed devcontainer..."

PROJECT_DIRECTORY:=project/
project_install:
	@echo "Installing..."
	$(MAKE) -C $(PROJECT_DIRECTORY)

OLLAMA_URL:=https://ollama.com/install.sh
ollama_install:
	@echo "Installing Ollama..."
	curl -fsSL $(OLLAMA_URL) | sh

ollama_pull_gemma3:
	@echo "Pulling gemma3:latest..."
	ollama pull gemma3:latest

# Would like to make this a service, but it is very complicated getting systemd working in Docker containers... I did find this possible alternative https://github.com/gdraheim/docker-systemctl-replacement
ollama_start:
	@echo "Starting Ollama server..."
	ollama serve

start: ollama_start