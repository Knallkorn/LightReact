import os
from window import MainWindow
from PySide6 import QtCore, QtWidgets, QtGui

class TrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, parent = None, window: MainWindow = None):
        # Init the tray icon with icon image
        super().__init__(QtGui.QIcon(os.path.join(os.path.dirname(__file__), "assets", "icon.png")), parent)
        self.window = window

        self.setToolTip("LightReact")

        # Set up context menu
        self.menu = QtWidgets.QMenu()
        self.quitAction = self.menu.addAction("Quit")
        self.quitAction.triggered.connect(self.quitApp)
        self.openAction = self.menu.addAction("Open")
        self.openAction.triggered.connect(self.showWindow)

        # Override close event of main window
        self.window.closeEvent = self.windowClose

        # Finalize tray icon
        self.setContextMenu(self.menu)
        self.activated.connect(self.onActivated)

    # On click in tray
    @QtCore.Slot(QtWidgets.QSystemTrayIcon.ActivationReason)
    def onActivated(self, reason):
        if reason != QtWidgets.QSystemTrayIcon.Context:
            self.showWindow()

    # Reopens main window
    def showWindow(self):
        self.window.show()
        self.hide()
    
    # Used to extend close event of main window
    @QtCore.Slot(QtGui.QCloseEvent)
    def windowClose(self, event):
        self.show()

    @QtCore.Slot()
    def quitApp(self):
        self.window.stopDriver()
        QtWidgets.QApplication.quit()
