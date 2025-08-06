#!/bin/sh
echo "Setting up groups for devcontainer"

groupadd devcontainer
usermod -a -G devcontainer root
usermod -a -G devcontainer vscode

chown -R :devcontainer /usr/bin
chown -R :devcontainer /usr/lib
chown -R :devcontainer /usr/share

chmod -R g+w /usr/bin
chmod -R g+w /usr/lib
chmod -R g+w /usr/share