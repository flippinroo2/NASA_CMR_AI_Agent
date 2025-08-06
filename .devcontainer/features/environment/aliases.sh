#!/bin/sh
# Adding .shell_aliases file to ".bashrc"
printf '\n\nif [ -f ~/.shell/.shell_aliases ]; then\n    . ~/.shell/.shell_aliases\nfi' >> ${_REMOTE_USER_HOME}/.bashrc

# Creating ".shell" directory to hold the configuration file if it doesn't exist
if [ -d "${_REMOTE_USER_HOME}/.shell" ]; then
    echo "${_REMOTE_USER_HOME}/.shell already exists"
else
    mkdir "${_REMOTE_USER_HOME}/.shell"
fi

# Creating ".shell_aliases" file
printf 'echo "Initalizing .bash_aliases"...\n\n# Aliases\n\n## System Aliases\nalias l="ls -CF --color=auto"\nalias la="ls-A --color=auto"\nalias lf="ls -F --color=auto"\nalias ll="ls -Fla --color=auto"\nalias of="lsof -nP +c 15 | grep LISTEN"' > ${_REMOTE_USER_HOME}/.shell/.shell_aliases