# SmartThings GUI (Qt)
SmartThings GUI (Qt) is a simple graphical interface for interacting with SmartThings on Linux, built with Qt and Python. I have developed it for personal use, but you can use it as a GUI alternative to the command-line interface.

## Prerequisites
Before running the app, ensure you have the following installed:

- SmartThings CLI

- Poetry (Python dependency management)

## Installation
Clone the repository:
```bash
git clone git@github.com:kallilsouza/smartthings-gui-qt.git
cd smartthings-gui-qt
```

Enter the Poetry environment and install dependencies:

```bash
poetry shell
poetry install
```

Run the application:

```bash
poetry run python smartthings_gui.py
```

## Notes
### Authentication
You must be authenticated with SmartThings CLI before using the GUI.

### Supported devices
I have only tested it with a few personal devices that were connected to SmartThings.
I am not sure that it will work with your devices as well.

If it doesn't, feel free to modify the code to fit your needs.