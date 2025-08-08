#!/bin/sh
echo "Creating settings.json for python"

# Creating ".vscode" directory to hold the debugger files if it doesn't exist
if [ -d "/home/vscode/.vscode" ]; then
    echo "/home/vscode/.vscode already exists"
else
    mkdir -p "/home/vscode/.vscode"
fi

# Setting permissions on the newly created ".vscode" directory
chown -R vscode:vscode /home/vscode/.vscode
chmod -R g+w /home/vscode/.vscode

# Creating settings.json
cat << EOF > /home/vscode/.vscode/settings.json
{
  "explorer.autoReveal": true,
  "makefile.configureOnOpen": false
}
EOF