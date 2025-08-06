#!/bin/sh
# Adding .shell_env file to ".bashrc"
printf '\n\nif [ -f ~/.shell/.shell_env ]; then\n    . ~/.shell/.shell_env\nfi' >> $_REMOTE_USER_HOME/.bashrc

# Creating ".shell" directory to hold the configuration file if it doesn't exist
if [ -d "$_REMOTE_USER_HOME/.shell" ]; then
    echo "$_REMOTE_USER_HOME/.shell already exists"
else
    mkdir "$_REMOTE_USER_HOME/.shell"
fi

# Creating ".shell_env" file
printf 'echo "Initalizing .shell_env..."\n\nexport DEVELOPMENT_FOLDER="$HOME"\n\nexport LOCAL_BINARIES="$HOME/.local/bin"' > $_REMOTE_USER_HOME/.shell/.shell_env