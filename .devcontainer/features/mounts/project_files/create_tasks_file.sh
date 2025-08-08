#!/bin/sh
echo "Creating tasks.json for project"

# Making sure "jq" is installed so we can work with JSON files.
apt-get install -y \
  jq

# Creating ".vscode" directory to hold the debugger files if it doesn't exist
if [ -d "/home/vscode/.vscode" ]; then
    echo "/home/vscode/.vscode already exists"
else
    mkdir -p "/home/vscode/.vscode"
fi

# Setting permissions on the newly created ".vscode" directory
chown -R vscode:vscode /home/vscode/.vscode
chmod -R g+w /home/vscode/.vscode

# Actually doing the creation / modification of the tasks.json
if [ -f "/home/vscode/.vscode/tasks.json" ]; then
    jq '.tasks += [
    {
      "label": "Ollama - Pull gemma3:latest",
      "type": "shell",
      "command": "ollama pull gemma3:latest",
      "hide": true
    },
    {
      "label": "Unit Tests - Run",
      "type": "shell",
      "options": {
        "cwd": "/home/vscode/project"
      },
      "command": "make test",
      "hide": true
    }]' "/home/vscode/.vscode/tasks.json" > "/home/vscode/.vscode/temp.json" && mv -f "/home/vscode/.vscode/temp.json" "/home/vscode/.vscode/tasks.json"
else
    # Creating tasks.json
    cat << EOF > /home/vscode/.vscode/tasks.json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Ollama - Pull gemma3:latest",
      "type": "shell",
      "command": "ollama pull gemma3:latest",
      "hide": true
    },
    {
      "label": "Unit Tests - Run",
      "type": "shell",
      "options": {
        "cwd": "/home/vscode/project"
      },
      "command": "make test",
      "hide": true
    }
  ]
}
EOF
fi