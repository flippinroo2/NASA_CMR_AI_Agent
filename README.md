# NASA CMR AI Agent

> This application is in a __VERY__ early state... Check back in a few days when v0.0.1 tag is created, and the debugging comments have been removed.

## INSTALLATION

__#1 The first step is to clone this repository into a directory of your choosing.__

The easiest way to install this application is to use the provided Docker configurations. However, if your local machine has Python and Ollama setup, it is also pretty simple to install.

<details>
  <summary>INSTALLATION - LOCAL MACHINE</summary>

1. Navigate to the `NASA_CMR_AI_Agent/project` directory.
2. Run the `make` command.
   - If your local machine does not have the `make` command, or if the `make` command fails. You can either run `poetry install --no-root` or run `pip install -r requirements.txt` command.
3. Activate the virtual environment created from above, and run the `NASA_CMR_AI_Agent/project/__main__.py__` file.

>This will not provide access to the neo4j graph database. If you want to use the neo4j database, you will need to install it on your local machine as well.
</details>

<details>
  <summary>INSTALLATION - DOCKER</summary>

Inside the top-level `NASA_CMR_AI_Agent/project/.devcontainer` folder, you will see a `docker-compose.yml` file. This file is used to setup two Docker containers for this application.

1. An Ubuntu container pre-configured with Python 3.12.7 and NVIDIA capabilities.
2. A neo4j container configured to run a graph database for this application.

</details>

<details>
  <summary>INSTALLATION - DEVCONTAINER</summary>

This project comes included with a `NASA_CMR_AI_Agent/project/.devcontainer` folder, which should be recognized by most development environments.

This will allow you to open a fully configured and secluded development environment within Docker.

Here are the instructions for devcontainer installation:

1. Open the repository in your favorite development environment (*this project was developed in VS Code, but it should work in many popular development environments*)
2. Select to open project inside the devcontainer.
    - This will automatically setup an Ubuntu machine with various utilities, including NVIDIA capabilities. (*As long as you have the NVIDIA container toolkit installed on your host machine.*)
3. Open a terminal in the default directory and run the `make` command.
    - This will install Ollama within the container.
    - Create a virtual environment and install all necessary python packages.
    - Begin running the Ollama server inside the currently active terminal.

</details>

## USAGE

You will notice a `NASA_CMR_AI_Agent/prompts` directory in the root of this project. This project will iterate through each of the `.txt` files in that directory and treat them as a prompt to be processed by the Agentic application.

## DEBUGGING

This project is setup for debugging within VS Code. (*These conigurations are located in `NASA_CMR_AI_Agent/.vscode`*)

You should be able to start the application with debugging enabled by navigating to the "Run and Debug" tab within VS Code and pressing the play button.
