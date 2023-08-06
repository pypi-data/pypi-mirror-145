# Installing For Development

The project comes with a complete development environment to
let you get started in minutes. The environment includes extensions for:

* Running and debugging the application
* Executing and summarizing tests
* Easily pushing to the git repo without having to remember those confusing `git` commands.
* ...Much more



## Installation

Here are the steps for installing SaasLess locally on your computer.

* [Install Docker](#1-install-docker) 

* [Install and configure Git](#2-install-and-configure-git) 

* [Clone git repo](#3-clone-the-git-repo) 

* [Install VSCode](#4-install-vscode) 

* [Install VSCode Remote Containers](#5-add-remote-containers) 

* [Load the repo in VSCode](#6-load-the-repo-in-vscode) 

* [Reopen in container](#7-reopen-in-container) 

* [Start the application](#8-start-the-application) 

Here are the detailed installation instructions.

### 1. Install docker

=== "Linux"
    #### _Linux_

    Install docker if not already installed using:
    ```bash
    sudo apt-get install docker.io
    sudo yum install docker-ce
    ```
    depending on the distribution.

    **Note.** Some newer Linux distributions come with "podman",    "buildah" and/or "moby-engine" which are docker alternatives.  They are not yet supported, please use dockerCE/EE only.

    Youy may need to add your user to docker group for non-root     access.

    ```bash
    sudo usermod -aG docker ${USER}
    ```

    Log out and log back in for the change to become effective,     but you may need to reboot the system depending on the way  shell is spawned. Once done, test docker without `sudo` after    reboot.

    ```bash
    docker ps
    ```
    If configure correctly, above command should not produce any    permission errors.

=== "MacOS"
    #### _MacOS_

    On MacOS, download and install Docker Desktop from https:// docs.docker.com/docker-for-mac/install/

=== "Windows"
    #### _Windows_

    On Windows, download and install Docker Desktop from https://   docs.docker.com/docker-for-windows/install/

    Docker Desktop on Windows requires Hyper-V. You may need to     enable it to use Docker Desktop and will probably not work on   a virtual windows install.

### 2. Install and configure git

Check if git is installed. To check whether or not you have git installed, open a terminal and enter:
```bash
$ git --version
git version 2.20.1
```

If you see an error like command not found go ahead and install git.

=== "Linux"
    #### _Linux_

    ```bash
    sudo apt install git
    sudo yum install git
    ```

=== "MacOS"
    #### _MacOS_
    On MacOS git is packaged with Xcode. You can install Xcode or manually install git using homebrew.

    ```bash
    brew install git
    ```
=== "Windows"
    #### _Windows_
    For windows you can download git from https://git-scm.com/download/win. Download and install the relevant version for your system.

### 3. Clone the git repo
Clone the SaasLess repo from github.
```bash
git clone https://github.com/saasjoy/saasless
```
This will create the directory/folder `saasless` in the current directory/folder.

### 4. Install VScode

Visual Studio Code is a free source-code editor available for Windows, Linux and macOS. Features include support for debugging, syntax highlighting, intelligent code completion, snippets, code refactoring, and embedded Git. Users can change the theme, keyboard shortcuts, preferences, and install extensions that add additional functionality. Visual Studio Code's source code is available on the VSCode repository of GitHub.com, under the permissive MIT License, while the compiled releases are freeware.

=== "Linux"
    #### _Linux_
    Download VSCode from https://code.visualstudio.com/download
    On linux get the .deb or .rpm depending on distribution. You can use the UI to install the package. Alternatively you can install using CLI.

    ```bash
    sudo apt install <Path to downloaded RPM package file>
    sudo yum install <Path to downloaded RPM package file>
    ```
=== "Windows or MacOS"
    #### _Windows_ and _MacOS_
    For Windows and MacOS follow instructions from above download site to install it.

If you have not used VSCode before it maybe a good idea to familiarize yourself with the product.

### 5. Install VSCode Remote Containers

The Visual Studio Code Remote - Containers extension lets you use a Docker container as a full-featured development environment. It allows you to open any folder inside (or mounted into) a container and take advantage of Visual Studio Code's full feature set. A devcontainer.json file in your project tells VS Code how to access (or create) a development container with a well-defined tool and runtime stack. This container can be used to run an application or to sandbox tools, libraries, or runtimes needed for working with a codebase.

This project comes with a Docker image that contains everything needed for development and debugging.  This image is used by the VSCode Devcontainer tool.

Start code, press <kbd>CTRL</kbd>-<kbd>SHIFT</kbd>-<kbd>X</kbd> (use <kbd>Command</kbd>-<kbd>SHIFT</kbd>-<kbd>X</kbd> on MacOS) and check installed extension. If not installed find it (probably in Recommended) and click install.

![Extensions](./images/remote_container_extn.png)
 
### 6. Load the repo in VSCode

Go to File->Open Folder or press <kbd>CTRL</kbd>-<kbd>K</kbd> <kbd>CTRL</kbd>-<kbd>O</kbd> (use <kbd>Command</kbd>-<kbd>K</kbd> <kbd>Command</kbd>-<kbd>O</kbd> on MacOS) 

Select the folder/directory saasless that was created by `git clone` and click `OK`.

### 7. Reopen in container

If the `Remote Containers` were already installed as instructed above. You will see a dialog in the bottom-right corner of the VSCode window.

![REOPEN In Container](./images/reopen_cont_dialog.png)

Go ahead and click on the `Reopen In Container` button.

If you miss the above dialog or do not see it for any reason.  Hit <kbd>CTRL</kbd>-<kbd>SHIFT</kbd>-<kbd>P</kbd> (use <kbd>Command</kbd>-<kbd>SHIFT</kbd>-<kbd>P</kbd> on MacOS)  and scroll to `Remote Containers: Reopen In Container` and select it.

VSCode will start building the container for the application, it may take a while. In the bottom-right corner you will see the status window with `Staring Dev Container (show log)`.

![Starting Dev Container](./images/starting_dev_container.png)

Clicking on the `(show log)` link will take you to the build console.

![Starting Dev Container](./images/container_build_log.png)

# Next Steps

Now you're ready to start developing the app! See the [Quickstart](quickstart.md) page to begin!