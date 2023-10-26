import maya.cmds as cmds
import random

from PySide2.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QPushButton
from PySide2.QtCore import Qt

# Define the CameraShake class for the application window
class CameraShake(QMainWindow):
    def __init__(self):
        super().__init__()

        # Call the setupUI class to create the user interface
        self.setupUI()

        # Initialize slider values
        self.value_x = self.frequency_x_slider.value()
        self.value_y = self.frequency_y_slider.value()
        self.value_z = self.frequency_z_slider.value()

        # Connect slider value change signals to their respective functions
        self.frequency_x_slider.valueChanged.connect(self.freq_slider_values_updated)
        self.frequency_y_slider.valueChanged.connect(self.freq_slider_values_updated)
        self.frequency_z_slider.valueChanged.connect(self.freq_slider_values_updated)
        self.keyframe_range_slider.valueChanged.connect(self.frame_range_slider_value_updated)

        # Connect button click signals to the apply/reset_values functions
        self.set_keyframe_button.clicked.connect(self.set_keyframe)
        self.set_keyframe_range_button.clicked.connect(self.set_keyframe_to_range)
        self.reset_button.clicked.connect(self.reset_values)

        # Get a list of selected cameras 
        self.selected_cameras = self.get_selected_cameras()

        # Get the number of frames in the scene
        self.num_frames = self.get_max_frame_number()

    # Define the UI layout and widgets
    def setupUI(self):

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        label_slider_layout = QHBoxLayout()

        # Create label layout and labels
        lb_layout = QVBoxLayout()
        lb_frequency_x = QLabel("Frequency X: ")
        lb_frequency_y = QLabel("Frequency Y: ")
        lb_frequency_z = QLabel("Frequency Z: ")
        lb_amplitude = QLabel("Amplitude: ")
        self.lb_keyframe_range = QLabel("Frame Range (1's): ")

        # Add labels to the label layout
        lb_layout.addWidget(lb_frequency_x)
        lb_layout.addWidget(lb_frequency_y)
        lb_layout.addWidget(lb_frequency_z)
        lb_layout.addWidget(lb_amplitude)
        lb_layout.addWidget(self.lb_keyframe_range)

        # Create slider layout and horizontal sliders
        slider_layout = QVBoxLayout()
        self.frequency_x_slider = QSlider(Qt.Horizontal)
        self.frequency_y_slider = QSlider(Qt.Horizontal)
        self.frequency_z_slider = QSlider(Qt.Horizontal)
        self.amplitude_slider = QSlider(Qt.Horizontal)
        self.keyframe_range_slider = QSlider(Qt.Horizontal)

        # Set the slider ranges
        self.frequency_x_slider.setRange(0, 10)
        self.frequency_y_slider.setRange(0, 10)
        self.frequency_z_slider.setRange(0, 10)
        self.amplitude_slider.setRange(1, 10)
        self.keyframe_range_slider.setRange(1, 3)

        # Add the sliders to the slider layout
        slider_layout.addWidget(self.frequency_x_slider)
        slider_layout.addWidget(self.frequency_y_slider)
        slider_layout.addWidget(self.frequency_z_slider)
        slider_layout.addWidget(self.amplitude_slider)
        slider_layout.addWidget(self.keyframe_range_slider)

        # Create a button layout and buttons
        button_layout = QHBoxLayout()
        self.set_keyframe_button = QPushButton("Set Keyframe")
        self.set_keyframe_range_button = QPushButton("Set Keyframes To Range")
        self.reset_button = QPushButton("Reset")

        # Add the buttons to the button layout
        button_layout.addWidget(self.set_keyframe_button)
        button_layout.addWidget(self.set_keyframe_range_button)
        button_layout.addWidget(self.reset_button)

        # Add the label and slider layouts to a label/slider layout
        label_slider_layout.addLayout(lb_layout)
        label_slider_layout.addLayout(slider_layout)

        # Add the label_slider and button layouts to the main layout
        main_layout.addLayout(label_slider_layout)
        main_layout.addLayout(button_layout)

    # Returns a list of the selected camera transforms in the scene
    def get_selected_cameras(self):
        # List all cameras in the scene
        all_cameras = cmds.ls(type="camera", long=True)

        # Get the parent transform nodes for every camera
        all_camera_transforms = [cmds.listRelatives(cam, parent=True)[0] for cam in all_cameras]

        # Get the currently selected objects in the scene
        selected_objects = cmds.ls(selection=True)

        # Filter selected objects to only include camera transforms
        selected_cameras = [cam for cam in selected_objects if cam in all_camera_transforms]
        
        return selected_cameras

    # Gets the number of frames in the scene and returns its value as an integer
    def get_max_frame_number(self):
        num_frames = int(cmds.playbackOptions(q=True, maxTime=True))

        return num_frames
    
    # Divide the freq slider values by 500 whenever slider value is changed
    def freq_slider_values_updated(self):
        self.value_x = self.frequency_x_slider.value() / 500
        self.value_y = self.frequency_y_slider.value() / 500
        self.value_z = self.frequency_z_slider.value() / 500

    # Changes the QLabel for the frame range slider when the slider value is changed
    def frame_range_slider_value_updated(self):
        value = self.keyframe_range_slider.value()
        self.lb_keyframe_range.setText(f"Frame Range ({value}'s): ")

    # Returns the current translation values of the selected camera as a tuple
    def get_current_translate_values(self, camera):
        translation_values = cmds.getAttr(camera + ".translate")[0]
        
        return translation_values

    # Generate random translation coordinates based on sliders
    def random_translate_coordinate(self):
        random_x = random.uniform(-self.value_x, self.value_x) * self.amplitude_slider.value()
        random_y = random.uniform(-self.value_y, self.value_y) * self.amplitude_slider.value()
        random_z = random.uniform(-self.value_z, self.value_z) * self.amplitude_slider.value()

        return random_x, random_y, random_z
    
    # Gets the updated coordinates when random translate coordinates are added to current translate coordinates
    def update_coordinates(self, camera):
        current_x, current_y, current_z = self.get_current_translate_values(camera)
        random_x, random_y, random_z = self.random_translate_coordinate()
        update_x = current_x + random_x
        update_y = current_y + random_y
        update_z = current_z + random_z
        
        return update_x, update_y, update_z

    # Apply camera shake to the current keyframe
    def set_keyframe(self):
        for camera in self.selected_cameras:
            current_frame = cmds.currentTime(query=True)
            update_x, update_y, update_z = self.update_coordinates(camera)
            
            cmds.setKeyframe(camera, attribute="translateX", t=current_frame, value=update_x)
            cmds.setKeyframe(camera, attribute="translateY", t=current_frame, value=update_y)
            cmds.setKeyframe(camera, attribute="translateZ", t=current_frame, value=update_z)
    
    # Apply camera shake by setting keyframes on each camera over a frame range
    def set_keyframe_to_range(self):
        frame_range = self.keyframe_range_slider.value()
        for camera in self.selected_cameras:
            for frame in range(1, self.num_frames, frame_range):
                cmds.currentTime(frame, edit=True)
                update_x, update_y, update_z = self.update_coordinates(camera)

                cmds.setKeyframe(camera, attribute="translateX", t=frame, value=update_x)
                cmds.setKeyframe(camera, attribute="translateY", t=frame, value=update_y)
                cmds.setKeyframe(camera, attribute="translateZ", t=frame, value=update_z)

    # Reset slider positions/values and remove set keyframes
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