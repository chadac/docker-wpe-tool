# WPEngine Command Line Utility

Managing multiple WPEngine installs can be a hassle, and Wordpress in general doesn't intuitively integrate well into modern development workflows. Deploying a WPEngine install locally can take several hours since you need to set up a web server, pull files from WPEngine,  and process the production database for use locally. It is even harder to manage multiple WPEngine installs on the same machine.

`wpe-tool` is a command line utility for managing Wordpress installs that integrates our own workflow into WPEngine-specific projects. It contains a boilerplate Wordpress install that includes configurations for:

* Continuous integration using GitLab CI using [wpe-deploy](https://github.com/utulsa/docker-wpe-deploy);
* Local deployments using `docker-compose`, and;
* Pulling from SFTP using `pysftp`

The goal behind this tool is to integrate our own workflow into an all-in-one tool that can exist outside the repository and with only install-specific information stored on the repository. Not only is running a local server as simple as running a one-line command, but it can also be used to deploy to WPEngine staging and production servers without any of these development configuration files.

The requirements are listed in the boilerplate [README](/wp-template/README.md). Further instructions on setting up continuous integration and local deployments are explained there.

## Install

    curl -L "https://github.com/utulsa/docker-wpe-tool/releases/download/0.1/wpe-tool" -o /usr/local/bin/wpe-tool

You will need [Docker](https://docs.docker.com/engine/installation/) to run the tool.

## Usage

The general help from the tool can be accessed by writing:

    wpe-tool

in the command line. Currently, it supports a narrow set of commands:

* `wpe-tool init` - Initializes a new local copy of a WPEngine install, and pulls the database/plugins/themes into the install so that it can run instantly.
* `wpe-tool sftp` - Downloads the database/plugins/themes/any other files from the WPEngine SFTP servers
* `wpe-tool reconfigure` - Reconfigures WPE-specific information
* `wpe-tool reset` - Reverts files in the repository back to the template from

Configurations for `wpe-tool` are stored in `wpe-config.json` in the root of the install directory. Secrets for SFTP and Git are stored in `wpe-secrets.json`, which is kept separate so it will not be committed to any repository.
