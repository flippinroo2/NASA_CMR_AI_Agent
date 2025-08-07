# NASA CMR AI Agent

> This application is in a __VERY__ early state... Check back in a few days when v0.0.1 tag is created and the debugging comments have been removed.

## INSTALLATION

This project comes included with a ".devcontainer" folder, which will allow you to open a secluded environment within Docker for local development.

Here are the instructions for local development installation:

1. Simply clone the repository.
2. Open the repository if your favorite development environment (*this project was developed in VS Code, but it should work in many popular development environments*)
3. Select to open project inside devcontainer.
  - This will automatically setup an Ubuntu machine with various utilities, including NVIDIA capabilities. (*As long as you have the NVIDIA container toolkit installed on your host machine*)
4. Open a terminal in the default directory and run the `make` command.
  - This will install Ollama within the container.
  - Create a virtual environment and install all necessary python packages.

### INSTALLATION - DEBUGGING

This project is already setup for debugging within VS Code. You should be able to start the application with debugging enabled by navigating to the "Run and Debug" tab within VS Code and pressing the play button.

## USAGE

You will notice a "prompts" directory in the root of this project. This project will iterate through each of the files and 