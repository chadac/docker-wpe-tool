# Generated WPEngine Template for `${wpe_install_name}`

This is a Wordpress template generated from `wpe-tool`. This documentation outlines several of the cool things that this tool will allow you to manage, but you should probably replace it later with something more fitting.

The settings for your website are saved to a `wpe-config.json` file, which will be included in this repository but *not* pushed to WPEngine, as long as you use [wpe-deploy](https://github.com/utulsa/docker-wpe-deploy) to manage deployments to WPEngine.

## Some useful `wpe-tool` commands

Note that all of these tools currently need to be run in the root directory of your install.

### `wpe-tool reconfigure`

This exists in the case that you need to reconfigure WPEngine-specific information. It will re-run the init process and update `wpe-config.json`.

### `wpe-tool gen-secrets`

Generates a secrets file `wpe-secrets.json` at the root of your install. The `wpe-secrets.json` file stores SFTP and Git information. It will not be committed to the Git repository or the WPEngine website, and will also be initialized with permissions `600` to prevent other users from reading it.

### `wpe-tool import-db`

Imports the database from over SFTP into the local install. You will need to manually restart your Docker containers once the import is complete.
