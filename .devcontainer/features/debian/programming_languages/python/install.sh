#!/bin/bash
echo "Installing Python for Debian LINUX"

# Installing dependencies
apt-get install -y \
  gstreamer1.0-plugins-base \
  gstreamer1.0-plugins-bad \
  libavif-dev \
  libbz2-dev \
  libcairo-gobject2 \
  libcairo2-dev \
  libdb5.3-dev \
  libenchant-2-dev \
  libevent-2.1-7 \
  libevent-dev \
  libexpat1-dev \
  libffi-dev \
  libflite1 \
  libgdk-pixbuf2.0-dev \
  libgdbm-dev \
  libgstreamer1.0-dev \
  libgtk-3-dev \
  libhyphen-dev \
  liblzma-dev \
  libmanette-0.2-dev \
  libncurses5-dev \
  libncursesw5-dev \
  libopus-dev \
  libpangocairo-1.0-0 \
  libreadline-dev \
  libsecret-1-dev \
  libsqlite3-dev \
  libssl-dev \
  libsstp-api-0-dev \
  libvpx-dev \
  libwoff-dev \
  libx11-xcb-dev \
  libx264-dev \
  libxcursor-dev \
  libxslt1-dev \
  uuid-dev \
  sqlite3 \
  tk-dev \
  zlib1g-dev


python_version="${PYTHON_VERSION:-3.12}" # TODO: Figure out what the :-3.12 does???

echo "
OS: $OS
ARCH: $ARCH
"

update_apt_packages(){
  # Updating the apt-get repository & base packages
  sudo apt-get update -y
  sudo apt-get upgrade -y

  # Installing dependencies
  sudo apt-get install -y \
    curl

  # Cleaning the apt-get cache after intalling new packages
  sudo apt-get clean
}

install_pyenv(){
  # Removes the ".pyenv" folder if it exists already
  rm -rf ${HOME}/.pyenv

  # Install Pyenv
  curl https://pyenv.run | bash

  # Move the ".pyenv" folder to the container user's home directory
  mv ${HOME}/.pyenv ${_REMOTE_USER_HOME}/.pyenv

  # Rehashing the binary files after moving the ".pyenv" folder
  ${_REMOTE_USER_HOME}/.pyenv/bin/pyenv rehash

  chown -R vscode:devcontainer ${_REMOTE_USER_HOME}/.pyenv
  chmod -R 755 ${_REMOTE_USER_HOME}/.pyenv
}

install_uv(){
  # Install uv
  curl -LsSf https://astral.sh/uv/install.sh | sh

  # Creating a ".local" and ".local/bin" folder in the ${_REMOTE_USER_HOME} directory
  mkdir ${_REMOTE_USER_HOME}/.local
  mkdir ${_REMOTE_USER_HOME}/.local/bin

  # Moving the "uv" and "uvx" binaries to the ${_REMOTE_USER_HOME}/.local/bin directory
  sudo mv ${HOME}/.local/bin/uv ${_REMOTE_USER_HOME}/.local/bin/uv
  sudo mv ${HOME}/.local/bin/uvx ${_REMOTE_USER_HOME}/.local/bin/uvx

  chown -R vscode:vscode ${_REMOTE_USER_HOME}/.local
  chmod -R 755 ${_REMOTE_USER_HOME}/.local
}

create_python_variables_file(){
  # Dynamically adding the PYTHON_VERSION environment variable to the ".python_variables" file
  printf '\n\n# Python Version Variable\nexport PYTHON_VERSION="%s"\n\n# Poetry Variables\nexport POETRY_VIRTUALENVS_CREATE=true\nexport POETRY_VIRTUALENVS_IN_PROJECT=true\n\n# Pipenv Variables\nexport PIPENV_VENV_IN_PROJECT=true' ${PYTHON_VERSION} >> ${_REMOTE_USER_HOME}/.shell/.python_variables
}

create_ruff_configuration_file(){
  # Creating "ruff.toml" file
  printf 'indent-width = 2\nline-length = 119\n\n[format]\ndocstring-code-format = true\nindent-style = "space"\nline-ending = "lf"\nquote-style = "single"' > $_REMOTE_USER_HOME/ruff.toml
  chown vscode:vscode ${_REMOTE_USER_HOME}/ruff.toml
  chmod 755 ${_REMOTE_USER_HOME}/ruff.toml
}

create_pywright_configuration_file(){
  # pyrightconfig.json
  #   {
  #   "exclude": [
  #     "node_modules",
  #     "dist",
  #     "build",
  #     "venv",
  #     ".git",
  #     "logs",
  #     "temp",
  #     "data",
  #     "**/cache"
  #   ]
  # }
  # .vscode/settings.json
  #   {
  #   "files.exclude": [
  #     "**/node_modules",
  #     "**/dist",
  #     "**/build",
  #     "**/venv",
  #     "**/.git",
  #     "**/logs",
  #     "**/temp",
  #     "**/data",
  #     "**/cache"
  #   ]
  # }
  # pyproject.toml
  # [tool.pyright]
  # exclude = [
  #     "**/node_modules",
  #     "**/__pycache__",
  #     "**/.venv",
  #     "**/tests",
  #     "**/migrations",
  #     "**/data",
  #     "**/build",
  #     "**/dist",
  #     ".git",
  #     "path/to/specific/large/directory"
  # ]
  # include = ["src"]
  # # Other Pyright options...
  echo "create_pywright_configuration_file"
}

update_apt_packages
install_pyenv
install_uv
create_python_variables_file
create_ruff_configuration_file
# create_pywright_configuration_file


echo "Python Version: ${python_version} installed."