# QGIS Plugin Template

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/kartoza/qgis-plugin-template/ci.yml?branch=master)
![GitHub](https://img.shields.io/github/license/kartoza/qgis-plugin-template)

This repository serves as a **QGIS plugin template** for building QGIS plugins. It provides the necessary structure and tools to kick-start plugin development, including components for configuration, development, testing, and packaging.

### Repository Components

The repository includes the following key components to help you get started with building your QGIS plugin:

- **`admin.py`**: A script used for managing plugin installations, creating releases, and uploading them to GitHub. This script simplifies common tasks such as installing dependencies and packaging the plugin for distribution.
- **`requirements-dev.txt`**: A list of development dependencies needed to work with the plugin template. This file is used to install the necessary packages for plugin development.
- **Plugin source code**: Contains the core functionality and the template structure for your plugin development.

### Development

To use the plugin for development purposes, follow these steps:

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/{github-user}/{plugin-repo-name}.git
   cd {plugin-repo-name}
   
2. Install virtualenv (if you don't have it already) to create a project-specific Python environment:
   ```bash 
   pip install virtualenv
   ```
3. Create a virtual environment for the project:
    
    ```bash
    virtualenv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

4. Install the development dependencies listed in requirements-dev.txt:
    
    ```bash
    pip install -r requirements-dev.txt
    ```

5. To install the plugin into QGIS, run the following command:
    
    ```bash
    python admin.py install
    ```
For plugin development, you can edit the source code located in the repository and 
test the changes within your QGIS environment.

### Testing
To ensure your plugin works as expected, it is important to have a reliable testing process. The following steps outline how to run tests for the plugin:

1. Install pytest (if it's not already included in the requirements-dev.txt):
    
    ```bash
    pip install pytest
    ```
2. Run the tests using pytest:

    ```bash
    pytest
   ```
   
    This will automatically discover and run all tests in the repository. Ensure that your test files are named with the prefix test_ to allow pytest to find them.
3. To run tests for specific files or functions, you can provide the test file or function name:

    ```bash
    pytest test_myplugin.py
    pytest test_myplugin.py::test_function_name
   ```
   
If you are working in the QGIS environment and have made changes to the plugin, it is recommended to manually test the plugin within QGIS as well.

### Deployment and Release
The release process for this repository can be handled through git tags and the release action workflow.
To create a release:

1. Create a Git Tag:
    - Tag your commit with a version number (e.g., v1.0.0).
2. Push the tag into the repository.
    ```bash 
    git push remote_name tag
   ```
Make sure the repository contains a branch named `release` based from the main branch, this will be used to keep track of the 
custom staging repository plugin versions.

Once the tag is pushed to GitHub, the release action workflow will trigger the release process. 
The release package will be associated with the GitHub tag, and the plugin will be available for users to download.
