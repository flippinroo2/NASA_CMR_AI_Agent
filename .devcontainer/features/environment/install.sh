#!/bin/sh
echo "Setting up environment for devcontainer"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"


if [ "${ALIASES}" = "true" ]; then
  . "${SCRIPT_DIR}/aliases.sh"
fi

if [ "$GROUPS" = "true" ]; then
  . "${SCRIPT_DIR}/groups.sh"
fi

if [ "$PYTHON" = "true" ]; then
  . "${SCRIPT_DIR}/python_environment.sh"
fi

if [ "${VARIABLES}" = "true" ]; then
  . "${SCRIPT_DIR}/variables.sh"
fi

. "${SCRIPT_DIR}/permissions.sh"