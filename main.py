import maya.cmds as cmds
import maya.OpenMaya as om
import random

from PySide2.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QPushButton
from PySide2.QtCore import Qt

class CameraShake(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

        self.value_x = self.frequency_x_slider.value()
        self.value_y = self.frequency_y_slider.value()
        self.value_z = self.frequency_z_slider.value()

        self.frequency_x_slider.valueChanged.connect(self.freq_slider_values_updated)
        self.frequency_y_slider.valueChanged.connect(self.freq_slider_values_updated)
        self.frequency_z_slider.valueChanged.connect(self.freq_slider_values_updated)

        self.apply_button.clicked.connect(self.apply_values)
        self.reset_button.clicked.connect(self.reset_values)

        self.selected_cameras = self.get_selected_cameras()
        self.num_frames = self.get_max_frame_number()

    # Creates the UI 
    def setupUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        label_slider_layout = QHBoxLayout()

        lb_layout = QVBoxLayout()

        lb_frequency_x = QLabel("Frequency X: ")
        lb_frequency_y = QLabel("Frequency Y: ")
        lb_frequency_z = QLabel("Frequency Z: ")
        lb_amplitude = QLabel("Amplitude: ")

        lb_layout.addWidget(lb_frequency_x)
        lb_layout.addWidget(lb_frequency_y)
        lb_layout.addWidget(lb_frequency_z)
        lb_layout.addWidget(lb_amplitude)

        slider_layout = QVBoxLayout()

        self.frequency_x_slider = QSlider(Qt.Horizontal)
        self.frequency_y_slider = QSlider(Qt.Horizontal)
        self.frequency_z_slider = QSlider(Qt.Horizontal)
        self.amplitude_slider = QSlider(Qt.Horizontal)

        self.frequency_x_slider.setRange(0, 10)
        self.frequency_y_slider.setRange(0, 10)
        self.frequency_z_slider.setRange(0, 10)
        self.amplitude_slider.setRange(1, 10)

        slider_layout.addWidget(self.frequency_x_slider)
        slider_layout.addWidget(self.frequency_y_slider)
        slider_layout.addWidget(self.frequency_z_slider)
        slider_layout.addWidget(self.amplitude_slider)

        button_layout = QHBoxLayout()
        
        self.apply_button = QPushButton("Apply")
        self.reset_button = QPushButton("Reset")
        button_layout.addWidget(self.apply_button)
        button_layout.addWidget(self.reset_button)

        label_slider_layout.addLayout(lb_layout)
        label_slider_layout.addLayout(slider_layout)
        main_layout.addLayout(label_slider_layout)
        main_layout.addLayout(button_layout)

    # Returns a list of the selected camera transforms in the scene
    def get_selected_cameras(self):
        all_cameras = cmds.ls(type="camera", long=True)

        all_camera_transforms = [cmds.listRelatives(cam, parent=True)[0] for cam in all_cameras]

        selected_objects = cmds.ls(selection=True)

        selected_cameras = [cam for cam in selected_objects if cam in all_camera_transforms]
        
        return selected_cameras

    # Gets the number of frames in the scene and returns its value as an integer
    def get_max_frame_number(self):
        num_frames = int(cmds.playbackOptions(q=True, maxTime=True))

        return num_frames
    
    def freq_slider_values_updated(self):
        self.value_x = self.frequency_x_slider.value() / 500
        self.value_y = self.frequency_y_slider.value() / 500
        self.value_z = self.frequency_z_slider.value() / 500

    def random_translate_coordinate(self):
        random_x = random.uniform(-self.value_x, self.value_x) * self.amplitude_slider.value()
        random_y = random.uniform(-self.value_y, self.value_y) * self.amplitude_slider.value()
        random_z = random.uniform(-self.value_z, self.value_z) * self.amplitude_slider.value()

        return random_x, random_y, random_z
    
    def apply_values(self):        
        for frame in range(self.num_frames):
            random_x, random_y, random_z = self.random_translate_coordinate()

            if frame % 2 == 0:
                for camera in self.selected_cameras:
                    cmds.setKeyframe(camera, attribute="translateX", t=frame, value=random_x)
                    cmds.setKeyframe(camera, attribute="translateY", t=frame, value=random_y)
                    cmds.setKeyframe(camera, attribute="translateZ", t=frame, value=random_z)

    def reset_values(self):
        self.frequency_x_slider.setValue(0)
        self.frequency_y_slider.setValue(0)
        self.frequency_z_slider.setValue(0)
        self.amplitude_slider.setValue(1)
        
        self.frequency_x_slider.setSliderPosition(0)
        self.frequency_y_slider.setSliderPosition(0)
        self.frequency_z_slider.setSliderPosition(0)
        self.amplitude_slider.setSliderPosition(1)
        
        for frame in range (self.num_frames):
            for camera in self.selected_cameras:
                cmds.cutKey(camera, attribute="translateX", t=(frame, frame))
                cmds.cutKey(camera, attribute="translateY", t=(frame, frame))
                cmds.cutKey(camera, attribute="translateZ", t=(frame, frame))

if __name__ == '__main__':
    app = QApplication.instance()
    if not app:
        app = QApplication()
    
    window = CameraShake()
    window.show()