import maya.cmds as cmds
import maya.OpenMaya as om
from PySide2.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider
from PySide2.QtCore import Qt

class CameraShake(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

        self.frequency_slider.valueChanged.connect(self.camera_frequency_update)
        self.amplitude_slider.valueChanged.connect(self.camera_amplitude_update)

    def setupUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        lb_layout = QVBoxLayout()
        lb_frequency = QLabel("Frequency: ")
        lb_amplitude = QLabel("Amplitude: ")
        lb_layout.addWidget(lb_frequency)
        lb_layout.addWidget(lb_amplitude)

        slider_layout = QVBoxLayout()
        self.frequency_slider = QSlider(Qt.Horizontal)
        self.amplitude_slider = QSlider(Qt.Horizontal)
        self.frequency_slider.setRange(0, 10)
        self.amplitude_slider.setRange(0, 10)
        slider_layout.addWidget(self.frequency_slider)
        slider_layout.addWidget(self.amplitude_slider)

        main_layout.addLayout(lb_layout)
        main_layout.addLayout(slider_layout)

    def camera_frequency_update(self):
        print("placeholder")

    def camera_amplitude_update(self):
        print("placeholder")


if __name__ == '__main__':
    app = QApplication.instance()
    if not app:
        app = QApplication()
    
    window = CameraShake()
    window.show()