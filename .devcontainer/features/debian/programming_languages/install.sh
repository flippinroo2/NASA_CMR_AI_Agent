#!/bin/sh
# Updating the apt-get repository & base packages
apt-get update -y
apt-get upgrade -y

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ "$NODEJS" = "true" ]; then
  . "$SCRIPT_DIR/nodejs.sh"
fi

# Cleaning the apt-get cache after intalling new packages
apt-get clean