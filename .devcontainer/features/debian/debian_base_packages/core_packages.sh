#!/bin/sh
echo "Installing core packages for Debian LINUX"

# Installing core packages
apt-get install -y \
    apt-transport-https \
    bash \
    bash-completion \
    build-essential \
    ca-certificates \
    cmake \
    coreutils \
    curl \
    direnv \
    dnsutils \
    gcc \
    git \
    git-lfs \
    gnupg \
    libssl-dev \
    locales \
    lsof \
    make \
    mlocate \
    nano \
    net-tools \
    pkg-config \
    software-properties-common \
    sudo \
    wget