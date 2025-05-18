import json
import logging
import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QWidget,
    QScrollArea,
)
from PyQt5.QtCore import Qt, QTimer
import os


logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)


class SmartThingsGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.loaded_devices = []

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("SmartThings")
        self.setGeometry(300, 300, 300, 200)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.main_title = QLabel("Loading connected devices...")
        self.main_title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.main_title)

        self.load_devices()

    def load_devices(self):
        try:
            smartthings_path = os.path.expanduser("~/smartthings")
            result = subprocess.run(
                [smartthings_path, "devices"],
                capture_output=True,
                text=True,
                check=True,
            )

            devices = json.loads(result.stdout)
            LOGGER.info("Devices loaded successfully")

            self.loaded_devices = devices

            # Clear the main layout
            central_widget = self.centralWidget()
            for i in reversed(range(central_widget.layout().count())):
                widget = central_widget.layout().itemAt(i).widget()
                if widget:
                    widget.deleteLater()

            self.main_title = QLabel("Devices connected:")
            self.main_title.setAlignment(Qt.AlignCenter)
            central_widget.layout().addWidget(self.main_title)

            # Add a scroll area for the devices
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            central_widget.layout().addWidget(scroll_area)

            devices_widget = QWidget()
            devices_layout = QVBoxLayout(devices_widget)
            scroll_area.setWidget(devices_widget)

            for device in devices:
                device_label = device.get("label", "Unknown Device")
                device_id = device.get("deviceId", None)

                if not device_id:
                    LOGGER.warning("Device ID not found for device: %s", device_label)
                    continue

                # Create a widget for the device
                device_widget = QWidget()
                device_layout = QHBoxLayout(device_widget)

                label = QLabel(device_label)
                toggle_button = QPushButton("Toggle")

                device_layout.addWidget(label)
                device_layout.addWidget(toggle_button)

                devices_layout.addWidget(device_widget)

                # Store the widget for future use
                setattr(self, device_id, device_widget)

        except Exception as e:
            self.main_title.setText(f"Error loading devices: {e}")
            LOGGER.error("Error loading devices: %s", e)


def main():
    app = QApplication(sys.argv)
    window = SmartThingsGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
