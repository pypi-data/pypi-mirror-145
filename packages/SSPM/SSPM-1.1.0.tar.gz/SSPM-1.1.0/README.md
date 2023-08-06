# Super Simple Plugin Manager - SSPM

## About SSPM

Super Simple Plugin Manager - SSPM is a simple Python library I created based off of Thibauld Nion's yapsy. 
I liked how yapsy uses a config file in conjunction with a python module for locating and describing plugins.
This plugin manager does not have the robustness and customizability that yapsy has but allows for much quicker 
implementation out of the box. It is meant to be a very simple ready to go hands off plugin manager.

## Usage

1. Initialize the plugin manager

	``` shell
	plugin_manager = PluginManager(plugin_folder=\<INSERT PLUGINS DIR PATH HERE\>)
	```
	
2. Import the plugins in the plugins directory

	``` shell
	plugin_manager.import_plugins()
	```
 
3. Get the imported plugin

	```shell
	plugin = sspm.get_active_plugin("Plugin name")
	```
 
    or

    ```shell
    plugins = sspm.active_plugins
    ```
