"""
My Weather App main module.

Author: João Pereira
"""

import sys

from controller.main_window_controller import MainWindowController
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

# Constants
ICON_FILE_PATH = "app/icons/lighting.jpg"
WINDOW_OPACITY = 0.95


def create_window():
    """Create the main window and set its properties."""

    window = MainWindowController()
    window.setWindowTitle("Weather Forecast")
    window.setWindowIcon(QIcon(ICON_FILE_PATH))
    window.setWindowOpacity(WINDOW_OPACITY)
    return window


def run_application():
    """Run the application event loop."""

    app = QApplication(sys.argv)

    window = create_window()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_application()
