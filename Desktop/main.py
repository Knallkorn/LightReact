import sys
from PySide6 import QtCore, QtWidgets, QtGui
from window import MainWindow
from trayIcon import TrayIcon

if __name__ == "__main__":
    # Init app
    app = QtWidgets.QApplication([])
    app.setQuitOnLastWindowClosed(False)

    # Add main window
    widget = MainWindow()
    widget.resize(800, 600)
    widget.show()

    # Init tray icon
    # Will show on window close
    trayIcon = TrayIcon(app, widget)

    sys.exit(app.exec())