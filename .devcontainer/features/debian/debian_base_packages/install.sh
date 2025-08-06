#!/bin/sh
echo "Installing base packages for Debian LINUX"

# Updating the apt-get repository & base packages
apt-get update -y
apt-get upgrade -y

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Installing core packages
. "$SCRIPT_DIR/core_packages.sh"

# Installing extra packages
if [ "$EXTRAS" = "true" ]; then
  . "$SCRIPT_DIR/extra_packages.sh"
fi

# Cleaning the apt-get cache after installing new packages
apt-get clean