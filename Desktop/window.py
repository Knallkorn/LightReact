from PySide6 import QtCore, QtWidgets, QtGui

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QVBoxLayout(self)

        self.button = QtWidgets.QPushButton("Click me!")
        self.button.clicked.connect(self.func)

        self.text = QtWidgets.QLabel("No Colour")

        self.layout.addWidget(self.button)
        self.layout.addWidget(self.text)
        
    @QtCore.Slot()
    def func(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.text.setText(f"Selected Color: {color.name()}")