#!/usr/bin/env bash

echo "Installing NVIDIA drivers for Debian LINUX"

# This tells the script to exit right away if any command fails.
set -e

# This directory is where apt stores metadata about available packages from repositories (e.g. lists of packages, versions, and dependencies)
# After this is ran, it will delete everything in that metadata directory. apt will then re-download fresh metadata from all configured repositories the next time "apt update" is ran.
rm -rf /var/lib/apt/lists/*

# Captures values from the devcontainer-feature options into variables.
INSTALL_CUDA_DEV=${INSTALLCUDADEV}
INSTALL_CUDNN=${INSTALLCUDNN}
INSTALL_CUDNNDEV=${INSTALLCUDNNDEV}
INSTALL_NVTX=${INSTALLNVTX}
INSTALL_TOOLKIT=${INSTALLTOOLKIT}
CUDA_VERSION=${CUDAVERSION}
CUDNN_VERSION=${CUDNNVERSION}

# This below gives us access to many useful system related environment variables.
. /etc/os-release 

if [ "$(id -u)" -ne 0 ]; then
    echo -e 'Script must be run as root. Use sudo, su, or add "USER root" to your Dockerfile before running this script.'
    exit 1
fi

apt_get_update(){
  if [ "$(find /var/lib/apt/lists/* | wc -l)" = "0" ]; then
    echo "Running apt-get update..."
    apt-get update -y
  fi
}

# Checks if packages are installed and installs them if not
check_packages() {
  if ! dpkg -s "$@" > /dev/null 2>&1; then
    apt_get_update
    apt-get -y install --no-install-recommends "$@"
  fi
}

if [ $VERSION_CODENAME = "bookworm" ] || [ $VERSION_CODENAME = "jammy" ] && [ $CUDA_VERSION \< 11.7 ]; then  
  echo "(!) Unsupported distribution version '${VERSION_CODENAME}' for CUDA < 11.7"
  exit 1
fi

# This below will disable any of the interactive prompts like the ones used during package installations and system configurations.
export DEBIAN_FRONTEND=noninteractive

check_packages wget ca-certificates

# Determine system architecture and set NVIDIA repository URL accordingly
ARCH=$(uname -m)
case $ARCH in
    x86_64)
        NVIDIA_ARCH="x86_64"
        ;;
    aarch64 | arm64)
        NVIDIA_ARCH="arm64"
        ;;
    *)
        echo "Unsupported architecture: $ARCH"
        exit 1
        ;;
esac

NVIDIA_REPO_URL="https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/$NVIDIA_ARCH" # Using ubuntu2204 as ubuntu 20.04 is going out of support.
KEYRING_PACKAGE="cuda-keyring_1.1-1_all.deb"
KEYRING_PACKAGE_URL="$NVIDIA_REPO_URL/$KEYRING_PACKAGE" # Same as https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb

# TODO: Delete this function once this has been well tested enough.
install_nvidia_cuda_drivers(){
  wget "$KEYRING_PACKAGE_URL"
  dpkg -i "$KEYRING_PACKAGE" # This is missing in the function below. How important is it? Is it replaced by a newer method below?
  apt-get update
  apt-get install -y cuda-drivers # This is also missing and seems important???
}
# install_nvidia_cuda_drivers

add_nvidia_to_apt(){
  # Add NVIDIA's package repository to apt so that we can download packages
  KEYRING_PACKAGE_PATH="$(mktemp -d)"
  KEYRING_PACKAGE_FILE="$KEYRING_PACKAGE_PATH/$KEYRING_PACKAGE"
  wget -O "$KEYRING_PACKAGE_FILE" "$KEYRING_PACKAGE_URL"
  apt-get install -yq "$KEYRING_PACKAGE_FILE"
  apt-get update -yq
}
add_nvidia_to_apt

install_cuda(){
  # Ensure that the requested version of CUDA is available
  cuda_pkg="cuda-libraries-${CUDA_VERSION/./-}"
  cuda_development_pkg="cuda-libraries-dev-${CUDA_VERSION/./-}"
  if ! apt-cache show "$cuda_pkg"; then
      echo "The requested version of CUDA is not available: CUDA $CUDA_VERSION"
      if [ "$NVIDIA_ARCH" = "arm64" ]; then
          echo "Note: arm64 supports limited CUDA versions. Please check available versions:"
          echo "https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/arm64"
      fi
      exit 1
  fi

  echo "Installing CUDA libraries..."
  if [ "$INSTALL_CUDA_DEV" = "true" ]; then
    apt-get install -yq "$cuda_development_pkg"
  else
    apt-get install -yq "$cuda_pkg"
  fi
  apt-get update -yq --fix-missing
}
install_cuda

install_cudnn(){
  # auto find recent cudnn version
  major_cuda_version=$(echo "${CUDA_VERSION}" | cut -d '.' -f 1)
  if [ "$CUDNN_VERSION" = "automatic" ]; then
      if [[ "$CUDA_VERSION" < "12.3" ]]; then
          CUDNN_VERSION=$(apt-cache policy libcudnn8 | grep "$CUDA_VERSION" | grep -Eo '^[^-1+]*' | sort -V | tail -n1 | xargs)
      else
          CUDNN_VERSION=$(apt-cache policy libcudnn9-cuda-$major_cuda_version | grep "Candidate" | awk '{print $2}' | grep -Eo '^[^-+]*')
      fi
  fi
  major_cudnn_version=$(echo "${CUDNN_VERSION}" | cut -d '.' -f 1)

  if [ "$INSTALL_CUDNN" = "true" ]; then
      # Ensure that the requested version of cuDNN is available AND compatible
      #if major cudnn version is 9, then we need to install libcudnn9-cuda-<major_cuda_version>_<CUDNN_VERSION>-1 package
      #else we need to install libcudnn8_<CUDNN_VERSION>-1+cuda<CUDA_VERSION>" package
      if [[ $major_cudnn_version -ge "9" ]]
      then
          cudnn_pkg_version="libcudnn9-cuda-${major_cuda_version}=${CUDNN_VERSION}-1"
      else
          cudnn_pkg_version="libcudnn8=${CUDNN_VERSION}-1+cuda${CUDA_VERSION}"
      fi

      if ! apt-cache show "$cudnn_pkg_version"; then
          echo "The requested version of cuDNN is not available: cuDNN $CUDNN_VERSION for CUDA $CUDA_VERSION"
          if [ "$NVIDIA_ARCH" = "arm64" ]; then
              echo "Note: arm64 has limited cuDNN package availability"
          fi
          exit 1
      fi

      echo "Installing cuDNN libraries..."
      apt-get install -yq "$cudnn_pkg_version"
  fi

  if [ "$INSTALL_CUDNNDEV" = "true" ]; then
      # Ensure that the requested version of cuDNN development package is available AND compatible
      #if major cudnn version is 9, then we need to install libcudnn9-dev-cuda-<major_cuda_version>_<CUDNN_VERSION>-1 package
      #else we need to install libcudnn8-dev_<CUDNN_VERSION>-1+cuda<CUDA_VERSION>" package
      if [[ $major_cudnn_version -ge "9" ]]
      then
          cudnn_dev_pkg_version="libcudnn9-dev-cuda-${major_cuda_version}=${CUDNN_VERSION}-1"
      else
          cudnn_dev_pkg_version="libcudnn8-dev=${CUDNN_VERSION}-1+cuda${CUDA_VERSION}"
      fi
      if ! apt-cache show "$cudnn_dev_pkg_version"; then
          echo "The requested version of cuDNN development package is not available: cuDNN $CUDNN_VERSION for CUDA $CUDA_VERSION"
          if [ "$NVIDIA_ARCH" = "arm64" ]; then
              echo "Note: arm64 has limited cuDNN development package availability"
          fi
          exit 1
      fi

      echo "Installing cuDNN dev libraries..."
      apt-get install -yq "$cudnn_dev_pkg_version"
  fi
}
install_cudnn

install_nvtx(){
  echo "Installing NVTX..."
  nvtx_pkg="cuda-nvtx-${CUDA_VERSION/./-}"
  apt-get install -yq "$nvtx_pkg"
}
if [ "$INSTALL_NVTX" = "true" ]; then
  install_nvtx
fi


install_nvidia_cuda_toolkit(){
  echo "Installing CUDA Toolkit..."
  toolkit_pkg="cuda-toolkit-${CUDA_VERSION/./-}"
  apt-get install -yq "$toolkit_pkg"

  nvcc_pkg="cuda-nvcc-${CUDA_VERSION/./-}"
  apt-get install -yq "$nvcc_pkg"
  
  cudart_dev_pkg="cuda-cudart-dev-${CUDA_VERSION/./-}"
  apt-get install -yq "$cudart_dev_pkg"
}
if [ "$INSTALL_TOOLKIT" = "true" ]; then
  install_nvidia_cuda_toolkit
fi

echo "Complete..."