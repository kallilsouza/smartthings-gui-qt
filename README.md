# SmartThings GUI (Qt)
SmartThings GUI (Qt) is a simple graphical interface for interacting with SmartThings on Linux, built with Qt and Python. I have developed it for personal use, but you can use it as a GUI alternative to the command-line interface.

![Screenshot from 2025-05-18 08-22-06](https://github.com/user-attachments/assets/9a01eb44-dee9-4299-9e9a-ad24e7a413dc)

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

## Desktop entry
You can also create a desktop entry to run it without even opening your terminal.

Create a file like smartthings-gui.desktop in your ~/.local/share/applications/ directory
```bash
nano ~/.local/share/applications/smartthings-gui.desktop
```

Adapt this and paste to it:
```bash
[Desktop Entry]
Version=1.0
Type=Application
Name=SmartThings
Comment=Launch SmartThings GUI (Qt)
Exec=bash -c "cd /path/to/project/smartthings-gui-qt && /
path/to/poetry/.local/bin/poetry run python smartthings_gui.py"
Icon=/path/to/icon/smartthings-logo.png
Terminal=false
Categories=Utility;
StartupWMClass=smartthings_gui.py
```
The icon is optional. You must download one for this.
If you don't want it, just delete the line that starts with "Icon=".

## Notes
### Authentication
You must be authenticated with SmartThings CLI before using the GUI.

### Supported devices
I have only tested it with a few personal devices that were connected to SmartThings.
I am not sure that it will work with your devices as well.

If it doesn't, feel free to modify the code to fit your needs.
