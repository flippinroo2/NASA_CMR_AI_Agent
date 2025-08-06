#!/bin/sh
echo "Setting up permissions for devcontainer"


chown -R vscode:devcontainer /tmp

chown -R vscode:devcontainer ${_REMOTE_USER_HOME}/.shell

chmod -R 770 ${_REMOTE_USER_HOME}/.shell

# sudo: /usr/bin/sudo must be owned by uid 0 and have the setuid bit set
chown root:root /usr/bin/sudo
chmod 4755 /usr/bin/sudo