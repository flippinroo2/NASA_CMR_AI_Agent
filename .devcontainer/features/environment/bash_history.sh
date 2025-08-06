#!/bin/sh
echo "Setting up bash history for devcontainer"

# Changing the ownership of the ".bash_history" file
chown -R vscode:devcontainer ${_REMOTE_USER_HOME}/.bash_history
chmod -R 511 ${_REMOTE_USER_HOME}/.bash_history

# Adding the HISTSIZE & HISTFILESIZE variable to the ".bashrc" file to increase the history size
printf '\n\nexport HISTFILESIZE=10000\nexport HISTSIZE=100000' >> ${_REMOTE_USER_HOME}/.bashrc