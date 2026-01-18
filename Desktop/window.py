from PySide6 import QtCore, QtWidgets
from driver import Driver
from time import sleep

class MainWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.numLeds = 140
        self.mode = Driver.LEDMode.REACTIVE
        self.doLerp = True
        self.doBrightness = True
        self.brightnessMod = 100

        self.layout = QtWidgets.QVBoxLayout(self)

        self.runButton = QtWidgets.QPushButton("Run")
        self.runButton.clicked.connect(self.runDriver)

        self.stopButton = QtWidgets.QPushButton("Stop")
        self.stopButton.clicked.connect(self.stopDriver)

        self.driverControlLayout = QtWidgets.QHBoxLayout()
        self.driverControlLayout.addWidget(self.runButton)
        self.driverControlLayout.addWidget(self.stopButton)


        self.modeText = QtWidgets.QLabel("Mode: ")
        self.modeText.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.modeDropdown = QtWidgets.QComboBox()
        self.modeDropdown.addItems(['Reactive', 'Red', 'Green', 'Blue', 'Rainbow'])
        self.modeDropdown.currentIndexChanged.connect(self.updateMode)

        self.modeLayout = QtWidgets.QHBoxLayout()
        self.modeLayout.addWidget(self.modeText)
        self.modeLayout.addWidget(self.modeDropdown)


        self.brightnessText = QtWidgets.QLabel("Reactive Brightness: ")
        self.brightnessCheckbox = QtWidgets.QCheckBox(tristate=False)
        self.brightnessCheckbox.stateChanged.connect(self.updateReactiveBrightness)

        self.brightnessSliderText = QtWidgets.QLabel(f"Brightness Modifer: {self.brightnessMod}")
        self.brightnessSliderText.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.brightnessSlider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.brightnessSlider.setRange(0, 100)
        self.brightnessSlider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksBelow)
        self.brightnessSlider.setTickInterval(10)
        self.brightnessSlider.setSingleStep(1)
        self.brightnessSlider.setValue(self.brightnessMod)
        self.brightnessSlider.valueChanged.connect(self.updateBrightnessSlider)
        self.brightnessSliderLayout = QtWidgets.QVBoxLayout()
        self.brightnessSliderLayout.addWidget(self.brightnessSliderText)
        self.brightnessSliderLayout.addWidget(self.brightnessSlider)
        self.brightnessSliderLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.brightnessLayout = QtWidgets.QHBoxLayout()
        self.brightnessLayout.addWidget(self.brightnessText)
        self.brightnessLayout.addWidget(self.brightnessCheckbox)
        self.modeLayout.addLayout(self.brightnessLayout)


        self.colorButton = QtWidgets.QPushButton("Color Picker")
        self.colorButton.clicked.connect(self.openPicker)

        self.colorText = QtWidgets.QLabel("No Colour")


        self.numLedsText = QtWidgets.QLabel("Number of LEDs: ")
        self.numLedsSpinbox = QtWidgets.QSpinBox(minimum=0, maximum=255, singleStep=1, value=140)
        self.numLedsSpinbox.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.numLedsSpinbox.valueChanged.connect(self.updateNumLeds)

        self.numLedsLayout = QtWidgets.QHBoxLayout()
        self.numLedsLayout.addWidget(self.numLedsText)
        self.numLedsLayout.addWidget(self.numLedsSpinbox)


        self.layout.addLayout(self.driverControlLayout)
        self.layout.addLayout(self.modeLayout)
        self.layout.addLayout(self.brightnessSliderLayout)
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
            sleep(1)
        self.driver = Driver(mode=self.mode, numLeds=self.numLeds, doLerp=self.doLerp, 
                             reactiveBrightness=self.doBrightness, brightnessMod=self.brightnessMod)
        self.driver.started.connect(self.driver.run)
        self.driver.finished.connect(self.driver.deleteLater)
        self.driver.start()

    @QtCore.Slot()
    def stopDriver(self):
        try:
            print(self.driver)
        except:
            pass
        else:
            self.driver.requestInterruption()
    
    @QtCore.Slot()
    def updateMode(self):
        mode = Driver.LEDMode(self.modeDropdown.currentIndex())
        self.mode = mode
        if mode == Driver.LEDMode.REACTIVE:
            self.doLerp = True
            self.brightnessCheckbox.setDisabled(False)
        else:
            self.doLerp = False
            self.brightnessCheckbox.setDisabled(True)
            self.brightnessCheckbox.setCheckState(QtCore.Qt.CheckState.Unchecked)
    
    @QtCore.Slot()
    def updateReactiveBrightness(self):
        self.doBrightness = self.brightnessCheckbox.isChecked()
    
    @QtCore.Slot()
    def updateBrightnessSlider(self):
        self.brightnessMod = self.brightnessSlider.value()
        self.brightnessSliderText.setText(f"Brightness Modifier: {self.brightnessMod}")

    @QtCore.Slot()
    def openPicker(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.colorText.setText(f"Selected Color: {color.name()}")
    
    @QtCore.Slot()
    def updateNumLeds(self):
        self.numLeds = self.numLedsSpinbox.value()