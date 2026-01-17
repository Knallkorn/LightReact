from PySide6 import QtCore, QtWidgets
from driver import Driver
from time import sleep

class MainWindow(QtWidgets.QWidget):

    stopDriver = QtCore.Signal()

    def __init__(self):
        super().__init__()

        self.numLeds = 140

        self.layout = QtWidgets.QVBoxLayout(self)

        self.runButton = QtWidgets.QPushButton("Run")
        self.runButton.clicked.connect(self.runDriver)

        self.colorButton = QtWidgets.QPushButton("Color Picker")
        self.colorButton.clicked.connect(self.openPicker)

        self.colorText = QtWidgets.QLabel("No Colour")

        self.ledDownButton = QtWidgets.QPushButton("<")
        self.ledDownButton.clicked.connect(self.ledDown)

        self.ledUpButton = QtWidgets.QPushButton(">")
        self.ledUpButton.clicked.connect(self.ledUp)

        self.numLedsText = QtWidgets.QLabel(f"{self.numLeds}")

        self.numLedsLayout = QtWidgets.QHBoxLayout()
        self.numLedsLayout.addWidget(self.ledDownButton)
        self.numLedsLayout.addWidget(self.numLedsText)
        self.numLedsLayout.addWidget(self.ledUpButton)

        self.layout.addWidget(self.runButton)
        self.layout.addWidget(self.colorButton)
        self.layout.addWidget(self.colorText)
        self.layout.addLayout(self.numLedsLayout)

    @QtCore.Slot()
    def runDriver(self):
        try:
            print(self.driver)
        except:
            pass
        else:
            self.driver.requestInterruption()
            sleep(5)
        self.driver = Driver()
        self.driver.started.connect(self.driver.run)
        self.driver.finished.connect(self.driver.deleteLater)
        self.driver.start()

    @QtCore.Slot()
    def openPicker(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.colorText.setText(f"Selected Color: {color.name()}")
    
    @QtCore.Slot()
    def ledDown(self):
        self.numLeds -= 1
        self.numLedsText.setText(f"{self.numLeds}")
    
    @QtCore.Slot()
    def ledUp(self):
        self.numLeds += 1
        self.numLedsText.setText(f"{self.numLeds}")