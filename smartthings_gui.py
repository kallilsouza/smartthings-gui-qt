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
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
import os


logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)


class DeviceStatusThread(QThread):
    status_fetched = pyqtSignal(str, dict)  # Signal to send device_id and status_data

    def __init__(self, smartthings_path, device_id, parent=None):
        super().__init__(parent)
        self.smartthings_path = smartthings_path
        self.device_id = device_id

    def run(self):
        try:
            result = subprocess.run(
                [self.smartthings_path, "devices:status", self.device_id],
                capture_output=True,
                text=True,
                check=True,
            )
            status_data = json.loads(result.stdout)
            self.status_fetched.emit(self.device_id, status_data)
        except Exception as e:
            LOGGER.error("Error fetching device status: %s", e)


class SmartThingsGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.loaded_devices = []
        self.threads = []  # List to keep track of running threads

        self.init_ui()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.load_devices_status)
        self.timer.start(10000)

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
                toggle_button = QPushButton("Loading status...")
                toggle_button.setEnabled(False)
                setattr(self, f"{device_id}_toggle_button", toggle_button)

                device_layout.addWidget(label)
                device_layout.addWidget(toggle_button)

                devices_layout.addWidget(device_widget)

                # Store the widget for future use
                setattr(self, device_id, device_widget)

        except Exception as e:
            self.main_title.setText(f"Error loading devices: {e}")
            LOGGER.error("Error loading devices: %s", e)

    def load_devices_status(self):
        try:
            smartthings_path = os.path.expanduser("~/smartthings")
            for device in self.loaded_devices:
                device_id = device.get("deviceId", None)
                if not device_id:
                    continue

                # Create and start a thread for each device
                thread = DeviceStatusThread(smartthings_path, device_id, self)
                thread.status_fetched.connect(self.update_device_status)
                thread.finished.connect(
                    lambda t=thread: self.remove_thread(t)
                )  # Safely remove thread
                self.threads.append(thread)  # Keep a reference to the thread
                thread.start()

        except Exception as e:
            LOGGER.error("Error loading device status: %s", e)

    def remove_thread(self, thread):
        """Safely remove a thread from the list."""
        if thread in self.threads:
            self.threads.remove(thread)

    def update_device_status(self, device_id, status_data):
        try:
            LOGGER.info("Status loaded successfully for device: %s", device_id)

            current_status = (
                status_data.get("components", {})
                .get("main", {})
                .get("healthCheck", {})
                .get("DeviceWatch-DeviceStatus", {})
                .get("value")
            )

            button_name = f"{device_id}_toggle_button"
            if getattr(self, button_name, None):
                if current_status == "offline":
                    getattr(self, button_name).setText("Offline")
                    getattr(self, button_name).setEnabled(False)
                elif current_status == "online":
                    switch_data = (
                        status_data.get("components", {})
                        .get("main", {})
                        .get("switch", {})
                        .get("switch", {})
                    )
                    if switch_data.get("value") == "on":
                        getattr(self, button_name).setText("Turn Off")
                        getattr(self, button_name).setEnabled(True)
                    else:
                        getattr(self, button_name).setText("Turn On")
                        getattr(self, button_name).setEnabled(True)
        except Exception as e:
            LOGGER.error("Error updating device status: %s", e)

    def closeEvent(self, event):
        # Stop all running threads before closing the application
        for thread in self.threads:
            thread.quit()
            thread.wait()
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = SmartThingsGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
