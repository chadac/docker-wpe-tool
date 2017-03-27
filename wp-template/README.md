# Generated WPEngine Template for `${wpe_install_name}`

Production URL: [${prod__url}]

Staging URL: [${staging__url}]

This is a Wordpress template generated from `wpe-tool`. This documentation outlines several of the cool things that this tool will allow you to manage, but you should probably replace it later with something more fitting.

## Installation

### Starting up a local server

#### Requirements

Local servers are deployed using `docker-compose`. You will need the following installed:

1. [Docker CE](https://docs.docker.com/engine/installation/)
2. [docker-compose](https://docs.docker.com/compose/install/)
3. [wpe-tool](https://github.com/utulsa/docker-wpe-tool)
4. You will also need an nginx container running to correctly route DNS records. This setup assumes you are using `jwilder/nginx-proxy`.

You can start the nginx container with the following command:

    docker run -d -p 80:80 -v /var/run/docker.sock:/tmp/docker.sock:ro --restart always jwilder/nginx-proxy

Note that this only needs to be run once for all installs, and will automatically restart when the machine shuts down.

Finally, you will need to modify your `/etc/hosts` file to redirect your virtual hosts back to your machine. Add the following line to `/etc/hosts`:

    127.0.0.1 ${virtual_hosts},${phpmyadmin_virtual_host}

#### Importing the database

If you are cloning this repository, you will need to import the database using the following command:

    wpe-tool sftp get-db

This will automatically replace instances of the production URL with your local install, so there will probably be no need to manually reprocess the DB.

#### Running

To run the virtual server, simply run

    docker-compose up

in the root of your project folder, and then visit (any of) the following URL(s): "${virtual_hosts}"

### Deployment via Gitlab CI

A sample GitLab CI file has been included that automatically deploys the `production` and `staging` branches to their corresponding WPEngine Git repositories, using the [wpe-deploy](https://github.com/utulsa/docker-wpe-deploy) image. You may configure files that will not be pushed to the WPEngine Git repos using the file named `.wpe-gitignore`, which behaves exactly like `.gitignore` except that it only applies to WPEngine.

You will need to do the following to set up continuous integration with WPEngine:

1. Configure your GitLab server to support [GitLab CI](https://docs.gitlab.com/ce/ci/quick_start/#configuring-a-runner).
2. Create a [private/public SSH key pair](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/) for GitLab CI.
3. Add the contents of the *public key* to your SSH Public Keys in WP Engine, which may be accessed via `${wpe_install_name}` > Git push.
4. Add the contents of the *private key* in GitLab repository to the variable `SSH_PRIVATE_KEY`. Your repository variables can be configured in Settings > Variables.

Finally, make a test push to the `staging` branch to guarantee that this works. You will be able to see the progress of the Git push under `Pipelines` in your repository, and can verify it works by manually checking the staging website.

Note that `wpe-deploy` messes up your history when pushing to WPEngine, since it removes several files that belong on the internal repository but should not be tracked on WPEngine. If your GitLab `production` and `staging` branches are accurate, there will be no need to separately track history on the feature-limited WPEngine. You should take into account this effect when integrating `wpe-tool` and `wpe-deploy` into your workflow.
