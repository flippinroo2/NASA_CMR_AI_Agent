#!/bin/sh
echo "Installing NodeJS for Debian LINUX"

# Installing NodeJS
apt-get install -y curl
curl -fsSL https://deb.nodesource.com/setup_lts.x | bash -
apt-get install -y nodejs

echo "
NodeJS Version: $(node --version)
NPM Version: $(npm --version)
"

corepack prepare pnpm@latest --activate
corepack enable
corepack install -g pnpm@latest

chown -R :devcontainer /usr/bin/corepack
chown -R :devcontainer /usr/bin/node
chown -R :devcontainer /usr/bin/nodejs
chown -R :devcontainer /usr/bin/npm
chown -R :devcontainer /usr/bin/npx
chown -R :devcontainer /usr/bin/pnpm
chown -R :devcontainer /usr/bin/pnpx
chown -R :devcontainer /usr/bin/yarn
chown -R :devcontainer /usr/bin/yarnpkg
chown -R :devcontainer /usr/lib/node_modules

chmod -R 755 /usr/lib/node_modules

# Adding Node JS variables to PATH
printf '\n\nif [ -f ~/.shell/.node_js_variables ]; then\n    . ~/.shell/.node_js_variables\nfi' >> $_REMOTE_USER_HOME/.bashrc

# Creating ".shell" directory to hold the configuration file if it doesn't exist
if [ -d "$_REMOTE_USER_HOME/.shell" ]; then
    echo "$_REMOTE_USER_HOME/.shell already exists"
else
    echo "Directory does not exist."
    mkdir "$_REMOTE_USER_HOME/.shell"
fi

# Creating ".node_js_variables" file
printf 'echo "Initializing .node_js_variables"\n\n#Creating Variable for NodeJS Binary\nexport NODE_BINARY="/usr/bin/node"\n\nexport PNPM_STORE_DIR="$(pnpm root -g)"' > $_REMOTE_USER_HOME/.shell/.node_js_variables