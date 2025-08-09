#!/bin/sh
echo "Creating launch.json for project"

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

# Actually doing the creation / modification of the launch.json
if [ -f "/home/vscode/.vscode/launch.json" ]; then
    jq '.configurations += [
    {
      "name": "Python Debugger: Current File",
      "type": "debugpy",
      "request": "launch",
      "env": {
        "PYTHONPATH": "/home/vscode/project"
      },
      "python": "/home/vscode/project/.venv/bin/python",
      "program": "${file}",
      "console": "integratedTerminal",
      "justMyCode": false
    },
    {
      "name": "NASA CMR AI Agent - __main__.py",
      "type": "debugpy",
      "request": "launch",
      "preLaunchTask": "Ollama - Pull gemma3:latest",
      "python": "/home/vscode/project/.venv/bin/python",
      "program": "/home/vscode/project/__main__.py",
      "console": "integratedTerminal",
      "justMyCode": false
    },
    {
      "name": "NASA CMR AI Agent - Module with uvicorn",
      "type": "debugpy",
      "request": "launch",
      "preLaunchTask": "Ollama - Pull gemma3:latest",
      "python": "/home/vscode/project/.venv/bin/python",
      "console": "integratedTerminal",
      "module": "uvicorn",
      "args": [
        "project/__init__:app",
      ],
      "justMyCode": false
    },
    {
      // TODO: Enable breakpoints on errors / failed tests
      "name": "NASA CMR AI Agent - Run Tests",
      "type": "debugpy",
      "request": "launch",
      "preLaunchTask": "Ollama - Pull gemma3:latest",
      "cwd": "/home/vscode/project",
      "python": "/home/vscode/project/.venv/bin/python",
      "console": "integratedTerminal",
      "module": "unittest",
      "args": [
        "discover",
        "-s",
        "tests"
      ],
      "justMyCode": false
    }]' "/home/vscode/.vscode/launch.json" > "/home/vscode/.vscode/temp.json" && mv -f "/home/vscode/.vscode/temp.json" "/home/vscode/.vscode/launch.json"
else
    # Creating launch.json
    cat << EOF > /home/vscode/.vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "NASA CMR AI Agent - __main__.py",
      "type": "debugpy",
      "request": "launch",
      "preLaunchTask": "Ollama - Pull gemma3:latest",
      "cwd": "/home/vscode/project",
      "python": "/home/vscode/project/.venv/bin/python",
      "program": "/home/vscode/project/__main__.py",
      "console": "integratedTerminal",
      "justMyCode": false
    },
    {
      "name": "NASA CMR AI Agent - Module with uvicorn",
      "type": "debugpy",
      "request": "launch",
      "preLaunchTask": "Ollama - Pull gemma3:latest",
      "cwd": "/home/vscode/project",
      "python": "/home/vscode/project/.venv/bin/python",
      "console": "integratedTerminal",
      "module": "uvicorn",
      "args": [
        "__init__:app",
      ],
      "justMyCode": false
    }
  ]
}
EOF
fi