from PySide6 import QtCore, QtWidgets, QtGui

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.numLeds = 140

        self.layout = QtWidgets.QVBoxLayout(self)

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

        self.layout.addWidget(self.colorButton)
        self.layout.addWidget(self.colorText)
        self.layout.addLayout(self.numLedsLayout)

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