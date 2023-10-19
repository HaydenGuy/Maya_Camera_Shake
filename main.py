import maya.cmds as cmds
import maya.OpenMaya as om
import random

from PySide2.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider
from PySide2.QtCore import Qt

class CameraShake(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

        self.frequency_x_slider.valueChanged.connect(self.camera_shake_update)
        self.frequency_y_slider.valueChanged.connect(self.camera_shake_update)
        self.frequency_z_slider.valueChanged.connect(self.camera_shake_update)
        self.amplitude_slider.valueChanged.connect(self.camera_shake_update)

        self.selected_cameras = self.get_selected_cameras()
        self.num_frames = self.get_max_frame_number()

    # Creates the UI 
    def setupUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

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

        main_layout.addLayout(lb_layout)
        main_layout.addLayout(slider_layout)

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
    
    def camera_shake_update(self):
        value_x = self.frequency_x_slider.value() / 100
        value_y = self.frequency_y_slider.value() / 100
        value_z = self.frequency_z_slider.value() / 100

        for frame in range(self.num_frames):
            random_x = random.uniform(-value_x, value_x) * self.amplitude_slider.value()
            random_y = random.uniform(-value_y, value_y) * self.amplitude_slider.value()
            random_z = random.uniform(-value_z, value_z) * self.amplitude_slider.value()
            
            for camera in self.selected_cameras:
                cmds.setKeyframe(camera, attribute="translateX", t=frame, value=random_x)
                cmds.setKeyframe(camera, attribute="translateY", t=frame, value=random_y)
                cmds.setKeyframe(camera, attribute="translateZ", t=frame, value=random_z)

if __name__ == '__main__':
    app = QApplication.instance()
    if not app:
        app = QApplication()
    
    window = CameraShake()
    window.show()