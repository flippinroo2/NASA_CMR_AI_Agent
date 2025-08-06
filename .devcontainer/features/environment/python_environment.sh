#!/bin/sh
# Adding Python variables to PATH
printf '\n\nif [ -f ~/.shell/.python_variables ]; then\n    . ~/.shell/.python_variables\nfi' >> ${_REMOTE_USER_HOME}/.bashrc

# Creating ".shell" directory to hold the configuration file if it doesn't exist
if [ -d "${_REMOTE_USER_HOME}/.shell" ]; then
    echo "${_REMOTE_USER_HOME}/.shell already exists"
else
    echo "Directory does not exist."
    mkdir "${_REMOTE_USER_HOME}/.shell"
fi

# Creating ".python_variables" file
printf 'echo "Initializing .python_variables..."\n\n# Creating a variable for Pyenv\nexport PYENV_ROOT="$HOME/.pyenv"\n\n# Adding Pyenv binary to PATH\nPATH="$PYENV_ROOT/bin:$PATH"\n\n# Initalizing Pyenv\neval "$(pyenv virtualenv-init -)"\neval "$(pyenv init -)"' > ${_REMOTE_USER_HOME}/.shell/.python_variables
