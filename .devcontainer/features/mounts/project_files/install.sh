#!/bin/sh
echo "Mounting project files to use for project"

. ./create_launch_file.sh
. ./create_tasks_file.sh
. ./create_settings_file.sh

# Setting permissions on the newly created ".vscode" directory
chown -R vscode:vscode /home/vscode/.vscode
chmod -R g+w /home/vscode/.vscode

# Creating "NASA_CMR_AI_Agent.code-workspace" file
printf '{
  "folders": [
    {
      "name": "project",
      "path": "./project"
    },
  ],
  "launch": {
    "version": "0.2.0",
    "configurations": [],
    "compounds": []
  },
  "tasks": {
    "version": "2.0.0",
    "tasks": []
  }
}' > $_REMOTE_USER_HOME/python.code-workspace