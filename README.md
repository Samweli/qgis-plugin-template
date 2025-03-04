# QGIS plugins template


![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/samweli/qgis-plugin-template/ci.yml?branch=master)
![GitHub](https://img.shields.io/github/license/samweli/qgis-plugin-template)

QGIS plugin description.

### Installation

During the development phase the plugin is available to install via 
a dedicated plugin repository 
[https://raw.githubusercontent.com/samweli/qgis-plugin-template/release/docs/repository/plugins.xml](https://raw.githubusercontent.com/samweli/qgis-plugin-template/release/docs/repository/plugins.xml)

#### Install from QGIS plugin repository

- Open QGIS application and open plugin manager.
- Search for `QGIS Plugin template` in the All page of the plugin manager.
- From the found results, click on the `QGIS Plugin template` result item and a page with plugin information will show up. 
  
- Click the `Install Plugin` button at the bottom of the dialog to install the plugin.


#### Install from ZIP file

Alternatively the plugin can be installed using **Install from ZIP** option on the 
QGIS plugin manager. 

- Download zip file from the required plugin released version
https://github.com/{github-user}/{plugin-repo-name}/releases/download/{tagname}/qgis-plugin-template.{version}.zip

- From the **Install from ZIP** page, select the zip file and click the **Install** button to install plugin

#### Install from custom plugin repository

- Open the QGIS plugin manager, then select the **Settings** page

- Click **Add** button on the **Plugin Repositories** group box and use the above url to create
the new plugin repository.
- The plugin should now be available from the list
of all plugins that can be installed.

Disable QGIS official plugin repository in order to not fetch plugins from it.

**NOTE:** While the development phase is on going the plugin will be flagged as experimental, make
sure to enable the QGIS plugin manager in the **Settings** page to show the experimental plugins
in order to be able to install it.


When the development work is complete the plugin will be available on the QGIS
official plugin repository.


### Usage


### Development 

To use the plugin for development purposes, clone the repository locally,
install pip, a python dependencies management tool see https://pypi.org/project/pip/

#### Create virtual environment

Using any python virtual environment manager create project environment. 
Recommending to use [virtualenv-wrapper](https://virtualenvwrapper.readthedocs.io/en/latest/).

It can be installed using python pip 

```
pip install virtualenvwrapper
```

 1. Create virtual environment

    ```
    mkvirtualenv env
    ```

2. Using the pip, install plugin development dependencies by running 

    ```
    pip install -r requirements-dev.txt
   ```


To install the plugin into the QGIS application, activate virtual environment and then use the below command

```
 python admin.py install
```
