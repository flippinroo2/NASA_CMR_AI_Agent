#!/bin/sh
echo "Mounting the api_keys file into the .shell directory."

# Adding .api_keys file to PATH
printf '\n\nif [ -f ~/.shell/.api_keys ]; then\n    . ~/.shell/.api_keys\nfi' >> $_REMOTE_USER_HOME/.bashrc